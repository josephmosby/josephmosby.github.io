---
layout: post
title: Type experiments with mypy
tags: code
---

At PyCon 2015, much hullabaloo was made over [PEP 484](https://www.python.org/dev/peps/pep-0484/) and the notion that "types" would be coming to Python. As I only vaguely understood the meat behind these protests, I decided to take a look at the PEP and the science behind it. 

A "type" in computer programming is pretty much exactly what it sounds like: it's a type of data. One commonly sees integers, strings, floating-point numbers (simplistically, just numbers with decimals), Booleans (true/false), and lists in any language that uses types. Programming languages that use types allow the computer to predict and organize data at the machine level in the optimal way for the type. 

I had no trouble understanding types, but I had to think on "static" versus "dynamic" typing for a while. Static typing means that data types are declared when writing the program, and a type checker will protest if data is of the "wrong" type. This can be illustrated with an example from C:

	static int numOne, numTwo, sum;
	numOne = 5;
	numTwo = 8;
	sum = numOne + numTwo;

In this example, `numOne` and `numTwo` are declared as integers, and can only be integers. If later on in the program, you want to do something like this:

	numOne = "hello";

the compiler will throw a Type Error, and you won't be able to compile your code. It's not an execution problem -- the program hasn't even run yet -- it's the compiler checking up on you and letting you know that you said two conflicting things. You tried to say `numOne` was an integer, then later on tried to say it was a string, and that is *NOT OK.*

Dynamic typing, by contrast, takes a more YOLO approach to typing. Variable types don't need to be explicitly spelled out in the program, and variables can change types over the life cycle of the program. This is all totally okay in Python's lack-of-type system:

	num_one = 5
	num_two = 8
	sum = num_one + num_two

	< moar code >

	num_one = "hello"

Python's totally cool with all of this in its dynamically typed world. 

In 2012, Jukka Lehtosalo announced he was working on a statically typed Python derivative called [mypy](http://mypy-lang.org/index.html). `mypy` allows programmers to declare types in their Python programs and realize the performance benefits of static typing while maintaining the dynamic typing that's part of the Python core. `mypy` puts this example on their homepage: 

	# regular Python

	def fibonacci(n):
		a, b = 0, 1
		while a < n:
			yield a
			a, b = b, a+b

	# mypy

	def fibonacci(n: int) -> Iterator[int]:
		a, b = 0, 1
		while a < n:
			yield a
			a, b = b, a+b

I'm skeptical. Let's do some timing comparisons.

I pulled these scripts off of the [mypy examples page](http://mypy-lang.org/examples.html), just to make sure I wasn't messing with any data by writing a bad program. We have a test with [dynamic types](https://gist.github.com/josephmosby/deed574acae4012c6f5e) and one with [static types](https://gist.github.com/josephmosby/7677272079fd9ccfb761). There are two tweaks in each program to adjust for differences between Python 2 and Python 3 (on line 13, `numbers.next()` was changed to `next(numbers)` and on line 18, `itertools.ifilter()` was changed to `filter()`). 

	$ python dyn_test.py
	dyn_test.py
	100003
	Time one
	7.158545970916748
	100003
	Time two
	7.493566989898682
	100003
	Time three
	8.433957815170288
	100003
	Time four
	7.388293027877808
	100003
	Time five
	7.045740127563477

	$ python mypy_test.py
	mypy_test.py
	100003
	Time one
	7.473484992980957
	100003
	Time two
	7.3924078941345215
	100003
	Time three
	7.513011932373047
	100003
	Time four
	8.032839059829712
	100003
	Time five
	7.929549932479858

Well... I can't detect any statistically significant differences here. I remain skeptical.

Now, where I _can_ call out some perks: the `mypy` type checker is super awesome. It does a lot of pre-compile lint work on the code and helped me detect the two errors I noted above. I could also see this being useful in a codebase that's touched by a lot of enterprise developers. But does it offer significant performance benefits? \*shrug\* I'm not sure. Perhaps in a more complex world.