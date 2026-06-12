#!/usr/bin/env python3
"""residual_spectrum.py — structure inside the lognormal residual (§12).

z(p) = ln f(p), detrended by half-octave window mean and mod-840 class mean.
Questions answered, all out-of-sample where it matters:
  (1) For each prime modulus q coprime to 840 (11 ≤ q ≤ 97): how much of
      var(z) do the residues p mod q explain (R²_q), and is the non-residue
      side richer (s_q = mean z over NR − mean z over QR), as Theorem F
      predicts (channels at modulus q exist only on NR classes)?
  (2) The decay law of s_q and the cumulative congruence-explained variance:
      does congruence structure exhaust the residual or saturate?
  (3) Beyond congruence: do the K-criteria factorization features
      (4pm+1 having a prime factor ≡ 3 mod 4, m = 1, 2, 3) still predict z
      after the full mod-q model is removed?
Fits use only p ≤ 2×10⁸ (hard_1e7_full + hard_1e8_2e8); hard_1e9_slice is
never touched here (it is the blind set for target_frontier.py).
Writes residual_effects.json for the targeting script.

Run: PYTHONNOUSERSITE=1 python3 residual_spectrum.py
"""
import json, math, random
import numpy as np

SQ840 = (1, 121, 169, 289, 361, 529)
QS = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def jacobi(a, n):
    a %= n; r = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): r = -r
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: r = -r
        a %= n
    return r if n == 1 else 0

def load(path):
    a = np.loadtxt(path, delimiter=",", skiprows=1)
    return a[:, 0].astype(np.int64), a[:, 2] + a[:, 3]          # p, f = fI + fII

def detrend(p, f, classes):
    """z = ln f − half-octave window mean − class mean; returns z and class map"""
    z = np.log(f)
    w = np.floor(np.log2(p) * 2).astype(int)                     # half-octave id
    for wid in np.unique(w):
        m = w == wid
        z[m] -= z[m].mean()
    cls = (p % 840).astype(int)
    cmeans = {}
    for c in classes:
        m = cls == c
        cmeans[int(c)] = float(z[m].mean())
        z[m] -= z[m].mean()
    return z, cmeans

p7, f7 = load("hard_1e7_full.csv")                                # 24 classes, ≤ 10⁷
p8, f8 = load("hard_1e8_2e8.csv")                                 # 6 sq classes
print(f"fit sets: {len(p7):,} primes ≤ 10⁷ (24 classes), {len(p8):,} in [10⁸,2×10⁸] (6 classes)")

# ---------- (1)+(2) the spectrum, 24-class science version on the 10⁷ set ----------
z7, cm7 = detrend(p7, f7, np.unique(p7 % 840))
print(f"\nafter window+class detrend: σ(z) = {z7.std():.4f}  (10⁷ set)")
print(f"{'q':>4} {'R²_q %':>8} {'s_q (NR−QR)':>12} {'SE':>7}   spectrum on the 10⁷ set, all 24 classes")
spec7 = {}
var7 = z7.var()
for q in QS:
    r = (p7 % q).astype(int)
    sums = np.bincount(r, weights=z7, minlength=q)
    cnts = np.bincount(r, minlength=q).astype(float)
    means = np.where(cnts > 0, sums / np.maximum(cnts, 1), 0.0)
    r2 = float((cnts * means**2).sum() / (len(z7) * var7))
    sgn = np.array([jacobi(rr, q) for rr in range(q)])
    nr, qr = (sgn == -1) & (cnts > 0), (sgn == 1) & (cnts > 0)
    s = float((cnts[nr] @ means[nr]) / cnts[nr].sum() - (cnts[qr] @ means[qr]) / cnts[qr].sum())
    se = float(z7.std() * math.sqrt(1 / cnts[nr].sum() + 1 / cnts[qr].sum()))
    spec7[q] = (r2, s, se)
    print(f"{q:>4} {100*r2:>8.3f} {s:>12.5f} {se:>7.5f}   {'NR richer ✓' if s > 2*se else ('—' if abs(s) <= 2*se else 'QR richer ?!')}")

# ---------- pooled square-class fit (the targeting model) ----------
msq7 = np.isin(p7 % 840, SQ840)
P = np.concatenate([p7[msq7], p8]); F = np.concatenate([f7[msq7], f8])
Z, cmS = detrend(P, F, np.unique(P % 840))
print(f"\nsquare-class pool for the score: {len(P):,} primes; σ(z) = {Z.std():.4f}")
effects = {}
pred = np.zeros(len(Z))
for q in QS:
    r = (P % q).astype(int)
    sums = np.bincount(r, weights=Z - pred, minlength=q)          # fit residually (orthogonal-ish anyway)
    cnts = np.bincount(r, minlength=q).astype(float)
    means = np.where(cnts > 0, sums / np.maximum(cnts, 1), 0.0)
    effects[q] = means.tolist()
    pred += means[r]
r2_add = 1 - np.var(Z - pred) / np.var(Z)
print(f"additive mod-q model (q ≤ 97), in-sample R² on pooled square classes: {100*r2_add:.2f}%")

# honest split-half check of the additive model (random deterministic halves)
h = np.zeros(len(P), bool); h[np.random.default_rng(42).permutation(len(P))[:len(P)//2]] = True
pr2 = np.zeros(len(Z))
eff_h = {}
for q in QS:
    r = (P % q).astype(int)
    sums = np.bincount(r[h], weights=(Z - pr2)[h], minlength=q)
    cnts = np.bincount(r[h], minlength=q).astype(float)
    means = np.where(cnts > 0, sums / np.maximum(cnts, 1), 0.0)
    eff_h[q] = means
    pr2 += means[r]
oos = 1 - np.var((Z - pr2)[~h]) / np.var(Z[~h])
print(f"split-half out-of-sample R² of the additive model: {100*oos:.2f}%")

# ---------- (3) factorization features beyond the congruence model ----------
print("\nK-features (does the factorization of 4pm+1 predict z beyond all mod-q?)")
small_primes = []
sieve = np.ones(60000, bool); sieve[:2] = False
for i in range(2, 60000):
    if sieve[i]:
        small_primes.append(i); sieve[i*i::i] = False
def k_alive(N):
    n = N
    for sp in small_primes:
        if sp * sp > n: break
        if n % sp == 0:
            if sp % 4 == 3: return 1
            while n % sp == 0: n //= sp
    if n == 1: return 0
    # n is prime or semiprime of primes > 6×10⁴; n ≡ 3 mod 4 ⇒ has a 3-mod-4 prime
    if n % 4 == 3: return 1
    # n ≡ 1 mod 4: prime ⇒ no; semiprime q1q2 ⇒ both ≡1 or both ≡3 — undecidable cheaply
    return 0 if is_prime(n) else -1                               # −1 = ambiguous (rare)
def is_prime(n):
    if n < 2: return False
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % a == 0: return n == a
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True

rng = random.Random(424242)
idx = rng.sample(range(len(P)), 30000)
resid = (Z - pred)[idx]
feats = np.zeros((len(idx), 3))
amb = 0
for j, i in enumerate(idx):
    pp = int(P[i])
    for mi, m in enumerate((1, 3, 4)):       # m=2 is degenerate: 3 | 8p+1 for all p ≡ 1 (24)
        v = k_alive(4 * pp * m + 1)
        if v < 0: amb += 1; v = 0
        feats[j, mi] = v
print(f"  sample 30,000 primes; ambiguous semiprime cases set to 0: {amb}")
for mi, m in enumerate((1, 3, 4)):
    a, b = resid[feats[:, mi] == 1], resid[feats[:, mi] == 0]
    se = resid.std() * math.sqrt(1/len(a) + 1/len(b))
    print(f"  channel m={m} alive (4·{m}p+1 has a 3-mod-4 prime): {len(a):,} vs {len(b):,} | "
          f"Δ(mean residual z) = {a.mean()-b.mean():+.4f} ± {se:.4f}")
half = len(idx) // 2
X1, X2 = feats[:half], feats[half:]
y1, y2 = resid[:half], resid[half:]
beta, *_ = np.linalg.lstsq(np.c_[np.ones(len(X1)), X1], y1, rcond=None)
pred2 = np.c_[np.ones(len(X2)), X2] @ beta
r2k = 1 - np.var(y2 - pred2) / np.var(y2)
print(f"  K-features beyond the full mod-q model (split-half OOS): R² = {100*r2k:.2f}%  "
      f"of the post-congruence residual")

json.dump({"class_means_sq": cmS, "effects": {str(q): effects[q] for q in QS},
           "qs": QS, "sigma_resid": float((Z - pred).std())},
          open("residual_effects.json", "w"))
print("\nwrote residual_effects.json (square-class score: class + Σ_q effects)")
