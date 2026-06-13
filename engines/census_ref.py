#!/usr/bin/env python3
"""census_ref.py — Python reference for fsigned.c (same window dictionary that
verify_signed.py validates against the independent naive census).  Emits the
identical CSV so the C engine can be diffed column-for-column.
usage: python3 census_ref.py LO HI > ref.csv"""
import sys
from math import gcd

def factorize(m):
    f = {}; d = 2
    while d*d <= m:
        while m % d == 0: f[d] = f.get(d, 0) + 1; m //= d
        d += 1 if d == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f

def divisors_sq(f):
    ds = [1]
    for p, e in f.items():
        ds = [d * p**k for d in ds for k in range(2*e + 1)]
    return ds

def row(n):
    out = {k: 0 for k in ('f0','f0I','f0II','f1','f1I','f1II','f1III','f2','f2I','f2II')}
    fac_n = factorize(n); n2 = n*n
    for x in range(1, (3*n)//4 + 1):
        a = 4*x - n
        if a == 0: continue
        B = n*x; m = abs(a); dmin = 2*x*(2*x - n)
        fac = dict(fac_n)
        for p, e in factorize(x).items(): fac[p] = fac.get(p, 0) + e
        for d0 in divisors_sq(fac):
            for d in (d0, -d0):
                if (d + B) % m: continue
                slot2 = B + B*B // d
                if (B + d) % a or slot2 % a: continue
                y, z = (B + d)//a, slot2//a
                if y == 0 or z == 0: continue
                if x + y == 0 or x + z == 0 or y + z == 0: continue
                v = 0 if d0 % n else (1 if d0 % n2 else 2)
                if a > 0:
                    if 1 <= d <= B and d >= dmin:
                        assert v < 2; out['f0'] += 1; out['f0I' if v == 0 else 'f0II'] += 1
                    elif dmin <= d <= -1:
                        out['f1'] += 1; out[('f1I','f1II','f1III')[v]] += 1
                else:
                    if d <= dmin:
                        out['f1'] += 1; out[('f1I','f1II','f1III')[v]] += 1
                    elif 1 <= d <= B:
                        assert v < 2; out['f2'] += 1; out['f2I' if v == 0 else 'f2II'] += 1
    return out

if __name__ == "__main__":
    LO, HI = int(sys.argv[1]), int(sys.argv[2])
    cols = ('f0','f0I','f0II','f1','f1I','f1II','f1III','f2','f2I','f2II')
    print("n," + ",".join(cols))
    for n in range(max(2, LO), HI + 1):
        r = row(n)
        print(f"{n}," + ",".join(str(r[c]) for c in cols))
