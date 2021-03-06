---
layout: post
title: Chip Economics
tags: code
---

Over the past few weeks, I've been working through [NAND2Tetris](http://nand2tetris.org) after the recommendation of [Julian Gindi](http://juliangindi.com/). The NAND2Tetris course takes a single NAND electronic gate, which returns 0 if both inputs are 1 and returns 1 otherwise, and uses this as a building block for a whole host of electronic gates. It's possible to make a NOT gate out of NAND chips. It's also possible to build a multiplexer (which picks between inputs based on a control input). And most impressively, we can build an arithmetic logic unit - the core part of a CPU responsible for addition and subtraction - solely out of a stack of NAND chips. When all is said and done, I'll have built a working computer emulator solely out of these single atomic pieces.

Now, at this point in computer development, I've never even _seen_ a real NAND hardware chip, and it's likely impossible I could see one even if you held it up. They've now been shrunk down to a few nanometers wide. Engineers at Intel and AMD obsess over ALU design (I expect, maybe even they don't any more), but it's so far abstracted away from my day-to-day work that I could get away with never knowing how one worked for my entire career. But once upon a time, that wasn't the case. Chips were things you could actually touch, and solder onto a breadboard, and make arcade games out of them. 

This exercise has made me look at some of the feats of early computer engineers in a totally different light. In the 1970s, Steve Wozniak was building Pong and [Breakout!](http://thedoteaters.com/?bitstory=breakout) arcade games out of hardware chips, soldering together [more sophisticated] logic gates to build games. Atari was willing to pay $5000 ($22K in today's dollars) for a Breakout chip design that only used 44 chips because chips actually cost enough for that to matter. Logic gates weren't just vague ideas embedded into processor designs - they were things you could touch, and they cost money. 
