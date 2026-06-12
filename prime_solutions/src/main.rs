/*
 * CUDA-Rust kernel for counting solutions of 4/p = 1/x + 1/y + 1/z
 *
 * Port of fp.c to NVIDIA CUDA via cuda-oxide (pure Rust → PTX).
 *
 * Algorithm:
 *   For x in (p/4, 3p/4] and prime p > 3:
 *     a = 4x - p,  B = p*x  (gcd(a,B)==1 for prime>3)
 *     Solutions ↔ divisors d | x^2 meeting modular conditions:
 *       Type I (p ∤ d):  d ≡ -4x² (mod a),  d ≥ dmin
 *       Type II (d=pd'):  d' ≡ -x (mod a), d' ≤ x,  p·d' ≥ dmin
 *     Ordered count: 6*(cI + cII) - 3*n3   (n3 for degenerate x==y or y==z)
 *
 * GPU design: one thread per (x, p_i) pair.
 *   - SPF table pre-computed on CPU for O(log x) factorization
 *   - Divisors of x² generated per-thread (max ~60K for x < 2·10⁶)
 *   - Atomic i64 additions accumulate ford/fI/fII per prime
 */

use cuda_core::{CudaContext, DeviceBuffer, LaunchConfig};
use cuda_device::atomic::DeviceAtomicI64;
use cuda_device::{DisjointSlice, kernel, thread};
use cuda_host::cuda_module;

// Per-thread divisor buffer cap. CAUTION: (a) 65536×8 B = 512 KB of local
// memory per thread — at or beyond the hardware limit, and an occupancy
// killer at any scale; (b) any x with d(x²) > MAX_DIVS is silently
// undercounted. Safe at the demo scale here (pmax ≈ 10⁴ ⇒ d(x²) ≤ ~400);
// NOT safe for production. The validated production engine (files/fp.cu)
// enumerates divisors with an odometer instead — no buffer, no cap.
const MAX_DIVS: usize = 65536;

// ============================================================
// GPU KERNELS
// ============================================================

#[cuda_module]
mod kernels {
    use super::*;

    /// Per-thread divisor buffer (stack-allocated, fits in registers/local mem).
    /// Each (x, p_i) thread generates divisors of x² inline.
    #[kernel]
    pub fn solve_for_x(
        spf: &[u32],
        spf_len: u32,
        primes: &[u32],
        n_primes: u32,
        pmin: u32,
        x_max: u32,
        ford: &[i64],
        fI: &[i64],
        fII: &[i64],
    ) {
        let gid_raw = thread::index_1d().get();
        let n_primes_usize = n_primes as usize;
        let x_max_usize = x_max as usize;

        // Decode global thread id into (x, p_i)
        let x = (gid_raw / n_primes_usize) + 2; // x starts at 2
        let ip = gid_raw % n_primes_usize;

        if x > x_max_usize || ip >= n_primes_usize {
            return;
        }

        let p = primes[ip as usize] as u64;
        let x64 = x as u64;

        // Window: x in (p/4, 3p/4], matching fp.c / fpr.rs.
        // Keep x iff  p < 4x  (x > p/4)  and  4x <= 3p  (x <= 3p/4).
        // NOTE: an earlier revision had the first test inverted (kept x > 3p/4,
        // the exact complement of the window) — fixed 2026-06-11; validated
        // production engine is files/fp.cu.
        if 3u64 * p < 4u64 * x64 {
            return; // x > 3p/4 — beyond the window
        }
        if p >= 4u64 * x64 {
            return; // x <= p/4 — below the window
        }

        let a = 4u64 * x64 - p; // a = 4x - p

        // --- Generate divisors of x² using SPF table ---
        let mut divs: [i64; MAX_DIVS] = [0i64; MAX_DIVS];
        let mut nd: usize = 1;
        divs[0] = 1;

        let mut t = x as u32;
        while t > 1 {
            if (t as usize) >= spf_len as usize {
                break;
            }
            let q = spf[t as usize] as u64;
            let mut e = 0usize;
            while t as u64 % q == 0 {
                t /= q as u32;
                e += 1;
            }

            let base = nd;
            let mut pe: u64 = 1;
            for _n in 0..2usize * e {
                pe *= q;
                for i2 in 0..base {
                    if nd < MAX_DIVS {
                        divs[nd] = (divs[i2] as u64 * pe) as i64;
                        nd += 1;
                    }
                }
            }
        }

        // Modular targets
        let xm = x64 % a;
        let r0 = (a - ((4u64 * xm) % a) * xm
            % a)
            % a;                         // (-4x²) mod a
        let r1 = (a - xm) % a;           // (-x)  mod a

        let dmin = if 2u64 * x64 > p {
            2u64 * x64 * (2u64 * x64 - p)
        } else {
            0u64
        };

        let mut c0: u64 = 0;  // Type I count
        let mut c1: u64 = 0;  // Type II count
        let mut n3: u64 = 0;  // degenerate (x==y or y==z)

        for i2 in 0..nd {
            let d_u64 = divs[i2] as u64;
            if d_u64 == 0 {
                continue;
            }
            let m = d_u64 % a;

            // Type I: d ≡ -4x² (mod a), d >= dmin
            if m == r0 && d_u64 >= dmin {
                c0 += 1;
                if dmin > 0 && d_u64 == dmin {
                    n3 += 1; // x == y
                }
            }

            // Type II: d' ≡ -x (mod a), d' <= x, p*d' >= dmin
            if d_u64 <= x64 && m == r1 && p * d_u64 >= dmin {
                c1 += 1;
                if d_u64 == x64 {
                    n3 += 1; // y == z
                }
                if dmin > 0 && p * d_u64 == dmin {
                    n3 += 1; // x == y (tier II)
                }
            }
        }

        // Atomic add into result arrays
        let contrib = 6i64 * (c0 as i64 + c1 as i64) - 3i64 * (n3 as i64);

        let ip_usize = ip as usize;

        // ford[ip] += contrib
        let atomic_ford: &DeviceAtomicI64 =
            unsafe { &*(ford.as_ptr().add(ip_usize) as *const DeviceAtomicI64) };
        atomic_ford.fetch_add(contrib, cuda_device::atomic::AtomicOrdering::Relaxed);

        // fI[ip] += c0
        let atomic_fi: &DeviceAtomicI64 =
            unsafe { &*(fI.as_ptr().add(ip_usize) as *const DeviceAtomicI64) };
        atomic_fi.fetch_add(c0 as i64, cuda_device::atomic::AtomicOrdering::Relaxed);

        // fII[ip] += c1
        let atomic_fii: &DeviceAtomicI64 =
            unsafe { &*(fII.as_ptr().add(ip_usize) as *const DeviceAtomicI64) };
        atomic_fii.fetch_add(c1 as i64, cuda_device::atomic::AtomicOrdering::Relaxed);
    }
}

// ============================================================
// HOST: Sieve, SPF, prime list, device transfer, kernel launch
// ============================================================

/// Simple sieve to find all primes up to pmax (returns Vec<u32>).
fn sieve_primes(pmax: u32, pmin: u32) -> Vec<u32> {
    let mut is_comp = vec![false; (pmax as usize) + 1];
    for i in 2u32..=((pmax as f64).sqrt() as u32) {
        if !is_comp[i as usize] {
            let mut j = i * i;
            while j <= pmax {
                is_comp[j as usize] = true;
                j += i;
            }
        }
    }
    let start = if pmin < 5 { 5 } else { pmin };
    (start..=pmax).filter(|&i| !is_comp[i as usize]).collect()
}

/// Smallest prime factor table for all integers up to n.
fn spf_table(n: u32) -> Vec<u32> {
    let mut spf = vec![0u32; (n as usize) + 1];
    for i in 2..=n {
        if spf[i as usize] == 0 {
            let mut j = i;
            while j <= n {
                if spf[j as usize] == 0 {
                    spf[j as usize] = i;
                }
                j += i;
            }
        }
    }
    spf
}

fn main() {
    // ---------- parameters ----------
    let pmin: u32 = 5;
    let pmax: u32 = 10007;
    let mode: usize = 0; // 0=all primes, 1=only p%24==1

    println!("=== Fermi-Pick 4/p = 1/x + 1/y + 1/z (cuda-oxide) ===");
    println!("prime range: [{}, {}]  mode: {}", pmin, pmax, mode);

    // ---------- host-side sieves ----------
    let primes_raw = sieve_primes(pmax, pmin);
    let primes: Vec<u32> = if mode == 1 {
        primes_raw.into_iter().filter(|&p| p % 24 == 1).collect()
    } else {
        primes_raw
    };
    let n_primes = primes.len() as u32;
    println!("primes found: {}", n_primes);

    let x_max = (3u32 * pmax / 4) + 2;
    let spf = spf_table(x_max);
    println!("spf table size: {}  (x range: 2..{})", spf.len(), x_max);

    // x goes from 2 to x_max inclusive → x_count values
    let x_count = x_max - 1; // 2,3,...,x_max
    let total_threads = x_count as u64 * n_primes as u64;
    println!("total (x, p_i) threads: {}", total_threads);

    // ---------- CUDA context & device buffers ----------
    let ctx = CudaContext::new(0).expect("CUDA context creation failed");
    let stream = ctx.default_stream();

    let spf_dev = DeviceBuffer::from_host(&stream, &spf).expect("spf transfer failed");
    let primes_dev =
        DeviceBuffer::from_host(&stream, &primes).expect("primes transfer failed");

    let ford_dev = DeviceBuffer::<i64>::zeroed(&stream, n_primes as usize)
        .expect("ford allocation failed");
    let fi_dev = DeviceBuffer::<i64>::zeroed(&stream, n_primes as usize)
        .expect("fI allocation failed");
    let fii_dev = DeviceBuffer::<i64>::zeroed(&stream, n_primes as usize)
        .expect("fII allocation failed");

    // ---------- load embedded module & launch kernel ----------
    let module = kernels::load(&ctx).expect("Failed to load embedded CUDA module");

    let launch = if (total_threads as u64) == (total_threads as u32) as u64 {
        LaunchConfig::for_num_elems(total_threads as u32)
    } else {
        // For huge problem sizes, use multiple blocks explicitly
        let block_dim = 512u32;
        let grid_dim = ((total_threads as u64 + block_dim as u64 - 1) / block_dim as u64) as u32;
        LaunchConfig {
            grid_dim: (grid_dim, 1, 1),
            block_dim: (block_dim, 1, 1),
            shared_mem_bytes: 0,
        }
    };

    let start = std::time::Instant::now();

    module
        .solve_for_x(
            &stream,
            launch,
            &spf_dev,
            spf.len() as u32,
            &primes_dev,
            n_primes,
            pmin,
            x_max,
            &ford_dev,
            &fi_dev,
            &fii_dev,
        )
        .expect("Kernel launch failed");

    // ---------- readback & print first 20 primes ----------
    let ford_host = ford_dev.to_host_vec(&stream).expect("ford readback failed");
    let fi_host = fi_dev.to_host_vec(&stream).expect("fI readback failed");
    let fii_host = fii_dev.to_host_vec(&stream).expect("fII readback failed");

    let elapsed = start.elapsed();
    println!("\nGPU elapsed: {:.2?}", elapsed);
    println!("\n{:10} {:>12} {:>12} {:>12}", "p", "ford", "fI", "fII");
    println!("{:-<48}", "");

    let show = n_primes.min(20);
    for i in 0..show {
        println!(
            "{:10} {:>12} {:>12} {:>12}",
            primes[i as usize], ford_host[i as usize], fi_host[i as usize], fii_host[i as usize]
        );
    }
    if n_primes as usize > 20 {
        println!("... ({} more primes)", n_primes as usize - 20);
    }

    // ---------- summary stats ----------
    let total_ford: i64 = ford_host.iter().copied().sum();
    let total_fi: i64 = fi_host.iter().copied().sum();
    let total_fii: i64 = fii_host.iter().copied().sum();
    println!("\ntotal ford: {}", total_ford);
    println!("total fI: {}", total_fi);
    println!("total fII: {}", total_fii);
    println!("=== DONE ===");
}
