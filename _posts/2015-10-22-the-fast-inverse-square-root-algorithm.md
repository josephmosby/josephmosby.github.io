---
layout: post
title: The fast inverse square root algorithm
---

Taking a break from operating systems to do some algorithm training: something I revisit about once a year. I have the Khan Academy bit on the [Towers of Hanoi](https://www.khanacademy.org/computing/computer-science/algorithms/towers-of-hanoi/a/towers-of-hanoi) up, but I want to first pause to go look at Quake's "fast inverse square root" algorithm.

An inverse square root is used to calculate vectors for lighting and reflecting, so it's incredibly useful for video games and rendering. Rendering uses millions upon billions of these tiny calculations, so a speedup over floating-point division can make a game much, much faster. Quake sped it up with the following steps:

	1. Take a floating point number n.
	2. Shift the bits of n to treat n like an integer.
	3. Shift n right one bit to make longword w.
	4. Subtract w from the magic number 0x5f3759df (this step made a Quake developer comment "what the f***" in the code)
	5. This number is within a few percentage points of the final answer. 
	6. One iteration with the Newton-Raphson method to come to the final answer.

I was amused by this approach and can only imagine the total confusion on the part of the developer when the algorithm worked. 