---
layout: post
title: Spearman&apos;s rank-order correlation
---

This is a mini-post: something I learned about today at work that I thought was awesome in and of itself. It's called "Spearman's rank-order correlation," and it tells you if two data sets move in the same direction.

Two sets of data can have what's called a "monotonic" relationship, which basically means that if one value goes up, the other value goes up; and if one value goes down, the other goes right down with it. Monotonicity doesn't necessarily care about the direction of that relationship. It just cares that the two go together. 

Let's look at something topical. Specifically, let's see how Kirk Cousins's and Eli Manning's passing yards compare over a given sixteen-game season. If Cousins and Manning had a strong Spearman rank-order correlation (shortened as Spearman's rho, because mathematicians like Greek), we would Manning's passing yards go up if Cousins has a great game, and if Manning only throws for a hundred yards, Cousins will have a bad game too. I'm going to ignore bye weeks in this example so each will have exactly sixteen games.

    from scipy.stats import spearmanr

    kirk = [196, 203, 316, 290, 219, 196, 317, 217, 324, 207, 302, 219, 300, 319, 365, 176]
    eli = [189, 292, 279, 212, 441, 189, 170, 350, 213, 361, 321, 297, 337, 245, 234, 302]

    spearmanr(kirk, eli)
    # SpearmanrResult(correlation=-0.19602068697550504, pvalue=0.46686779279825008)

Okay, so not really correlated... in fact, they're actually slightly negatively correlated, which would imply that Cousins has bad games when Manning has good ones and vice versa. But it's a loose relationship, so we won't compare that too much.

This isn't much of a fair comparison, though. If the Giants were playing the Patriots on the same week that Washington was playing Philadelphia, we'd expect Manning to have a bad game while Cousins has a great one. So let's compare how they fared when facing similar teams and see if the correlation improves.

| Team | KC  | EM  |
|------|-----|-----|
| PHI  | 290 | 302 |
| ATL  | 219 | 292 |
| NYJ  | 196 | 297 |
| TB   | 317 | 213 |
| NE   | 217 | 361 |
| NO   | 324 | 350 |
| CAR  | 207 | 245 |
| DAL  | 219 | 170 |
| BUF  | 319 | 212 |

So now if we run our calculation:

    kirk_vs_teams = [290, 219, 196, 317, 217, 324, 207, 219, 319]
    eli_vs_teams = [302, 292, 297, 213, 361, 350, 245, 170, 212]
    SpearmanrResult(correlation=-0.10041928905068677, pvalue=0.7971388092372127)

Okay.. almost no correlation at all! Good to know for fantasy purposes, that if you want to hedge your QB bets, put Cousins and Manning on the field together!

That's all I've got, that's Spearman's rho. Go have fun with it! 
