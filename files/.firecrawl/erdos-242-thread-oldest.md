[![Logo](https://www.erdosproblems.com/static/EPLogo.png)](https://www.erdosproblems.com/)

[Forum](https://www.erdosproblems.com/forum) [Inbox](https://www.erdosproblems.com/dm) [Favourites](https://www.erdosproblems.com/favourites) [Tags](https://www.erdosproblems.com/tags)

More

[FAQ](https://www.erdosproblems.com/faq) [Prizes](https://www.erdosproblems.com/prizes) [Problem Lists](https://www.erdosproblems.com/lists) [Definitions](https://www.erdosproblems.com/definitions) [Links](https://www.erdosproblems.com/links)

[Forum](https://www.erdosproblems.com/forum)

Menu

[Inbox](https://www.erdosproblems.com/dm) [Favourites](https://www.erdosproblems.com/favourites) [Tags](https://www.erdosproblems.com/tags) [FAQ](https://www.erdosproblems.com/faq) [Prizes](https://www.erdosproblems.com/prizes) [Problem Lists](https://www.erdosproblems.com/lists) [Definitions](https://www.erdosproblems.com/definitions) [Links](https://www.erdosproblems.com/links)

Go

Go

[Dual View](https://www.erdosproblems.com/forum/thread/242?order=oldest#) [Random Solved](https://www.erdosproblems.com/random_solved) [Random Open](https://www.erdosproblems.com/random_open)

FALSIFIABLE

Open, but could be disproved with a finite counterexample.


For every 𝑛>2 there exist distinct integers 1≤𝑥<𝑦<𝑧 such that4𝑛=1𝑥+1𝑦+1𝑧.

[#242](https://www.erdosproblems.com/242): [\[Er50c\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) [\[Er61\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) [\[Er79\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) [\[ErGr80\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) [\[Va99,1.13\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242)

[number theory](https://www.erdosproblems.com/tags/number%20theory) \|

[unit fractions](https://www.erdosproblems.com/tags/unit%20fractions)


The open status of this problem reflects the current belief of the owner of this website. There may be literature on this problem that I am unaware of, which may partially or completely solve the stated problem. Please do your own literature search before expending significant effort on solving this problem. If you find any relevant literature not mentioned here, please add this in a comment.


Comment activity that has not yet been incorporated into the remarks

NonePartialSolution

There are no solutions, partial or complete, claimed in the comments.




The [Erdős-Straus conjecture](https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Straus_conjecture). Perhaps the first place it appears in the literature is in a paper of Obláth [\[Ob50\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) (submitted in 1948), which describes it as a conjecture of Erdős.

The existence of a representation of 4/𝑛 as the sum of at most four distinct unit fractions follows trivially from a greedy algorithm.

Schinzel conjectured (see [\[Si56\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242)) the generalisation that, for any fixed 𝑎, if 𝑛 is sufficiently large in terms of 𝑎 then there exist distinct integers 1≤𝑥<𝑦<𝑧 such that𝑎𝑛=1𝑥+1𝑦+1𝑧.When 𝑎=5 this conjecture is due to Sierpiński [\[Si56\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242). For more background and results on this generalisation see Pomerance and Weingartner [\[PoWe25\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242).

It suffices to prove this when 𝑛 is prime. This has been verified for all 𝑛≤1018 [\[MiDu25\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242).

There are many partial results, some of which are listed below.

- Obláth [\[Ob50\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) noted it is true if 𝑛+1 is divisible by a prime ≡3⁢(mod⁡4). This implies almost all 𝑛 have the required decomposition.
- Arguing via parametric solutions, Mordell [\[Mo69\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) proved it is true for all 𝑛 except those congruent to one of {1,121,169,289,361,529} modulo 840.
- Terzi [\[Te71\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) extended this to prove that it is true for all 𝑛 except those congruent to one of 198 possible bad congruences modulo 120120.
- Vaughan [\[Va70\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) proved that the number of exceptions in \[1,𝑥\] is≤𝑥⁢exp⁡(−𝑐⁢(log⁡𝑥)2/3)for some constant 𝑐>0.
- This conjecture is equivalent (see Theorem 1 of [\[BlEl22\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242)) to the statement that, for any prime 𝑝, there exist integers 𝑎,𝑐,𝑑≥1 such that either 𝑝≡−𝑎/𝑐⁢(mod⁡4⁢𝑎⁢𝑐⁢𝑑−1) or 𝑝≡−4⁢𝑐2⁢𝑑+1𝑘⁢(mod⁡4⁢𝑐⁢𝑑) for some 𝑘∣4⁢𝑐2⁢𝑑+1.
- Bright and Loughran [\[BrLo20\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) have shown there is no Brauer-Manin obstruction to the existence of solutions.
- If 𝑓⁡(𝑛) counts the number of solutions then Elsholtz and Tao [\[ElTa13\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) have proved∑𝑝≤𝑁𝑓⁡(𝑝)=𝑁⁢(log⁡𝑁)2+𝑜⁡(1)and 𝑓⁡(𝑝)≤𝑝3/5+𝑜⁡(1) for all primes 𝑝.
- Elsholtz and Planitzer [\[ElPl20\]](https://www.erdosproblems.com/forum/thread/242?order=oldest#bib-container242) have proved that for almost all 𝑛𝑓⁡(𝑛)≥(log⁡𝑛)log⁡6+𝑜⁡(1).

[View the LaTeX source](https://www.erdosproblems.com/latex/242)


This page was last edited 07 May 2026. [View history](https://www.erdosproblems.com/history/242)

External data from [the database](https://github.com/teorth/erdosproblems) \- you can help update this



Formalised statement?

[Yes](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/242.lean)

Related OEIS sequences:



[A073101](https://oeis.org/A073101) [A075245](https://oeis.org/A075245) [A075246](https://oeis.org/A075246) [A075247](https://oeis.org/A075247) [A075248](https://oeis.org/A075248) [A287116](https://oeis.org/A287116)

[18 comments on this problem](https://www.erdosproblems.com/forum/discuss/242)

|     |     |
| --- | --- |
| **Likes this problem** | [old-bielefelder](https://www.erdosproblems.com/forum/user/old-bielefelder), <br> <br> [jgold](https://www.erdosproblems.com/forum/user/jgold), <br> <br> [TFBloom](https://www.erdosproblems.com/forum/user/TFBloom), <br> <br> [jbbaehr22](https://www.erdosproblems.com/forum/user/jbbaehr22), <br> <br> [Dogmachine](https://www.erdosproblems.com/forum/user/Dogmachine) |
| **Interested in collaborating** | [jgold](https://www.erdosproblems.com/forum/user/jgold), <br> <br> [Bradford](https://www.erdosproblems.com/forum/user/Bradford), <br> <br> [auro](https://www.erdosproblems.com/forum/user/auro) |
| **Currently working on this problem** | [jgold](https://www.erdosproblems.com/forum/user/jgold), <br> <br> [alansbor](https://www.erdosproblems.com/forum/user/alansbor), <br> <br> [Bradford](https://www.erdosproblems.com/forum/user/Bradford), <br> <br> [auro](https://www.erdosproblems.com/forum/user/auro) |
| **This problem looks difficult** | [Vjeko\_Kovac](https://www.erdosproblems.com/forum/user/Vjeko_Kovac), <br> <br> [TFBloom](https://www.erdosproblems.com/forum/user/TFBloom), <br> <br> [TerenceTao](https://www.erdosproblems.com/forum/user/TerenceTao) |
| **This problem looks tractable** | [auro](https://www.erdosproblems.com/forum/user/auro), <br> <br> [jbbaehr22](https://www.erdosproblems.com/forum/user/jbbaehr22) |
| **The results on this problem could be formalisable** | [jbbaehr22](https://www.erdosproblems.com/forum/user/jbbaehr22) |
| **I am working on formalising the results on this problem** | [jbbaehr22](https://www.erdosproblems.com/forum/user/jbbaehr22), <br> <br> [auro](https://www.erdosproblems.com/forum/user/auro) |

**Additional thanks to**: Alfaiz and Bryce Orloski


When referring to this problem, please use the original sources of Erdős. If you wish to acknowledge this website, the recommended citation format is:

T. F. Bloom, Erdős Problem #242, https://www.erdosproblems.com/242, accessed 2026-06-11

Order by
[oldest first](https://www.erdosproblems.com/forum/thread/242?order=oldest) or
[newest first](https://www.erdosproblems.com/forum/thread/242?order=newest). (The most recent comments are highlighted in a red border.)

- This question belongs to the class of other first-order questions one might ask about whole numbers. For example, is every integer is the sum of four cubes? In general, they are algorithmically undecidable.



**[Dogmachine](https://www.erdosproblems.com/forum/user/Dogmachine)**

— [18:49 on 09 Aug 2025](https://www.erdosproblems.com/forum/thread/242#post-29)

👍0📝0🤖0

- In the case 𝑎=4, the conjecture has been verified for 𝑛<5000 by Straus, 𝑛<8000 by Bernstein [here](https://gdz.sub.uni-goettingen.de/id/PPN243919689_0211?tify=%7B%22pages%22%3A%5B5%5D%2C%22pan%22%3A%7B%22x%22%3A0.495%2C%22y%22%3A0.757%7D%2C%22view%22%3A%22info%22%2C%22zoom%22%3A0.33%7D), 𝑛<20000 by Shapiro, 𝑛<106128 by Oblath in \[Ob49\], 𝑛<171649 by Rosati [here](http://www.bdim.eu/item?id=BUMI_1954_3_9_1_59_0&fmt=pdf), 𝑛<400000 by C. Ko, C. Sun and S. J. Chang in \[KoSuCh64\], 𝑛<107 by Yamamoto in \[Ya65\], 𝑛<1.1×107 by Jollensten in \[Jo??\] and 𝑛≤1017 by Salez [here](https://arxiv.org/pdf/1406.6307).



\[Ob49\]: R. Oblath, "Sur l'équation diophantienne 4/𝑛=1/𝑥1+1/𝑥2+1/𝑥3" , Mathesis, 59 (1949), 308-316.

\[KoSuCh64\]: Chan Ko, Chi Sun, AND S. J. Chang, On equations 4/𝑛=𝑙/𝑥+𝑙/𝑦+𝑙/𝑧, Acta Sci. Natur. Szechuanensis 2 (1964), 21-35.

\[Ya65\]: K. Yamamoto, " On the diophantine equation 4/𝑛=1/𝑥+1/𝑦+1/𝑧", Mem. Fac. Sci. Kyushu University Ser. A, 19 (1965), 37-47.

\[Jo??\]: R. M. Jollensten, A note on the Egyption problem, in “Proceedings of the Seventh Southeastern Conference on Combinatorics, Graph Theory and Computing” (F. Hoffman et al., Eds.), pp. 578-589, Winnipeg Utilitas Math. Publ. Inc., Winnipeg.



There is a lot of literature on this conjecture. Surprisingly, I came across a [paper](https://www.researchgate.net/publication/368513385_A_simple_direct_proof_of_the_Erdos--Straus_conjecture) which claims to solve the Erdos-Straus Conjecture. Another [paper](https://arxiv.org/html/2508.07367v1) claims to be an "almost" complete proof of the Generalized Erdos Straus Conjecture.



I am highly skeptical of both these papers, but professionals can take a look at'em.



**[Alfaiz](https://www.erdosproblems.com/forum/user/Alfaiz)**

— [10:31 on 18 Nov 2025](https://www.erdosproblems.com/forum/thread/242#post-1747)

👍0📝0🤖0


  - Thanks! Yes, this conjecture has attracted quite a few 'proofs' over the years. Of those that I have looked at, none have seemed credible.



    **[Thomas Bloom](https://www.erdosproblems.com/forum/user/TFBloom)**

     — [10:52 on 18 Nov 2025](https://www.erdosproblems.com/forum/thread/242#post-1748)

    👍0📝0🤖0

  - The paper which claims to solve the Erdos-Straus Conjecture is again very mistaken.

    Just had a look at the start of page 2, and it is full of unclear/ false steps.



    **[StijnC](https://www.erdosproblems.com/forum/user/StijnC)**

     — [13:12 on 18 Nov 2025](https://www.erdosproblems.com/forum/thread/242#post-1753)

    👍1📝0🤖0
- Li Delang in [his paper](https://www.sciencedirect.com/science/article/pii/0022314X81900391) has proved that for any given positive integers 𝑁 and 𝑘 the number of integers 𝑛<𝑁 for which the equation 4/𝑛=1/𝑥+1/𝑦+1/𝑧 is unsolvable in positive integers x, y, z is not greater than 𝑐⁢𝑁/(log⁡𝑁)𝑘, where 𝑐 is a constant depending only on 𝑘.



Also previously, Vaughan in [this paper](https://www.cambridge.org/core/journals/mathematika/article/abs/on-a-problem-of-erdos-straus-and-schinzel/6622BF4A083315C30DF1114A6F600223) has given the upper bound on the count of possible exceptions as 𝑁/exp⁡(𝑐⁢(log⁡𝑁)2/3) for a positive constant 𝑐.




(The site has been updated to address this comment.)




**[Alfaiz](https://www.erdosproblems.com/forum/user/Alfaiz)**

— [12:35 on 23 Nov 2025](https://www.erdosproblems.com/forum/thread/242#post-1794)

👍0📝0🤖0

- A [new paper](https://arxiv.org/pdf/2511.16817) by C. Pomerance and A. Weingartner is the latest paper which deals with this problem. This paper also gives a great account of past improvements/progress on this problem.




(The site has been updated to address this comment.)




**[Alfaiz](https://www.erdosproblems.com/forum/user/Alfaiz)**

— [11:43 on 24 Nov 2025](https://www.erdosproblems.com/forum/thread/242#post-1814)

👍1📝1🤖0

- Mordell in \[Mo68\] has shown it is true, except possibly in cases where 𝑛 is prime and congruent to 12,112,132,172,192 or 232 (mod 840)



\[Mo68\]: Mordell, L. J. Diophantine Equations, pp. 287-290. Academic Press,1968.




(The site has been updated to address this comment.)




**[Alfaiz](https://www.erdosproblems.com/forum/user/Alfaiz)**

— [13:47 on 07 Dec 2025](https://www.erdosproblems.com/forum/thread/242#post-2078)

👍0📝1🤖0


- \[Va70\] is unable to load any reference.




(The site has been updated to address this comment.)




**[Alfaiz](https://www.erdosproblems.com/forum/user/Alfaiz)**

— [05:33 on 29 Jan 2026](https://www.erdosproblems.com/forum/thread/242#post-3906)

👍0📝1🤖0

- I've been formalizing Erdős-Straus in Lean, 531 formalized items, 484 complete, hope it might be of use to one of you to finish this off: https://github.com/leochlon/erdstrau



Sorry-free lean4 proofs including: ES for 𝑛=420⁢𝑘+𝑟 with 𝑘 odd, 𝑟∈{121,169,289,361}; all 𝑛≡529⁢(mod⁡840) via CRT (174 declarations, witnesses like (133,23460,71764140) for 𝑛=529); 348/420 coverage; 20 conditional certificates for 𝑛≡1⁢(mod⁡840) (reducing to divisor conditions); and a formal refutation of one proposed ED2 covering scheme.



Showed the full conjecture reduces to one construction: given 𝑞≡3⁢(mod⁡4) and 𝑠2+𝑝=𝑞⁢𝑘, find 𝛿,𝑏,𝑐 with (4⁢𝑏−1)⁢(4⁢𝑐−1)=4⁢𝑝⁢𝛿+1 and 𝛿∣𝑏⁢𝑐. Setting 𝑏=(𝑞+1)/4 works for small 𝑞; general case open.



**[leonchlon](https://www.erdosproblems.com/forum/user/leonchlon)**

— [20:25 on 27 Jan 2026](https://www.erdosproblems.com/forum/thread/242#post-3855)

👍0📝0🤖0


  - For the reduction at the end;

    Could you add a few quantifiers to have a clear remaining goal?





    We need to prove it for every k, or for one value of k of a particular parity?

    There is a constraint on 𝑠?

    (Or 𝑝 is just minus a quadratic residue mod 𝑞?)



    **[StijnC](https://www.erdosproblems.com/forum/user/StijnC)**

     — [06:32 on 29 Jan 2026](https://www.erdosproblems.com/forum/thread/242#post-3907)

    👍0📝0🤖0

  - See the remarks for some well-known parametric solutions (which I assume your formalisation is using). In particular it's not too hard to prove via elementary methods that this conjecture follows from (and is in fact equivalent to) the statement that for any prime 𝑝, there exist integers 𝑎,𝑐,𝑑≥1 such that either 𝑝≡−𝑎/𝑐⁢(mod⁡4⁢𝑎⁢𝑐⁢𝑑−1) or 𝑝≡−4⁢𝑐2⁢𝑑+1𝑘⁢(mod⁡4⁢𝑐⁢𝑑) for some 𝑘∣4⁢𝑐2⁢𝑑+1. This might be nice, and not too hard, to formalise, see Theorem 1 of \[BlEl22\] for a proof of the equivalence.



    Using this you can prove the conjecture for many congruence classes, and can efficiently check it's true for all small primes 𝑝. One can certainly refine Mordell's modulo 840 conditions for example - this was already done by Terzi in 1971 to a modulo 120120 condition. I'm sure that by continuing computations one can forever narrow down the congruential conditions, but I don't think this is a viable path to the full conjecture.



    **[Thomas Bloom](https://www.erdosproblems.com/forum/user/TFBloom)**

     — [07:28 on 29 Jan 2026](https://www.erdosproblems.com/forum/thread/242#post-3909)

    👍0📝0🤖0

  - In case anyone is curious, [this file](https://github.com/leochlon/erdstrau/blob/5d0f0467ef8a0a87b708b54c40213697ce4d66b6/ESLean/Residues/R529.lean) contains the claimed proof of "Full CRT coverage for n ≡ 529 (mod 840)". I think a quick look at this file is highly informative as to the source and veracity of the claimed results.



    **[BorisAlexeev](https://www.erdosproblems.com/forum/user/BorisAlexeev)**

     — [11:59 on 29 Jan 2026](https://www.erdosproblems.com/forum/thread/242#post-3911)

    👍1📝0🤖0


    - Aha, thanks for pointing that out Boris. So this isn't actually a proof of anything - it's just verifying the conjecture for a collection of small 𝑛, and appeals to 'periodicity' to extend this to an infinite congruence class. This does not work, since the statement is obviously not periodic, so I'm not sure what they have in mind here.



      I do think, however, that a genuine formalisation of the known congruence classes cases (and/or the equivalence mentioned in my earlier comment) would be valuable, and presumably quite straightforward to do automatically, since this is just messing about with elementary identities.



      **[Thomas Bloom](https://www.erdosproblems.com/forum/user/TFBloom)**

       — [12:15 on 29 Jan 2026](https://www.erdosproblems.com/forum/thread/242#post-3912)

      👍1📝0🤖0
- Perhaps It is easier to prove that solutions exist for almost all prime denominators?



**[Dogmachine](https://www.erdosproblems.com/forum/user/Dogmachine)**

— [14:31 on 01 Feb 2026](https://www.erdosproblems.com/forum/thread/242#post-4034)

👍1📝0🤖0


  - This is true, and follows e.g. from Vaughan's (much stronger) almost all result listed in the remarks.



    **[Thomas Bloom](https://www.erdosproblems.com/forum/user/TFBloom)**

     — [15:33 on 01 Feb 2026](https://www.erdosproblems.com/forum/thread/242#post-4037)

    👍0📝0🤖0
- A solution to this conjecture has been "claimed" by K. Bradford in his latest preprint [\[Br26\]](https://arxiv.org/abs/2602.11774).



**[Alfaiz](https://www.erdosproblems.com/forum/user/Alfaiz)**

— [04:33 on 13 Feb 2026](https://www.erdosproblems.com/forum/thread/242#post-4274)

👍0📝0🤖0


  - The final sentence on the covering system seems to hint it is incorrect/ incomplete.

    Taking the first primes modulo different moduli doesnt create a covering system.



    In particular, none of the 6 remaining residues modulo 840 by Mordell are excluded here.



    **[StijnC](https://www.erdosproblems.com/forum/user/StijnC)**

     — [06:36 on 13 Feb 2026](https://www.erdosproblems.com/forum/thread/242#post-4276)

    👍2📝0🤖0

  - While not \*quite\* as notorious as \[ [1135](https://www.erdosproblems.com/1135)\], this problem also regularly attracts a large number of low-quality solution attempts. I would not give too much attention to any new preprints on this problem unless either (a) the result has been accepted for publication in a reputable journal, (b) the author has an existing track record of reputable publications in the general area of diophantine equations or analytic number theory, (c) only realistic partial results are claimed, (d) an expert is willing to vouch for the correctness (or at least plausibility) of the results, or (e) the result has been properly formalized.



    EDIT: For what it is worth, [here is the ChatGPT Pro critique](https://chatgpt.com/share/698ed01e-2ad4-800e-9986-b121ce41ae76) of this latest attempt.



    **[TerenceTao](https://www.erdosproblems.com/forum/user/TerenceTao)**

     — [06:46 on 13 Feb 2026](https://www.erdosproblems.com/forum/thread/242#post-4277)

    👍2📝0🤖0

[Show 4 more comments](https://www.erdosproblems.com/forum/thread/242?order=oldest#)

**All comments are the responsibility of the user. Comments appearing on this page are not verified for correctness. Please keep posts mathematical and on topic.**

[Log in](https://www.erdosproblems.com/forum/login?next=%2Fforum%2Fthread%2F242) to add a comment.

[Back to the forum](https://www.erdosproblems.com/forum/)