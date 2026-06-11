#!/usr/bin/env python3
"""Final 10^7 analysis: merge segments, cross-validate, concentration law, exponents.
Self-contained stdlib-only. Run from files/ directory."""
import csv, glob, math, os, sys, collections

SQ = {1, 121, 169, 289, 361, 529}

def load_ours():
    rows = {}
    for fn in ['hard_1e6.csv'] + sorted(glob.glob('hard_seg*.csv')):
        if not os.path.exists(fn): continue
        with open(fn) as f:
            for r in csv.DictReader(f):
                p = int(r['p'])
                rows[p] = (int(r['ford']), int(r['fI']), int(r['fII']))
    ps = sorted(rows)
    print(f'[merge] {len(ps)} primes from {ps[0]} to {ps[-1]}')
    return ps, rows

def cross_validate(ps, rows):
    theirs = {}
    with open('esc2025_fp_to_3.5e7.csv') as f:
        for r in csv.DictReader(f):
            theirs[int(r['Prime'])] = (int(r['Type-1']), int(r['Type-2']))
    bad = gaps = n = 0
    pmax = ps[-1]
    for p, (t1, t2) in theirs.items():
        if p > pmax: continue
        if p not in rows:
            gaps += 1; continue
        n += 1
        if (rows[p][1], rows[p][2]) != (t1, t2): bad += 1
    print(f'[xval] vs ESC2025: {n} primes compared, {bad} mismatches, {gaps} coverage gaps')
    return bad == 0 and gaps == 0

def analysis(ps, rows):
    win = collections.defaultdict(list)
    for p in ps:
        win[int(math.log2(p))].append(p)
    print('\nwin        n(all) | min f  at p        class sq? | min f(covered cls) | bottom-10 sq')
    botsq_tot = bot_tot = 0
    for w in sorted(win):
        lst = win[w]
        if len(lst) < 40: continue
        T = lambda p: rows[p][1] + rows[p][2]          # unordered total
        srt = sorted(lst, key=T)
        pm = srt[0]
        sq = pm % 840 in SQ
        cov = [p for p in lst if p % 840 not in SQ]
        mincov = min((T(p) for p in cov), default=-1)
        bot = srt[:10]
        bsq = sum(1 for p in bot if p % 840 in SQ)
        botsq_tot += bsq; bot_tot += len(bot)
        print(f'2^{w:<3} {len(lst):>7} | {T(pm):>5}  {pm:>10} {pm%840:>5} {"Y" if sq else "N":>3} | {mincov:>14}     | {bsq}/10')
    # population share: square classes are 6 of 24 classes ≡1 mod 24
    nsq = sum(1 for p in ps if p % 840 in SQ)
    print(f'\n[concentration] square-class population share: {nsq/len(ps):.1%} (expect ~25%)')
    print(f'[concentration] square-class share of bottom-10s: {botsq_tot}/{bot_tot} = {botsq_tot/max(bot_tot,1):.1%}')

    # exponent fits on dyadic minima and medians (own data)
    def fit(pairs):
        xs = [math.log(math.log(p)) for p, _ in pairs]; ys = [math.log(v) for _, v in pairs]
        n = len(xs); sx, sy = sum(xs), sum(ys)
        sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
        a = (n*sxy - sx*sy)/(n*sxx - sx*sx)
        return a
    minp, medp = [], []
    for w in sorted(win):
        lst = win[w]
        if len(lst) < 40 or 2**w < 2000: continue
        T = lambda p: rows[p][1] + rows[p][2]
        srt = sorted(T(p) for p in lst)
        pm = min(lst, key=T)
        minp.append((pm, srt[0])); medp.append((int(2**w*1.5), srt[len(srt)//2]))
    if len(minp) > 3:
        print(f'[exponents] min f ~ (ln p)^{fit(minp):.2f}   median ~ (ln p)^{fit(medp):.2f}')

    # record sequence
    print('[records] new all-time lows for p>1000 (full 1mod24 class):')
    best = 10**9
    for p in ps:
        if p < 1000: continue
        t = rows[p][1] + rows[p][2]
        if t < best:
            best = t
            print(f'   p={p:<9} f={t:<4} class={p%840}{" SQUARE" if p%840 in SQ else ""}')

if __name__ == '__main__':
    ps, rows = load_ours()
    ok = cross_validate(ps, rows)
    analysis(ps, rows)
    print('\nXVAL_' + ('OK' if ok else 'FAILED'))
