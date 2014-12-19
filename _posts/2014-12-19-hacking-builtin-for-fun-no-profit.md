---
layout: post
title: Hacking __builtin__ for fun, no profit
---

Python's `__builtin__` module contains all of the language's [built-in functions](https://docs.python.org/2.7/library/functions.html), which should be reasonably obvious from the name. Python is really, really insistent that its built-ins are perfectly sufficient and that you shouldn't go around messing with them. This is a large part of the reason that I almost threw up the first time I had to go [monkeypatching](http://stackoverflow.com/questions/394144/what-does-monkey-patching-exactly-mean-in-ruby) in Ruby... it just doesn't _feel_ right. But for the sake of argument, let's do some screwing around with the built-in functions.

	import __builtin__

	def hex(x):
		'''Return the basic hex function, but with extra YOLO attached.'''
		f = __builtin__.hex(x)
		if f[0] == '-':
			return f[0] + 'yol' + f[1:]
		else:
			return 'yol' + f


The [hex function](https://docs.python.org/2.7/library/functions.html#hex) is designed to return the hexadecimal representation of an integer, prefixed with 0x. I felt like this representation could be much improved with a bit of extra YOLO, and patched the function accordingly. *_Now_* I can call `hex(255)` and receive back "yol0xff", a marked improvement over the prior implementation. 

	import __builtin__

	def len(s):
		'''Return the basic len function, but subtract one so we show what the last position number is.'''
		l = __builtin__.len(s)
		return l-1

I'm lazy, and don't always like to calculate the length of a list or string then subtract one to access the last element of a list. Why not ask `len()` to do that work for me? Now I can call `len('hello')` and receive a value of 4, allowing me to easily determine the number of the last character any time and every time.

Okay, okay... I can think of no reason why any programmer would want to go messing around with the `__builtin__` library. It would be horribly un-Pythonic to start wrapping the core Python functions like this. But it's good to know that we can.