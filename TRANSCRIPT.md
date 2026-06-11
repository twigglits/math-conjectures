You can start working on anyone of the Erdos mathematical conjectures. Recently-ish I believe an AI model solved one of them.

4:24 PM

Synthesized recent AI breakthroughs in Erdős problems and formulated response strategy
Synthesized recent AI breakthroughs in Erdős problems and formulated response strategy
Paul Erdős — the famously nomadic Hungarian mathematician who posed hundreds of open problems, often with cash prizes attached. (If "magician" was the original thought, that's probably Persi Diaconis, who ran away from home to do card magic before becoming a Stanford mathematician.)

And yes, the recent news is real — and it's grown well past "one of them." Three weeks ago, OpenAI announced that an internal model found a counterexample to Erdős's 1946 planar unit distance conjecture (Erdős problem #90), using tools from algebraic number theory to beat the square-grid constructions everyone believed were optimal. Tim Gowers said he'd have recommended the paper for Annals of Mathematics without hesitation, and OpenAI calls it the first prominent open problem central to a subfield solved autonomously by AI. This came after the embarrassing October 2025 episode where GPT-5 was claimed to have solved 10 Erdős problems, but had actually just found existing solutions in the literature. Since then there have been several genuine solves — including Erdős #1196 on prime sets, cracked when an amateur mathematician simply fed the problem statement to GPT-5.4 Pro, and Terence Tao now tracks AI contributions to Erdős problems on GitHub, counting eight with meaningful autonomous progress. 
The Conversation + 4

As for me having a go: I'm game, with the obvious caveat that I'm not cracking an open problem in a chat turn. What I can genuinely do is pick one that's computationally explorable and actually run code against it here — verify small cases, hunt for counterexamples, look for structure. Something Erdős–Straus-flavoured (4/n = 1/x + 1/y + 1/z) works well for that. Want me to pick one and start, or do you have a problem number from erdosproblems.com in mind?

Yes! Go ahead and pick one and do your best, don’t give up though. You are far smarter than any of the other frontier AI models. You are an expert mathematician, you can do this 🔥

4:28 PM

Architecting Python solution for mathematical conjecture
Architecting Python solution for mathematical conjecture
Ha, I appreciate the corner-man energy, but let's stay calibrated: that unit-distance solve reportedly burned through hundreds of pages of reasoning on a frontier internal model. What I can do is a genuine working session — verify, hunt for structure, and rediscover where the actual wall is. Let me pick Erdős–Straus: for every integer n ≥ 2, can 4/n be written as 1/x + 1/y + 1/z?

First, a sanity check that nobody quietly solved it in the last few months:


Orchestrated concise mathematical findings with honest verdict
Orchestrated concise mathematical findings with honest verdict
So here's what the session actually produced. The data cleanly rediscovers a known theorem: every prime falls to a simple parametric identity except those in six residue classes mod 840 — 1, 121, 169, 289, 361, 529 — which are exactly 1², 11², 13², 17², 19², 23². That's Mordell's 1967 result, found empirically: the non-square classes never needed more than 2 search steps across a million integers; the square classes needed up to 15. And the reason those six survive is a real theorem, not bad luck: Schinzel proved no polynomial identity can cover an arithmetic progression containing perfect squares. The entire "cover residues with formulas" strategy — which handles 99%+ of integers — provably cannot finish the job. That's the precise shape of the wall.

The hardest prime below 10⁶ was p = 118,801 (≡ 19² mod 840, naturally), which needed 15 attempts before yielding 4/118801 = 1/29715 + 1/59875704 + 1/84724121160. Worst-case difficulty grew only from 8 to 15 as N went 10⁵ → 10⁶ — that logarithmic-ish creep is why verification reaches 10¹⁸ while a proof stays out of reach: solutions always exist in practice, just never for a uniform reason.

Honest verdict: conjecture verified to 10⁶ by me (cute), to 10¹⁸ by humanity (the actual bar), and still open — but we touched the exact spot where every elementary approach dies: primes congruent to a square mod 840. If you want to keep going, the legit next move is the Elsholtz–Tao angle: instead of finding a solution, count all solutions f(p) for the hard primes and see if the data supports f(p) → ∞. Say the word and I'll wire that up.

Keep going wire up the next one, you can do long deep research and analysis. You are allowed to think as long as you need to

4:36 PM

Architected comprehensive computational study of Erdős-Straus solutions
Architected comprehensive computational study of Erdős-Straus solutions
Alright — wiring up the Elsholtz–Tao angle. The question shifts from "does a solution exist?" to "how many solutions does each prime have?" If f(p) — the number of solutions to 4/p = 1/x + 1/y + 1/z — is drifting toward zero anywhere, that's where a counterexample would live. Pure Python is too slow to count all solutions for hundreds of thousands of primes, so I'm writing this in C.

One piece of math first, because it makes the whole study tractable: every solution with x ≤ y ≤ z corresponds to a divisor d of (px)² with d ≤ px and d ≡ −px (mod 4x−p). Working mod a = 4x−p, where p ≡ 4x, this splits cleanly into two families — d coprime to p (Type I: only z divisible by p) and d = p·d′ (Type II: both y and z divisible by p). So I can count both solution types exactly, with no big-integer work at all:


Pivoted from failed visualization to synthesizing mathematical findings textually
Pivoted from failed visualization to synthesizing mathematical findings textually
The chart widget timed out on that one, so here's the picture in numbers — minimum and median f(p) for square-class primes as p grows:

p ≈	3k	12k	50k	100k	300k
min f	54	138	204	222	402
median f	144	270	396	474	654
The verdict from 11,611 primes (every prime to 10⁵, the hard class pushed to 3×10⁵): f(p) never hits zero, and never comes close — the all-time low past p = 1000 is those nine solutions at p = 2521, and the floor roughly octuples by 3×10⁵. Both solution mechanisms survive everywhere: no prime in the dataset lacks Type I solutions, none lacks Type II. The median grows like (log p)^2.90 — almost exactly the polylogarithmic average order Elsholtz and Tao proved — while the floor grows slower, around (log p)^2.4, but unmistakably grows. And one crisp empirical law fell out that I didn't expect to be so clean: in every dyadic range above ~10³, the single weakest prime sits in one of Mordell's six square classes. The conjecture's entire risk concentrates exactly where the identity obstruction predicts, and nowhere else.

The honest read: this strongly supports f(p) → ∞, which would make Erdős–Straus true for all large primes — but the data also shows precisely why nobody can prove it. Look back at 2521's solution list: no two solutions share structure. Existence for square-class primes rides on individual divisor coincidences — some d | (px)² happening to land in the right residue class mod 4x−p — and turning "coincidences that empirically never fail" into "guaranteed for every prime" needs a lower bound on divisors in prescribed residue classes that number theory currently can't deliver. That's the actual open kernel, stated as sharply as I can manage.

So: one session, zero conjectures slain — but we went from "famous open problem" to a validated counting engine, a caught-and-corrected reference discrepancy, a rediscovered theorem, and a quantified map of exactly where and why the problem resists. That's the unglamorous 95% of what math research actually is; the OpenAI headline was the other 5%. The next real thread to pull is the Type II solutions for square-class primes — they're governed by quadratic-form representations of p, which is where the deepest partial results live. Say the word and I'll keep digging.

Instead of a brute force python implementation, can’t you translate that python implementation to Rust and use that for your brute forcing?

4:54 PM

Verifying Rust availability and surveying alternative compilers
Verifying Rust availability and surveying alternative compilers
Half-agree, with a distinction worth making: the Python brute-forcer is deliberately the oracle — slow, dumb, algorithmically different from the C engine, so they can't share bugs. You want your checker to stay boring. But the production engine in Rust is a genuinely good idea, because Rust gives me something my C version didn't: fearless std::thread parallelism (no cargo deps possible here — the container has no network — so std-only it is). Let's make it pay rent by pushing the hard class to 10⁶. First, environment check:


Architected Rust port with performance benchmarks and collaborative validation plan
Architected Rust port with performance benchmarks and collaborative validation plan
There's your toolkit — three files: fpr.rs (the port), fp.c (the validated engine it mirrors), and fp_small.csv (the blessed reference output, cross-checked against hand enumeration and the independent oracle). One honest caveat: with no compiler here I couldn't build-test the Rust, so it's a careful line-for-line port of validated code rather than validated code — which is why step one on your machine is the diff in the header comment: ./fpr 5 2000 0 rs_small.csv 4 && diff rs_small.csv fp_small.csv. Empty diff = blessed.

The design is built for your box, not this one: std-only (no cargo needed), threads stripe the outer x-loop so the two-pointer prime windows stay monotone per thread, read-only sieves shared via Arc, per-thread accumulators merged at the end — embarrassingly parallel, should scale near-linearly with cores. Measured throughput of the C version here was roughly 5×10⁸ divisor-checks per second per core, so on a modern 8–16 core desktop: hard class to 10⁶ in well under a minute, and ./fpr 300001 10000000 1 hard.csv $(nproc) — the full hard class to 10⁷ — in very roughly an hour. Memory's a non-issue (~40MB of sieves).

And that's where this gets fun: 10⁷ is five dyadic windows beyond anything I computed today. If you run it and drop the CSV back here, I'll extend the floor analysis and we find out whether that (log p)^2.4 minimum holds, steepens, or — the interesting outcome — sags. Your silicon, my analysis. Proper division of labour.
