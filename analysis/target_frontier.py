#!/usr/bin/env python3
"""target_frontier.py — adversarial targeting of the disproof frontier (§12).

The score: ẑ(p) = class₈₄₀-effect + Σ_q effect_q[p mod q]   (q ≤ 97, coprime to 840)
fitted in residual_spectrum.py on p ≤ 2×10⁸ ONLY (residual_effects.json).
A counterexample, if one exists, is a prime where f₀ = 0 — the lowest-ẑ primes
are where the conjecture is thinnest, so a search that enumerates only the
bottom of the score order gets the floor at a fraction of the sweep cost.

Validation protocol (blind): the model never saw p > 2×10⁸.
  test 1: ../data/hard_1e9_slice.csv  (14,955 primes in [10⁹, 1.01×10⁹], known truth)
  test 2: ../data/fresh_2e9_slice.csv (the new GPU run at [2×10⁹, 2.01×10⁹]) — pass
          the filename as argv[1] when it exists.

Run from analysis/: PYTHONNOUSERSITE=1 python3 target_frontier.py [../data/slice.csv]
"""
import json, math, sys
import numpy as np

eff = json.load(open("residual_effects.json"))
QS = eff["qs"]
EQ = {int(q): np.array(v) for q, v in eff["effects"].items()}
CM = {int(c): m for c, m in eff["class_means_sq"].items()}

def score(p):
    s = np.array([CM[int(c)] for c in p % 840])
    for q in QS:
        s += EQ[q][(p % q).astype(int)]
    return s

def gumbel_min_prediction(lf, n):
    """lognormal-EV in-window minimum prediction (the §10.4 method)"""
    mu, sd = lf.mean(), lf.std()
    a = math.sqrt(2 * math.log(n))
    zmin = -(a - (math.log(math.log(n)) + math.log(4 * math.pi)) / (2 * a))
    return math.exp(mu + sd * zmin)

def evaluate(path, label):
    a = np.loadtxt(path, delimiter=",", skiprows=1)
    p, fI, fII = a[:, 0].astype(np.int64), a[:, 2], a[:, 3]
    f = fI + fII
    n = len(p)
    print(f"\n=== {label}: {n:,} primes in [{p.min():,}, {p.max():,}] ===")
    print(f"zero-free: min f = {int(f.min())}, min fI = {int(fI.min())}, min fII = {int(fII.min())}"
          f"  → ESC + both-mechanisms law {'HOLD' if f.min() > 0 and fI.min() > 0 and fII.min() > 0 else 'FAIL'}")
    imin = int(np.argmin(f))
    print(f"window minimum: f = {int(f[imin])} at p = {p[imin]:,} ≡ {p[imin] % 840} (mod 840)"
          f"   [lognormal-EV in-window prediction: {gumbel_min_prediction(np.log(f), n):.0f}]")
    s = score(p)
    # ranks: low score should pick low f
    rs = s.argsort()                       # predicted poorest first
    rf = f.argsort()
    def spearman(x, y):
        rx = x.argsort().argsort().astype(float); ry = y.argsort().argsort().astype(float)
        rx -= rx.mean(); ry -= ry.mean()
        return float((rx * ry).sum() / math.sqrt((rx * rx).sum() * (ry * ry).sum()))
    print(f"Spearman(score, f) = {spearman(s, np.log(f)):+.3f}   (score fitted on p ≤ 2×10⁸ only)")
    k1 = max(1, n // 100)
    cap = len(set(rs[:k1]) & set(rf[:k1])) / k1
    print(f"true bottom-1% captured by predicted bottom-1%: {100*cap:.0f}%  (random baseline 1%)")
    for K in (50, 150):
        sub = rs[:K]
        rank_of_min = int(np.where(rs == imin)[0][0]) + 1
        print(f"min f inside predicted-bottom-{K}: {int(f[sub].min())}"
              f"  (true slice min {int(f.min())}; true minimizer is score-rank {rank_of_min}/{n})")
    # the budget claim: enumerate only predicted bottom-1% → what floor do you see?
    found = int(f[rs[:k1]].min())
    print(f"adversarial budget: enumerating only the predicted bottom-1% ({k1} primes, "
          f"~{100*k1/n:.1f}% of sweep cost) finds f = {found} vs true min {int(f.min())}")
    return p, f, s

evaluate("../data/hard_1e9_slice.csv", "BLIND TEST at 10⁹ (model never saw any p > 2×10⁸)")
if len(sys.argv) > 1:
    evaluate(sys.argv[1], f"FRESH FRONTIER {sys.argv[1]}")
