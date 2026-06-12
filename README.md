# Erdős–Straus conjecture: An experimental expansion approach

<div align="justify">

This repository is an effort towards a solution of the **Erdős–Straus
conjecture** (Erdős & Straus, 1948) — by exhaustive computation, machine-verified
proof attempts, statistical law-finding, and a structural extension of the problem
to the negative integers. The conjecture remains **open**; what this project
contributes is measurement and structure: the largest per-prime solution-count
datasets we are aware of, several empirical laws confirmed by blind prediction, a
set of machine-verified theorems locating exactly *why* the elementary toolbox
cannot close the problem, and the first quantitative study (to our knowledge) of
the conjecture over $\mathbb{Z}$.

</div>

## The conjecture

> For every integer $n \ge 2$ there exist **positive** integers $x, y, z$ with
>
> $$\frac{4}{n} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}.$$

<div align="justify">

It suffices to prove it for primes. Solutions are known to exist for every $n$
except possibly primes in the six "square classes"
$p \equiv 1^2,\, 11^2,\, 13^2,\, 17^2,\, 19^2,\, 23^2 \pmod{840}$, where every
covering-congruence identity provably dies (Mordell, Schinzel). The conjecture has
been verified up to $10^{17}$ (Salez 2014; a 2025 preprint claims $10^{18}$). See
[References](#references) for the canonical statements.

</div>

## Abstract

<div align="justify">

We study $f(p)$, the number of unordered solutions of
$\frac{4}{p} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}$, across $278{,}570$ primes
of the hard residue classes from $73$ up to $2.01\times10^{9}$ — beyond the largest
published per-prime dataset ($3.5\times10^{7}$) — using four independently written
engines (C, Rust, CUDA, Python) that agree byte-for-byte at five scales and
reproduce the published external dataset with zero discrepancies. Empirically,
$\ln f(p)$ is window-normal with shrinking dispersion; its extreme-value
consequences predicted the minima of three then-uncomputed ranges blind
($\min f = 191 \in [175, 225]$ at $2\times10^{8}$; $347$ vs $345$ at $10^{9}$;
median $681$ exact and $\min f = 405$ vs $[351, 404]$ at $2\times10^{9}$). A
machine-verified proof-attempt section re-derives the square obstruction in full,
proves an $\varepsilon$-covering theorem — identity families can approach but never
reach full coverage, at cost $T \approx \exp(\varepsilon^{-2})$ — and a
no-finite-channel-system theorem, locating the precise wall: a pointwise lower
bound for divisors of shifted integers in prescribed residue classes, available
today only on average.

Extending the problem to **negative integers** — this repository's guiding
question — collapses it (two signed unit fractions always suffice; the failure sets
of the two $2$-term forms are exactly complementary) and reveals the conjecture to
be a *chirality statement*: the solution set is graded by the number of negative
denominators, the negative-$n$ axis is an exact mirror, the square obstruction
lives only in the positive-sign sector, and the "starved" hard classes are the
*richest* in one-negative solutions (rank correlation $-0.43$; the record prime
$p = 2521$ has $9$ positive solutions and $684$ signed ones). Finally, the
lognormal residual itself decomposes: $\approx$58% is a congruence ladder obeying
a measured decay law $s_q \approx 18\cdot q^{-1.95}$ (non-residues richer at every
modulus, as the obstruction theory predicts), $\approx$42% is factorization
noise — and the maximally hostile congruence configuration reaches only 10% of
the depth a counterexample needs. A congruence-only score built from the ladder
ranks the $f$-landscape at $10\times$ its fitting range ($\rho \approx +0.72$) and
locates window floors for $\sim$1% of sweep cost — an instrument for adversarial
searches at scales where exhaustion is impossible.

None of this proves or disproves the conjecture — the project's own theorems
explain why this toolbox cannot — but the laws, datasets, and the signed-world
structure are, as far as a careful literature search could establish (2026-06; we
could not access MathSciNet/zbMATH), not previously recorded.

</div>

## Methodology

The project's rule: **no claim without a machine check, no engine without
independent validation, no model without a blind test.**

- **Validation-first computation.** Four engines written independently:
  `files/fp.c` (C), `files/fpr.rs` (Rust), `files/fp.cu` (CUDA, RTX 5090),
  `files/fsigned.c` (C/OpenMP, signed grading). Byte-identical outputs at five
  scales ($2\times10^{3}$, $10^{6}$, $3.5\times10^{7}$, $10^{8}$, $2\times10^{9}$),
  against a blessed hand-validated reference, and against the independent published
  dataset of arXiv:2509.00128 on $22{,}662$ overlapping primes — zero mismatches
  anywhere.
- **Machine-verified mathematics.** Every numbered claim in the proof-attempt and
  signed-extension sections is checked in exact arithmetic:
  `files/verify_lemmas.py` ($8{,}719$ assertions, REPORT §9) and
  `files/verify_signed.py` ($536{,}988$ assertions, REPORT §11).
- **Blind prediction protocol.** Statistical models are fitted on small scales,
  frozen, and tested on uncomputed ranges (fits $\le 2\times10^{8}$; tests at
  $10^{9}$ and $2\times10^{9}$, stated in the transcript before the runs finished).
- **Exact arithmetic everywhere** (integer / `Fraction` in Python; `__int128` in
  C); divisor-class enumeration via the kernel described in REPORT §9.1.
- Hardware: i9-9900K ($16$ threads), RTX 5090 ($32$ GB). A $10^{7}$-wide hard-class
  slice at $2\times10^{9}$ takes ${\sim}46$ GPU-minutes.
- All sessions were conducted as an interactive human–AI collaboration (direction
  and the extension idea: repository owner; derivations, engines, and analyses:
  Claude, Anthropic — see commit trailers). Every result above is verified by code
  that does not depend on the assistant's reasoning being correct.

## Findings

Full details and tables live in [REPORT.md](REPORT.md); figures in `files/plots/`.

<div align="justify">

**F1 — The landscape: zero-free, rising, tightening.**
$f, f_I, f_{II} > 0$ for all $278{,}570$ computed hard-class primes to
$2.01\times10^{9}$; the floor grows as ${\sim}(\ln p)^{3.4 \pm 0.2}$ at the same
exponent as the median; $\sigma(\ln f)$ shrinks $0.30 \to 0.144$ across five
decades. Code: `files/fp.cu`, `files/fpr.rs`, `files/analyze_final.py`,
`files/analyze_session2.py`; data `files/hard_*.csv`, `files/fresh_2e9_slice.csv`;
REPORT §2, §10, §12.5.

</div>

![The f(p) landscape](files/plots/1_landscape.png)

<div align="justify">

**F2 — The lognormal law and its blind confirmations.**
Per dyadic window, $\ln f$ is normal to high precision ($263{,}763$ primes pooled);
window minima are pure order statistics. Three blind tests hit:
$[175, 225] \to 191$ ($2\times10^{8}$), $345 \to 347$ ($10^{9}$), median
$681 \to 681$ exact and $[351, 404] \to 405$ ($2\times10^{9}$). The closest
published work fits no distribution to $f(p)$, so this law appears to be unrecorded.
Code: `files/analyze_session2.py`, `files/target_frontier.py`; REPORT §5,
§10.3–10.4, §12.5; figure `files/plots/5_lognormal.png`.

</div>

<div align="justify">

**F3 — The channel decomposition and the class fingerprint.**
$f(p)$ decomposes into congruence "channels"; Mordell's identities are class-wide
channels, and the six square classes are exactly the classes with none. Within
$p \equiv 1 \pmod{24}$, mean $f_0$-percentile climbs a quadratic-residue ladder
($0.215 / 0.526 / 0.724$ for QR-at-both-$5,7$ / NR-at-one / NR-at-both) — and the
one-negative count $f_1$ descends the same ladder backwards. REPORT §3, §10.2,
§11.7; figure `files/plots/2_fingerprint.png`.

</div>

![The class fingerprint and its inversion](files/plots/2_fingerprint.png)

<div align="justify">

**F4 — The wall, proved in-project (REPORT §9).**
Machine-verified: the kernel bijection (Lemma A); explicit sufficient criteria
(Lemma B) and an infinite channel family (Lemma C); the square obstruction
re-proved in full via two Jacobi-symbol facts (Lemma D); the $\varepsilon$-covering
theorem (Theorem E: coverage $1-\varepsilon$ costs $\exp(\varepsilon^{-2})$
identities); and Theorem F: **no finite channel system covers any class containing
squares** — so the six square classes can never be closed by identities, covering
congruences, or the circle method. Code: `files/verify_lemmas.py`.

</div>

<div align="justify">

**F5 — Erdős–Straus over $\mathbb{Z}$: the conjecture is a chirality statement
(REPORT §11).**
With signs allowed, two unit fractions always suffice (Theorem G), and the failure
sets of the sum-form and difference-form are exactly complementary — the hard class
of one world is the easy class of the other. The solution set is graded by the
number of negative denominators; the grading is pure window-position inside the
*same* divisor classes (Lemma H); negative $n$ is an exact mirror (Theorem J); the
square obstruction is chiral — it empties only the positive windows (Lemma K); and
no channel system can flip chirality (Corollary L). Empirically the §10.2 starvation
law *inverts* in the signed sector ($f_1$ window minima land in square classes
$0/7$ vs $7/7$ for $f_0$): **channel starvation is displacement of solution mass
into the other chirality, not absence** — $\tilde f(2521) = (9, 377, 307)$. Counting
signed representations appears to be entirely unstudied (no literature, no OEIS
sequence as of 2026-06). Code: `files/verify_signed.py`, `files/fsigned.c`,
`files/census_ref.py`, `files/analyze_signed.py`; data `files/signed_*.csv`;
figures `files/plots/3_seesaw.png`, `files/plots/4_strata.png`.

</div>

![The chirality see-saw](files/plots/3_seesaw.png)

<div align="justify">

**F6 — Inside the residual: 58% ladder, 42% factorization (REPORT §12.1–12.3).**
After removing the window trend and mod-$840$ fingerprint, the residues $p \bmod q$
still predict $\ln f$ at every prime modulus $q \le 199$, non-residue side richer —
Theorem F's sign at every modulus — with measured decay
$s_q \approx 18\cdot q^{-1.95}$ and out-of-sample saturation at $\approx$58% of
the variance. The
remaining $\approx$42% carries the factorization statistics of the shifted
integers $4pm+1$. Maximally hostile congruence reaches only **10%** of the depth
a counterexample needs ($\Delta\ln f = -0.66$ of $-6.41$): a counterexample would
have to be a large-prime factorization conspiracy, not a congruence event. Code:
`files/residual_spectrum.py` (writes `files/residual_effects.json`); figure
`files/plots/6_spectrum.png`.

</div>

<div align="justify">

**F7 — The adversarial frontier (REPORT §12.4–12.5).**
A congruence-only score fitted at $\le 2\times10^{8}$ ranks $f$ at $10^{9}$ and
$2\times10^{9}$ with Spearman $\approx +0.72$ and finds window floors from within
its predicted bottom-1% — at $2\times10^{9}$ it found the exact floor
($f = 405$ at $p = 2{,}004{,}535{,}009 \equiv 13^2 \pmod{840}$) for $\sim$1% of
the sweep cost. This is the search instrument for ranges beyond $10^{18}$ where
exhaustive verification is impossible; its honest limit: the unexplained 42%
decides individual primes, so targeting compresses a search but only enumeration
certifies. Code: `files/target_frontier.py`, `files/plot_residual.py`.

</div>

![Adversarial targeting](files/plots/7_targeting.png)

## The expanded logic: negative integers, and the structures they reveal

<div align="justify">

The extension driving the 2026-06-12 sessions was a question posed by the repository
owner: *what happens to the conjecture if negative integers are allowed — does it
still hold, and what patterns appear in the negative domain?* The answers turned out
to be structural, and they reorganize the whole problem:

1. **The graded count vector.** Over $\mathbb{Z}^{*}$ the natural object is not one
   number $f(p)$ but the vector
   $(\tilde f_0, \tilde f_1, \tilde f_2, \tilde f_3)(n)$ — solutions graded by how
   many denominators are negative (trivial cancelling triples $\{t, -t, n/4\}$,
   which exist iff $4 \mid n$, are excluded). The classical $f$ is the grade-$0$
   component; the conjecture is $\tilde f_0 \ge 1$.
2. **An even function with a grade flip.** Negation gives
   $\tilde f_k(-n) = \tilde f_{3-k}(n)$, so the total
   $\tilde F = \sum_k \tilde f_k$ is an *even* function on $\mathbb{Z}$ — the
   negative axis is an exact mirror and adds no new conjecture. The conjecture over
   $\mathbb{Z}$ reads: *the even function $\tilde F$ keeps its grade-$0$ component
   positive on the positive axis.* That is what "Erdős–Straus is a chirality
   statement" means. ($n = 2$ is the unique "signless" point:
   $\tilde F(2) = f(2) = 1$; $\tilde f_1 = 0$ exactly at $n \in \{2, 4\}$.)
3. **The window dictionary.** All grades live in the *same* arithmetic object: the
   divisor classes $d \equiv -nx \pmod{4x-n}$ of the classical kernel. The grade of
   a solution is purely the *window* its divisor lands in (positive window
   $\to \tilde f_0$, negative windows $\to \tilde f_1$, mirror-modulus window
   $\to \tilde f_2$). Positivity — the entire content of the conjecture — is
   geometry inside a residue class, not a different equation.
4. **A third mechanism.** The signed windows admit a stratum that provably cannot
   exist in the positive world ("Type III": $p^2$ divides the window divisor). At
   the record prime $2521$ it is the *largest* stratum ($177$ of $377$ one-negative
   solutions).
5. **The chirality of the obstruction, and the see-saw.** The Jacobi-symbol
   obstruction that makes the conjecture hard kills only the positive windows
   (Lemma K); the same arithmetic that empties a prime's positive window fills its
   negative ones — measured as $\mathrm{corr}(\tilde f_0, \tilde f_1) = -0.43$
   overall and $-0.22$ within residue classes. The hard classes are not poor; they
   are *polarized*.

So: the conjecture survives the extension trivially (two signed terms always
suffice), and the extension pays for itself by exposing the data structures —
grading, evenness, windows, strata — in which the original difficulty becomes
geometrically visible: everything hard about Erdős–Straus is the statement that the
positive window always gets its share.

</div>

## Repository file tree

```text
.
├── README.md                     this file
├── REPORT.md                     the full study (§0–§12)
├── TRANSCRIPT.md                 original phone-session log that started it
├── LICENSE
├── files/                        engines, analyses, datasets, figures
│   ├── fp.c                      f(p) counter — C reference
│   ├── fpr.rs                    f(p) counter — Rust (multi-threaded, std-only)
│   ├── fp.cu                     f(p) counter — CUDA
│   ├── fsigned.c                 signed graded-census engine (§11)
│   ├── census_ref.py             Python reference for the signed census
│   ├── verify_lemmas.py          machine verification of §9
│   ├── verify_signed.py          machine verification of §11
│   ├── residual_spectrum.py      §12 spectrum
│   ├── target_frontier.py        §12 adversarial targeting score
│   ├── analyze_final.py          analyses
│   ├── analyze_session2.py
│   ├── analyze_signed.py
│   ├── plot_types.py             figure generators
│   ├── plot_residual.py
│   ├── run_segments.sh           segmented sweep driver
│   ├── residual_effects.json
│   ├── plots/                    the figure atlas (1–7, PNG)
│   └── *.csv                     datasets (per-prime counts; graded census)
├── prime_solutions/              Rust/CUDA crate (cuda-oxide)
│   ├── Cargo.toml
│   ├── Cargo.lock
│   ├── rust-toolchain.toml       pinned nightly
│   └── src/main.rs
└── bend/                         HVM/Bend port experiment
    ├── fp.bend
    ├── test.bend
    ├── temp_test.bend
    └── instructions_bend_run.md
```

<div align="justify">

(Build artifacts — `target/`, compiled binaries, transient run output — are
git-ignored and not shown; see `.gitignore`.)

</div>

## Repository map

| Path | What it is |
| --- | --- |
| `REPORT.md` | The full study: §0–§8 landscape + laws, §9 proof attempt, §10 datasets, §11 signed extension, §12 residual + frontier |
| `TRANSCRIPT.md` | The original phone-session log that started the project |
| `files/fp.c`, `files/fpr.rs`, `files/fp.cu` | The positive-world engines (C / Rust / CUDA) |
| `files/fsigned.c`, `files/census_ref.py` | The signed-grading engine + Python reference |
| `files/verify_lemmas.py`, `files/verify_signed.py` | Machine verification of §9 / §11 ($8{,}719$ / $536{,}988$ assertions) |
| `files/residual_spectrum.py`, `files/target_frontier.py` | §12: the spectrum + the adversarial score |
| `files/analyze_*.py`, `files/plot_*.py` | Analyses and the figure atlas (`files/plots/1–7`) |
| `files/hard_*.csv`, `files/fresh_2e9_slice.csv`, `files/signed_*.csv` | The datasets (per-prime counts; graded census) |

<div align="justify">

Build/run commands are in REPORT §8, §11.9, §12.7. (Plotting note: on this machine
run plot scripts with `PYTHONNOUSERSITE=1` — see `files/plot_types.py` header.)

</div>

## Usage

<div align="justify">

If you clone this repo and want to reproduce the outputs, here is what each part
needs. Every engine is self-contained — full build/run notes live in the header
comment of each source file.

</div>

### Prerequisites

| Tool | Used for | Install (Debian/Ubuntu) |
| --- | --- | --- |
| C compiler (`gcc`, OpenMP) | `files/fp.c`, `files/fsigned.c` | `sudo apt install build-essential` |
| Python ≥ 3.8 | all `files/*.py` analyses & verification | `sudo apt install python3 python3-pip` |
| `numpy`, `matplotlib` | the plotting / spectrum scripts only | `pip install numpy matplotlib` |
| Rust (nightly) | `files/fpr.rs`, `prime_solutions/` | [rustup.rs](https://rustup.rs) |
| CUDA toolkit (`nvcc`) | `files/fp.cu` (needs an NVIDIA GPU) | NVIDIA CUDA Toolkit ≥ 12.0 |

<div align="justify">

Only Python (with `numpy` / `matplotlib`) is needed to re-run the analyses and
regenerate the figures from the CSVs already in the repo. The C/Rust/CUDA engines
are only needed to regenerate the raw per-prime datasets themselves.

The Python scripts depend solely on the standard library plus `numpy` and
`matplotlib`; there is no `requirements.txt`, so:

</div>

```bash
pip install numpy matplotlib
```

### Positive-world solution counter $f(p)$

```bash
# C (single-threaded reference)
gcc -O3 -march=native files/fp.c -o files/fp
./files/fp 5 2000 0 fp_small.csv          # pmin pmax mode(0=all,1=p≡1 mod24) out.csv

# Rust (multi-threaded, std-only — no crates)
rustc -C opt-level=3 -C target-cpu=native files/fpr.rs -o files/fpr
./files/fpr 5 2000 0 rs_small.csv 4        # ...last arg = threads
diff rs_small.csv fp_small.csv             # must be empty

# CUDA (needs an NVIDIA GPU)
nvcc -O3 -arch=compute_80 files/fp.cu -o files/fpcuda
./files/fpcuda 5 2000 0 cuda_small.csv
```

### Signed-world graded census (REPORT §11)

```bash
gcc -O3 -march=native -fopenmp files/fsigned.c -o files/fsigned
./files/fsigned 2 200 all > census.csv     # LO HI all|pMOD:R
```

### Analyses, verification, and figures

```bash
# machine verification of the proof attempts (§9 / §11)
python3 files/verify_lemmas.py
python3 files/verify_signed.py

# regenerate the figure atlas (files/plots/1–7) from the CSVs
PYTHONNOUSERSITE=1 python3 files/plot_types.py
PYTHONNOUSERSITE=1 python3 files/plot_residual.py
PYTHONNOUSERSITE=1 python3 files/residual_spectrum.py
```

<div align="justify">

(`PYTHONNOUSERSITE=1` is only needed on machines where a user-site install shadows
the venv `matplotlib` — see the `files/plot_types.py` header.)

</div>

## Status

<div align="justify">

**The Erdős–Straus conjecture is open.** Nothing here proves or disproves it — §9
and §12 prove, inside this project's own framework, that identity/covering/channel
methods cannot, and quantify how far congruence structure alone can reach (10% of
a counterexample). Open directions logged at the end of REPORT §12: fold
factorization features into the targeting score, the second moment of the window
split, a $10^{10}$ probe (requires auditing the CUDA engine's 64-bit arithmetic),
OEIS submission of the signed sequences, Lean formalization of Lemma D.

</div>

## References

**The conjecture**

- Wikipedia: Erdős–Straus conjecture — <https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Straus_conjecture>
- Erdős Problems #242 (T. Bloom) — <https://www.erdosproblems.com/242>
- OEIS: A073101 ($0 < x < y < z$), A192787 ($x \le y \le z$ — this project's $f$), A292581 (ordered) — <https://oeis.org/A192787>

**Principal literature used**

- C. Elsholtz, T. Tao, *Counting the number of solutions to the Erdős–Straus
  equation on unit fractions*, J. Aust. Math. Soc. 94 (2013) 50–105 —
  <https://arxiv.org/abs/1107.1010>
- L. J. Mordell, *Diophantine Equations*, Academic Press (1969), pp. 287–290
- A. Schinzel, *On sums of three unit fractions with polynomial denominators*,
  Funct. Approx. Comment. Math. 28 (2000) 187–194
- S. E. Salez, *The Erdős–Straus conjecture: new modular equations and checking up
  to $N = 10^{17}$* (2014) — <https://arxiv.org/abs/1406.6307>
- M. Spiridon, B. C. Dumitru, *Further verification and empirical evidence for the
  Erdős–Straus conjecture* (2025, preprint; the external $f(p)$ dataset
  cross-validated here) — <https://arxiv.org/abs/2509.00128>
- C. Pomerance, A. Weingartner, *Exceptions to the Erdős–Straus–Schinzel conjecture*
  (2025) — <https://arxiv.org/abs/2511.16817>
- J. H. Jaroma, *On expanding $4/n$ into three Egyptian fractions*, Crux
  Mathematicorum 30 (2004) 36–37 — the documented trace of the signed variant
- T. Bloom, C. Elsholtz, *Egyptian Fractions* (survey, 2022) —
  <https://arxiv.org/abs/2210.04496>
</content>
</invoke>
