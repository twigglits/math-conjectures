/* fsigned.c — graded census of SIGNED solutions of 4/n = 1/x + 1/y + 1/z
 *
 * Counts multisets {x,y,z} ⊂ ℤ* (trivial cancelling triples excluded) graded
 * by k = #negatives:  f0 (the classical f), f1, f2 — via the window
 * dictionary of REPORT.md §11.3, machine-validated in verify_signed.py
 * against an independent naive census for all 2 ≤ n ≤ 200:
 *
 *   x = least positive denominator (k∈{0,1}) or the unique one (k=2),
 *   a = 4x−n, B = nx, dmin = 2x(2x−n); solutions ↔ divisors d of B²,
 *   d ≡ −B (mod |a|) (+ exact partner integrality when gcd(a,B)>1), with
 *     k=0:  n/4 < x ≤ 3n/4,  max(1,dmin) ≤ d ≤ B
 *     k=1:  n/4 < x ≤ n/2,   dmin ≤ d ≤ −1
 *     k=1:  1 ≤ x < n/4,     d ≤ dmin (< −B)
 *     k=2:  1 ≤ x < n/4,     1 ≤ d ≤ B
 *   slots y = (B+d)/a, z = (B+B²/d)/a.
 *
 * Type strata by v = ν_n(|d|) ∈ {0,1,2}: v=0 ⇔ Type I shape, v=1 ⇔ Type II,
 * v=2 ⇔ "Type III" — provably impossible in the positive windows (asserted).
 *
 * build:  gcc -O3 -march=native -fopenmp fsigned.c -o fsigned
 * usage:  ./fsigned LO HI all          > census.csv        (every n in [LO,HI])
 *         ./fsigned LO HI p24:1        > primes.csv        (primes ≡ 1 mod 24)
 *         ./fsigned LO HI p840:73      > covered.csv       (primes ≡ 73 mod 840)
 * output: n,f0,f0I,f0II,f1,f1I,f1II,f1III,f2,f2I,f2II
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#ifdef _OPENMP
#include <omp.h>
#endif

typedef __int128 i128;
typedef long long i64;

static int32_t *spf;                 /* smallest prime factor, 2..HI */
static void sieve(int64_t N) {
    spf = malloc((N + 1) * sizeof *spf);
    if (!spf) { fprintf(stderr, "sieve alloc failed\n"); exit(1); }
    for (int64_t i = 0; i <= N; i++) spf[i] = 0;
    for (int64_t i = 2; i <= N; i++) {
        if (!spf[i]) for (int64_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = (int32_t)i;
    }
}

static int factor_into(i64 m, i64 *pr, int *ex, int k) {
    /* append factorization of m (≤ sieve bound) into pr/ex, merging duplicates */
    while (m > 1) {
        i64 p = spf[m]; int e = 0;
        while (m % p == 0) { m /= p; e++; }
        int j;
        for (j = 0; j < k; j++) if (pr[j] == p) { ex[j] += e; break; }
        if (j == k) { pr[k] = p; ex[k] = e; k++; }
    }
    return k;
}

#define DCAP (1 << 19)

typedef struct { i64 f0, f0I, f0II, f1, f1I, f1II, f1III, f2, f2I, f2II; } row_t;

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s LO HI all|pMOD:R\n", argv[0]); return 1; }
    i64 LO = atoll(argv[1]), HI = atoll(argv[2]);
    i64 pmod = 0, pres = 0; int primes_only = 0;
    if (strcmp(argv[3], "all") != 0) {
        if (sscanf(argv[3], "p%lld:%lld", &pmod, &pres) != 2) {
            fprintf(stderr, "bad mode %s\n", argv[3]); return 1;
        }
        primes_only = 1;
    }
    sieve(HI);
    row_t *rows = calloc(HI - LO + 1, sizeof *rows);
    int8_t *sel = calloc(HI - LO + 1, 1);
    i64 nsel = 0;
    for (i64 n = LO; n <= HI; n++) {
        if (n < 2) continue;
        if (primes_only && (spf[n] != n || n % pmod != pres)) continue;
        sel[n - LO] = 1; nsel++;
    }
    fprintf(stderr, "fsigned: %lld values in [%lld,%lld] mode %s\n", nsel, LO, HI, argv[3]);

#pragma omp parallel
    {
        i128 *div = malloc(DCAP * sizeof *div);
        if (!div) { fprintf(stderr, "divbuf alloc failed\n"); exit(1); }
#pragma omp for schedule(dynamic, 8)
        for (i64 n = LO; n <= HI; n++) {
            if (!sel[n - LO]) continue;
            i64 prn[24]; int exn[24];
            int kn = factor_into(n, prn, exn, 0);
            i64 n2 = n * n;            /* n ≤ ~3e5 here: n² < 2^63 */
            row_t R; memset(&R, 0, sizeof R);
            for (i64 x = 1; 4 * x <= 3 * n; x++) {
                i64 a = 4 * x - n;
                if (a == 0) continue;                     /* trivial-family row */
                i64 m = a > 0 ? a : -a;
                i64 B = n * x;
                i64 dmin = 2 * x * (2 * x - n);           /* may be negative */
                i64 pr[24]; int ex[24];
                memcpy(pr, prn, kn * sizeof *pr); memcpy(ex, exn, kn * sizeof *ex);
                int k = factor_into(x, pr, ex, kn);
                /* enumerate divisors of B² */
                i64 cnt = 1; div[0] = 1;
                for (int i = 0; i < k; i++) {
                    i64 c0 = cnt;
                    if (cnt * (2 * ex[i] + 1) > DCAP) { fprintf(stderr, "DCAP n=%lld x=%lld\n", n, x); exit(2); }
                    i128 pw = 1;
                    for (int e = 1; e <= 2 * ex[i]; e++) {
                        pw *= pr[i];
                        for (i64 j = 0; j < c0; j++) div[cnt++] = div[j] * pw;
                    }
                }
                i128 B2 = (i128)B * B;
                for (i64 i = 0; i < cnt; i++) {
                    i128 d0 = div[i];
                    if (d0 <= B) {                         /* u64-fast small side */
                        i64 dl = (i64)d0;
                        if (a > 0) {
                            /* k0: d=+d0 in [max(1,dmin), B] */
                            if (dl >= dmin && (dl + B) % a == 0) {
                                i128 sl2 = B + (i128)(B2 / d0);
                                if (sl2 % a == 0) {
                                    i64 y = (dl + B) / a;             /* int64-safe: ≤ 2B/a */
                                    i128 z = sl2 / a;
                                    int triv = (n % 4 == 0) &&
                                        (x + y == 0 || x + z == 0 || y + z == 0);
                                    if (!triv) {
                                        int v = dl % n ? 0 : (dl % n2 ? 1 : 2);
                                        if (v == 2) { fprintf(stderr, "f0 TypeIII?! n=%lld\n", n); exit(3); }
                                        R.f0++; if (v == 0) R.f0I++; else R.f0II++;
                                    }
                                }
                            }
                            /* k1a: d=−d0, window [dmin,−1] ⇔ d0 ≤ 2x(n−2x) */
                            if (dl <= -dmin && (B - dl) % a == 0) {
                                i128 sl2 = B - (i128)(B2 / d0);
                                if (sl2 % a == 0) {
                                    i64 y = (B - dl) / a;
                                    i128 z = sl2 / a;
                                    int triv = (n % 4 == 0) &&
                                        ((i128)x + y == 0 || (i128)x + z == 0 || y + z == 0);
                                    if (!triv) {
                                        int v = dl % n ? 0 : (dl % n2 ? 1 : 2);
                                        R.f1++; if (v == 0) R.f1I++; else if (v == 1) R.f1II++; else R.f1III++;
                                    }
                                }
                            }
                        } else {
                            /* k2: d=+d0 in [1, B] (x < n/4) */
                            if ((dl + B) % m == 0) {
                                i128 sl2 = B + (i128)(B2 / d0);
                                if (sl2 % a == 0) {
                                    int v = dl % n ? 0 : (dl % n2 ? 1 : 2);
                                    if (v == 2) { fprintf(stderr, "f2 TypeIII?! n=%lld\n", n); exit(3); }
                                    /* trivial impossible in k2 for n>0 */
                                    R.f2++; if (v == 0) R.f2I++; else R.f2II++;
                                }
                            }
                        }
                    } else if (a < 0) {
                        /* k1b: d=−d0 ≤ dmin ⇔ d0 ≥ 2x(n−2x) (> B); x < n/4 */
                        if (d0 >= (i128)2 * x * (n - 2 * x) && (B - d0) % m == 0) {
                            i128 sl2 = B - (i128)(B2 / d0);
                            if (sl2 % a == 0) {
                                i128 y = (B - d0) / a;       /* = (d0−B)/m > 0 */
                                i128 z = sl2 / a;
                                int triv = (n % 4 == 0) &&
                                    ((i128)x + y == 0 || (i128)x + z == 0 || y + z == 0);
                                if (!triv) {
                                    int v = d0 % n ? 0 : (d0 % n2 ? 1 : 2);
                                    R.f1++; if (v == 0) R.f1I++; else if (v == 1) R.f1II++; else R.f1III++;
                                }
                            }
                        }
                    }
                }
            }
            rows[n - LO] = R;
        }
        free(div);
    }
    printf("n,f0,f0I,f0II,f1,f1I,f1II,f1III,f2,f2I,f2II\n");
    for (i64 n = LO; n <= HI; n++) {
        if (!sel[n - LO]) continue;
        row_t *R = &rows[n - LO];
        printf("%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld\n",
               n, R->f0, R->f0I, R->f0II, R->f1, R->f1I, R->f1II, R->f1III,
               R->f2, R->f2I, R->f2II);
    }
    return 0;
}
