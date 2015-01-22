---
layout: post
title: String presentation with textwrap
tags:
- pymod
---

I haven't written that many programs that run solely from the command line with a lot of user instructions incorporated into the program flow, so I haven't done much Python display text processing. But if I had, `textwrap` would very likely be one of my best friends.

The `textwrap` module is designed to wrap text, produce some formatted paragraphs, or totally strip out indentation from strings. It's there for your convenience. Let's take a look at what it can do:

	import textwrap

	my_string = "The textwrap module is designed to wrap text, produce some formatted paragraphs, or totally strip out indentation from strings. It's there for your convenience. Let's take a look at what it can do:"

	print my_string

	print textwrap.wrap(my_string, 60)

Whoa whoa whoa there, that's some weirdness. I've clearly got a cut-up string there, but it's in list format. Let's clean that up a bit:

	print "\n".join(textwrap.wrap(my_string, 60))

But wait a second, that seems like writing a bunch of characters that I didn't want to write. Let's use `fill()`!

	print textwrap.fill(my_string)

Okay, so `fill()` pretty much does the exact same thing as `wrap()`, but it automatically joins everything and adds some newlines in. 

Now let's fiddle around with `dedent()`:
	
	my_string = "\t\t" + my_string

	print my_string

	print textwrap.dedent(my_string)

I've added in some tabs here just to showcase what `dedent()` is designed to do. You can add whitespace to the beginning of your strings - such as if you wanted to include paragraphs in the source code - but then strip it out for presentation in your app.

And that's a `textwrap`!