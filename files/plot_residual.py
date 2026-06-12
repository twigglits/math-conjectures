#!/usr/bin/env python3
"""plot_residual.py — figures 6–7: the congruence spectrum of the residual and
the adversarial-targeting validation.  Run AFTER residual_spectrum.py.
    PYTHONNOUSERSITE=1 python3 plot_residual.py [fresh_slice.csv]
"""
import json, math, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("plots", exist_ok=True)

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

QS = [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

# ---------- recompute the 24-class spectrum on the 10⁷ set ----------
a = np.loadtxt("hard_1e7_full.csv", delimiter=",", skiprows=1)
p7, f7 = a[:, 0].astype(np.int64), a[:, 2] + a[:, 3]
z = np.log(f7)
w = np.floor(np.log2(p7) * 2).astype(int)
for wid in np.unique(w):
    m = w == wid; z[m] -= z[m].mean()
for c in np.unique(p7 % 840):
    m = (p7 % 840) == c; z[m] -= z[m].mean()
var = z.var()
r2s, sqs, ses = [], [], []
for q in QS:
    r = (p7 % q).astype(int)
    sums = np.bincount(r, weights=z, minlength=q)
    cnts = np.bincount(r, minlength=q).astype(float)
    means = np.where(cnts > 0, sums / np.maximum(cnts, 1), 0)
    r2s.append((cnts * means**2).sum() / (len(z) * var))
    sgn = np.array([jacobi(rr, q) for rr in range(q)])
    nr, qr = (sgn == -1) & (cnts > 0), (sgn == 1) & (cnts > 0)
    sqs.append((cnts[nr] @ means[nr]) / cnts[nr].sum() - (cnts[qr] @ means[qr]) / cnts[qr].sum())
    ses.append(z.std() * math.sqrt(1 / cnts[nr].sum() + 1 / cnts[qr].sum()))

fig, (axa, axb) = plt.subplots(1, 2, figsize=(13.2, 5.4))
axa.errorbar(QS, sqs, yerr=np.array(ses), fmt="o", c="#1f77b4", capsize=3, ms=6)
qq = np.linspace(10, 100, 200)
axa.plot(qq, 1.05 / qq, c="#d62728", lw=1.6, ls="--", label="c/q guide  (c ≈ 1)")
axa.set(xscale="log", yscale="log", xlabel="modulus q", ylabel="s_q = mean z(NR) − mean z(QR)",
        title="Theorem F, measured at every modulus:\nnon-residues mod q are f-richer, decaying like ~1/q")
axa.legend(); axa.grid(alpha=0.25, which="both")
axb.bar(range(len(QS)), 100 * np.array(r2s), color="#9ecae1", edgecolor="#5a8fbb",
        label="R²_q (variance of z explained by p mod q)")
axb.plot(range(len(QS)), 100 * np.cumsum(r2s), "o-", c="#d62728", lw=2, ms=4,
         label="cumulative (in-sample)")
axb.axhline(54.86, c="#2ca02c", lw=2, ls="--",
            label="additive model, split-half out-of-sample: 54.9%")
axb.set_xticks(range(len(QS))); axb.set_xticklabels(QS, fontsize=8)
axb.set(xlabel="modulus q", ylabel="% of residual variance",
        title="Over half of the “Gaussian residue” is congruence ladder\n(82,887 primes ≤ 10⁷, window+class-840 detrended)")
axb.legend(fontsize=9); axb.grid(alpha=0.25, axis="y")
fig.tight_layout(); fig.savefig("plots/6_spectrum.png", dpi=135); plt.close(fig)

# ---------- figure 7: targeting validation ----------
eff = json.load(open("residual_effects.json"))
EQ = {int(q): np.array(v) for q, v in eff["effects"].items()}
CM = {int(c): m for c, m in eff["class_means_sq"].items()}
def score(p):
    s = np.array([CM[int(c)] for c in p % 840])
    for q in QS: s += EQ[q][(p % q).astype(int)]
    return s

slices = [("hard_1e9_slice.csv", "blind test at 10⁹ (model fitted on p ≤ 2×10⁸)")]
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    slices.append((sys.argv[1], "fresh frontier at 2×10⁹ (computed after the model was frozen)"))
fig, axes = plt.subplots(1, len(slices), figsize=(6.8 * len(slices), 6))
axes = np.atleast_1d(axes)
for ax, (path, label) in zip(axes, slices):
    a = np.loadtxt(path, delimiter=",", skiprows=1)
    p, f = a[:, 0].astype(np.int64), a[:, 2] + a[:, 3]
    s = score(p)
    pct = s.argsort().argsort() / (len(s) - 1)
    ax.scatter(100 * pct, f, s=4, c="#b0b0b8", alpha=0.35, lw=0, rasterized=True)
    ax.axvspan(0, 1, color="#fdd", zorder=0)
    k1 = max(1, len(p) // 100)
    order = s.argsort()
    ax.scatter(100 * pct[order[:k1]], f[order[:k1]], s=10, c="#d62728", lw=0,
               label=f"predicted bottom-1% — min f = {int(f[order[:k1]].min())}")
    im = int(np.argmin(f))
    ax.scatter([100 * pct[im]], [f[im]], marker="*", s=240, c="#7b0000", zorder=5,
               label=f"true minimum f = {int(f[im])} at p = {p[im]:,}")
    rx = pct.argsort().argsort(); ry = f.argsort().argsort()
    rho = np.corrcoef(rx, ry)[0, 1]
    ax.set(yscale="log", xlabel="congruence-score percentile (0 = predicted poorest)",
           ylabel="f(p)", title=f"{label}\nSpearman = {rho:+.2f}")
    ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.25, which="both")
fig.suptitle("Adversarial targeting: a congruence-only score finds the floor primes "
             "for ~1% of the sweep cost", y=1.0)
fig.tight_layout(); fig.savefig("plots/7_targeting.png", dpi=135); plt.close(fig)
print("wrote plots/6_spectrum.png, plots/7_targeting.png")
