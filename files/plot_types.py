#!/usr/bin/env python3
"""plot_types.py — the visual atlas of the Erdős–Straus solution counts.

Five figures into files/plots/ :
  1_landscape.png   f(p), Type I, Type II over five decades (73 → 1.01×10⁹)
  2_fingerprint.png the mod-840 class fingerprint of f₀ vs f₁ (the inversion)
  3_seesaw.png      the chirality see-saw: f₀ vs f₁ in-window percentiles
  4_strata.png      mechanism census: positive strata vs signed strata (Type III)
  5_lognormal.png   the actual law: lognormal collapse + the σ concentration march

Inputs: hard_1e7_full.csv, hard_1e8_2e8.csv, hard_1e9_slice.csv (p,ford,fI,fII),
        signed_p24_to_6e5.csv (graded, see fsigned.c header).

NOTE on this machine: the apt matplotlib needs the apt numpy; run as
    PYTHONNOUSERSITE=1 python3 plot_types.py
to keep the ~/.local numpy-2 from shadowing it.
"""
import csv, os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SQ840 = {1, 121, 169, 289, 361, 529}
SQROOT = {1: "1²", 121: "11²", 169: "13²", 289: "17²", 361: "19²", 529: "23²"}
os.makedirs("plots", exist_ok=True)

def load_pos(path):
    a = np.loadtxt(path, delimiter=",", skiprows=1)
    p, fI, fII = a[:, 0], a[:, 2], a[:, 3]
    return p, fI + fII, fI, fII

def load_signed(path):
    rows = list(csv.DictReader(open(path)))
    g = lambda k: np.array([float(r[k]) for r in rows])
    return {k: g(k) for k in rows[0].keys()}

p1, f1_, fI1, fII1 = load_pos("hard_1e7_full.csv")
p2, f2_, fI2, fII2 = load_pos("hard_1e8_2e8.csv")
p3, f3_, fI3, fII3 = load_pos("hard_1e9_slice.csv")
P  = np.concatenate([p1, p2, p3])
F  = np.concatenate([f1_, f2_, f3_])
FI = np.concatenate([fI1, fI2, fI3])
FII = np.concatenate([fII1, fII2, fII3])
S = load_signed("signed_p24_to_6e5.csv")

def binstats(p, v, width=0.5, lo=11, hi=30.5, minn=25):
    """per log2-bin: (geometric centre, median, min) for bins with ≥ minn points"""
    lg = np.log2(p)
    cs, meds, mins = [], [], []
    e = lo
    while e < hi:
        m = (lg >= e) & (lg < e + width)
        if m.sum() >= minn:
            cs.append(2 ** (e + width / 2))
            meds.append(np.median(v[m]))
            mins.append(v[m].min())
        e += width
    return np.array(cs), np.array(meds), np.array(mins)

# ---------------------------------------------------------------- figure 1
fig, ax = plt.subplots(figsize=(12, 7))
sq_mask = np.isin(P % 840, list(SQ840))
ax.scatter(P, F, s=1.2, c="#b0b0b8", alpha=0.18, rasterized=True, lw=0,
           label="f(p) per prime (263,982 primes ≡ 1 mod 24)")
for v, c, lab in [(F, "#222222", "median f"), (FI, "#1f77b4", "median Type I"),
                  (FII, "#d62728", "median Type II")]:
    cs, meds, mins = binstats(P, v)
    ax.plot(cs, meds, c=c, lw=2.2, label=lab)
    if v is F:
        ax.plot(cs, mins, c=c, lw=1.4, ls="--", label="window min f")
# the (ln p)^3.42 guide, pinned at the 10⁶ median
cs, meds, _ = binstats(P, F)
guide = (np.log(cs) ** 3.42); guide *= meds[len(meds)//2] / guide[len(meds)//2]
ax.plot(cs, guide, c="#2ca02c", lw=1.4, ls=":", label=r"c·(ln p)$^{3.42}$ guide")
for (pp, ff, txt, dy) in [(2521, 9, "p=2521, f=9\n(all-time record)", -0.4),
                          (142361209, 191, "p≈1.42×10⁸\nf=191 (predicted 175–225)", -0.45),
                          (1007635561, 347, "f=347\n(EV model: 345)", -0.45)]:
    ax.annotate(txt, (pp, ff), xytext=(pp, ff * 10 ** dy), fontsize=8.5,
                ha="center", arrowprops=dict(arrowstyle="->", lw=0.8), color="#5a0000")
ax.set(xscale="log", yscale="log", xlabel="p", ylabel="solution count",
       title="The Erdős–Straus landscape: f(p) = Type I + Type II over five decades — "
             "a rising sheet whose floor tracks its median")
ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
ax.grid(alpha=0.25, which="both")
fig.tight_layout(); fig.savefig("plots/1_landscape.png", dpi=135); plt.close(fig)

# ---------------------------------------------------------------- in-window percentiles (band)
def percentiles_in_windows(pvals, v):
    out = np.full(len(v), np.nan)
    lg = np.log2(pvals)
    for k in range(13, 20):
        m = (lg >= k) & (lg < k + 1)
        if m.sum() < 40: continue
        idx = np.where(m)[0]
        order = v[idx].argsort().argsort()          # ranks 0..n-1
        out[idx] = order / (len(idx) - 1)
        # ties: fine for visual purposes
    return out

pb = S["n"]; sqb = np.isin(pb % 840, list(SQ840))
pct0 = percentiles_in_windows(pb, S["f0"])
pct1 = percentiles_in_windows(pb, S["f1"])
ok = ~np.isnan(pct0)

# ---------------------------------------------------------------- figure 2
def boosts(r):
    """which of mod 5 / mod 7 give a non-residue (= class-wide channel boost)"""
    out = []
    if r % 5 in (2, 3): out.append("5")
    if r % 7 in (3, 5, 6): out.append("7")
    return out

classes = sorted(set((pb % 840).astype(int)))
mean0 = {r: pct0[ok & (pb % 840 == r)].mean() for r in classes}
mean1 = {r: pct1[ok & (pb % 840 == r)].mean() for r in classes}
classes = sorted(classes, key=lambda r: mean0[r])          # sort by f₀ richness
fig, ax = plt.subplots(figsize=(13, 6.4))
xs = np.arange(len(classes))
for i, r in enumerate(classes):
    if r in SQ840:
        ax.axvspan(i - 0.5, i + 0.5, color="#ffe9b3", zorder=0)
ax.plot(xs, [mean0[r] for r in classes], "o-", c="#1f77b4", lw=2, ms=7,
        label="f₀ (positive solutions)")
ax.plot(xs, [mean1[r] for r in classes], "s-", c="#d62728", lw=2, ms=7,
        label="f₁ (one negative denominator)")
ax.axhline(0.5, c="gray", lw=1, ls="--")
ax.set_xticks(xs)
ax.set_xticklabels([f"{r}\n{SQROOT.get(r, '')}\n{'·'.join(boosts(r)) or '—'}"
                    for r in classes], fontsize=8)
ax.text(0.02, 0.97,
        "mean f₀ percentile by channel tier (proved mechanism, Lemma C / §10.2):\n"
        "  QR mod 5 and 7 (= the six square classes, '—'):  0.22   ← no class-wide channel exists (Theorem F)\n"
        "  non-residue at one of 5, 7:                                0.53\n"
        "  non-residue at both ('5·7'):                                0.72\n"
        "f₁ runs the same ladder exactly backwards: 0.65 → 0.51 → 0.34",
        transform=ax.transAxes, fontsize=8.8, va="top",
        bbox=dict(fc="white", ec="#999", alpha=0.92))
ax.set(xlabel="p mod 840, sorted by f₀ richness — third label row: which of mod 5 / mod 7 "
              "supply a class-wide channel ('—' = none; shaded = square classes)",
       ylabel="mean in-window percentile of the count",
       title="The class fingerprint and its inversion (6,068 primes, 73 ≤ p ≤ 6×10⁵):\n"
             "f₀ climbs the quadratic-residue ladder, f₁ descends it — starvation is chirality displacement")
ax.legend(fontsize=10, loc="center right"); ax.grid(alpha=0.25, axis="y")
fig.tight_layout(); fig.savefig("plots/2_fingerprint.png", dpi=135); plt.close(fig)

# ---------------------------------------------------------------- figure 3
def spearman(x, y):
    rx = x.argsort().argsort().astype(float); ry = y.argsort().argsort().astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / math.sqrt((rx**2).sum() * (ry**2).sum()))
rho = spearman(pct0[ok], pct1[ok])
fig, ax = plt.subplots(figsize=(8.6, 8))
ax.scatter(pct0[ok & ~sqb], pct1[ok & ~sqb], s=7, c="#1f77b4", alpha=0.25, lw=0,
           label="non-square classes")
ax.scatter(pct0[ok & sqb], pct1[ok & sqb], s=9, c="#d62728", alpha=0.45, lw=0,
           label="six square classes")
# fan the floor-prime callouts out vertically so the labels never overlap
label_y = (0.955, 0.815, 0.675)
for fp, ly in zip((132721, 471241, 589681), label_y):
    i = np.where(pb == fp)[0][0]
    ax.annotate(f"p={fp}\n(REPORT 10.2 floor prime)", (pct0[i], pct1[i]),
                xytext=(0.30, ly), textcoords="data",
                fontsize=8.5, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", lw=0.8,
                                connectionstyle="arc3,rad=0.12"))
ax.set(xlabel="f₀ percentile within dyadic window", ylabel="f₁ percentile within dyadic window",
       title=f"The chirality see-saw (Spearman ρ = {rho:+.2f}):\n"
             "primes poor in positive solutions are rich in signed ones")
ax.legend(fontsize=10, loc="lower left"); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("plots/3_seesaw.png", dpi=135); plt.close(fig)

# ---------------------------------------------------------------- figure 4
fig, (axl, axr) = plt.subplots(1, 2, figsize=(13.5, 6))
for v, c, lab in [(FI, "#1f77b4", "Type I (p | z only)"), (FII, "#d62728", "Type II (p | y and z)")]:
    cs, meds, mins = binstats(P, v)
    axl.plot(cs, meds, c=c, lw=2.2, label=f"median {lab}")
    axl.plot(cs, mins, c=c, lw=1.2, ls="--", label=f"window min")
axl.set(xscale="log", yscale="log", xlabel="p", ylabel="count",
        title="Positive world: the two allowed mechanisms\n(neither min ever touches 0 — that IS the conjecture)")
axl.legend(fontsize=9); axl.grid(alpha=0.25, which="both")
for key, c, lab in [("f1I", "#1f77b4", "f₁ Type I (p | negative member)"),
                    ("f1II", "#d62728", "f₁ Type II (p | both)"),
                    ("f1III", "#2ca02c", "f₁ Type III (p² | d) — impossible in the positive world")]:
    cs, meds, _ = binstats(pb, S[key], lo=13, hi=19.6)
    axr.plot(cs, meds, "o-", c=c, lw=2, ms=4, label=lab)
axr.set(xscale="log", yscale="log", xlabel="p", ylabel="median count",
        title="Signed world (grade 1): three mechanisms —\nthe forbidden stratum is the largest")
axr.legend(fontsize=9); axr.grid(alpha=0.25, which="both")
fig.suptitle("Mechanism census across the strata", y=1.0)
fig.tight_layout(); fig.savefig("plots/4_strata.png", dpi=135); plt.close(fig)

# ---------------------------------------------------------------- figure 5
fig, (axa, axb) = plt.subplots(1, 2, figsize=(13.5, 5.6))
zs, sigs, cents = [], [], []
lg = np.log2(P)
for k in np.arange(11, 30, 1.0):
    m = (lg >= k) & (lg < k + 1)
    if m.sum() < 200: continue
    lf = np.log(F[m])
    mu, sd = lf.mean(), lf.std()
    zs.append((lf - mu) / sd); sigs.append(sd); cents.append(2 ** (k + 0.5))
z = np.concatenate(zs)
axa.hist(z, bins=80, density=True, color="#9ecae1", edgecolor="white", lw=0.3)
xx = np.linspace(-4.5, 4.5, 400)
axa.plot(xx, np.exp(-xx**2 / 2) / math.sqrt(2 * math.pi), c="#d62728", lw=2,
         label="standard normal")
axa.set(xlabel="z = (ln f − μ_window)/σ_window", ylabel="density",
        title=f"The actual pattern: ln f(p) is window-normal\n({len(z):,} primes pooled across all dyadic windows)")
axa.legend(); axa.grid(alpha=0.25)
axb.plot(cents, sigs, "o-", c="#444", lw=2)
axb.set(xscale="log", xlabel="p (window centre)", ylabel="σ(ln f) per window",
        title="…and it concentrates: σ(ln f) falls as p grows\n(the sheet tightens — a counterexample needs ln f = −∞)")
axb.grid(alpha=0.25, which="both")
fig.tight_layout(); fig.savefig("plots/5_lognormal.png", dpi=135); plt.close(fig)

print("wrote plots/1_landscape.png .. plots/5_lognormal.png")
