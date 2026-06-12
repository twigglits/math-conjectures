#!/usr/bin/env python3
"""analyze_signed.py — analyses for REPORT.md §11.7 (stdlib only).
Inputs (produced by fsigned, see §11.9):
  signed_census_1e4.csv        every n in [2, 10^4]
  signed_p24_to_6e5.csv        every prime ≡ 1 (mod 24) in [73, 6×10^5]
  signed_floor_exemplars.csv   §10.2 floor primes + same-window median partners
"""
import csv, math
from statistics import median

SQ840 = {1, 121, 169, 289, 361, 529}          # the six square classes mod 840

def load(path):
    out = []
    for r in csv.DictReader(open(path)):
        out.append({k: int(v) for k, v in r.items()})
    return out

# ---------------- census [2, 10^4] ----------------
cen = load('signed_census_1e4.csv')
print("=== census n ∈ [2, 10⁴] ===")
z1 = [r['n'] for r in cen if r['f1'] == 0]
z2 = [r['n'] for r in cen if r['f2'] == 0]
print(f"f̃₁ = 0 exactly at n ∈ {z1}   (Theorem G part (iii): {{2,4}})")
print(f"f̃₂ = 0 at {len(z2)} values: {z2[:25]}{' ...' if len(z2) > 25 else ''}")
z2odd = [n for n in z2 if n % 2]
print(f"   of which odd: {z2odd[:20]}{' ...' if len(z2odd) > 20 else ''} "
      f"(all prime? {all(is_p for is_p in map(lambda m: all(m % q for q in range(2, int(m**.5)+1)), z2odd))})")
for dec in [(2,100),(100,1000),(1000,10000)]:
    rows = [r for r in cen if dec[0] <= r['n'] < dec[1]]
    r10 = median(r['f1'] / r['f0'] for r in rows if r['f0'])
    print(f"n ∈ [{dec[0]},{dec[1]}): median f̃₁/f̃₀ = {r10:.2f},  "
          f"median (f̃₀,f̃₁,f̃₂) = ({median(r['f0'] for r in rows):.0f},"
          f"{median(r['f1'] for r in rows):.0f},{median(r['f2'] for r in rows):.0f})")
print("first terms  f̃₁(n), n = 2..40:", [r['f1'] for r in cen if r['n'] <= 40])
print("first terms  F̃(n) , n = 2..40:", [r['f0']+r['f1']+r['f2'] for r in cen if r['n'] <= 40])

# ---------------- the chirality experiment ----------------
pri = load('signed_p24_to_6e5.csv')
for r in pri:
    r['sq'] = (r['n'] % 840) in SQ840
    r['F'] = r['f0'] + r['f1'] + r['f2']
print("\n=== primes ≡ 1 (mod 24), 73 ≤ p ≤ 6×10⁵: square classes vs the rest ===")
print("share square-class:", f"{sum(r['sq'] for r in pri)/len(pri):.4f}", f"(n = {len(pri)})")
print(f"{'window':>8} | {'n_sq':>5} {'min f₀ sq':>10} {'min f₀ ¬sq':>10} | "
      f"{'min f₁ sq':>10} {'min f₁ ¬sq':>10} | {'med f₁ sq':>9} {'med f₁ ¬sq':>9} | f₀-min@ f₁-min@")
f0_sq_hits = f1_sq_hits = nwin = 0
for k in range(13, 20):
    win = [r for r in pri if 2**k <= r['n'] < 2**(k+1)]
    if len(win) < 40: continue
    nwin += 1
    sq  = [r for r in win if r['sq']]; nq = [r for r in win if not r['sq']]
    m0 = min(win, key=lambda r: r['f0']); m1 = min(win, key=lambda r: r['f1'])
    f0_sq_hits += m0['sq']; f1_sq_hits += m1['sq']
    print(f"  2^{k:>2}   | {len(sq):>5} {min(r['f0'] for r in sq):>10} {min(r['f0'] for r in nq):>10} | "
          f"{min(r['f1'] for r in sq):>10} {min(r['f1'] for r in nq):>10} | "
          f"{median(r['f1'] for r in sq):>9.0f} {median(r['f1'] for r in nq):>9.0f} | "
          f"{'SQ' if m0['sq'] else '--':>6} {'SQ' if m1['sq'] else '--':>6}")
print(f"window minima in square classes: f₀: {f0_sq_hits}/{nwin}, f₁: {f1_sq_hits}/{nwin} "
      f"(base rate {sum(r['sq'] for r in pri)/len(pri):.2f})")

def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0]*len(v); i = 0
        while i < len(order):
            j = i
            while j+1 < len(order) and v[order[j+1]] == v[order[i]]: j += 1
            for t in range(i, j+1): rk[order[t]] = (i+j)/2 + 1
            i = j+1
        return rk
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx)/len(rx), sum(ry)/len(ry)
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
    return num/den

# de-trend by window: ranks within each dyadic window, pooled
print("\nSpearman rank correlations within dyadic windows (pooled):")
for (cx, cy) in [('f0','f1'), ('f0','f2'), ('f1','f2')]:
    acc_x, acc_y = [], []
    for k in range(13, 20):
        win = [r for r in pri if 2**k <= r['n'] < 2**(k+1)]
        if len(win) < 40: continue
        # normalize to in-window percentile to pool across windows
        xs = [r[cx] for r in win]; ys = [r[cy] for r in win]
        sx = sorted(xs); sy = sorted(ys)
        acc_x += [sx.index(v)/len(win) for v in xs]
        acc_y += [sy.index(v)/len(win) for v in ys]
    print(f"  corr({cx},{cy}) = {spearman(acc_x, acc_y):+.3f}")

rho = sorted(r['f0']/r['F'] for r in pri)
print(f"\nρ = f̃₀/F̃ over the band: min {rho[0]:.4f}  p5 {rho[len(rho)//20]:.4f}  "
      f"median {rho[len(rho)//2]:.4f}  p95 {rho[-len(rho)//20]:.4f}  max {rho[-1]:.4f}")
print(f"ρ medians: square classes {median(r['f0']/r['F'] for r in pri if r['sq']):.4f}, "
      f"others {median(r['f0']/r['F'] for r in pri if not r['sq']):.4f}")
lo = min(pri, key=lambda r: r['f0']/r['F'])
print(f"lowest positivity share: p = {lo['n']} (≡ {lo['n']%840} mod 840): "
      f"(f₀,f₁,f₂) = ({lo['f0']},{lo['f1']},{lo['f2']}), ρ = {lo['f0']/lo['F']:.4f}")

# in-band §10.2 floor primes: how healthy is their f1?
print("\nfloor primes inside the band — f₁ percentile within their dyadic window:")
for fp in [132721, 471241, 589681]:
    k = fp.bit_length() - 1
    win = [r for r in pri if 2**k <= r['n'] < 2**(k+1)]
    me = next(r for r in win if r['n'] == fp)
    pct1 = sum(r['f1'] < me['f1'] for r in win)/len(win)
    pct0 = sum(r['f0'] < me['f0'] for r in win)/len(win)
    print(f"  p = {fp}: f₀ percentile {100*pct0:4.1f} (floor), f₁ = {me['f1']} "
          f"percentile {100*pct1:4.1f}, f₁III = {me['f1III']}")

# ---------------- exemplars table ----------------
print("\n=== §10.2 floor primes vs same-window median partners (graded) ===")
ex = load('signed_floor_exemplars.csv')
half = len(ex)//2
print(f"{'p':>9} {'mod840':>6} {'role':>7} | {'f₀':>4} {'f₁':>6} {'f₂':>6} {'F̃':>7} "
      f"{'f₁/f₀':>6} {'ρ':>6} {'f₁III':>6}")
for i, r in enumerate(ex):
    role = 'FLOOR' if i < half else 'median'
    F = r['f0']+r['f1']+r['f2']
    print(f"{r['n']:>9} {r['n']%840:>6} {role:>7} | {r['f0']:>4} {r['f1']:>6} {r['f2']:>6} {F:>7} "
          f"{r['f1']/r['f0']:>6.1f} {r['f0']/F:>6.3f} {r['f1III']:>6}")
