---
layout: pymod
title: Exploring the __future__ module and learning about division
tags:
- pymod
---

Python adds new features to the language all the time, but occasionally those features are completely incompatible with existing features of the language. In many cases, they completely rewrite a core [built-in function](/2014/12/19/hacking-builtin-for-fun-no-profit.html) or key operator of the language. The `__future__` [module](https://docs.python.org/2.7/library/__future__.html#module-__future__) contains several of those new features - some of which have already made it into Python 2.7 at the time of this writing. A few of them are designed to prepare Python 2.x users for sea changes coming with Python 3.x.

The `print()` function is one of those new features. In 2.x, the `print` statement allowed developers to print to `stdout`, but it wasn't very robust. If you wanted to print to a different output, or rewrite part of how `print` formats its output, you just couldn't. `print` was too hard-coded into the syntax of how Python worked. By changing it into a function, though, we can change the separators, add different ends, or output to a file.

The `print()` syntax looks like this, as specified in [PEP 3105](https://www.python.org/dev/peps/pep-3105/):

`def print(*args, sep=' ', end='\n', file=None)`

And we can experiment with it like this:

	from __future__ import print_function

	print('Next level printing with print()')
	print('Can\'t do this any more: print "Hello World!"')
	print('Have to use print("Hello World!")')
	print("Hello", "world", sep="-", end="flipper\n")

Cool, no? Though syntactically it's a big mental shift from the current `print`, it's unquestionably much more robust.

Python 3.x also brings in a new mechanism for handling division. Python 2.x used something called "floor division" when the `/` operator was called. It would divide and then discard the remainder and round downward to yield an integer, so "8/7" would yield "1" rather than "1.142857...". By bringing in Python 3.x's version of division, 8/7 will yield the float. 8//7 will bring in the old floor division.

	from __future__ import division, print_function
	print('8/7:', 8/7)
	print('8//7', 8//7)

And finally, Python has even included an Easter egg for those developers who love and miss C's mechanism for separating code blocks using braces instead of whitespace:

	from __future__ import braces

:)