---
layout: post
title: Learning closures and decorators
tags: code
---

I don't know why it took me such a long time to pick up closures. They seem so nifty. I have no idea what I'll use them for [yet] but I like that they're there.

And now it's time to play with them.

![](/images/closure.png)

According to StackOverflow:

	The most simple way to think of a closure is a function that can be stored as a variable (referred to as a "first-class function"), that has a special ability to access other variables local to the scope it was created in.

According to StackOverflow (again):

	A closure is a persistent local variable scope

According to Wikipedia:

	In programming languages, closures (also lexical closures or function closures) are a technique for implementing lexically scoped name binding in languages with first-class functions. Operationally, a closure is a data structure storing a function together with an environment: a mapping associating each free variable of the function (variables that are used locally, but defined in an enclosing scope) with the value or storage location the name was bound to at the time the closure was created.

Wikipedia's definition sounds super fancy. 

So a closure is a way to encapsulate variables within a function definition. Then we can access the variables within that function through function calls. Rock on. Let's make some.

In JavaScript: 

	var closure = function() { 
		var count, counter;
		count = 1;
		counter = function() {
			count = count + 1; 
			return count;
		}
		return counter;
	}

	var testClosure = closure();

	testClosure(); // 2
	testClosure(); // 3
	testClosure(); // 4

I tested this out in a Node.js evaluator on my local machine, but you can do the same in your browser console. 

In Python:

	def closure():
		count = 1
		def counter():
			count += 1
			return count
		return counter

	test_closure = closure()
	test_closure() # UnboundLocalError: local variable 'count' referenced before assignment

Wat. That didn't go as expected. Python is giving me an `UnboundLocalError`, which indicates that I called a variable before assigning it. The detailed stack trace points me to line 4, which is `count += 1`. 

It looks like Python uses something called the "decorator" pattern to deal with this sort of work, and the syntax looks different than we would do it with JavaScript. There's a fantastic [guide to decorators here](http://thecodeship.com/patterns/guide-to-python-function-decorators/). Let's make use of one to get this code up and running.

	def counter(count):
		return count += 1

	def count_decorate(func):
		def func_wrapper(count):
			return func(count)
		return func_wrapper

There's still something wrong with this - it's not preserving state like I'd want it to. `count` isn't preserved across function calls. Perhaps you can't do that in Python? 

Here's another example of our last bit: (from [The Quick Python Book](http://affiliate.manning.com/idevaffiliate.php?id=1221&url=33)):

	def makeInc(y):
		def inc(x):
			return y + x
		return inc

	test_closure = makeInc(5)

And one more thing: bonus material! Since talking about decorators led me to start researching decorators in Python (thinking they're the same thing), I decided to write a little timer that would tell me how long it took to compute a function: 

	import time

	class timer(object):
		
		def __init__(self, f):
			self.f = f

		def __call__(self, n):
			self.time1 = time.time()
			value = self.f(n) # run the function and establish a value
			self.time2 = time.time()
			print("it took ", self.time2-self.time1, " to execute")
			return value # return the function's computed value after timing it

	@timer
	def fib(n):
		a, b = 0, 1
		for i in range(0, n):
			a, b = b, a + b
		return a

Our timer object, armed with its `__init__` and `__call__` methods, is ready to be a Python decorator! Just by sticking that little `@timer` in front of our function, we'll now time its execution before allowing it to finish processing. It's the same thing that happens with all of those `@login_required` decorators I have sprinkled throughout my Django code. 

What happens if I rewrite my Fibonacci code as a recursive algorithm?

	@timer
	def fib(n):
		if n <= 2:
			return n
		else:
			return fib(n-1) + fib(n-2)

It behaves almost exactly like we'd expect - every time our recursive algorithm calls the `fib(n)` in the recursive algorithm, we rerun the timer! Recursion doesn't work quite as well in this scenario. Maybe if we tweaked the timer.. that's for a later experiment.

Have fun with these! Go write all your own decorators now!