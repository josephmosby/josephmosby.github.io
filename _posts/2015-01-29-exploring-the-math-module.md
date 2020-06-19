---
layout: post
title: Exploring the math module
tags: code
---

I could write code for days using the `math` module and never hit the end. `math` is huge. It's designed to keep you from rewriting a stack of mathematical functions that someone had inevitably written before (formulas for calculating the sine, cosine, tangent, etc). 

So rather than write a stack of example code, let's instead discuss what `math` can do for you. `math` can do any of these functions on integers only - `cmath` provides the same, but allows complex numbers.

### Number-theoretic and representation functions

These functions deal with a few basic theoretical calculations that didn't quite fit anywhere else. Things like `factorial()`, `fabs()` (which calculates absolute value), and `modf()` which returns the fractional and integer parts of a float can all be found here. 

### Power and logarithmic functions

As can be expected, you'll find things with exponents and logarithms here. Need to calculate e^x? Use `exp(x)`. Need to get x^y? Use `pow(x, y)`. Logarithms use `log(x, [base])`. Easy stuff here.

### Trigonometric functions

This is where all of the trigonometric functions live: things like `sin(x)`, `cos(x)`, `tan(x)`. I wish I'd known about this in the eleventh grade with Mrs. May. 

### Angular conversion functions

Need to go from degrees to radians? Use `radians(x)`. Need to go from radians to degrees? Use `degrees(x)`.

### Hyperbolic functions

I never used these in eleventh grade and am only moderately aware of what they do. If you need the hyperbolic tangent of x - `tanh(x)` - or the inverse hyperbolic cosine - `acosh(x)` - this is where to look. 

### Error functions

Same thing for error functions. I am not proud of how much math I don't know right now.

### Constants

These I've got, though! This is where `pi` and `e` live.

`math` is great, and if you're going to using Python for statistical or scientific computing, it's a must-know. 