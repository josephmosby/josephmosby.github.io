---
layout: post
title: Object presentation with pprint
tags:
- pymod
---

In my [last post](/2015/01/21/string-presentation-with-textwrap.html), I discovered that there are all sorts of awesome things you can do to format strings for presentation in a Python program. In this episode, I learn that it's possible to do the same thing with all Python objects using `pprint`!

Let's crack it open and get to some pretty-printing!

	import pprint

	pp = pprint.PrettyPrinter(indent=4, width=60)

Okay, I've implemented a `PrettyPrinter` object that expects to indent things at the four-space mark and each line can only be 60 characters long. Cool. 

	team = ['We', 'live', 'in', 'cities', 'you\'ll', 'never', 'see', 'on', 'screen', 'not', 'very', 'pretty', 'but', 'we', 'sure', 'know', 'how', 'to', 'run', 'things']

	# yes, that is a list of words in the chorus of Lorde's "Team"

	pp.pprint(team)

Okay, awesome. I now print everything on its own line with a slight indentation. 

What happens if I throw a custom object at it?

	class Dog:
		def __init__(self, name, owner):
			self.name = name
			self.owner = owner

	my_dog = Dog('Rufus', 'Joe')

	pp.pprint(my_dog) # <__main__.Dog instance at 0x1007ebc20>

Oh, that's disappointing. I was	hoping I'd get a nifty way of doing this without having to define a custom `repr()` method on `Dog`. Ah well.

So `pprint` does some stuff awesome, and some stuff... not as awesome. Onward!