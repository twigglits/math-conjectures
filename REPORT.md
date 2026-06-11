# Erdős–Straus at 3.5×10⁷: floor growth, the channel decomposition, and the lognormal law

**Session date:** 2026-06-11 · **Status of conjecture: OPEN** (erdosproblems.com #242; verified to 10¹⁸)
**Continuation of:** phone session (TRANSCRIPT.md) — f(p) counting engine, Elsholtz–Tao program

---

## 0. Honest headline

The Erdős–Straus conjecture (every 4/p = 1/x + 1/y + 1/z) was not solved today and was
never going to be — it has resisted since 1948 for a provable structural reason (§4).
What this session produced instead:

1. an independently **cross-validated dataset** of solution counts f(p) far beyond the
   phone session's horizon (3×10⁵ → 3.5×10⁷, using our engine + a validated external dataset),
2. the **collapse of the phone session's open question** — the floor does not sag and does not
   grow at a separate slower exponent; it tracks the median's exponent exactly,
3. a **channel decomposition** of f(p) (new synthesis; ingredients classical) making
   Mordell's identities, Schinzel's obstruction, and the floor primes' starvation one
   single phenomenon, visible prime-by-prime in data,
4. an empirical **lognormal law** for f(p) precise enough to explain every record-low prime
   as a pure order-statistics event and to make testable predictions at 10⁸–10⁹.

## 1. Provenance and validation (all checks passed, zero discrepancies)

| Check | Result |
|---|---|
| Rust engine (fpr.rs) vs blessed phone-validated CSV (301 primes) | identical |
| Rust vs C engine rebuilt on this machine | identical |
| 1-thread vs 16-thread output | byte-identical |
| Segmented runs vs single run | identical |
| **Our engine vs arXiv:2509.00128 published dataset** (independent authors, independent code) | **4,519 primes compared, 0 mismatches** (incl. Type I/II splits) |
| Our solution enumerator (3rd implementation, Python) vs both | exact on all targets |
| Bradford (INTEGERS 25 #A54, 2025) x ≤ ⌈p/2⌉ range theorem | re-proved by hand (§3.1), confirmed by engine agreement |

External data: `esc2025_fp_to_3.5e7.csv` = per-prime f(p), Type-1/Type-2, for all 66,737
primes in the six hard residue classes mod 840 up to 3.5×10⁷, from the Sept 2025 paper
(github.com/esc-paper/erdos-straus), now cross-validated against our engine on its overlap.

## 2. The floor to 3.5×10⁷ (115× the phone session's range)

Per dyadic window of the hard classes (f = unordered solution count):

| window | n | min f | at p | p mod 840 | median |
|---|---|---|---|---|---|
| 2¹¹ | 6 | **9** | **2521** | 1 | 24 |
| 2¹⁴ | 45 | 23 | 20521 | 361 | 52 |
| 2¹⁷ | 321 | 46 | 132721 | 1 | 98 |
| 2²⁰ | 2,238 | 88 | 1,202,881 | 1 | 170 |
| 2²³ | 16,010 | 120 | 8,628,481 | 1 | 272 |
| 2²⁴ | 30,825 | 151 | 20,322,481 | 361 | 314 |
| 2²⁵ | 2,557 | 171 | 34,103,161 | 1 | 336 |

- **Fitted exponents:** min f ~ (ln p)^3.27, median ~ (ln p)^3.30 (effective local exponents;
  both consistent with the Elsholtz–Tao average order log³p · (loglog factors)).
  The phone session's tentative "floor ~ (log p)^2.4" was an artifact of fitting to 3×10⁵.
  **The floor and the median grow at the same exponent.**
- **p = 2521 (≡ 1 mod 840) is the all-time record: f = 9 (6 Type I + 3 Type II).**
  No prime among the 66,734 that follow it (four orders of magnitude) sets a new record,
  or comes close. Records after 1000: 1009 → 19, 1201 → 11, 2521 → 9, then nothing to 3.5×10⁷.
- **Neither mechanism ever fails:** min Type-1 and min Type-2 per window grow steadily;
  no prime to 3.5×10⁷ lacks Type I or Type II solutions (phone session's law, now at 115× range).
- min/median per window is **stable at 0.47 ± 0.05** while window populations grow 6 → 30,825.
  Explained quantitatively in §5 — it is *not* a hard edge.

## 3. The channel decomposition

Every solution with least denominator x sits in the window ⌈p/4⌉ ≤ x ≤ ⌈p/2⌉ (Bradford 2025;
re-proved below) and corresponds to a divisor of x² in a prescribed residue class mod 4x−p
(equivalently Bradford's Propositions 3–4; our engine and the 2025 paper's engine both
implement exactly this test — hence their exact agreement).

**Type II (p | y, p | z).** Writing y = py₁, z = pz₁, the solutions are exactly the pairs
(m, x) for which t² − m(4x−p)t + mx has positive integer roots (y₁, z₁) — i.e. Vieta:
   y₁ + z₁ = m(4x−p),  y₁z₁ = mx.
Equivalently: factorizations (4y₁−1)(4z₁−1) = **4pm+1** with both factors ≡ 3 (mod 4) and
m | y₁z₁. We call m the **channel**. Channel m is *arithmetically closed* iff 4pm+1 has no
prime factor ≡ 3 (mod 4) (e.g. 4·2521+1 = 5 × 2017, both ≡ 1: closed). Verified: every
Type II solution of every test prime maps to an integer m; per-prime channel sums reproduce
the engine's counts exactly.

**Type I (p | z only).** The cofactor e = x²/d satisfies 4e ≡ −1 (mod 4x−p), so solutions
correspond to pairs (e, a): a | 4e+1, x = (p+a)/4 ∈ ℤ, e | x² (+ range/dmin conditions).
Channel (e, a) imposes congruence conditions on p modulo 4 and modulo the primes of e.

### 3.1 The x-range theorem (re-derivation)
For x > p/2 (s = 2x−p ≥ 1): Type II needs d′ ≡ x+s (mod 2x+s) with d′ ≤ x < x+s — impossible.
Type I needs 4e ≡ −1 (mod a), whose least solution e ≥ (a−1)/4 = x − (p+1)/4 exceeds the
ceiling e ≤ x/(2s) whenever s ≥ 3; s = 1 forces e = x/2, giving exactly the classical
p ≡ 3 (mod 4) identity x = y = (p+1)/2, z = p(p+1)/4. Hence x ≤ (p+1)/2 always, and
x ≤ (p−1)/2 for p ≡ 1 (mod 4).

### 3.2 Mordell's identities = class-wide channels; Schinzel = their death
Computed demonstration (first firing channels, eight consecutive primes per class):

- covered class p ≡ 73 (840):  Type I channel **e = 5 fires for every prime** (m-channel 1–2)
- covered class p ≡ 193 (840): same — e = 5 every time
- hard class p ≡ 1 (840):  Type I channels e ≤ 12: **never fire** (except e = 11 sporadically)
- hard class p ≡ 361 (840): same

Why: channel e = 5 requires 5 | x with x = (p+a)/4, i.e. p ≡ 2 or 3 (mod 5) — exactly the
non-residues. A prime ≡ square (mod 840) is a QR mod 3, 5, 7, so **every channel whose
congruence conditions live on the primes of 840 is dead**. Channels on new primes (11, 13, …)
fire only for the ~1/q of the class with the right residue — never class-wide. That is
Schinzel's theorem (no identity family covers a progression containing squares), expressed
channel-by-channel and visible in data. Floor primes' Type I spectra start at e = 116 (2521),
23 (4201), 124 (9601), 261 (20521) — versus e = 5 for every covered-class prime.

### 3.3 What makes a floor prime
Channel availability is measurably the driver, but statistically, not via any single channel:
- channel 1 (4p+1 has a factor ≡ 3 mod 4) is open for 36.0% of bottom-decile primes vs
  58.9% of top-decile primes (66,737-prime census); floor primes: 4/15 open vs 47.5% base;
- 2521's first eight Type II channels are all closed (spectrum {9, 11, 98});
- but some floor primes fire at m = 1 and some median primes first fire at m = 9 —
  **f(p) is the aggregate of hundreds of thin channels, and the floor is reached only when
  unusually many fail at once.** No single guaranteed channel exists for square-class p —
  which is precisely why the conjecture is hard (§4).

## 4. Why this can't be turned into a proof (the precise wall)

For covered classes, one channel fires identically for the whole class: a one-line proof.
For the six square classes: every individual channel is a statement of the form "the integer
4pm+1 has a divisor ≡ 3 (mod 4) [with a side condition]" or "x = (p+a)/4 has square divisible
by e" — each fails for a positive-density set of primes, and no finite union provably covers
everything (Schinzel). What a proof needs is a *lower bound for divisors of shifted integers
in prescribed residue classes*, uniformly in p — which current analytic number theory cannot
deliver. Elsholtz–Tao get: average Σ_{p≤N} f(p) ≍ N log²N; pointwise upper f(p) ≪ p^{3/5+o(1)}
(Type II thinner: f_II ≪ p^{2/5+o(1)}, matching Type II being the scarcer mechanism in our
data); and a pointwise **lower** bound f(p) ≥ (log p)^{0.549} — but only on a **density-1**
subset of primes (ET Thm 1.8). The conjecture is precisely the gap "density 1 → all primes".
Deeper still (ET Prop 1.6, after Schinzel/Yamamoto): for odd perfect squares n,
f_I(n) = f_II(n) = 0 identically, by quadratic reciprocity — so **any method proving
f_I(p) > 0 or f_II(p) > 0 for all p must fail when p is replaced by p²**, which kills finite
covering-congruence strategies *and the circle method* outright. Square-class primes are
exactly the primes that "look like squares" to all small moduli; our channel census is the
per-prime empirical shadow of that obstruction. Note also ET Remark 1.3: even the second
moment Σ f_I(p)² is declared out of reach of current methods — the variance and distribution
shape measured in §5 are data on quantities theory cannot yet touch.

## 5. The lognormal law (new empirical finding)

Per dyadic window, f(p) is lognormal to high precision:

- **var/mean grows 3.45 → 10.5** across windows, matching the lognormal identity
  var/mean = mean·(e^{σ²}−1) within ~10% everywhere and ~3% in well-populated windows;
- σ(ln f) shrinks 0.266 → 0.176 across 2¹⁴ → 2²⁵ — **relative concentration**;
- the observed window minima sit exactly at the lognormal extreme-value prediction
  (window 2²⁴: predicted 152.6, observed 151; z-scores −3 to −4.3 across windows, as expected
  for samples of these sizes). **2521's f = 9 is an unremarkable order-statistics event.**
- the "stable left edge" min/med ≈ 0.47: σ shrinks at almost exactly the rate √(2 ln n) grows,
  keeping exp(−z·σ) constant over our window sizes. A scaling coincidence, not a hard edge.
- **out-of-sample test** (μ, σ trends fitted on 2¹⁵–2²² only, minima of 2²³–2²⁵ predicted blind):
  predicted 132 / 152 / 200, observed 120 / 151 / 171. One of three inside the 80% band, the
  misses both on the *low* side ⇒ the left tail is mildly heavier than lognormal (~10% in f).
  The model predicts held-out minima to ~10%; treat the tail as lognormal × a small
  left-enhancement.

Consequence (heuristic, explicitly an extrapolation): with μ(ln f) ≈ ln(c ln³p) growing and
σ shrinking, a counterexample (f = 0) at p ~ 10²⁰ would be a ≳30σ lognormal event; summed
over all primes the expected number of failures beyond 10¹⁸ is astronomically small.
This quantifies — but does not prove — why the conjecture is safe.

**Testable predictions** (lognormal-EV; μ = 3.42·lnln p − 3.98; two σ-shrinkage models,
linear-in-lnln and c/√ln p, fitted to windows 2¹⁵–2²⁵; bands widened ~10% downward for the
observed left-tail enhancement):
min f over hard primes in [10⁸, 2×10⁸] ≈ **175–225**; in [10⁹, 2×10⁹] ≈ **245–335**.
Falsifiable by anyone willing to burn the CPU (~10× resp. ~10³× this session's compute).

## 6. In progress

Full p ≡ 1 (mod 24) sweep to 10⁷ on this machine (16 threads, ~3h) — completes the one test
the external dataset cannot do: whether every dyadic minimum over the *full* 1-mod-24 class
lands in the six square classes (phone session's law, confirmed to 10⁶, 4× the class size).
Also adds an independent re-validation of the external dataset on ~16,600 more primes.

## 7. Related fields: where a proof could come from (deep-research synthesis)

Ranked by likely contribution, with the current best theorem and the precise obstruction in each.

**(a) The truth boundary — generalized numerators (Pomerance–Weingartner, arXiv:2511.16817,
Nov 2025).** The sharpest recent structural result: for m/n = three unit fractions, **exceptions
provably exist** — for every m ≥ 6.52×10⁹ there is a prime p ∈ (m², 2m²) with m/p not
representable (empirically already for every m ≥ 20), and Schinzel's n_m must exceed
exp(m^{1/3−ε}); most primes near that bound are exceptions, while beyond exp(m^{1/2+ε}) none
are expected. The order parameter is exactly the channel intensity λ ≈ log³p/m. **Erdős–Straus
is the m = 4 slice, sitting ever deeper inside the "true" phase as p → ∞.** Their exception
construction is the formal dual of our channel census: at m ~ √p only O(1) channels exist, so
finitely many congruence conditions on p kill them all (CRT + Dirichlet); at m = 4 the channel
count grows like log³p, and Schinzel's obstruction forbids any finite kill-set — but nobody can
*prove* a live channel. Our lognormal measurements are in-phase measurements of this order
parameter; their theorems are the out-of-phase ground truth.

**(b) Sieve theory / divisors in residue classes — the kernel field.** The conjecture is
equivalent (Bloom–Elsholtz 2022; Bradford 2025; our channel form; independently the Lean
project leochlon/erdstrau reduced to literally our Type II equation (4b−1)(4c−1) = 4pδ+1,
δ | bc) to a **lower-bound problem for divisors of shifted integers in prescribed residue
classes**. What sieves currently deliver: upper bounds and averages (ET's Σf(p) ≍ N log²N via
Brun–Titchmarsh + Bombieri–Vinogradov; the half-dimensional sieve controls the
"all prime factors ≡ 1 mod 4" events that close our channels, density ~ C/√log). What they
cannot deliver: "every p has a live channel" — pointwise lower bounds on thin divisor sums,
where even the **second moment Σ f_I(p)² is explicitly out of reach** (ET Remark 1.3). A proof
here likely needs bilinear/parity-breaking inputs of Friedlander–Iwaniec strength applied to
the channel sums. Most plausible contributing field, least forgiving technically.

**(c) Arithmetic geometry.** The surface 4xyz = n(xy+yz+zx) has **no Brauer–Manin obstruction
to solubility (Bright–Loughran 2020)** — cohomology certifies "nothing blocks it." But the real
obstruction is finer than BM sees: Yamamoto/Schinzel (ET Prop 1.6) — f_I(n²) = f_II(n²) = 0
identically for odd squares, by quadratic reciprocity. Any proof technique for primes must
break when p is replaced by p², which **rules out finite covering systems and the circle
method**. Geometry has cleared its checkpoint; it owns no production mechanism for integral
points on this singular (non-proper) surface. Verdict: explains why the problem is honest,
unlikely to finish it.

**(d) Conditional results: there are none.** No proof of ES is known under GRH, EH, or any
standard conjecture (checked: ET 2013, the 2025 survey literature, erdosproblems.com #242
remarks — none cite one). This is informative: GRH equidistributes primes, but the kernel needs
divisor existence in *specific* shifted sequences 4pm+1 — Hooley/Linnik territory where GRH
improves averages, not instances. The only "conditional" statement in the field is the
Poisson/Borel–Cantelli heuristic (ET Remark 1.2), which our data refines (§5): the true law is
lognormal with shrinking σ — *more* concentrated than Poisson, hence even safer, and even
further from provable.

**(e) Almost-all methods (large sieve).** Vaughan 1970: exceptions below N number
≤ N exp(−c log^{2/3}N); now explicit in m (PW Thm 1.3: exp(−C log^{2/3}N/φ(m)^{1/3}));
Li Delang 1981, Elsholtz–Planitzer 2020 (f(n) ≥ (log n)^{log 6+o(1)} almost all n), ET Thm 1.8
(f(p) ≥ (log p)^{0.549} on density-1 primes). These methods saturate at density 1 — the
remaining set is already smaller than any power saving, and the gap "density 1 → all" **is**
the conjecture. Incremental wins available (improve 0.549 toward 3 — our measured exponent;
kill ET's loglog), none decisive.

**(f) Additive combinatorics (Croot, Bloom).** Bloom 2021 settled Erdős–Graham (unit fractions
summing to 1 in any dense set) with density-increment/Fourier methods — but those live on
*unbounded-length* representations, where smooth flexibility exists. Length-3 is rigid
quadric arithmetic; no transfer mechanism is known, and the field's principals (Bloom owns
#242 and tags it "difficult"; Tao likewise) see none. Verdict: wrong shape.

**(g) Formalization & AI activity (2025–26).** Official Lean statement exists
(formal-conjectures/242.lean). The leochlon/erdstrau project (531 items) independently reduced
the conjecture to our Type II kernel — convergent evidence the kernel is canonical — though its
claimed "529 mod 840 by CRT" was debunked by Bloom/Alexeev (finite verification masquerading as
periodicity). One claimed proof (Bradford, arXiv:2602.11774, Feb 2026) was rejected within
hours — its covering system cannot exclude the six square classes, the exact failure mode ET
Prop 1.6 predicts for all covering attempts. Tao tracks AI progress on Erdős problems; #242 has
attracted attempts and zero breakthroughs. Status as of May 2026 (page edit): **open**.

**Bottom line.** The proof, if it comes soon, comes from (b) — a pointwise-or-second-moment
breakthrough on divisor sums in residue classes — possibly guided by the quantitative targets
this session measured (σ², left-tail shape, channel-failure statistics). Fields (a)/(e) will
keep tightening the boundary; (c) has certified the playing field; (f) is structurally
mismatched. Until then the honest state is: true with overwhelming, *quantified*, and now
phase-diagram-located empirical margin — and unproven.

## 8. Reproducibility

- `files/fpr.rs` (engine; build: `rustc -C opt-level=3 -C target-cpu=native fpr.rs -o fpr`)
- `files/fp.c` (C original), `files/fp_small.csv` (blessed reference)
- `files/hard_1e6.csv`, `files/hard_seg2..6.csv` (our sweep), `files/esc2025_fp_to_3.5e7.csv`
- External: arXiv:2509.00128 + github.com/esc-paper/erdos-straus; Bradford, INTEGERS 25 (2025) #A54;
  Elsholtz–Tao, J. Aust. Math. Soc. 94 (2013) 50–105 (arXiv:1107.1010); Salez arXiv:1406.6307;
  Pomerance–Weingartner, arXiv:2511.16817; Bright–Loughran (no Brauer–Manin obstruction, 2020);
  Elsholtz–Planitzer 2020; Vaughan 1970; T. Bloom, Erdős Problem #242
  (erdosproblems.com/242, accessed 2026-06-11, last edited 2026-05-07) + forum thread.
- Analysis scripts: inline in session transcript (Python, stdlib only) + files/analyze_final.py.
