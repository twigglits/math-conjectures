// fp.c — count solutions of 4/p = 1/x + 1/y + 1/z for primes p
// Method: for x in (p/4, 3p/4], a = 4x-p, B = px (gcd(a,B)=1 for prime p>3).
// Solutions with this smallest denominator x <-> divisors d | B^2, d <= B,
// d ≡ -B (mod a), with y = (d+B)/a, z = (B^2/d + B)/a, plus filter y >= x
// i.e. d >= dmin = 2x(2x-p) when 2x > p.
// Since p ≡ 4x (mod a):  Type I (p ∤ d): d' | x^2 with d' ≡ -4x^2 (mod a)
//                        Type II (d = p d'): d' | x^2, d' <= x, d' ≡ -x (mod a)
// Ordered count: distinct triple -> 6, one equal pair -> 3 (x=y iff d==dmin>0; y=z iff d==B i.e. tier-II d'==x)
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
typedef long long ll;

int main(int argc, char** argv) {
    if (argc < 5) { fprintf(stderr, "usage: fp pmin pmax mode(0=all,1=only p%%24==1) out.csv\n"); return 1; }
    int pmin = atoi(argv[1]), pmax = atoi(argv[2]), mode = atoi(argv[3]);
    const char* out = argv[4];
    int XMAX = (int)((3LL * pmax) / 4) + 2;

    char* comp = calloc(pmax + 1, 1);
    for (ll i = 2; i * i <= pmax; i++)
        if (!comp[i]) for (ll j = i * i; j <= pmax; j += i) comp[j] = 1;

    int np = 0;
    for (int i = (pmin < 5 ? 5 : pmin); i <= pmax; i++)
        if (!comp[i] && (mode == 0 || i % 24 == 1)) np++;
    int* P = malloc(sizeof(int) * np);
    ll *ford = calloc(np, sizeof(ll)), *fI = calloc(np, sizeof(ll)), *fII = calloc(np, sizeof(ll));
    int k = 0;
    for (int i = (pmin < 5 ? 5 : pmin); i <= pmax; i++)
        if (!comp[i] && (mode == 0 || i % 24 == 1)) P[k++] = i;

    int* spf = calloc(XMAX + 1, sizeof(int));
    for (int i = 2; i <= XMAX; i++)
        if (!spf[i]) for (ll j = i; j <= XMAX; j += i) if (!spf[j]) spf[j] = i;

    ll* divs = malloc(sizeof(ll) * 60000);
    int lo = 0, hi = 0;
    clock_t t0 = clock();

    for (int x = 2; x <= XMAX; x++) {
        while (lo < np && 3LL * P[lo] < 4LL * x) lo++;     // need x <= 3p/4
        if (lo >= np) break;
        while (hi < np && (ll)P[hi] < 4LL * x) hi++;       // need x > p/4
        if (lo >= hi) continue;

        // divisors of x^2
        int nd = 1; divs[0] = 1;
        int t = x;
        while (t > 1) {
            int q = spf[t], e = 0;
            while (t % q == 0) { t /= q; e++; }
            int base = nd; ll pe = 1;
            for (int j = 1; j <= 2 * e; j++) {
                pe *= q;
                for (int i2 = 0; i2 < base; i2++) divs[nd++] = divs[i2] * pe;
            }
        }

        for (int ip = lo; ip < hi; ip++) {
            ll p = P[ip];
            ll a = 4LL * x - p;
            ll xm = (ll)x % a;
            ll r0 = (a - (4 * xm % a) * xm % a) % a;   // (-4x^2) mod a
            ll r1 = (a - xm) % a;                      // (-x)  mod a
            ll dmin = (2LL * x > p) ? 2LL * x * (2LL * x - p) : 0;
            ll c0 = 0, c1 = 0, n3 = 0;
            for (int i2 = 0; i2 < nd; i2++) {
                ll d = divs[i2], m = d % a;
                if (m == r0 && d >= dmin) {
                    c0++;
                    if (dmin > 0 && d == dmin) n3++;          // x == y
                }
                if (d <= (ll)x && m == r1 && p * d >= dmin) {
                    c1++;
                    if (d == (ll)x) n3++;                     // y == z
                    if (dmin > 0 && p * d == dmin) n3++;      // x == y (tier II)
                }
            }
            ford[ip] += 6 * (c0 + c1) - 3 * n3;
            fI[ip] += c0; fII[ip] += c1;
        }
    }

    FILE* f = fopen(out, "w");
    fprintf(f, "p,ford,fI,fII\n");
    for (int i = 0; i < np; i++) fprintf(f, "%d,%lld,%lld,%lld\n", P[i], ford[i], fI[i], fII[i]);
    fclose(f);
    fprintf(stderr, "primes=%d  time=%.1fs\n", np, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
