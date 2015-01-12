---
layout: pymod
title: And here I was thinking arrays were for JavaScript and lists were for Python
tags:
- pymod
---

Python has arrays. Python even has an entirely special module that lets you build arrays. Like arrays in Java and C++, arrays from the `arrays` module must all be of a certain type of data. I assume these things must be wicked fast, but I wonder how large the array would have to be before there would be a noticeable difference.

Having nothing further to say about single-type arrays, let us proceed with the code!

	import array

	a = array.array('c', 'check out my sick array')

	print "As array:", a

In our first little snippet here, we're turning a string into an array to start conducting experiments. The first parameter - `'c'` - specifies that this array will be full of _characters_.

	a.extend(', it has so many bytes')

	print a

	print a[10:23]

We continue fiddling with our array by extending it. We can also slice arrays into smaller arrays, as we see here. 

	output_data = open('array-ex', 'wb')
	
	a.tofile(output_data)
	
	output_data.flush()

Arrays built using `array.array()` have a built-in function to save the data to a file. By opening a file object, calling `tofile(file_name)` on the array, and flushing the file object, we write our array to disk.

	input_data = open('array-ex', 'rb')
	
	raw_data = input_data.read()

	print 'Raw data:', raw_data

We've extracted our raw data from the file as binary information. To read it into a new array we'll do the following:

	input_data.seek(0)

	second_array = array.array('c')

	second_array.fromfile(input_data, len(a))

	print second_array

And that's about it for arrays. Super easy on memory, super fast, and useful in situations where performance is critical.

* special thanks to PYMOTW for [some inspiration](http://pymotw.com/2/array/) on stuff to do with arrays as examples