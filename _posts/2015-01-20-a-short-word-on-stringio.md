---
layout: post
title: A short word on StringIO
tags: code
---

The `StringIO` library has a nifty purpose. It provides you with a buffer in memory that allows you to read and write strings without saving a file to disk. 

	import StringIO

	output = StringIO.StringIO()

	output.write('This is a string!\n')
	output.write('This is a second line string!')

Okay, so we've got ourselves a string buffer with some strings. Now what can we do?

	print output.read()

Wait... that didn't really do anything. Ah yes! Because it's a file-like object, we have to return to the beginning of the object to read it again.

	output.seek(0)
	print output.read()

Anything you can do with a file, you can do with this string buffer. It's quite useful for capturing output or dealing with test cases like these. And in the event that you need a much faster cousin, `StringIO` comes with a `cStringIO` [just like our](/2015/01/12/storing-objects-with-the-best-named-module-ever-pickle.html) `pickle` module came with its `cPickle`. We'll see this again in future test applications.