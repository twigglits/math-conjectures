// fpr.rs — Erdős–Straus solution counter f(p) with Type I / Type II split.
// Std-only port of the validated C engine (fp.c); no crates needed.
//
// Build:    rustc -C opt-level=3 -C target-cpu=native fpr.rs -o fpr
// Run:      ./fpr <pmin> <pmax> <mode: 0 = all primes, 1 = only p ≡ 1 mod 24> <out.csv> [threads]
// Verify:   ./fpr 5 2000 0 rs_small.csv 4   &&   diff rs_small.csv fp_small.csv
//           (fp_small.csv was validated against hand enumeration and an
//            independent brute-force oracle; the diff must be empty.)
// Example:  ./fpr 300001 10000000 1 hard_to_1e7.csv $(nproc)
//
// Method recap: for each x in (p/4, 3p/4], let a = 4x − p, B = px
// (gcd(a, B) = 1 for prime p > 3). Solutions with smallest denominator x
// correspond to divisors d | B² with d ≤ B and d ≡ −B (mod a), filtered by
// the y ≥ x condition d ≥ dmin = 2x(2x − p) whenever 2x > p.
// Since p ≡ 4x (mod a), this splits into:
//   Type I  (p ∤ d):   d  | x²,            d  ≡ −4x² (mod a)   [only z divisible by p]
//   Type II (d = pd'): d' | x²,  d' ≤ x,   d' ≡ −x   (mod a)   [y and z divisible by p]
// Ordered count: distinct triple → 6; one repeated pair → 3
//   (x = y iff d == dmin > 0;  y = z iff Type II with d' == x).
// Parallelism: threads stripe the outer x loop (x ≡ t mod T); each thread's
// two-pointer prime window stays monotone; per-thread accumulators merge at the end.

use std::env;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::sync::Arc;
use std::thread;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 5 {
        eprintln!("usage: fpr pmin pmax mode(0=all,1=p%24==1) out.csv [threads]");
        std::process::exit(1);
    }
    let pmin: i64 = args[1].parse().expect("pmin");
    let pmax: i64 = args[2].parse().expect("pmax");
    let mode: i64 = args[3].parse().expect("mode");
    let out_path = args[4].clone();
    let nthreads: usize = if args.len() > 5 { args[5].parse().expect("threads") } else { 1 };

    let t0 = Instant::now();
    let n = pmax as usize;
    let xmax: usize = (3 * n) / 4 + 2;

    // --- prime sieve to pmax ---
    let mut comp = vec![false; n + 1];
    let mut i = 2usize;
    while i * i <= n {
        if !comp[i] {
            let mut j = i * i;
            while j <= n {
                comp[j] = true;
                j += i;
            }
        }
        i += 1;
    }
    let start = if pmin < 5 { 5usize } else { pmin as usize };
    let primes: Vec<i64> = (start..=n)
        .filter(|&k| !comp[k] && (mode == 0 || k % 24 == 1))
        .map(|k| k as i64)
        .collect();
    let np = primes.len();

    // --- smallest-prime-factor sieve to xmax (for fast factorization of x) ---
    let mut spf = vec![0u32; xmax + 1];
    for k in 2..=xmax {
        if spf[k] == 0 {
            let mut j = k;
            while j <= xmax {
                if spf[j] == 0 {
                    spf[j] = k as u32;
                }
                j += k;
            }
        }
    }

    let primes = Arc::new(primes);
    let spf = Arc::new(spf);

    let mut handles = Vec::new();
    for t in 0..nthreads {
        let primes = Arc::clone(&primes);
        let spf = Arc::clone(&spf);
        handles.push(thread::spawn(move || {
            let mut lford = vec![0i64; np];
            let mut lf1 = vec![0i64; np];
            let mut lf2 = vec![0i64; np];
            let mut divs: Vec<i64> = Vec::with_capacity(8192);
            let (mut lo, mut hi) = (0usize, 0usize);
            let mut x = 2 + t;
            while x <= xmax {
                let xi = x as i64;
                // window of primes with x in (p/4, 3p/4]:  4x/3 <= p < 4x
                while lo < np && 3 * primes[lo] < 4 * xi {
                    lo += 1;
                }
                if lo >= np {
                    break;
                }
                while hi < np && primes[hi] < 4 * xi {
                    hi += 1;
                }
                if lo < hi {
                    // divisors of x^2 from the factorization of x
                    divs.clear();
                    divs.push(1);
                    let mut tt = x;
                    while tt > 1 {
                        let q = spf[tt] as usize;
                        let mut e = 0usize;
                        while tt % q == 0 {
                            tt /= q;
                            e += 1;
                        }
                        let base = divs.len();
                        let mut pe: i64 = 1;
                        for _ in 0..(2 * e) {
                            pe *= q as i64;
                            for i2 in 0..base {
                                let v = divs[i2] * pe;
                                divs.push(v);
                            }
                        }
                    }
                    for ip in lo..hi {
                        let p = primes[ip];
                        let a = 4 * xi - p;
                        let xm = xi % a;
                        let r0 = (a - (4 * xm % a) * xm % a) % a; // (-4x^2) mod a
                        let r1 = (a - xm) % a; //                     (-x)  mod a
                        let dmin = if 2 * xi > p { 2 * xi * (2 * xi - p) } else { 0 };
                        let mut c0 = 0i64;
                        let mut c1 = 0i64;
                        let mut n3 = 0i64;
                        for &d in divs.iter() {
                            let m = d % a;
                            if m == r0 && d >= dmin {
                                c0 += 1;
                                if dmin > 0 && d == dmin {
                                    n3 += 1; // x == y
                                }
                            }
                            if d <= xi && m == r1 && p * d >= dmin {
                                c1 += 1;
                                if d == xi {
                                    n3 += 1; // y == z
                                }
                                if dmin > 0 && p * d == dmin {
                                    n3 += 1; // x == y via Type II
                                }
                            }
                        }
                        lford[ip] += 6 * (c0 + c1) - 3 * n3;
                        lf1[ip] += c0;
                        lf2[ip] += c1;
                    }
                }
                x += nthreads;
            }
            (lford, lf1, lf2)
        }));
    }

    let mut ford = vec![0i64; np];
    let mut f1 = vec![0i64; np];
    let mut f2 = vec![0i64; np];
    for h in handles {
        let (a, b, c) = h.join().unwrap();
        for k in 0..np {
            ford[k] += a[k];
            f1[k] += b[k];
            f2[k] += c[k];
        }
    }

    let f = File::create(&out_path).expect("create out");
    let mut w = BufWriter::new(f);
    writeln!(w, "p,ford,fI,fII").unwrap();
    for k in 0..np {
        writeln!(w, "{},{},{},{}", primes[k], ford[k], f1[k], f2[k]).unwrap();
    }
    eprintln!(
        "primes={} threads={} time={:.1}s",
        np,
        nthreads,
        t0.elapsed().as_secs_f64()
    );
}
