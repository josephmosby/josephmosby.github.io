---
layout: post
title: Saving yourself from command-line parsing hell with argparse
---

Before `argparse`, I thought the only way to deal with command line arguments was to use `sys.argv`. You throw a series of arguments at a program, munge through them with `sys.argv[0]`, `sys.argv[1]`, etc. and hope for the best. And you hope that you always have full control over the arguments coming at your program through the command line. But what do you do if you have optional arguments, or flags? You could write your own parsers to handle all of that, but that's where `argparse` comes in. 

`argparse` provides a wrapper around `sys.argv` that... well, it parses arguments. The name is rather intuitive. 

A program utilizing `argparse` requires an `ArgumentParser` object to be much use at all. The arguments supplied to the `ArgumentParser` upon initialization provide much of the information on how we'll use the tool. We'll do that like so:
	
	import argparse

	parser = argparse.ArgumentParser(description='A custom tool for rustling or unrustling jimmies.', usage='Use the custom tool in a manner that keeps your jimmies unrustled.')

The "description" and "usage" strings provide information that will be displayed when a user wants to read the manual on your program. We'll look at that output in a bit once we add some arguments.

	parser.add_argument('jimmies', type=int, nargs='+', help='Jimmies, in this instance, are a list of integers delimited by spaces.')

I've added an argument here that will be named 'jimmies.' By design, any argument that does not have a '-' preceding its name is a positional argument. `jimmies` expects arguments to be integers (`type=int`) and everything supplied on the command line will be cobbled together into a list (`nargs='+'`). We've also provided some help text here.

	parser.add_argument('--rustle', dest='rustle', action='store_const', const=shuffle, default=unshuffle, help='The rustle flag determines if you would like further rustling of your jimmies. Otherwise, this program will naturally seek unrustlement.')

I've now added an optional flag here called `--rustle`. This will send everything into a function called `rustle`. `rustle` will do one of two things here: it will either make use of a function called `shuffle` if the flag is present, or it will make use of a function called unshuffle if the flag is absent. The `action` parameter indicates that we should store a constant value regardless. We'll use a default value if the `--rustle` flag isn't present, but we'll use the `const` otherwise.

Let's assume that `unshuffle()` and `shuffle()` were defined elsewhere in the program like so.

	import random 

	def unshuffle(parsed_items):
		parsed_items.sort()
		return parsed_items

	def shuffle(parsed_items):
		random.shuffle(parsed_items)
		return parsed_items

Then finally, we have to use the program:

	if __name__ == "__main__":
		args = parser.parse_args()
		print args.rustle(args.jimmies)

The `args = parser.parse_args()` will produce a list of arguments based on what was supplied at the command-line. Now that we have some `args` in our namespace, we can `args.rustle()` our `args.jimmies`.

	$ python argparse-example.py --help

	usage: Use the custom tool in a manner that keeps your jimmies unrustled.

	A custom tool for rustling or unrustling jimmies.

	positional arguments:
	  jimmies     Jimmies, in this instance, are a list of integers delimited by
	              spaces.

	optional arguments:
	  -h, --help  show this help message and exit
	  --rustle    The rustle flag determines if you would like further rustling of
	              your jimmies. Otherwise, this program will naturally seek
	              unrustlement.

    $ python argparse-example.py 4 8 1 2
	[1, 2, 4, 8]

	$ python argparse-example.py 4 8 1 2 --rustle
	[2, 8, 1, 4]

