---
layout: pymod
title: What in heaven's name is an abstract base class?
tags:
- pymod
---

Let's talk about duck-typing for a second. Duck-typing is an object-oriented programming principle that allows an object's methods and properties to handle the semantics and behavior of an object without the need to determine what type of object it actually is. The idea is that "if it looks like a duck and quacks like a duck, it's a duck" and the programmer doesn't need to first ask the object if it's actually a duck. We can just start asking it to quack.

An example:

	[1, 2, 3, 4, 5].len() # 5
	"hello".len()		  # 5

I don't need to ask the object if it's a string or a list before calling `len()`. I'm trusting that the object's `len()` method already knows what to do. 

_Abstract base classes_ complement duck-typing by providing an alternative way to define an interface when all of the possible use cases for an object might not have been anticipated by the designer. This scenario might pop up in a large development team, or if a software plugin might be written by an external team. In theory, we create an abstract base class by defining a class and marking its methods as _abstract_, then registering a concrete class with the interface or by simply subclassing the abstract class.

Confused yet? Don't worry, my head's spinning a bit too. Let's continue.

I define an abstract base class like so:

	import abc

	class Animal:
		__metaclass__ = abc.ABCMeta

		@abc.abstractmethod
		def greet(self):
			return

With the `__metaclass__ = abc.ABCMeta` declaration, we've defined `Animal` as an abstract base class. We've also defined an abstract method, `greet()`, that doesn't do anything but return. That's totally okay - anything that inherits from `Animal` will need to write their own `greet()` anyway, as concrete classes can't access those abstract methods directly. Let's finish this out:

	import abc

	class Animal:
		__metaclass__ = abc.ABCMeta

		@abc.abstractmethod
		def greet(self):
			return

	class Lion:

		def greet(self):
			return "ROAR"

	Animal.register(Lion)

	print('Subclass:', issubclass(Lion, Animal))
	print('Instance:', isinstance(Lion(), Animal))

Our `Lion` implements the `Animal` API, but it's not derived from `Animal`. 

We'll see this approach again when we look at the [collections](https://docs.python.org/2/library/collections.html#module-collections) module, which uses abstract base classes to test whether a collection is hashable or a mapping.
