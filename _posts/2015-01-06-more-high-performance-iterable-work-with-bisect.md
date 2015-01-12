---
layout: pymod
title: More high-performance iterable work with bisect
tags:
- pymod
---

In my [last post](/2015/01/05/and-here-i-was-thinking-arrays-were-for-javascript-and-lists-were-for-python.html), I explored the Python array data structure. In keeping with the vibe of iterable data structures, I'm moving on to cover the `bisect` module.

`bisect` uses a simple bisection algorithm to insert items into a list without botching the sort. The gist of the algorithm is simple: we're going to create a midpoint using the low and high marks of the list, check if our value is greater than or less than the midpoint, then use the midpoint to slice the list into smaller and smaller lists until our item falls right at the midpoint.

You can see this in action here:

	def bisect_pseudo(a_list, my_value):
		low = 0
		high = len(a_list)

		while low < high:
			midpoint = (low+high)//2

			if my_value < a_list[midpoint]:
				high = midpoint
			else:
				low = midpoint + 1

			print "low:", low, "high", high

		return low

	my_list = [1, 4, 9, 16, 25]

	print "Value greater than midpoint: "
	bisect_pseudo(my_list, 10)

	print "Value less than midpoint: "
	bisect_pseudo(my_list, 2)

In this example, we see the algorithm sifting through our list, searching for the point in the list where our test value would naturally slide in. This is a left bisection algorithm - where we start from the left side of the list and work up - and the reverse would be a right bisection algorithm. The `bisect` module includes both.

	import bisect

	names = ['Joe', 'Beth', 'Steve']

	names.sort()

	print names

	print bisect.bisect_left(names, 'David')

	bisect.insort_left(names, 'David')

	print names

In this example, we're using the `bisect_left()` function, an implementation of the same algorithm described above, to find the midpoint in our sorted list. The `insort_left()` function will perform this algorithm and then insert our value exactly where it needs to be. The code using the right bisection algorithm looks similar:

	print bisect.bisect_right(names, 'Shamyl')

	bisect.insort_right(names, 'Shamyl')

	print names

The Python `bisect` module is fairly quick, but it will use a faster C implementation if one's available. That's all there is to it! 