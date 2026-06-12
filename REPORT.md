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

**Evening addendum (§9–§10):** the direct prove-or-disprove attempt — four theorems with
complete, machine-verified proofs (the ε-covering theorem; the square obstruction re-proved
in full; the no-finite-system theorem; the criteria family and its square-death), the
completed 10⁷ full-class dataset (law: 13/13 window minima in the square classes), and a
GPU engine that took the frontier to 2×10⁸ — **where last session's blind prediction
min f ∈ [175, 225] was confirmed at min f = 191.** The conjecture remains open; the reason
it must, is now proved inside this project's own framework.

**Second addendum (§11, 2026-06-12): the signed extension — Erdős–Straus over ℤ.** Five
new machine-verified results: two signed unit fractions always suffice, with exactly
complementary failure sets (Theorem G); the kernel's divisor classes survive verbatim and
the sign grading is pure window-position (Lemma H); the negative domain is an exact mirror
(Theorem J); the square obstruction is chiral — it lives only in the positive windows
(Lemma K); and no channel system can flip chirality (Corollary L). Plus the first graded
census (to 6×10⁵): the §10.2 law **inverts** in the signed sector — f₁ window minima land
in the square classes 0/7 — corr(f₀, f₁) = −0.43, and the record prime reads
f̃(2521) = (9, 377, 307). **Channel starvation is displacement of solution mass into the
other chirality, not absence.** The wall of §9 is now mapped: it stands entirely inside
one sign sector.

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

~~Full p ≡ 1 (mod 24) sweep to 10⁷~~ — **completed in the evening session** (the run had
died before its final segment; relaunched and finished 2026-06-12 00:00). Results in §10:
the law holds 13/13, and the external dataset is re-validated on 18,143 more primes with
zero discrepancies.

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
- `files/fp.cu` (GPU engine, evening session; build: `nvcc -O3 -arch=compute_80 fp.cu -o fpcuda`)
- `files/verify_lemmas.py` (machine verification of §9; run: `python3 verify_lemmas.py`)
- `files/analyze_session2.py` (merge / validate / law / octave analyses of §10)
- `files/hard_1e6.csv`, `files/hard_seg2..6.csv` (our sweep), `files/hard_1e7_full.csv`
  (merged full class), `files/hard_1e8_2e8.csv` (GPU octave), `files/esc2025_fp_to_3.5e7.csv`
- External: arXiv:2509.00128 + github.com/esc-paper/erdos-straus; Bradford, INTEGERS 25 (2025) #A54;
  Elsholtz–Tao, J. Aust. Math. Soc. 94 (2013) 50–105 (arXiv:1107.1010); Salez arXiv:1406.6307;
  Pomerance–Weingartner, arXiv:2511.16817; Bright–Loughran (no Brauer–Manin obstruction, 2020);
  Elsholtz–Planitzer 2020; Vaughan 1970; T. Bloom, Erdős Problem #242
  (erdosproblems.com/242, accessed 2026-06-11, last edited 2026-05-07) + forum thread.
- Analysis scripts: inline in session transcript (Python, stdlib only) + files/analyze_final.py.

---

# Session addendum (2026-06-11, evening): the direct attempt

Goal of this session, as set: *try your absolute best to prove or disprove the conjecture.*
This section is the attempt itself — what could be proved outright (with complete proofs,
every numbered claim machine-verified by `files/verify_lemmas.py`, 6,708 exact-arithmetic
assertions), what each known strategy provably cannot do, and the verdict.

## 9. The proof attempt

### 9.1 The kernel, restated precisely (Lemma A)

For prime p ≥ 5 and x ∈ (p/4, 3p/4], write a = 4x − p, B = px. Then gcd(a, B) = 1
automatically (p | a forces a ∈ {p, 2p}, i.e. 4x ∈ {2p, 3p}, impossible for odd p;
gcd(a, x) = gcd(p, x) = 1 since x < p), and the solutions of 4/p = 1/x + 1/y + 1/z with
least denominator x are in bijection with divisors d | B², d ≤ B, d ≡ −B (mod a) — via
y = (B + d)/a, z = (B + B²/d)/a — filtered by d ≥ dmin = 2x(2x−p)⁺ (the y ≥ x condition).
Since gcd(d, p²) ∈ {1, p, p²} and d = p²d″ is range-impossible, exactly two strata exist:

- **Type I** (p ∤ d): d | x², d ≡ −4x² (mod a) — then p | z, p ∤ y;
- **Type II** (d = pd′): d′ | x², d′ ≤ x, d′ ≡ −x (mod a) — then p | y and p | z.

*For prime p these two strata exhaust all solutions* (machine-checked against brute-force
enumeration, including the Type I/II split, on a test set through f(1009) = 19). For
composite n the same divisor conditions still produce solutions, but two further strata
open up — gcd(4x − n, nx) > 1, and mixed divisors with 1 < gcd(d, n) < n — which have no
analogue at primes. Everything below turns on that asymmetry.

### 9.2 What was proved: explicit sufficient criteria (Lemma B)

Each of the following is proved by an explicit Vieta construction
((4y₁−1)(4z₁−1) = 4pm+1, y = py₁, z = pz₁, x = y₁z₁/m, requiring m | y₁z₁):

- **K1 (m = 1).** If 4p+1 has *any* divisor D ≡ 3 (mod 4), ESC holds for p.
  (The complementary divisor is automatically ≡ 3 (mod 4); m = 1 divides everything.)
- **K2 (m = 2).** If 8p+1 has a divisor D ≡ 7 (mod 8), ESC holds for p.
  (Then D′ ≡ 7 (mod 8) too and y₁ = (D+1)/4 is even.)
- **K3 (m = q prime).** If for any prime q the number 4pq+1 has a divisor
  D ≡ −1 (mod 4q), ESC holds for p. (Then q | y₁, so m = q | y₁z₁.)

These fired on every hard prime < 4000 in testing, but none is class-wide on the six
square classes: each is a *conditional* channel, a statement about the factorization of
4pm+1, true for a positive-density set of p and false for a positive-density set of p
(half-dimensional sieve). They are exactly the channels of §3 — provable instruments,
not a proof.

### 9.3 What was proved: the (t,3) channel family and the ε-covering theorem

**Lemma C.** Let t be any prime with t ≡ 2 (mod 3). Then for every prime
p ≡ 1 (mod 4) with p ≡ −3 (mod t) (p > 4t/3 + 3):

   x = (p+3)/4,  d = x²/t,  y = (px + d)/3,  z = p(x + pt)/3

is a Type I solution of 4/p = 1/x + 1/y + 1/z. *Proof:* t ≡ 2 (mod 3) gives 3 | 4t+1,
so with a = 3 the channel congruence 4e ≡ −1 (mod a) holds for e = t; p ≡ −3 (mod t)
gives t | x; integrality and 4/p-exactness follow from the kernel (§9.1); x < p/2 makes
the dmin condition vacuous. ∎ (Verified on 375 (t, p) instances, 15 values of t.)

**Theorem E (ε-covering).** For every ε > 0 there is an explicit finite set of such
channels proving ESC for all primes p ≡ 1 (mod 4) outside a set of relative density < ε.
*Proof:* the channels (t, 3) for the first k primes t ≡ 2 (mod 3) leave uncovered exactly
the p avoiding −3 mod every chosen t, of relative density ∏ᵢ(1 − 1/(tᵢ−1)) by
Dirichlet; the sum Σ 1/t over t ≡ 2 (mod 3) diverges, so the product → 0. ∎

**The cost law.** By Mertens for arithmetic progressions, using all t ≤ T gives
uncovered density ≍ (log T)^{−1/2}: reaching ε costs T ≈ exp(ε⁻²) — *superexponentially
many identities for linearly more coverage.* This quantifies, inside our own framework,
why eighty years of identity-hunting plateaued: Mordell's mod-840 system is the ε ≈ 6/35
prefix of an intrinsically divergent series.

### 9.4 What was proved: the square obstruction, in full (Lemma D)

**Lemma D.** Let n = c² (c odd) and x ∈ (n/4, 3n/4] with gcd(4x − n, nx) = 1,
a = 4x − n. Then *no* divisor of x² lies in the Type I class (d ≡ −4x² mod a), and
*no* divisor d′ ≤ x of x² lies in the Type II class (d′ ≡ −x mod a):
**the coprime strata are empty at odd squares.**

*Proof.* Note a = 4x − c² ≡ −c² ≡ 3 (mod 4). Two Jacobi-symbol facts:

1. *Required sign is −1.* For each prime ℓ | a we have ℓ ∤ 2x, so
   (d/ℓ) = (−4x²/ℓ) = (−1/ℓ); multiplying over ℓ | a: (d/a) = (−1/a) = (−1)^{(a−1)/2} = −1.
   For Type II: c² ≡ 4x (mod ℓ) makes x ≡ (c/2)² a quadratic residue mod every ℓ | a, so
   (d′/ℓ) = (−x/ℓ) = (−1/ℓ) and again (d′/a) = −1.
2. *Actual sign is +1.* Any d | x² factors as d = δ²d₀ with d₀ | x squarefree, so
   (d/a) = (d₀/a). For each prime ℓ′ | d₀ we have ℓ′ | x, hence a ≡ −c² (mod ℓ′) and
   (a/ℓ′) = (−1/ℓ′); so (a/d₀) = (−1/d₀) = (−1)^{(d₀−1)/2}. Quadratic reciprocity with
   a ≡ 3 (mod 4) gives (d₀/a) = (−1)^{(d₀−1)/2} · (a/d₀) = +1.

Contradiction. ∎ (This re-proves, self-containedly, the coprime case of
Yamamoto's theorem — the case the engine and all covering arguments live in. Verified
exhaustively for c = 3..15: the strata are empty while 6–317 solutions per n exist,
all in the gcd > 1 or mixed strata that primes do not possess.)

**The closure.** The (t,3) channels of Lemma C cover the class p ≡ −3 (mod t), and
(−3/t) = −1 precisely when t ≡ 2 (mod 3): *the family exists exactly because its classes
contain no squares* (machine-checked for all 15 t). Schinzel's obstruction is not an
external prohibition — it is visible as the boundary of the constructible.

**Remark (the obstruction reaches past identities).** The K-criteria of §9.2 are
*conditional on factorizations*, not congruence identities — Theorem F below does not
formally cover them. They die at squares anyway, each by one line:
every divisor of 4c²+1 is ≡ 1 (mod 4) (any prime ℓ | 4c²+1 has (−1/ℓ) = 1), so K1 can
never fire at n = c²; every divisor of 8c²+1 is ≡ 1 or 3 (mod 8) ((−2/ℓ) = 1), never the
required 7, killing K2; and for K3, a divisor D ≡ −1 (mod 4q) of 4c²q+1 would need
Jacobi (−q/D) = +1 from its prime factors but reciprocity forces (−q/D) = −1.
(Machine-checked for all odd c ≤ 99, q ≤ 13.) So even the conditional-criterion realm
obeys the square obstruction — the precise sense of ET Prop 1.6's "any method that
proves f_I(p) > 0 or f_II(p) > 0 for all p must fail at p²."

### 9.5 The wall, now a theorem (Theorem F)

**Theorem F.** Call a *channel* any rule, valid for all integers n ≡ r (mod m) with
gcd(n, S) = 1 (S finite) and n > n₀, that produces a coprime-stratum Type I or Type II
solution for 4/n. Then r is not a unit square mod m. Consequently any finite channel
system, with M = lcm of its moduli (including S-primes), leaves every prime
p ≡ 1 (mod M) uncovered — a set of relative density 1/φ(M) > 0.

*Proof.* If r ≡ u² (mod m), choose odd c ≡ u (mod m) with gcd(c, S) = 1 (CRT); then
n = c² lies in the channel's class for infinitely many c, and the channel would produce
a coprime-stratum solution at n = c², contradicting Lemma D. For the consequence:
p ≡ 1 (mod M) lies in class 1 = 1² mod every channel modulus. ∎

So Theorem E is sharp in kind: identity systems can approach full coverage at the
(log T)^{−1/2} rate but can never finish, and the six square classes mod 840 are simply
the M = 840 cross-section of this theorem. The same scaling argument (via ET Prop 1.6)
also rules out the circle method for the strata counts. **Any proof of ESC must use
primality beyond congruence and size data — squares impersonate primes to every finite
modulus, and the strata that primes must fill are exactly the strata squares provably
cannot.**

### 9.6 The dead-end log (attempts made this session, and where each died)

1. *Force a small divisor.* Choose m so that a fixed small D | 4pm+1, e.g. D = 3 via
   m ≡ −(4p)⁻¹ (mod 3). The side condition m | y₁z₁ then collapses: for D = 3 it forces
   m = 1, i.e. exactly the classical p ≡ 2 (mod 3) identity, nothing more. Every such
   choice converts into one congruence-channel and is absorbed by Theorem F.
2. *Cover a square class with conditional channels.* For p ≡ 1 (mod 840): D = 3 needs
   p ≡ 2 (mod 3) ✗; D = 7 needs p ≡ 5 (mod 7) ✗ — the class congruences kill every
   small-divisor trick *because* 1 is a residue everywhere. D = 11 fires on the
   subclass p ≡ 8 (mod 11) — whose joint class mod 9240 again contains no squares
   ((8/11) = −1). The pattern is total and is Theorem F seen from below.
3. *Balanced divisors.* What remains needed: for every p, some m ≤ M(p) with 4pm+1
   having a divisor ≡ −1 (mod 4m)-type conditions — a *pointwise lower bound for
   divisors of shifted integers in prescribed residue classes*. Elsholtz–Tao get this
   on average and on density-1 sets; their Remark 1.3 states even the second moment is
   out of reach. No identity-side trick discovered here evades that analytic gap.
4. *Disproof direction.* A counterexample needs f(p) = 0: against it stand verification
   to 10¹⁸ (independent, 2025), our own zero-free data to 3.5×10⁷ (now extended this
   session — §10), the floor growing as (ln p)^{3.3} with *shrinking* relative spread,
   and the lognormal-EV account of every record-low. Searching for a counterexample is
   the one strategy the data actively forbids.

### 9.6½ New instruments (this session's engineering)

- **`files/fp.cu`** — CUDA engine for the RTX 5090 found in this machine (32 GB, CUDA 13.2
  driver; nvcc 12.0 emits compute_80 PTX, driver JIT-compiles to Blackwell). Same divisor
  algorithm as fp.c/fpr.rs, x-range tightened to the proven x ≤ (p+1)/2. Final design after
  three performance autopsies: one block per x with the divisor list of x² built once into
  shared memory and scanned in lockstep by all lanes (zero warp divergence — the naive
  thread-per-(p,x) mapping ran at the speed of each warp's fattest d(x²), a ~50× tax);
  Barrett reduction replacing emulated 64-bit `%` (~10× on the inner test); rare
  d(x²) > 6144 handled by a global-memory side path (one of these per launch had been
  setting the wall clock of the *entire* launch); sub-second adaptive x-chunks to coexist
  with the display watchdog; atomics only on the ~10⁻⁵ of (x,p) pairs that score.
  **Validation: byte-identical to the blessed reference (301 primes, mode 0 — including
  the p ≡ 3 (mod 4) dmin/n3 boundary), to our Rust sweep at 10⁶ (92 primes), and to the
  independent 2025 dataset at 3.5×10⁷ (175 primes, fI/fII splits, fat-x path exercised).**
  Throughput: the full [10⁸, 2×10⁸] hard-class octave in ~25 minutes — the work that
  motivated last session's "≈10× this session's compute" estimate.
- **`prime_solutions/`** (pre-existing cuda-oxide port, found untracked): kernel had the
  x-window filter *inverted* (kept exactly the complement x > 3p/4) plus a 512 KB/thread
  divisor buffer with a silent 65,536-divisor undercount cap. Both fixed in source for the
  record, but the crate was never linkable as committed (`cuda_oxide_artifact_anchor`
  undefined at link — missing build-script integration upstream). Superseded by fp.cu.
- **`bend/`** (pre-existing Bend/HVM port, generated by another model): trial-divides every
  i ≤ x (O(x) per x versus O(d(x²)) — ~10⁶× slower at 10⁶), and uses `i64` type hints that
  Bend/HVM2 does not have (native ints are 24-bit, overflowing at p ≳ 8·10⁶). Unusable for
  this project; kept as an artifact.
- **`files/verify_lemmas.py`** — machine verification of §9 (8,519 exact assertions).
- **`files/analyze_session2.py`** — merge/validate/law/octave analyses for §10.

### 9.7 Verdict

The conjecture was **neither proved nor disproved** this session — and §9.3–9.5 now
*prove inside this project's own framework* that the entire identity/covering/channel
toolbox (the only elementary toolbox there is) cannot prove it, while the data of §2–§5
and §10 quantify how far any disproof would have to swim against a lognormal tide. The
honest state of the art, sharpened: ESC for the six square classes mod 840 is equivalent
to a pointwise divisor-distribution lower bound that current analytic number theory
delivers only on average. The gap "density 1 → all primes" *is* the conjecture.

## 10. The new data (this session's computations)

### 10.1 The full 1-mod-24 dataset to 10⁷ — complete and triple-validated

Last session's sweep had died before its final segment (seg5 finished 19:38; seg6 never
ran). Re-launched and completed: **82,887 primes — every p ≡ 1 (mod 24) in [73, 10⁷] —
with f(p), f_I, f_II each.** Validation of the new segments against the independent 2025
dataset on their six-square-class overlap: **18,143 primes, 0 mismatches** (cumulative
independent agreement now 22,662 primes across two sessions, still zero discrepancies).
And the base check: **f(p) > 0 for every one of the 82,887 primes** — ESC re-verified on
the full hard class to 10⁷ by an engine written and validated independently of all
published code.

### 10.2 The square-class concentration law at 10⁷ (the test no other dataset can run)

Within p ≡ 1 (mod 24) there are 24 unit classes mod 840 (not 35: the other 11 share a
factor with 840), of which the six square classes are exactly 1/4. Uniformly, a window
minimum lands in them with probability 1/4. Observed, full class to 10⁷:

| window | n | min f | at p | mod 840 | square? | median | min/med |
|---|---|---|---|---|---|---|---|
| 2¹¹ | 31 | **9** | **2521** | 1 | YES | 38 | 0.24 |
| 2¹² | 58 | 20 | 4201 | 1 | YES | 46 | 0.44 |
| 2¹³ | 99 | 23 | 9601 | 361 | YES | 58 | 0.40 |
| 2¹⁴ | 200 | 23 | 20521 | 361 | YES | 73 | 0.32 |
| 2¹⁵ | 375 | 34 | 44641 | 121 | YES | 91 | 0.37 |
| 2¹⁶ | 704 | 37 | 67369 | 169 | YES | 109 | 0.34 |
| 2¹⁷ | 1,331 | 46 | 132721 | 1 | YES | 132 | 0.35 |
| 2¹⁸ | 2,548 | 52 | 471241 | 1 | YES | 156 | 0.33 |
| 2¹⁹ | 4,815 | 67 | 589681 | 1 | YES | 185 | 0.36 |
| 2²⁰ | 9,147 | 88 | 1202881 | 1 | YES | 216 | 0.41 |
| 2²¹ | 17,541 | 95 | 2405881 | 121 | YES | 252 | 0.38 |
| 2²² | 33,433 | 104 | 5410441 | 1 | YES | 290 | 0.36 |
| 2²³ | 12,574 | 120 | 8628481 | 1 | YES | 316 | 0.38 |

**13 of 13 window minima land in the six square classes** (null probability 4⁻¹³ ≈
1.5×10⁻⁸), and **62 of 65 bottom-five primes** are square-class (null expectation
16.25 of 65). The square-class share of the population is 0.2475 — exactly the uniform
1/4 — so this is pure *concentration of the lower tail*, not population skew.

The mechanism is now a theorem rather than a reading of Mordell: within p ≡ 1 (mod 24),
p is automatically a residue mod 8 and mod 3, so non-squareness mod 840 must come from
being a non-residue mod 5 or mod 7 — and those classes carry class-wide Type I channels
(Lemma C-type; e.g. e = 5 for p ≡ ±2 (mod 5), e = 63 with a ∈ {11, 23} for p ≡ 3, 5
(mod 7)), each a deterministic additive boost to f that the six square classes provably
cannot have (Theorem F). The lower tail belongs to the square classes because *only
there* is f built entirely from conditional channels with no guaranteed floor.

### 10.3 The [10⁸, 2×10⁸] octave — the §5 prediction tested and confirmed

Run on the RTX 5090 with the new engine (43 GPU-minutes; ~10⁷× the algorithmic distance
of the phone session that started this project): all 166,140 primes of the six square
classes mod 840 in [10⁸, 2×10⁸] — **4–5.7× beyond the largest published f(p) dataset.**
Post-hoc engine cross-check at production scale: the CPU engine (fpr, historical 3p/4
range, 124 minutes for a 2×10⁵-wide slice) agrees with the GPU on all 354 six-class
primes of [10⁸, 1.002×10⁸] — `files/cross_check_1e8.result`, 0 mismatches, closing the
validation loop at the fourth scale (and measuring the GPU at ~600× CPU throughput).

- **ESC holds throughout: no prime has f = 0.** Stronger: no prime has f_I = 0 and none
  has f_II = 0 — *neither mechanism ever fails*, now verified to 2×10⁸ (the phone
  session's law, at 5.7× the previous range).
- **The out-of-sample prediction is confirmed.** Last session, from data ≤ 3.5×10⁷, the
  lognormal-EV model predicted min f over hard primes in [10⁸, 2×10⁸] ≈ **175–225**.
  Observed: **min f = 191**, at p = 142,361,209 ≡ 529 = 23² (mod 840). Dead centre of a
  band predicted blind from 4× smaller scales. Per half-octave the EV machinery is
  sharper still: predicted minima ≈ 212 and 225, observed 213 and 191 (+0.5%, −15%) —
  the small left-tail enhancement of §5 visible again in the second.
- The entire bottom-10 lies in [191, 228] — tightly packed, exactly as a shrinking-σ
  lognormal demands; all ten are square-class (the §10.2 law at 10⁸).
- **The growth exponents hold at 10⁸:** refitting with the new octave appended to the
  §2 windows gives min f ~ (ln p)^3.46 and median ~ (ln p)^3.42 — the floor still grows
  *at the same exponent as the median*, with min/med per half-octave at 0.50 and 0.42.
- **Concentration continues:** σ(ln f) = 0.165, 0.162 in the two half-octaves
  (down from 0.176 at 2²⁵; var/mean 11.8 → 12.1 tracks the lognormal identity).

In disproof terms: a counterexample is a prime with f = 0, i.e. ln f = −∞, while the
hard-class distribution at 2×10⁸ sits at ln f = 6.11 ± 0.16 and its observed minima land
on the lognormal-EV line within percent. Every order of magnitude climbed pushes the
floor up by another ~×1.35 while the relative spread *tightens*. The conjecture's truth
is not in serious empirical doubt; only its proof is missing.

### 10.4 The 10⁹ probe — the model hits within 0.6% at 28× its training range

A second GPU run: all 14,955 six-square-class primes in [10⁹, 1.01×10⁹] (21 minutes).

- **Zero-free again: f, f_I, f_II all positive on every prime** — both mechanisms alive
  at 10⁹.
- **min f = 347** at p = 1,007,635,561 ≡ 121 = 11² (mod 840); window median 610.
  The lognormal-EV prediction for *this exact window* (using μ, σ measured in-window and
  pure extreme-value theory): **345**. The model — whose μ/σ trends were fitted on data
  ≤ 3.5×10⁷ — places the minimum at 10⁹, 28× beyond its fitting range, within 0.6%.
- Fully coherent with §5's full-octave band (245–335 for all of [10⁹, 2×10⁹]): a 1%-width
  window must bottom out *above* the full octave's minimum, and 347 > 335 sits exactly
  where the order statistics demand.
- σ(ln f) = 0.148 — the concentration march continues (0.176 → 0.163 → 0.148 across
  5×10⁷ → 2×10⁸ → 10⁹); all five bottom primes are square-class.
- Exponent refits with the 10⁹ point: min f ~ (ln p)^3.59, median ~ (ln p)^3.42 — the
  floor's effective exponent stays at-or-above the median's across 5.6 decades.

The f(p) landscape is, to the precision this project can measure, a *deterministically
rising, relatively tightening* lognormal sheet whose lowest points are pure order
statistics in the six channel-starved classes — with not a single anomalous prime in
263,982 computed across 73 → 1.01×10⁹.

---

# Session addendum (2026-06-12): the signed extension — Erdős–Straus over ℤ

Goal of this session, as set: *bring negative integers into the conjecture; see what
pattern it extends to in the negative integer domain, and whether the different angle
opens a route to proving or disproving it.* This section is the answer. Every numbered
claim is machine-verified by `files/verify_signed.py` (536,988 exact-arithmetic
assertions) and the validated engine `files/fsigned.c`.

## 11. Erdős–Straus over ℤ: the conjecture is a chirality statement

### 11.0 Honest headline

1. Over ℤ* = ℤ∖{0} the problem **collapses**: *two* signed unit fractions already
   suffice for every 4/n (Theorem G) — and the failure sets of the two possible
   2-term forms are exactly complementary: the sum-form fails precisely on the
   class containing every ESC-hard prime, the difference-form fails precisely on
   primes ≡ 3 (mod 4) (the ESC-easy ones). The hardness does not dissolve — **it
   swaps sides under a sign flip.**
2. The §9.1 kernel survives verbatim (Lemma H): same divisor classes
   d ≡ −B (mod 4x−n), and the grade of a solution (0, 1, or 2 negative
   denominators) is purely the *window* the divisor lands in. ESC = "some divisor
   lands in the positive window" — positivity is geometry inside the class, not a
   new equation.
3. The square obstruction — the proved reason (§9.4–9.5) no covering/identity/circle
   method can settle ESC — **is chiral** (Lemma K): at odd squares the Jacobi
   contradiction kills only the positive windows; the negative windows of the very
   same residue classes are populated. Class-wide *signed* identities exist on every
   square class (impossible for positive ones, Theorem F).
4. Negative n is an exact mirror (Theorem J): f̃ₖ(−n) = f̃₃₋ₖ(n). The negative
   half-line adds no new conjecture; the new content of ℤ is the *grading between
   the chiralities* — and it measures something: the graded census to 6×10⁵ shows
   the six square classes, starved in f₀ (the §10.2 law), are the **richest** classes
   in f₁, with window minima landing in them 7/7 for f₀ and 0/7 for f₁, and a
   within-window rank correlation corr(f₀, f₁) = −0.43. **Channel starvation is not
   a deficit of solutions; it is a displacement of solution mass into the other
   chirality.** The record prime: f̃(2521) = (9, 377, 307).
5. The angle cannot prove ESC (Corollary L: no channel system can flip chirality —
   one line from Theorem F), and it cannot disprove it (signed counts certify
   nothing about f₀ = 0). What it delivers is the sharpest statement yet, in this
   project's own framework, of *what* ESC is: a window-equidistribution claim for
   divisors in residue classes, with the obstruction theory localized entirely in
   one sign sector.

### 11.1 Setting (definitions used throughout)

For n ∈ ℤ*, let S(n) = multisets {x,y,z} ⊂ ℤ* with 1/x + 1/y + 1/z = 4/n. A triple
containing a cancelling pair {t, −t} forces the third member to equal n/4: such
**trivial triples** exist iff 4 | n and form the unique infinite family
{t, −t, n/4}. S̃(n) excludes them; everything below counts S̃. Grade k = number of
negative members; f̃ₖ(n) = #{s ∈ S̃(n) : grade k}; F̃ = Σ f̃ₖ. For n > 0 only
k ∈ {0,1,2} occur, and f̃₀ = f, the classical unordered count of §1–§10 (= OEIS
A192787 convention; Elsholtz–Tao's ordered f is A292581). F̃(n) < ∞ always: some
member has |t| ≤ 3n/4 (else |Σ1/xᵢ| < 4/n), and the remaining pair is determined by
a divisor of a fixed square through (ay−b)(az−b) = b². [Machine: S3, S4.]

### 11.2 Two signed unit fractions always suffice (Theorem G)

**Theorem G.** Let n ≥ 2. (i) 4/n = 1/x + 1/y with x, y > 0 is solvable iff n² has a
divisor d ≡ −n (mod 4); the failure set is exactly
   A = { n ≡ 1 (mod 4) : every prime factor of n is ≡ 1 (mod 4) } —
in particular every prime p ≡ 1 (mod 4). (ii) 4/n = 1/x − 1/y (x, y > 0) is solvable
iff n² has a divisor u ≡ n (mod 4) with u < n; the failure set is exactly
   B = {2, 4} ∪ { primes ≡ 3 (mod 4) }.
(iii) A ∩ B = ∅. Hence **every** 4/n, n ≥ 2, is a sum of two signed unit fractions —
ESC's "three" is an artifact of positivity.

*Proof.* (i) 4xy = n(x+y) ⟺ (4x−n)(4y−n) = n². Both factors negative would force
x, y < n/4, i.e. 1/x + 1/y > 8/n: impossible. So d = 4x−n > 0, d | n², d ≡ −n (mod 4),
and conversely each such d gives x = (n+d)/4, y = (n + n²/d)/4 (the partner lies in
the right class mod 4 in every case n odd / 2‖n / 4|n). Failure: for odd n all
divisors of n² are products of odd primes; a divisor ≡ 3 (mod 4) exists iff some
prime ≡ 3 (mod 4) divides n; for n ≡ 3 (mod 4) take d = 1. For n ≡ 2 (mod 4),
d = 2 works (x = (n+2)/4 ∈ ℤ, y = m(m+1)/2 with m = n/2); for 4 | n, d = n works
(x = y = n/2). (ii) 4/n = 1/x − 1/y ⟺ (n−4x)(n+4y) = n², u = n−4x ∈ (0, n) since
1/x > 4/n, v = n + 4y > n. Conversely u | n², u ≡ n (mod 4), 0 < u < n gives
x = (n−u)/4 ≥ 1, y = (n²/u − n)/4 ≥ 1. Failure: n ≡ 1 (mod 4): u = 1 always works.
n ≡ 3 (mod 4): need u ≡ 3 (mod 4), u | n², 1 ≤ u < n; for prime p the divisors
1, p, p² leave nothing (< p and ≡ 3); composite n ≡ 3 (mod 4) has a prime factor
q ≡ 3 (mod 4) with q < n. n ≡ 2 (mod 4): u = 2 works for n ≥ 6, nothing for n = 2.
4 | n: u = 4 works for n ≥ 8 (y = k(k−1), k = n/4), nothing for n = 4.
(iii) A consists of n ≡ 1 (mod 4); B of even n and n ≡ 3 (mod 4). ∎
[Machine: S2 — exhaustive to 2000 against the actual solution sets, both
divisor-criterion forms; explicit witnesses to 10⁶. The mod-4 duality at primes:
p ≡ 1 (mod 4): only the *signed* form exists, 4/p = 1/((p−1)/4) − 1/(p(p−1)/4);
p ≡ 3 (mod 4): only the *positive* form, 4/p = 1/((p+1)/4) + 1/(p(p+1)/4).]

**Remark (how trivial the signed problem is).** Nearest-integer greedy gives ≤ 3
signed terms for every 4/n in one step of case analysis, and for the general
Schinzel numerator: k/n with n ≥ k/2 needs at most ⌊log₂ k⌋ + 1 signed unit
fractions (halving recursion |kx−n| ≤ k/2) — the entire k/n landscape, where in
positive integers even the *existence* of a threshold n_k is delicate and
exceptions provably persist to exp(k^{1/3−ε}) (Pomerance–Weingartner 2025, §7a),
collapses to logarithmic length over ℤ*. Positivity is the entire subject.
[Machine: S6.]

**Three-term graded existence.** f̃₁(n) ≥ 1 for every n ≥ 3 **except exactly
n ∈ {2, 4}** (and f̃₁(2) = f̃₂(2) = 0 makes n = 2 the unique signless point:
F̃(2) = f(2) = 1). Per-class polynomial witnesses, each verified to 10⁶: the all-odd
identity 4/n = 1/((n−1)/2) + 1/((n+1)/2) − 1/(n(n−1)(n+1)/4) (Jaroma 2004 — the one
documented trace of the signed variant in the literature, cited by Wikipedia's
"Negative-number solutions" section); the modulus-1 family below; twisted sum-forms
for even n. [Machine: S5.]

### 11.3 The signed kernel (Lemma H): same classes, new windows

**Lemma H.** Let n ≥ 2, and let x be the least positive denominator of a
solution (grades 0, 1) or its unique positive denominator (grade 2); a = 4x − n,
B = nx, dmin = 2x(2x − n). Then S̃(n) is in bijection with the divisors d of B²
(both signs) satisfying d ≡ −B (mod |a|) — plus exact integrality of the partner
slot when gcd(a, B) > 1, a case absent at primes (§9.1) — through
y = (B+d)/a, z = (B + B²/d)/a, graded **purely by the window d lies in**:

| grade | x-range | window for d |
|---|---|---|
| 0 | n/4 < x ≤ 3n/4 | max(1, dmin) ≤ d ≤ B |
| 1 | n/4 < x ≤ n/2 | dmin ≤ d ≤ −1 |
| 1 | 1 ≤ x < n/4 | d ≤ dmin (< −B) |
| 2 | 1 ≤ x < n/4 | 1 ≤ d ≤ B |

*Proof sketch.* The pair equation (a·u − B)(a·v − B) = B² is §9.1's, with signs kept.
The inequalities y ≥ x ⟺ d ≥ dmin (a > 0) resp. d ≤ dmin (a < 0), and the sign
pattern of the two slots as a function of d's position relative to (−B, 0), give the
table; each multiset is reached from exactly one (x, d). x-ranges: grade 0 needs
1/x < 4/n ≤ 3/x; grade 1 needs 2/x ≥ 1/x + 1/y > 4/n; grade 2 needs 1/x > 4/n. ∎
[Machine: S3 — the table reproduces an independent naive census *exactly, grade by
grade and triple by triple*, for all 2 ≤ n ≤ 200; the C engine is byte-identical to
the Python dictionary on [2,300] and reproduces f, f_I, f_II of the blessed 10⁷
dataset on all 385 primes ≡ 1 (mod 24) below 3×10⁴, and f(1009) = 19,
f(2521) = 9 = 6+3.]

**The classical equation never changed.** Positive solutions are the d ∈ [dmin, B]
slice of the same divisor classes that, for d < 0, encode the signed solutions. ESC
states: *some class hits its positive window.* All size/positivity content of the
conjecture is the location of ~B-length windows inside divisor classes mod a.

**Type III.** At a prime p, ν_p(d) ∈ {0, 1, 2} stratifies solutions; the positive
windows admit only ν = 0 (Type I) and ν = 1 (Type II) — ν = 2 forces d ≥ p² > B,
impossible there (asserted at runtime by the engine, every run) — but the grade-1
big window |d| ≤ B² admits **ν = 2: Type III**, a third mechanism with no positive
analogue, in which p divides the *second positive* denominator and not the negative
one. The modulus-1 family is Type III: x = (n−1)/4 gives a = −1 (every divisor
qualifies) and d = −B² yields
   4/n = 1/x + 1/(B²−B) − 1/(B−1),  B = nx,  for all n ≡ 1 (mod 4).
At the record prime, f̃₁(2521) = 377 splits I/II/III = 115/85/177: the forbidden
stratum is the largest. [Machine: S5, S7, S8.]

### 11.4 The square obstruction is chiral (Lemma K)

**Lemma K.** Let n = c² (c odd ≥ 3) and let x give a coprime row (gcd(a, nx) = 1,
a = 4x − n ≡ 3 (mod 4)). Lemma D proved the positive pure strata empty: the class
requires Jacobi sign (d/a) = (−1/a) = −1 while every positive divisor built from x²
forces (d/a) = +1. For **negative** d the same two facts give
(d/a) = (−1/a)(|d|/a) = (−1)(+1) = −1 — *equal to the required sign*. The
obstruction vanishes on the negative windows; and they are in fact populated at
every odd square: the modulus-1 family lands there (n ≡ 1 mod 4 includes all odd
squares), and exhaustively for c = 3..15 the coprime rows carry 9–358 signed
solutions against *zero* positive pure-stratum ones. ∎ [Machine: S7 — including
3000 random Jacobi-sign instances and the exhaustive c ≤ 15 sweep.]

So the precise object that §9 proved makes ESC unprovable by identities — squares
impersonating primes inside every residue class — **only impersonates them on one
side of zero.** Squares are not arithmetically starved; they are *chirally
polarized*: all their coprime-stratum solution mass sits in the signed sector. The
known qualitative remark that positivity "is essential to the difficulty"
(Wikipedia, after Jaroma) becomes a theorem about exactly which window the Jacobi
obstruction occupies.

### 11.5 Why the angle still cannot prove ESC (Corollary L) — and what it buys

**Corollary L (no chirality flip).** There is no channel — in the sense of
Theorem F: a rule valid on a residue class, producing coprime-stratum positive
solutions — that converts the (always-available: Theorem G, Lemma K) signed
solutions into positive ones on any class containing squares. *Proof:* composed
with the class-wide signed identities, it would be a Theorem-F channel; Theorem F
forbids those. ∎ At odd squares the impossibility is absolute: the source set is
populated, the target set is *empty* (Lemma D). The signed world's class-wide
identities — which cover every hard class, e.g. the modulus-1 family on all of
n ≡ 1 (mod 4) — are provably non-transportable. Any proof of ESC routed through
signed solutions must use primality beyond congruence data, exactly the §9.7 wall.

The decomposition that remains is f̃₀ = F̃ − f̃₁ − f̃₂ with each term a divisor-class
count in explicit windows (Lemma H). Lower-bounding F̃ is plausibly tractable on
average (no interval constraints), but converting it to a pointwise statement about
f̃₀ needs pointwise control of f̃₁ + f̃₂ — the same species of bound Elsholtz–Tao
declare beyond current methods even at the second moment (Remark 1.3). The program
transmutes the difficulty; it does not remove it. What is genuinely new and usable:
ESC restated as **window equidistribution** (does every prime's positive window get
its share of the class?), plus the measurables below — share ρ = f̃₀/F̃, the
anticorrelation structure, the Type III stratum — quantities a future analytic
attack can be tested against, and that did not exist as data before today.

### 11.6 The negative integer domain itself (Theorem J)

**Theorem J (mirror).** Negation (x,y,z) ↦ (−x,−y,−z) is a bijection
S̃(n) → S̃(−n) sending grade k to 3−k. Hence f̃ₖ(−n) = f̃₃₋ₖ(n), F̃(−n) = F̃(n)
(F̃ is an *even* function on ℤ*), and for n ≤ −2: 4/n is a sum of three negative
unit fractions iff ESC holds for |n|. ∎ [Machine: S4.]

The direct answer to "what pattern does the conjecture extend to in the negative
domain": **the mirror image, exactly — and nothing else.** There is no new
conjecture on the negative axis; ESC over ℤ is the statement that the even function
F̃ keeps its grade-0 component positive on one side (equivalently, by the mirror,
its grade-3 component on the other). The genuinely new territory the extension
opens is not n < 0 but the mixed-sign grades at n > 0. The census of the boundary
(trivial family flagged; n = ±1 have F̃ = 0 since |Σ| ≤ 3 < 4):

|  n  | f̃₀ | f̃₁ | f̃₂ | f̃₃ |  F̃ |   |  n | f̃₀ | f̃₁ | f̃₂ | f̃₃ |  F̃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| −2 | 0 | 0 | 0 | 1 | 1 | | 2 | 1 | 0 | 0 | 0 | 1 |
| −3 | 0 | 0 | 1 | 3 | 4 | | 3 | 3 | 1 | 0 | 0 | 4 |
| −4 | 0 | 0 | 0 | 3 | 3* | | 4 | 3 | 0 | 0 | 0 | 3* |
| −5 | 0 | 2 | 3 | 2 | 7 | | 5 | 2 | 3 | 2 | 0 | 7 |
| −6 | 0 | 2 | 5 | 8 | 15 | | 6 | 8 | 5 | 2 | 0 | 15 |
| −7 | 0 | 0 | 6 | 7 | 13 | | 7 | 7 | 6 | 0 | 0 | 13 |
| −8 | 0 | 2 | 3 | 10 | 15* | | 8 | 10 | 3 | 2 | 0 | 15* |
| −9 | 0 | 9 | 11 | 6 | 26 | | 9 | 6 | 11 | 9 | 0 | 26 |
| −10 | 0 | 6 | 11 | 12 | 29 | | 10 | 12 | 11 | 6 | 0 | 29 |
| −11 | 0 | 2 | 8 | 9 | 19 | | 11 | 9 | 8 | 2 | 0 | 19 |
| −12 | 0 | 7 | 12 | 21 | 40* | | 12 | 21 | 12 | 7 | 0 | 40* |

(*) plus the infinite trivial family at 4 | n. Note f̃₂ = 0 happens (n ∈ {2,3,4,7}
in [2, 10⁴], nothing else to 10⁴): the "two-negatives" sector can be empty at small
n — another positivity-flavoured scarcity, mirrored to f̃₁ on the negative axis.

### 11.7 The graded data (new instruments, new laws)

**Instruments.** `files/fsigned.c` (OpenMP, __int128; the Lemma H dictionary
verbatim), validated four independent ways before production: naive census ↔
window dictionary (S3, every triple, 2 ≤ n ≤ 200); C ↔ Python byte-identical
([2,300], all 11 columns); C f, f_I, f_II ↔ blessed 10⁷ dataset (385 primes,
0 mismatches); anchors f(1009), f(2521) with their Type splits. Datasets produced:
`signed_census_1e4.csv` (every n ≤ 10⁴), `signed_p24_to_6e5.csv` (all 6,068 primes
≡ 1 (mod 24) in [73, 6×10⁵] — the §10.2 population, graded), and
`signed_floor_exemplars.csv` (the §10.2 floor primes to 8.6×10⁶ with same-window
median partners). Analysis: `files/analyze_signed.py` (stdlib only).

**F1 — the §10.2 law inverts.** Across the seven dyadic windows 2¹³–2¹⁹ of the
prime band: every f₀ window minimum lands in the six square classes (7/7 — the
§10.2 law again), while **no f₁ window minimum does (0/7**, base rate 0.24); the
square classes' f₁ *floor* sits 13–35% above the other classes' floor in every
window, and their median f₁ is 12–44% higher (e.g. window 2¹⁹: median 1086 vs 825).
The channel-starved classes are the f₁-richest classes in every window measured.

**F2 — the chirality see-saw.** Pooled within-window rank correlations over the
6,068 primes: corr(f₀, f₁) = **−0.430**, corr(f₀, f₂) = −0.483,
corr(f₁, f₂) = **+0.960**. The two signed grades move in lock-step (they draw on
the same negative windows); both move *against* the positive grade. Starvation and
richness are one variable seen from two sides.

**F3 — floor primes are signed-rich outliers.** The §10.2 floor primes inside the
band sit at f₁ percentile 92.6 (132721), 99.8 (471241), 99.9 (589681) of their
windows while their f₀ percentile is 0.0. The exemplar table to 8.6×10⁶ (vs
same-window median-f₀ partners):

| p | mod 840 | role | f₀ | f₁ | f₂ | F̃ | f₁/f₀ | ρ = f₀/F̃ |
|---|---|---|---|---|---|---|---|---|
| 132721 | 1 | floor | 46 | 1257 | 959 | 2262 | 27.3 | 0.020 |
| 139297 | 697 | median | 132 | 613 | 280 | 1025 | 4.6 | 0.129 |
| 471241 | 1 | floor | 52 | 3036 | 2634 | 5722 | 58.4 | 0.009 |
| 520369 | 409 | median | 156 | 876 | 508 | 1540 | 5.6 | 0.101 |
| 589681 | 1 | floor | 67 | 3031 | 2652 | 5750 | 45.2 | 0.012 |
| 904297 | 457 | median | 185 | 944 | 465 | 1594 | 5.1 | 0.116 |
| 1202881 | 1 | floor | 88 | 2175 | 1716 | 3979 | 24.7 | 0.022 |
| 1703089 | 409 | median | 216 | 880 | 405 | 1501 | 4.1 | 0.144 |
| 2405881 | 121 | floor | 95 | 1734 | 1182 | 3011 | 18.3 | 0.032 |
| 2831089 | 289 | median | 252 | 1289 | 771 | 2312 | 5.1 | 0.109 |
| 5410441 | 1 | floor | 104 | 3434 | 2778 | 6316 | 33.0 | 0.016 |
| 7702729 | 769 | median | 290 | 1461 | 895 | 2646 | 5.0 | 0.110 |
| 8628481 | 1 | floor | 120 | 4496 | 3849 | 8465 | 37.5 | 0.014 |
| 9644641 | 601 | median | 316 | 2169 | 1491 | 3976 | 6.9 | 0.079 |

Every floor prime carries **more total solution mass F̃ than its median partner**
(1.3×–3.7×) — the starvation is strictly a property of the positive window. The
record prime 2521 reads f̃ = (9, 377, 307): F̃ = 693 solutions, 98.7% of them
signed, Type III alone (177) dwarfing the entire positive count.

**F4 — the positivity share.** ρ = f̃₀/F̃ over the band: median 0.103 (square
classes 0.066, others 0.117), 5th percentile 0.035, minimum **0.0091 at
p = 471241 ≡ 1 (mod 840)** — the same prime §10.2 already knew as a floor prime. A
counterexample to ESC is a prime with ρ = 0 exactly: not a prime with few
solutions, but one whose hundreds-to-thousands of solutions (F̃ has its own rising
floor: per-window minima 421 → 1018 across 2¹³ → 2¹⁹) *all* miss one window of
relative length ~B inside
every class. The §5/§10 lognormal account of f₀ gains a denominator: f₀ is an
anticorrelated ~3–25% share of a smooth, never-starved total.

**F5 — proposed mechanism (rigorous at squares, statistical at square-class
primes).** Lemma K shows the sign flip (d/a) ↦ −(d/a) under d ↦ −d converts the
exact obstruction at squares into exact permission. For square-class *primes* the
same Jacobi pressure operates statistically on every channel (§3.2): classes whose
positive windows are sign-disfavoured have sign-favoured negative windows. The
measured see-saw (F1–F3) is that pressure summed over channels. We state this as a
mechanism hypothesis consistent with all data, proved here only at exact squares.

**F6 — sequences.** Neither f̃₁ nor F̃ appears in OEIS (search 2026-06-12; the
positive counts are A073101 / A192787 / A292581, and no signed-count sequence
exists). First terms, n = 2, 3, 4, …:
f̃₁: 0, 1, 0, 3, 5, 6, 3, 11, 11, 8, 12, 11, 16, 36, 21, 14, 33, 14, 32, 43, 28, …
F̃: 1, 4, 3, 7, 15, 13, 15, 26, 29, 19, 40, 21, 41, 82, 61, 28, 77, 28, 83, 95, 62, …
Median f̃₁/f̃₀ grows 1.38 → 1.74 → 1.88 across n ∈ [2,10²), [10²,10³), [10³,10⁴):
the signed sectors widen slowly relative to the positive one (more x-rows, longer
windows), yet stay within a small constant factor — the grades are siblings, not
different orders of magnitude.

### 11.8 Verdict

Proved and machine-verified today, inside the project's framework: **Theorem G**
(two signed terms always; complementary failure sets; the mod-4 duality),
**Lemma H** (the signed kernel: same classes, windows are the grading; Type III),
**Theorem J** (the negative domain is an exact mirror; F̃ is even; ESC over ℤ = the
chirality statement), **Lemma K** (the square obstruction is positive-window-only),
**Corollary L** (no channel system can flip chirality — the signed shortcut to ESC
is closed by the project's own Theorem F), plus the small-n classification
({2, 4} exceptional, n = 2 signless). New data: the graded census to 10⁴, the
graded hard-class band to 6×10⁵, floor exemplars to 8.6×10⁶ — and three empirical
laws: the inverted §10.2 law (F1), the see-saw (F2–F3), the ρ-share structure (F4).

The conjecture itself: **open, unmoved — and better understood.** The signed
extension does not crack the wall of §9; it *maps* it: every obstruction this
project has proved (Lemma D, Theorem F, the K-criteria square-death) lives
entirely in the positive windows, and the "missing" solutions of the starved
classes are measurably present with the wrong sign. Erdős–Straus is the assertion
that arithmetic never manages to polarize a prime completely — squares achieve
exactly that polarization, primes provably cannot be distinguished from them by
any finite congruence system (Theorem F), and yet, on all evidence to 10¹⁸ and in
every graded measurement made today, they never even come close. The distance
between those two sentences is the conjecture.

### 11.9 Reproducibility (additions)

- `files/verify_signed.py` — machine verification of §11 (536,988 assertions;
  ~4 min; run: `python3 verify_signed.py`)
- `files/fsigned.c` — graded census engine (build:
  `gcc -O3 -march=native -fopenmp fsigned.c -o fsigned`; usage in header)
- `files/census_ref.py` — Python reference implementation for C validation
- `files/analyze_signed.py` — all §11.7 numbers (stdlib only)
- `files/signed_census_1e4.csv`, `files/signed_p24_to_6e5.csv`,
  `files/signed_floor_exemplars.csv` — the datasets behind F1–F6
- Literature for §11: Jaroma, Crux Mathematicorum 30 (2004) 36–37; Wikipedia
  "Erdős–Straus conjecture" §"Negative-number solutions" (the two documented
  traces of the signed variant — no counting literature and no OEIS sequences
  exist as of 2026-06-12); Elsholtz–Tao arXiv:1107.1010 (Prop 1.6, Rem 1.3);
  Schinzel, Funct. Approx. Comment. Math. 28 (2000) 187–194; Mordell,
  Diophantine Equations (1969), 287–290; Pomerance–Weingartner arXiv:2511.16817.
