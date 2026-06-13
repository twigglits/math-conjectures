#!/usr/bin/env python3
"""
verify_signed.py — machine verification of every claim in REPORT.md §11
(the signed extension: Erdős–Straus over ℤ), exact arithmetic only.

Objects.  For n ∈ ℤ*, S(n) = multisets {x,y,z} ⊂ ℤ* with 1/x+1/y+1/z = 4/n,
EXCLUDING trivial triples (those containing a cancelling pair {t,−t}, which
exist iff 4 | n and form the unique infinite family).  Grade k = number of
negative members; f̃_k(n) = #{s ∈ S(n) : grade k}.  f̃₀ = the classical f.

Verified here:
  S1  the two-term solver (all signed {y,z} with 1/y+1/z = a/b) vs brute force
  S2  Theorem G (two terms suffice over ℤ*, ∀ n ≥ 2) and the exact
      complementary failure sets of the sum-form and difference-form
  S3  Lemma H (the signed kernel dictionary): the window table reproduces
      the naive census exactly, grade by grade, for all 2 ≤ n ≤ 200
  S4  Theorem J (mirror): f̃_k(−n) = f̃_{3−k}(n); F̃ is even on ℤ*
  S5  the explicit polynomial families (incl. the modulus-1 family) and the
      small-n exceptional set {2,4}
  S6  signed greedy: ≤ 3 terms for 4/n always; ≤ ⌊log₂k⌋+1 terms for k/n
  S7  Lemma K (chirality of the square obstruction): at n = c² the positive
      pure strata are empty (Lemma D) while signed solutions exist in
      coprime rows — incl. the proved Type III family — and the Jacobi sign
      that kills the positive window MATCHES on the negative window
  S8  anchors: f̃₀(1009) = 19, f̃₀(2521) = 9 through the new dictionary;
      graded counts at the record prime
  S9  the |n| ≤ 12 tapestry table (for §11.6) printed from the naive census
"""
import sys, random
from math import gcd
from fractions import Fraction

ok_count = 0
def check(cond, msg):
    global ok_count
    if not cond:
        print(f"FAIL: {msg}"); sys.exit(1)
    ok_count += 1

def is_prime(n):
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % q == 0: return n == q
    d, s = n-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def factorize(m):
    """prime → exponent, trial division (m ≤ ~10^7 here)."""
    f = {}
    d = 2
    while d*d <= m:
        while m % d == 0:
            f[d] = f.get(d, 0) + 1; m //= d
        d += 1 if d == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f

def merge(f1, f2):
    f = dict(f1)
    for p, e in f2.items(): f[p] = f.get(p, 0) + e
    return f

def divisors_from(f):
    ds = [1]
    for p, e in f.items():
        ds = [d * p**k for d in ds for k in range(e+1)]
    return ds

def divisors_sq(f):
    """divisors of m² given factorization of m"""
    return divisors_from({p: 2*e for p, e in f.items()})

def jacobi(a, n):
    a %= n; result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3,5): result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: result = -result
        a %= n
    return result if n == 1 else 0

# ---------------- S1: the signed two-term solver ----------------
# All integer solutions of 1/y + 1/z = a/b (gcd(a,b)=1, b>0, a≠0) are
# (ay−b)(az−b) = b²: d = ay−b runs over divisors of b² (both signs, d ≠ −b),
# y = (b+d)/a, z = (b+b²/d)/a, the congruence d ≡ −b (mod a) ⇔ integrality.
def two_term_all(a, b):
    if a < 0:
        return {tuple(sorted((-y, -z))) for (y, z) in two_term_all(-a, b)}
    sols = set()
    for d0 in divisors_sq(factorize(b)):
        for d in (d0, -d0):
            if d == -b: continue
            if (d + b) % a: continue
            y = (b + d) // a
            z = (b + b*b // d) // a
            check((b + b*b // d) % a == 0, f"partner integrality a={a} b={b} d={d}")
            if y and z: sols.add(tuple(sorted((y, z))))
    return sols

def two_term_brute(a, b):
    """independent: |1/y| ≥ a/(2b) for one slot ⇒ |y| ≤ 2b/a; solve z exactly."""
    sols = set()
    for y in range(-(2*b)//a - 2, (2*b)//a + 3):
        if y == 0: continue
        r = Fraction(a, b) - Fraction(1, y)
        if r == 0: continue
        if r.numerator in (1, -1):
            z = r.denominator * r.numerator
            sols.add(tuple(sorted((y, z))))
    return sols

print("S1: two-term solver vs brute force ...")
for a in range(1, 13):
    for b in range(1, 61):
        if gcd(a, b) != 1: continue
        check(two_term_all(a, b) == two_term_brute(a, b), f"two-term a={a} b={b}")
        check(two_term_all(-a, b) == {tuple(sorted((-y,-z))) for (y,z) in two_term_brute(a,b)},
              f"two-term negation a={a} b={b}")
print(f"  ok on {sum(1 for a in range(1,13) for b in range(1,61) if gcd(a,b)==1)} targets, both signs")

# ---------------- S2: two terms always suffice over ℤ* ----------------
# Sum-form  4/n = 1/x+1/y, x,y>0  ⇔ ∃ d | n², d ≡ −n (mod 4)
#   fails exactly on A = {n odd, n ≡ 1 (mod 4), all prime factors ≡ 1 (mod 4)}
# Diff-form 4/n = 1/x−1/y, x,y>0  ⇔ ∃ u | n², u ≡ n (mod 4), 0 < u < n
#   fails exactly on B = {2, 4} ∪ {primes ≡ 3 (mod 4)}
# A ∩ B = ∅, so over ℤ* two unit fractions ALWAYS suffice for 4/n, n ≥ 2.
print("S2: 2-term classifications + complementarity (n ≤ 2000) ...")
for n in range(2, 2001):
    sols = two_term_all(*Fraction(4, n).as_integer_ratio())
    has_sum  = any(y > 0 and z > 0 for (y, z) in sols)
    has_diff = any(y * z < 0 for (y, z) in sols)
    fac = factorize(n)
    in_A = (n % 4 == 1) and all(p % 4 == 1 for p in fac)
    in_B = n in (2, 4) or (is_prime(n) and n % 4 == 3)
    check(has_sum  == (not in_A), f"sum-form classification n={n}")
    check(has_diff == (not in_B), f"diff-form classification n={n}")
    check(not (in_A and in_B), f"failure sets must be disjoint n={n}")
    check(has_sum or has_diff, f"two terms must suffice over ℤ*: n={n}")
    # divisor-criterion forms of both classifications
    check(has_sum  == any(d % 4 == (-n) % 4 for d in divisors_sq(fac)), f"sum criterion n={n}")
    check(has_diff == any(u % 4 == n % 4 and u < n for u in divisors_sq(fac)), f"diff criterion n={n}")
print("  ok: failure sets are exactly A and B, disjoint; 2 signed terms always suffice")

print("S2b: the mod-4 duality at primes (p ≤ 2000) + explicit witnesses to 10⁶ ...")
for p in [p for p in range(3, 2001) if is_prime(p)]:
    sols = two_term_all(4, p)
    has_sum  = any(y > 0 and z > 0 for (y, z) in sols)
    has_diff = any(y * z < 0 for (y, z) in sols)
    if p % 4 == 1: check((not has_sum) and has_diff, f"duality p={p} ≡ 1 (4)")
    else:          check(has_sum and (not has_diff), f"duality p={p} ≡ 3 (4)")
# witnesses: u=1 family (n ≡ 1 mod 4):  4/n = 1/((n−1)/4) − 1/(n(n−1)/4)
#            d=1 family (n ≡ 3 mod 4):  4/n = 1/((n+1)/4) + 1/(n(n+1)/4)
wit = 0
for n in list(range(5, 10001)) + [random.Random(7).randrange(5, 10**6) for _ in range(2000)]:
    if n % 4 == 1:
        x, y = (n-1)//4, n*(n-1)//4
        check(Fraction(1,x) - Fraction(1,y) == Fraction(4,n), f"u=1 witness n={n}"); wit += 1
    if n % 4 == 3:
        x, y = (n+1)//4, n*(n+1)//4
        check(Fraction(1,x) + Fraction(1,y) == Fraction(4,n), f"d=1 witness n={n}"); wit += 1
print(f"  ok: duality on all primes ≤ 2000; {wit} explicit 2-term witnesses to 10⁶")

# ---------------- the naive graded census (independent method) ----------------
def census_naive(n):
    """grade → set of sorted triples; trivial triples excluded; works for n<0.
    Every solution has a member with |t| ≤ 3|n|/4 (since 4/|n| ≤ 3·max|1/t|)."""
    grades = {0: set(), 1: set(), 2: set(), 3: set()}
    trivial_seen = False
    N = abs(n)
    for t in range(-(3*N)//4 - 1, (3*N)//4 + 2):
        if t == 0: continue
        num, den = 4*t - n, n*t          # 4/n − 1/t = (4t−n)/(nt)
        if num == 0:
            trivial_seen = True          # remaining pair must cancel: trivial family
            continue
        g = gcd(abs(num), abs(den)); a, b = num//g, den//g
        if b < 0: a, b = -a, -b
        for (y, z) in two_term_all(a, b):
            tri = tuple(sorted((t, y, z)))
            if any(tri[i] + tri[j] == 0 for i in range(3) for j in range(i+1, 3)):
                trivial_seen = True; continue
            grades[sum(1 for v in tri if v < 0)].add(tri)
    return grades, trivial_seen

# ---------------- Lemma H: the signed kernel dictionary ----------------
def census_dict(n):
    """The §11.3 window dictionary, n ≥ 2.  x = least positive denominator
    (k ∈ {0,1}) or the unique positive one (k = 2);  B = nx;  all solutions
    correspond to divisors d of B² in the class d ≡ −B (mod |4x−n|), graded
    purely by which window d lies in:
       k=0:  n/4 < x ≤ 3n/4,  max(1, dmin) ≤ d ≤ B
       k=1:  n/4 < x ≤ n/2,   dmin ≤ d ≤ −1          (negative window, a > 0)
       k=1:  1 ≤ x < n/4,     d ≤ dmin (< −B)        (negative window, a < 0)
       k=2:  1 ≤ x < n/4,     1 ≤ d ≤ B              (positive window, a < 0)
    with dmin = 2x(2x−n) and (y,z)-slots ((B+d)/a, (B+B²/d)/a), a = 4x−n."""
    grades = {0: set(), 1: set(), 2: set(), 3: set()}
    fac_n = factorize(n)
    for x in range(1, (3*n)//4 + 1):
        a = 4*x - n
        if a == 0: continue              # the trivial-family row (4 | n)
        B = n*x
        m = abs(a)
        dmin = 2*x*(2*x - n)
        for d0 in divisors_sq(merge(fac_n, factorize(x))):
            for d in (d0, -d0):
                if (d + B) % m: continue
                slot2 = B + B*B // d
                y, z = (B + d) // a, slot2 // a
                if (B + d) % a or slot2 % a: continue   # (a<0 floor-div guard; exact only)
                if y == 0 or z == 0: continue
                if x + y == 0 or x + z == 0 or y + z == 0: continue  # trivial (4|n only)
                if a > 0:
                    if 1 <= d <= B and d >= dmin:        grades[0].add(tuple(sorted((x, y, z))))
                    elif dmin <= d <= -1:                grades[1].add(tuple(sorted((x, y, z))))
                else:
                    if d <= dmin:                        grades[1].add(tuple(sorted((x, y, z))))
                    elif 1 <= d <= B:                    grades[2].add(tuple(sorted((x, y, z))))
    return grades

print("S3: dictionary census ≡ naive census, grade by grade (2 ≤ n ≤ 200) ...")
for n in range(2, 201):
    gn, triv = census_naive(n)
    gd = census_dict(n)
    for k in range(4):
        check(gn[k] == gd[k], f"dictionary mismatch n={n} grade {k}: "
                              f"naive {len(gn[k])} vs dict {len(gd[k])}")
    check(not gn[3], f"grade 3 must be empty for n>0: n={n}")
    check(triv == (n % 4 == 0), f"trivial family ⇔ 4|n: n={n}")
    for k in range(3):                       # sanity: every triple is a solution
        for tri in gn[k]:
            check(sum(Fraction(1, v) for v in tri) == Fraction(4, n), f"identity n={n} {tri}")
print("  ok: 199 values of n, all grades — the window table IS the signed solution set")

# ---------------- Theorem J: the mirror ----------------
print("S4: Theorem J (mirror) f̃_k(−n) = f̃_{3−k}(n) (2 ≤ n ≤ 80) ...")
for n in range(2, 81):
    gp, tp = census_naive(n)
    gm, tm = census_naive(-n)
    for k in range(4):
        check({tuple(sorted(-v for v in tri)) for tri in gp[k]} == gm[3-k],
              f"mirror n={n} grade {k}")
    check(tp == tm, f"trivial mirror n={n}")
    check(sum(len(gp[k]) for k in range(4)) == sum(len(gm[k]) for k in range(4)),
          f"F̃ evenness n={n}")
print("  ok: negation is a grade-flipping bijection; F̃(−n) = F̃(n)")

# ---------------- S5: explicit families; the exceptional set ----------------
print("S5: polynomial families for f̃₁ ≥ 1 and the exceptional set {2,4} ...")
def assert_signed(n, tri, k):
    check(sum(Fraction(1, v) for v in tri) == Fraction(4, n), f"family identity n={n} {tri}")
    check(all(v != 0 for v in tri) and sum(1 for v in tri if v < 0) == k, f"family grade n={n}")
    check(not any(a + b == 0 for a in tri for b in tri), f"family nontrivial n={n}")
fam = 0
for n in list(range(5, 5001)) + [random.Random(11).randrange(5, 10**6) for _ in range(2000)]:
    if n % 2 == 1:   # Jaroma (2004) / Wikipedia: one identity for ALL odd n
        assert_signed(n, ((n-1)//2, (n+1)//2, -(n*(n-1)*(n+1))//4), 1); fam += 1
    if n % 4 == 1:
        x = (n - 1)//4; B = n*x
        assert_signed(n, (x, B*B - B, -(B - 1)), 1)            # the modulus-1 family
        x2 = (n - 1)//2
        assert_signed(n, (x2, x2, -(n*(n-1))//4), 1); fam += 2 # the doubled family
    elif n % 4 == 3 and n >= 7:
        x = (n + 1)//4; y = n*(n + 1)//4                        # twist of the d=1 family
        assert_signed(n, (x - 1, y, -x*(x - 1)), 1); fam += 1
    elif n % 4 == 2 and n >= 6:
        x = (n + 2)//4; y = (n*(n + 2))//8                      # sum-form: 4/n = 1/x + 1/y
        check(Fraction(1,x) + Fraction(1,y) == Fraction(4,n), f"even sum-form n={n}")
        assert_signed(n, (x - 1, y, -x*(x - 1)), 1); fam += 1
    elif n % 4 == 0 and n >= 8:
        x = n//2
        assert_signed(n, (x - 1, x, -x*(x - 1)), 1); fam += 1
check(fam >= 7000, "family coverage")
g3, _ = census_naive(3); check(len(g3[1]) >= 1, "f̃₁(3) ≥ 1")            # {1,2,−6}
for n in (2, 4):
    g, _ = census_naive(n)
    check(len(g[1]) == 0 and len(g[2]) == 0, f"f̃₁({n}) = f̃₂({n}) = 0")
print(f"  ok: {fam} family instances to 10⁶; f̃₁(n) ≥ 1 ∀ n ≥ 3 except exactly n ∈ {{2,4}}")

# ---------------- S6: the signed greedy ----------------
def greedy_signed(k, n):
    """nearest-integer greedy for k/n, returns list of signed unit fractions."""
    out, r = [], Fraction(k, n)
    while r != 0:
        if r.numerator in (1, -1):
            out.append(r.denominator * r.numerator); break
        x = round(Fraction(r.denominator, r.numerator))
        if x == 0: x = 1 if r > 0 else -1
        out.append(x)
        r -= Fraction(1, x)
    check(sum(Fraction(1, t) for t in out) == Fraction(k, n), f"greedy exact {k}/{n}")
    return out

print("S6: signed greedy — ≤3 terms for 4/n; ≤ ⌊log₂k⌋+1 terms for k/n ...")
for n in range(2, 10001):
    check(len(greedy_signed(4, n)) <= 3, f"greedy 4/{n} needs >3 terms")
import math as _m
for k in range(1, 65):
    for n in range(max(2, (k + 1)//2), 401):   # natural domain n ≥ k/2 (value ≤ 2)
        check(len(greedy_signed(k, n)) <= _m.floor(_m.log2(k)) + 1, f"greedy {k}/{n}")
print("  ok: the whole Schinzel k/n family collapses to ⌊log₂k⌋+1 terms over ℤ* (n ≥ k/2)")

# ---------------- S7: Lemma K — the square obstruction is chiral ----------------
print("S7: Lemma K — chirality at odd squares n = c² (c = 3..15) ...")
for c in range(3, 16, 2):
    n = c*c
    fac_n = factorize(n)
    pos_pure = 0      # Lemma D objects: coprime-row positive-window pure strata
    neg_coprime = 0   # signed-window solutions in coprime rows (any stratum)
    exhibit = None
    for x in range(1, (3*n)//4 + 1):
        a = 4*x - n
        if a == 0 or gcd(abs(a), n*x) != 1: continue
        B = n*x; m = abs(a); dmin = 2*x*(2*x - n)
        for d0 in divisors_sq(merge(fac_n, factorize(x))):
            for d in (d0, -d0):
                if (d + B) % m: continue
                if d == -B: continue
                y, z = (B + d)//a, (B + B*B//d)//a
                if (B + d) % a or (B + B*B//d) % a or y == 0 or z == 0: continue
                if a > 0 and 1 <= d <= B and d >= dmin:
                    if gcd(d, n*n) in (1, n):  # pure Type I / Type II shapes
                        pos_pure += 1
                elif (a > 0 and dmin <= d <= -1) or (a < 0 and d <= dmin):
                    neg_coprime += 1
                    if exhibit is None: exhibit = (x, y, z)
    check(pos_pure == 0, f"Lemma D re-derived: positive pure strata at n={n}")
    check(neg_coprime > 0, f"Lemma K: signed coprime-row solutions must exist at n={n}")
    x = (n - 1)//4; B = n*x
    assert_signed(n, (x, B*B - B, -(B - 1)), 1)   # the proved Type III family at squares
    print(f"  n={n:4d}: positive coprime strata EMPTY (Lemma D) — "
          f"signed coprime-row solutions: {neg_coprime:4d}, e.g. {exhibit}")
# the Jacobi sign: required class-sign for the positive window is −1 but every
# positive d | x² forces +1 (Lemma D); for d < 0 the SAME computation forces
# (d/a) = (−1/a)(|d|/a) = −1 — matching, so the obstruction vanishes. Random check:
rng = random.Random(99)
checked = 0
while checked < 3000:
    c = rng.randrange(1, 150)*2 + 1; n = c*c
    x = rng.randrange(1, (3*n)//4 + 1)
    a = 4*x - n
    if a <= 0 or gcd(a, 2*n*x) != 1: continue
    e = rng.choice(divisors_sq(factorize(x)))
    if gcd(e, a) != 1: continue
    check(jacobi((-4*x*x) % a, a) == -1, f"required sign c={c} x={x}")     # class sign
    check(jacobi(e % a, a) == 1, f"positive-window sign e={e} a={a}")      # Lemma D fact
    check(jacobi((-e) % a, a) == -1, f"negative-window sign e={e} a={a}")  # the chirality
    checked += 1
print(f"  ok: {checked} Jacobi instances — required −1; forced +1 for d>0, −1 for d<0")

# ---------------- S8: anchors against the validated engine/data ----------------
print("S8: f̃₀ anchors through the dictionary (1009, 2521) + graded records ...")
g1009 = census_dict(1009); g2521 = census_dict(2521)
check(len(g1009[0]) == 19, f"f(1009) = 19, got {len(g1009[0])}")
check(len(g2521[0]) == 9,  f"f(2521) = 9, got {len(g2521[0])}")
def type_split(n, k):
    """grade-k strata by v = ν_n(|d|) of the DESIGNATED window divisor —
    direct re-enumeration (same windows as census_dict), not reconstruction."""
    out = {0: 0, 1: 0, 2: 0}
    fac_n = factorize(n)
    for x in range(1, (3*n)//4 + 1):
        a = 4*x - n
        if a == 0: continue
        B = n*x; m = abs(a); dmin = 2*x*(2*x - n)
        for d0 in divisors_sq(merge(fac_n, factorize(x))):
            for d in (d0, -d0):
                if (d + B) % m: continue
                slot2 = B + B*B // d
                if (B + d) % a or slot2 % a: continue
                if (B + d)//a == 0 or slot2//a == 0: continue
                if a > 0:
                    grade = 0 if (1 <= d <= B and d >= dmin) else (1 if dmin <= d <= -1 else None)
                else:
                    grade = 1 if d <= dmin else (2 if 1 <= d <= B else None)
                if grade != k: continue
                v = 0 if d0 % n else (1 if d0 % (n*n) else 2)
                out[v] += 1
    return out
print(f"  f̃(2521) = (f₀,f₁,f₂) = ({len(g2521[0])}, {len(g2521[1])}, {len(g2521[2])})"
      f"   [record-low prime: f₀ = 9]")
print(f"  f̃(1009) = (f₀,f₁,f₂) = ({len(g1009[0])}, {len(g1009[1])}, {len(g1009[2])})")
s0, s1 = type_split(2521, 0), type_split(2521, 1)
check(s0 == {0: 6, 1: 3, 2: 0}, f"f₀(2521) strata 6+3 (REPORT §2), got {s0}")
check(s1[2] > 0, "Type III stratum must be populated in f̃₁(2521)")
check(sum(s1.values()) == len(g2521[1]), "f̃₁(2521) strata sum")
print(f"  Type strata of f̃₁(2521) (v = ν_p|d|): I(v=0)={s1[0]}, II(v=1)={s1[1]}, "
      f"III(v=2)={s1[2]} — Type III is impossible in the positive world")

# ---------------- S9: the tapestry (for §11.6) ----------------
print("\nS9: the graded tapestry over ℤ (trivial family excluded):")
print("    n :  f̃₀  f̃₁  f̃₂  f̃₃   F̃")
for n in list(range(-12, 0)) + list(range(2, 13)):
    if n in (-1, 0, 1): continue
    g, triv = census_naive(n)
    F = sum(len(g[k]) for k in range(4))
    star = " (+∞ trivial)" if triv else ""
    print(f"  {n:4d}:  {len(g[0]):3d} {len(g[1]):4d} {len(g[2]):4d} {len(g[3]):4d} {F:4d}{star}")

print(f"\nALL CHECKS PASSED ({ok_count} assertions)")
