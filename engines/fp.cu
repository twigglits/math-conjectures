/*
 * fp.cu — Erdős–Straus solution counter f(p) with Type I / Type II split.
 * CUDA port of the validated engines fp.c / fpr.rs. Same method, same output.
 *
 * Build:  nvcc -O3 -arch=compute_80 fp.cu -o fpcuda
 *         (PTX for compute_80; the driver JIT-compiles for the resident GPU,
 *          including Blackwell sm_120 — required because nvcc 12.0 predates it.)
 * Run:    ./fpcuda <pmin> <pmax> <mode> <out.csv>
 *         mode 0 = all primes, 1 = p ≡ 1 (mod 24),
 *         mode 2 = the six square classes mod 840 (1,121,169,289,361,529)
 * Verify: ./fpcuda 5 2000 0 cuda_small.csv && diff cuda_small.csv fp_small.csv
 *
 * Method (identical to fpr.rs): for each x in (p/4, (p+1)/2], a = 4x − p,
 * solutions with least denominator x correspond to divisors d | x²:
 *   Type I  (p ∤ d):   d ≡ −4x² (mod a),            d ≥ dmin
 *   Type II (d = pd'): d' ≡ −x  (mod a), d' ≤ x,    p·d' ≥ dmin
 * with dmin = 2x(2x − p) when 2x > p, else 0.
 * Ordered count per prime: ford = 6(cI + cII) − 3·n3, where n3 counts
 * degeneracies (x = y iff d == dmin > 0; y = z iff Type II with d' == x).
 * The x-range uses x ≤ (p+1)/2 (Bradford 2025; re-proved in REPORT.md §3.1);
 * the historical (p+1)/2 < x ≤ 3p/4 region provably contributes nothing.
 *
 * GPU design (v3 — divergence-free):
 *  - factor_chunk: one thread per x of the chunk factors x once via SPF into
 *    global scratch (k, q_i, E_i = 2e_i in x², qpow_i = q_i^{E_i}, nd = ∏(E_i+1)).
 *  - fp_kernel: ONE BLOCK PER x. Thread 0 enumerates the divisors of x² once
 *    (odometer) into dynamic shared memory; after one barrier, the block's
 *    threads stride the prime window p ∈ [2x−1, 4x) (binary-searched bounds:
 *    contiguous in the sorted prime list), each lane scanning the SAME shared
 *    divisor array with identical trip count — no warp divergence, broadcast
 *    shared loads, Barrett reduction (M = ⌊(2⁶⁴−1)/a⌋, ≤2 corrective subtracts)
 *    instead of ~100-cycle emulated 64-bit %.
 *  - Counts: a pair (x, p) scores a hit with probability ~10⁻⁵, so results are
 *    flushed with atomicAdd ONLY when nonzero — ~10⁷ atomics per 10¹⁴ tests.
 *  - x with d(x²) > SMEM_CAP (rare superabundant) take a same-kernel fallback:
 *    every lane runs the odometer privately — still divergence-free, since all
 *    lanes share the same x and trip count.
 *  - The display watchdog (~2 s) forbids long kernels: the global x range is
 *    cut into adaptive chunks targeted at ~0.25 s per launch, with persistent
 *    device accumulators and periodic CSV checkpoints.
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cuda_runtime.h>

typedef unsigned long long u64;
typedef unsigned int u32;

#define CUDA_CHECK(call) do { \
    cudaError_t err__ = (call); \
    if (err__ != cudaSuccess) { \
        fprintf(stderr, "CUDA error %s at %s:%d: %s\n", #call, __FILE__, __LINE__, \
                cudaGetErrorString(err__)); \
        exit(1); \
    } \
} while (0)

#define KMAX 10                  // max distinct primes of x (x ≤ 10⁹ ⇒ ≤ 9)
#define DX_CAP (1u << 19)        // chunk width cap (sizes the factor scratch)
#define SMEM_CAP 6144            // divisors held in shared memory (48 KB → 2 blocks/SM)
#define TPB 512                  // threads per block

// ============================ kernels ============================

__device__ __forceinline__ u64 bar_mod(u64 d, u64 a, u64 M)
{
    u64 r = d - __umul64hi(d, M) * a;
    while (r >= a) r -= a;
    return r;
}

// the per-(x,p) divisor-class test over an arbitrary divisor array
// (shared or global) — single implementation for all paths
__device__ __forceinline__ void scan_divs(const u64* __restrict__ divs, u32 nd,
                                          u64 x, u64 p,
                                          u64& c0, u64& c1, u64& n3)
{
    u64 a  = 4 * x - p;
    u64 M  = ~0ULL / a;
    u64 xm = bar_mod(x, a, M);
    u64 v  = bar_mod(bar_mod(4 * xm, a, M) * xm, a, M);
    u64 r0 = (a - v == a) ? 0 : a - v;        // (−4x²) mod a
    u64 r1 = (a - xm == a) ? 0 : a - xm;      // (−x)   mod a
    u64 dmin = (2 * x > p) ? 2 * x * (2 * x - p) : 0;
    for (u32 i = 0; i < nd; i++) {
        u64 d = divs[i];
        u64 m = bar_mod(d, a, M);
        if (m == r0 && d >= dmin) {
            c0++;
            if (dmin > 0 && d == dmin) n3++;          // x == y
        }
        if (d <= x && m == r1 && p * d >= dmin) {
            c1++;
            if (d == x) n3++;                          // y == z
            if (dmin > 0 && p * d == dmin) n3++;       // x == y via Type II
        }
    }
}

__global__ void factor_chunk(const u32* __restrict__ spf,
                             u64 X0, u32 len,
                             u32* __restrict__ kfac,
                             u32* __restrict__ ndfac,
                             u32* __restrict__ qfac,
                             u32* __restrict__ Efac,
                             u64* __restrict__ qpfac)
{
    u32 j = blockIdx.x * blockDim.x + threadIdx.x;
    if (j >= len) return;
    u32 tt = (u32)(X0 + j);
    u32 k = 0, nd = 1;
    while (tt > 1) {
        u32 qq = spf[tt];
        u32 e = 0;
        while (tt % qq == 0) { tt /= qq; e++; }
        u64 pw = 1;
        for (u32 i = 0; i < 2 * e; i++) pw *= qq;
        qfac [j * KMAX + k] = qq;
        Efac [j * KMAX + k] = 2 * e;
        qpfac[j * KMAX + k] = pw;
        nd *= (2 * e + 1);
        k++;
    }
    kfac[j] = k;
    ndfac[j] = nd;
}

// window helper: prime indices with p ∈ [2x−1, 4x) — contiguous in sorted list
__device__ __forceinline__ void prime_window(const u32* primes, int np, u64 x,
                                             int& lo_out, int& hi_out)
{
    u64 plo = 2 * x - 1, phi = 4 * x;
    int lo = 0, hi = np;
    while (lo < hi) { int m = (lo + hi) >> 1; if ((u64)primes[m] < plo) lo = m + 1; else hi = m; }
    lo_out = lo;
    int lo2 = lo; hi = np;
    while (lo2 < hi) { int m = (lo2 + hi) >> 1; if ((u64)primes[m] < phi) lo2 = m + 1; else hi = m; }
    hi_out = lo2;
}

// main kernel: one block per x; skips fat x (nd > SMEM_CAP)
__global__ void fp_kernel(const u32* __restrict__ primes, int np, u64 X0,
                          const u32* __restrict__ kfac,
                          const u32* __restrict__ ndfac,
                          const u32* __restrict__ qfac,
                          const u32* __restrict__ Efac,
                          const u64* __restrict__ qpfac,
                          u64* __restrict__ c0a, u64* __restrict__ c1a,
                          u64* __restrict__ n3a)
{
    extern __shared__ u64 s_divs[];
    __shared__ int s_lo, s_hi;

    u32 j  = blockIdx.x;
    u64 x  = X0 + j;
    u32 nd = ndfac[j];
    if (nd > SMEM_CAP) return;                     // fat x: handled separately

    if (threadIdx.x == 0) {
        prime_window(primes, np, x, s_lo, s_hi);
        if (s_lo < s_hi) {                         // fill shared divisor list
            u32 k = kfac[j];
            u32 q[KMAX], E[KMAX], f[KMAX]; u64 qp[KMAX];
            for (u32 i = 0; i < k; i++) {
                q[i] = qfac[j * KMAX + i]; E[i] = Efac[j * KMAX + i];
                qp[i] = qpfac[j * KMAX + i]; f[i] = 0;
            }
            u64 d = 1;
            for (u32 c = 0;; c++) {
                s_divs[c] = d;
                u32 i = 0;
                while (i < k) {
                    if (f[i] < E[i]) { f[i]++; d *= q[i]; break; }
                    f[i] = 0; d /= qp[i]; i++;
                }
                if (i == k) break;
            }
        }
    }
    __syncthreads();
    int lo = s_lo, hi = s_hi;
    if (lo >= hi) return;                          // uniform exit (after barrier)

    for (int ip = lo + threadIdx.x; ip < hi; ip += TPB) {
        u64 p = primes[ip];
        u64 c0 = 0, c1 = 0, n3 = 0;
        scan_divs(s_divs, nd, x, p, c0, c1, n3);
        if (c0 | c1) {                             // hits are ~10⁻⁵ rare
            atomicAdd((unsigned long long*)&c0a[ip], (unsigned long long)c0);
            if (c1) atomicAdd((unsigned long long*)&c1a[ip], (unsigned long long)c1);
            if (n3) atomicAdd((unsigned long long*)&n3a[ip], (unsigned long long)n3);
        }
    }
}

// fat-x path: list fat x's of the chunk, fill their divisors in global memory
// (one sequential odometer, ~1 ms), then scan with one thread per prime.
__global__ void collect_fat(const u32* __restrict__ ndfac, u32 len,
                            u32* __restrict__ fat_idx, u32* __restrict__ fat_cnt)
{
    u32 j = blockIdx.x * blockDim.x + threadIdx.x;
    if (j >= len) return;
    if (ndfac[j] > SMEM_CAP) {
        u32 slot = atomicAdd(fat_cnt, 1u);
        fat_idx[slot] = j;
    }
}

__global__ void fat_fill(u64 x, u32 k,
                         const u32* __restrict__ qfac,
                         const u32* __restrict__ Efac,
                         const u64* __restrict__ qpfac,
                         u32 j, u64* __restrict__ g_divs)
{
    if (blockIdx.x != 0 || threadIdx.x != 0) return;
    u32 q[KMAX], E[KMAX], f[KMAX]; u64 qp[KMAX];
    for (u32 i = 0; i < k; i++) {
        q[i] = qfac[j * KMAX + i]; E[i] = Efac[j * KMAX + i];
        qp[i] = qpfac[j * KMAX + i]; f[i] = 0;
    }
    u64 d = 1;
    for (u32 c = 0;; c++) {
        g_divs[c] = d;
        u32 i = 0;
        while (i < k) {
            if (f[i] < E[i]) { f[i]++; d *= q[i]; break; }
            f[i] = 0; d /= qp[i]; i++;
        }
        if (i == k) break;
    }
}

__global__ void fat_scan(const u32* __restrict__ primes, int np, u64 x, u32 nd,
                         const u64* __restrict__ g_divs,
                         u64* __restrict__ c0a, u64* __restrict__ c1a,
                         u64* __restrict__ n3a)
{
    int lo, hi;
    prime_window(primes, np, x, lo, hi);
    int ip = lo + blockIdx.x * blockDim.x + threadIdx.x;
    if (ip >= hi) return;
    u64 p = primes[ip];
    u64 c0 = 0, c1 = 0, n3 = 0;
    scan_divs(g_divs, nd, x, p, c0, c1, n3);
    if (c0 | c1) {
        atomicAdd((unsigned long long*)&c0a[ip], (unsigned long long)c0);
        if (c1) atomicAdd((unsigned long long*)&c1a[ip], (unsigned long long)c1);
        if (n3) atomicAdd((unsigned long long*)&n3a[ip], (unsigned long long)n3);
    }
}

// ============================ host ============================

static void write_csv(const char* path, const std::vector<u32>& primes,
                      const std::vector<u64>& c0, const std::vector<u64>& c1,
                      const std::vector<u64>& n3)
{
    FILE* f = fopen(path, "w");
    if (!f) { perror("fopen out"); exit(1); }
    fprintf(f, "p,ford,fI,fII\n");
    for (size_t ip = 0; ip < primes.size(); ip++) {
        long long ford = 6LL * (long long)(c0[ip] + c1[ip]) - 3LL * (long long)n3[ip];
        fprintf(f, "%u,%lld,%llu,%llu\n", primes[ip], ford, c0[ip], c1[ip]);
    }
    fclose(f);
}

int main(int argc, char** argv)
{
    if (argc < 5) {
        fprintf(stderr,
            "usage: fpcuda pmin pmax mode(0=all,1=p%%24==1,2=square classes mod 840) out.csv\n");
        return 1;
    }
    u64 pmin = strtoull(argv[1], nullptr, 10);
    u64 pmax = strtoull(argv[2], nullptr, 10);
    int mode = atoi(argv[3]);
    const char* out_path = argv[4];

    auto t_start = std::chrono::steady_clock::now();

    // ---- prime sieve over [2, pmax] ----
    size_t n = (size_t)pmax;
    std::vector<unsigned char> comp(n + 1, 0);
    for (size_t i = 2; i * i <= n; i++)
        if (!comp[i])
            for (size_t j = i * i; j <= n; j += i) comp[j] = 1;

    auto in_mode = [&](u64 p) -> bool {
        if (mode == 0) return true;
        if (mode == 1) return p % 24 == 1;
        u64 r = p % 840;
        return r == 1 || r == 121 || r == 169 || r == 289 || r == 361 || r == 529;
    };

    std::vector<u32> primes;
    u64 start = pmin < 5 ? 5 : pmin;
    for (u64 kk = start; kk <= pmax; kk++)
        if (!comp[kk] && in_mode(kk)) primes.push_back((u32)kk);
    comp.clear(); comp.shrink_to_fit();
    int np = (int)primes.size();
    fprintf(stderr, "primes in range/mode: %d\n", np);
    if (np == 0) { write_csv(out_path, primes, {}, {}, {}); return 0; }

    // ---- SPF table to xmax ----
    u64 xmax = (pmax + 1) / 2 + 2;
    std::vector<u32> spf(xmax + 1, 0);
    for (u64 i = 2; i <= xmax; i++)
        if (spf[i] == 0)
            for (u64 j = i; j <= xmax; j += i)
                if (spf[j] == 0) spf[j] = (u32)i;
    fprintf(stderr, "spf table built to %llu (%.1f MB)\n", xmax,
            (double)(spf.size() * 4) / 1e6);

    // ---- device buffers ----
    u32 *d_spf, *d_primes, *d_kfac, *d_ndfac, *d_qfac, *d_Efac;
    u64 *d_qpfac, *d_c0, *d_c1, *d_n3;
    CUDA_CHECK(cudaMalloc(&d_spf, spf.size() * sizeof(u32)));
    CUDA_CHECK(cudaMemcpy(d_spf, spf.data(), spf.size() * sizeof(u32),
                          cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMalloc(&d_primes, np * sizeof(u32)));
    CUDA_CHECK(cudaMemcpy(d_primes, primes.data(), np * sizeof(u32),
                          cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMalloc(&d_c0, (size_t)np * sizeof(u64)));
    CUDA_CHECK(cudaMalloc(&d_c1, (size_t)np * sizeof(u64)));
    CUDA_CHECK(cudaMalloc(&d_n3, (size_t)np * sizeof(u64)));
    CUDA_CHECK(cudaMemset(d_c0, 0, (size_t)np * sizeof(u64)));
    CUDA_CHECK(cudaMemset(d_c1, 0, (size_t)np * sizeof(u64)));
    CUDA_CHECK(cudaMemset(d_n3, 0, (size_t)np * sizeof(u64)));
    CUDA_CHECK(cudaMalloc(&d_kfac,  DX_CAP * sizeof(u32)));
    CUDA_CHECK(cudaMalloc(&d_ndfac, DX_CAP * sizeof(u32)));
    CUDA_CHECK(cudaMalloc(&d_qfac,  (size_t)DX_CAP * KMAX * sizeof(u32)));
    CUDA_CHECK(cudaMalloc(&d_Efac,  (size_t)DX_CAP * KMAX * sizeof(u32)));
    CUDA_CHECK(cudaMalloc(&d_qpfac, (size_t)DX_CAP * KMAX * sizeof(u64)));

    // fat-x machinery (x with d(x²) > SMEM_CAP)
    const u32 FATCAP = 262144;               // max d(x²) supported (x ≤ ~5·10⁸)
    u32 *d_fat_idx, *d_fat_cnt;
    u64 *d_fat_divs;
    CUDA_CHECK(cudaMalloc(&d_fat_idx, DX_CAP * sizeof(u32)));
    CUDA_CHECK(cudaMalloc(&d_fat_cnt, sizeof(u32)));
    CUDA_CHECK(cudaMalloc(&d_fat_divs, (size_t)FATCAP * sizeof(u64)));

    size_t smem_bytes = (size_t)SMEM_CAP * sizeof(u64);
    CUDA_CHECK(cudaFuncSetAttribute(fp_kernel,
        cudaFuncAttributeMaxDynamicSharedMemorySize, (int)smem_bytes));

    // ---- adaptive x-chunked launches (display watchdog ≈ 2 s) ----
    u64 Xcur  = pmin / 4 + 1; if (Xcur < 2) Xcur = 2;
    u64 Xend  = (pmax + 1) / 2;              // inclusive
    u64 dX    = 1 << 13;
    u64 launches = 0;
    std::vector<u64> h_c0(np), h_c1(np), h_n3(np);

    while (Xcur <= Xend) {
        u64 X1 = Xcur + dX;
        if (X1 > Xend + 1) X1 = Xend + 1;
        u32 len = (u32)(X1 - Xcur);

        auto t0 = std::chrono::steady_clock::now();
        factor_chunk<<<(len + 255) / 256, 256>>>(d_spf, Xcur, len,
                                                 d_kfac, d_ndfac, d_qfac, d_Efac, d_qpfac);
        CUDA_CHECK(cudaGetLastError());
        CUDA_CHECK(cudaMemset(d_fat_cnt, 0, sizeof(u32)));
        collect_fat<<<(len + 255) / 256, 256>>>(d_ndfac, len, d_fat_idx, d_fat_cnt);
        CUDA_CHECK(cudaGetLastError());
        fp_kernel<<<len, TPB, smem_bytes>>>(d_primes, np, Xcur,
                                            d_kfac, d_ndfac, d_qfac, d_Efac, d_qpfac,
                                            d_c0, d_c1, d_n3);
        CUDA_CHECK(cudaGetLastError());

        // fat x's of this chunk: fill global divisor list once, scan in parallel
        u32 fat_cnt = 0;
        CUDA_CHECK(cudaMemcpy(&fat_cnt, d_fat_cnt, sizeof(u32), cudaMemcpyDeviceToHost));
        if (fat_cnt > 0) {
            std::vector<u32> fat_idx(fat_cnt);
            CUDA_CHECK(cudaMemcpy(fat_idx.data(), d_fat_idx, fat_cnt * sizeof(u32),
                                  cudaMemcpyDeviceToHost));
            for (u32 fi = 0; fi < fat_cnt; fi++) {
                u32 j = fat_idx[fi];
                u32 kx = 0, nd = 0;
                CUDA_CHECK(cudaMemcpy(&kx, d_kfac + j, sizeof(u32), cudaMemcpyDeviceToHost));
                CUDA_CHECK(cudaMemcpy(&nd, d_ndfac + j, sizeof(u32), cudaMemcpyDeviceToHost));
                if (nd > FATCAP) {
                    fprintf(stderr, "FATAL: d(x²)=%u exceeds FATCAP at x=%llu\n",
                            nd, Xcur + j);
                    exit(1);
                }
                u64 x = Xcur + j;
                // prime window on host for the launch geometry
                u64 plo = 2 * x - 1, phi = 4 * x;
                int lo = (int)(std::lower_bound(primes.begin(), primes.end(), (u32)std::min<u64>(plo, ~0u)) - primes.begin());
                int hi = (int)(std::lower_bound(primes.begin(), primes.end(), (u32)std::min<u64>(phi, ~0u)) - primes.begin());
                if (lo >= hi) continue;
                fat_fill<<<1, 1>>>(x, kx, d_qfac, d_Efac, d_qpfac, j, d_fat_divs);
                CUDA_CHECK(cudaGetLastError());
                fat_scan<<<(hi - lo + TPB - 1) / TPB, TPB>>>(d_primes, np, x, nd,
                                                             d_fat_divs, d_c0, d_c1, d_n3);
                CUDA_CHECK(cudaGetLastError());
            }
        }
        CUDA_CHECK(cudaDeviceSynchronize());
        double dt = std::chrono::duration<double>(
                        std::chrono::steady_clock::now() - t0).count();

        Xcur = X1;
        launches++;
        if (dt < 0.12 && dX < DX_CAP) dX *= 2;
        else if (dt > 0.5 && dX > 1024) dX /= 2;

        if (launches % 100 == 0 || Xcur > Xend) {
            double frac = (double)(Xcur - (pmin / 4 + 1)) /
                          (double)(Xend - (pmin / 4 + 1) + 1);
            double el = std::chrono::duration<double>(
                            std::chrono::steady_clock::now() - t_start).count();
            fprintf(stderr, "x=%llu/%llu (%.1f%%) launches=%llu dX=%llu elapsed=%.0fs eta=%.0fs\n",
                    Xcur, Xend, 100.0 * frac, launches, dX, el,
                    frac > 0 ? el / frac - el : 0.0);
        }
        if (launches % 600 == 0) {           // checkpoint
            CUDA_CHECK(cudaMemcpy(h_c0.data(), d_c0, (size_t)np * sizeof(u64), cudaMemcpyDeviceToHost));
            CUDA_CHECK(cudaMemcpy(h_c1.data(), d_c1, (size_t)np * sizeof(u64), cudaMemcpyDeviceToHost));
            CUDA_CHECK(cudaMemcpy(h_n3.data(), d_n3, (size_t)np * sizeof(u64), cudaMemcpyDeviceToHost));
            char tmp[4096];
            snprintf(tmp, sizeof tmp, "%s.partial", out_path);
            write_csv(tmp, primes, h_c0, h_c1, h_n3);
        }
    }

    CUDA_CHECK(cudaMemcpy(h_c0.data(), d_c0, (size_t)np * sizeof(u64), cudaMemcpyDeviceToHost));
    CUDA_CHECK(cudaMemcpy(h_c1.data(), d_c1, (size_t)np * sizeof(u64), cudaMemcpyDeviceToHost));
    CUDA_CHECK(cudaMemcpy(h_n3.data(), d_n3, (size_t)np * sizeof(u64), cudaMemcpyDeviceToHost));
    write_csv(out_path, primes, h_c0, h_c1, h_n3);

    double total = std::chrono::duration<double>(
                       std::chrono::steady_clock::now() - t_start).count();
    fprintf(stderr, "primes=%d launches=%llu time=%.1fs\n", np, launches, total);
    return 0;
}
