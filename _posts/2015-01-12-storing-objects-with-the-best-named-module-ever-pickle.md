---
layout: default
title: Storing objects with the best-named module ever, pickle
---

I love `pickle`. I love that Python has a module named pickle. I have never used pickle before, but I like that it's there. Let's take a look at what pickle does.

Per the docs, `pickle` provides an algorithm for serializing and unserializing a Python object. When we pickle an object, we turn it into a stream of bytes that can be sent to another process or saved to a file to be reconstructed at a later time. You still have to define the class in the namespace of the process reading the pickle - a pickled object comes with object data but no way to tell the program about an object type that's not already in the process namespace. `pickle` also comes with a faster `cPickle` companion that's written in C to make it super fast. 

We can kick things off like so:

	import pickle

	class Cucumber:

		def __init__(self, height):
			self.height = height

		def grow(self):
			self.height += 1
			return "Current height is: ", str(self.height)

	veggie = Cucumber(2)
	veggie.grow()

	print pickle.dumps(veggie)

	veggie.grow()

	print pickle.dumps(veggie)

Here, I have created a `Cucumber` object type and given it a method `grow()`, which will increment its height. Calling the `pickle.dumps()` method on an instance of our `Cucumber` yields a short string of ASCII characters as a representation of our object. 

I can also save objects to files and reload them in perfect condition:

	veggie_two = Cucumber(4)

	file_save = open('pickled_veggies', 'w')

	pickle.dump(veggie_two, file_save)

	file_save.close()

	file_read = open('pickled_veggies', 'r')

	veggie_three = pickle.load(file_read)

	print "Veggie Three Height: ", str(veggie_three.height)

`pickle`'s `dump()` mechanism (not `dumps()` with a 's') is used to save these ASCII object strings to a file, and `load()` is used to read them back from that file. `loads()` would read them from a string. 

And that's what `pickle` does, simply and well. It makes your objects into strings, light, compact and ready to be stored forever. 