#!/usr/bin/env python3
"""
analyze_session2.py — evening-session analyses.

  merge    : hard_1e6 + hard_seg2..6 -> hard_1e7_full.csv (full p≡1 mod 24 to 10⁷)
  validate : six-square-class subset of the merged sweep vs esc2025 external data
  law      : square-class concentration law per dyadic window over the FULL class
  octave   : [1e8, 2e8] GPU results — zero-free check, window minima vs the
             §5 lognormal-EV prediction (min f in [10⁸,2×10⁸] ≈ 175–225),
             floor/median exponents, lognormal parameters per half-octave
"""
import sys, csv, math, statistics

SQ = {1, 121, 169, 289, 361, 529}   # square classes mod 840

def read_fp(path, fmin=None, fmax=None):
    rows = []
    with open(path) as f:
        r = csv.reader(f)
        head = next(r)
        for row in r:
            p = int(row[0])
            if fmin and p < fmin: continue
            if fmax and p > fmax: continue
            ford, fI, fII = int(row[1]), int(row[2]), int(row[3])
            rows.append((p, ford, fI, fII))
    return rows

def cmd_merge():
    import os
    segs = ["hard_1e6.csv", "hard_seg2.csv", "hard_seg3.csv",
            "hard_seg4.csv", "hard_seg5.csv", "hard_seg6.csv"]
    if not all(os.path.exists(s) for s in segs):
        print("segment files were removed in cleanup (git history @7a4e2b6 has them);")
        print("their verified union is the committed hard_1e7_full.csv — nothing to do")
        return
    out = []
    seen = set()
    for path in segs:
        rows = read_fp(path)
        for t in rows:
            assert t[0] not in seen, f"duplicate prime {t[0]}"
            seen.add(t[0])
        out += rows
    out.sort()
    # continuity check: consecutive p≡1(24) primes with no gaps at seams
    with open("hard_1e7_full.csv", "w") as f:
        f.write("p,ford,fI,fII\n")
        for p, ford, fI, fII in out:
            f.write(f"{p},{ford},{fI},{fII}\n")
    print(f"merged {len(out)} primes -> hard_1e7_full.csv  "
          f"(range {out[0][0]}..{out[-1][0]})")

def cmd_validate():
    ours = {p: (fI, fII) for p, _, fI, fII in read_fp("hard_1e7_full.csv")
            if p % 840 in SQ and p > 10**6}
    n = mism = 0
    with open("esc2025_fp_to_3.5e7.csv") as f:
        r = csv.reader(f); next(r)
        for row in r:
            p = int(row[0])
            if p in ours:
                n += 1
                if ours[p] != (int(row[2]), int(row[3])):
                    mism += 1
                    print(f"  MISMATCH p={p}: ours {ours[p]} vs ext ({row[2]},{row[3]})")
    print(f"validate vs external on (10^6,10^7]: {n} primes compared, {mism} mismatches")

def windows(rows, lo=2**11):
    w = lo
    while True:
        win = [t for t in rows if w <= t[0] < 2*w]
        if not win:
            if w > max(t[0] for t in rows): break
            w *= 2; continue
        yield w, win
        w *= 2

def cmd_law():
    rows = read_fp("hard_1e7_full.csv")
    # unordered count f = fI + fII
    rows = [(p, fI + fII, p % 840) for p, _, fI, fII in rows]
    # within p ≡ 1 (mod 24): 35 classes mod 840, of which 24 are units
    # (gcd(r,840)=1); the six square classes are 6 of those 24 → uniform 1/4
    print(f"full 1-mod-24 class to 10^7: {len(rows)} primes; "
          f"square-class share {sum(1 for r in rows if r[2] in SQ)/len(rows):.4f} "
          f"(uniform = 6/24 = {6/24:.4f})")
    print(f"{'win':>9} {'n':>7} {'minf':>6} {'argmin':>9} {'mod840':>7} {'sq?':>4} "
          f"{'med':>6} {'min/med':>8}")
    hits = tot = 0
    for w, win in windows(rows):
        mn = min(win, key=lambda t: t[1])
        med = statistics.median(t[1] for t in win)
        sq = mn[2] in SQ
        tot += 1; hits += sq
        print(f"{w:>9} {len(win):>7} {mn[1]:>6} {mn[0]:>9} {mn[2]:>7} "
              f"{'YES' if sq else 'NO':>4} {med:>6.0f} {mn[1]/med:>8.2f}")
    print(f"\nlaw: {hits}/{tot} window minima in the six square classes "
          f"(P_uniform = (1/4)^{tot} = {0.25**tot:.2e} if all hit)")
    # second-lowest analysis for the windows: are the bottom-5 also square-class?
    for w, win in windows(rows):
        bot = sorted(win, key=lambda t: t[1])[:5]
        share = sum(1 for t in bot if t[2] in SQ)
        print(f"  win 2^{int(math.log2(w))}: bottom-5 square-class share {share}/5")

def cmd_octave():
    rows = [(p, fI + fII, fI, fII, p % 840)
            for p, _, fI, fII in read_fp("hard_1e8_2e8.csv")]
    n = len(rows)
    zeros = [r for r in rows if r[1] == 0]
    zI = sum(1 for r in rows if r[2] == 0)
    zII = sum(1 for r in rows if r[3] == 0)
    print(f"[1e8,2e8] six square classes: {n} primes")
    print(f"ESC zero-free check: f=0 count = {len(zeros)} "
          f"{'*** COUNTEREXAMPLE CANDIDATE ***' if zeros else '(conjecture holds here)'}")
    print(f"  primes with fI=0: {zI}, with fII=0: {zII}")
    mn = min(rows, key=lambda t: t[1])
    print(f"octave minimum: f = {mn[1]} at p = {mn[0]} (≡ {mn[4]} mod 840, "
          f"fI={mn[2]}, fII={mn[3]})")
    print(f"§5 PREDICTION was min f ≈ 175–225 → "
          f"{'INSIDE' if 175 <= mn[1] <= 225 else 'OUTSIDE'} the band")
    bot = sorted(rows, key=lambda t: t[1])[:10]
    print("bottom 10:", [(t[0], t[1]) for t in bot])
    # per half-octave stats
    for lo, hi in [(10**8, int(1.414e8)), (int(1.414e8), 2*10**8)]:
        win = [t for t in rows if lo <= t[0] < hi]
        fs = [t[1] for t in win]
        lf = [math.log(v) for v in fs]
        mu, sd = statistics.mean(lf), statistics.pstdev(lf)
        med = statistics.median(fs)
        mnw = min(win, key=lambda t: t[1])
        # lognormal EV prediction for the window minimum
        import math as m
        N = len(win)
        z = m.sqrt(2*m.log(N)) - (m.log(m.log(N)) + m.log(4*m.pi))/(2*m.sqrt(2*m.log(N)))
        pred_min = m.exp(mu - z*sd)
        print(f"  [{lo:.3g},{hi:.3g}): n={N} med={med:.0f} mean(lnf)={mu:.3f} "
              f"sd(lnf)={sd:.3f} var/mean={statistics.pvariance(fs)/statistics.mean(fs):.2f} "
              f"min={mnw[1]}@{mnw[0]} lognormal-EV pred min≈{pred_min:.0f} "
              f"min/med={mnw[1]/med:.2f}")
    # effective exponents vs the 3.5e7 data: ln med / lnln p trend point
    med_all = statistics.median([t[1] for t in rows])
    p_mid = 1.5e8
    print(f"octave median {med_all:.0f}; effective exponent ln(med)/ln(ln p) = "
          f"{math.log(med_all)/math.log(math.log(p_mid)):.2f} (was ≈3.30 at 3.5e7)")

if __name__ == "__main__":
    {"merge": cmd_merge, "validate": cmd_validate,
     "law": cmd_law, "octave": cmd_octave}[sys.argv[1]]()
