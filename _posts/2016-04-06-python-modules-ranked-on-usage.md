---
layout: post
title: Python modules ranked on usage and what that says about the Python ecosystem
---

A few days ago, I asked myself a simple question: what are the most (and least) popular Python modules from the standard library? Or rather, I decided to ask GitHub. There are at least a dozen syntactic ways you can bring a module into a piece of Python code, but I thought it might be easiest to simply search for "import {{module}}" and see how many results came back. There will of course be some false positives and false negatives, but on average, this approach can serve as a proxy for total usage.

Here are the results for the most used libraries:

1. `os` (3,279,697 results)
2. `sys` (3,081,854 results)
3. `re` (1,304,857 results)
4. `datetime` (1,076,425 results)
5. `shutil` (968,583 results)

And the results for the least used:

1. `pathlib` (0 results)
2. `fpectl` (37 results)
3. `zipapp` (48 results)
4. `tracemalloc` (397 results)
5. `nis` (484 results)

The full dataset can be found [here](/files/python_modules.csv), for the curious.

What do these usage patterns say about us as Python developers? And why would the language developers keep these almost completely unused modules around?

I expected `os` and `sys` to be heavily used, though I did not expect them to blow away the #3 and #4 competitors as much as they did. Let's think about what they do. These are big, complex libraries that operate at the most basic levels of the operating system. If you want to traverse a directory tree and pop out all of the text files, you're using `os`. If you have a script that's dependent on system state - or even one that just needs to kill itself in a hurry - you're using `sys`. So with these modules being so heavily used, you're looking at a lot of usage by system engineers, operations teams, and any piece of software who has to talk to a machine directly instead of just buzzing around in application space. `re` and `datetime` are somewhat expected to land where they are, regular expressions and date management are both cornerstones of software development. `shutil` surprised me a little bit. I thought that `os` and `sys` and the standard `read()` and `write()` system calls would do most of the file work and something like `logging` or `unittest` would fill out the last of the top 5, but it looks like there's still a lot of pushing files around left to do.

So if you're a Python dev, there's a good chance you're doing a decent amount of work pushing files around and investigating your operating system. That makes complete sense - Python was started as a systems and automation scripting language, and that's still at its core even if we're now writing more complex software with it.

Now let's take a look at the bottom of the barrel.

`pathlib` is one of the newest modules added to the standard library, and it's currently only in there on a provisional basis. It provides a "simple hierarchy of classes to handle filesystem paths and the common operations users do over them." The usage rationale comes from [PEP 428](https://www.python.org/dev/peps/pep-0428/), citing the previous attempt to provide these features in [PEP 355](https://www.python.org/dev/peps/pep-0355/) and the [path.py module](https://github.com/jaraco/path.py) that treats filepaths like first-class players in the language. `pathlib` clearly has not taken off yet, but it's still new in the language.

`fpectl` deals with floating point exceptions. The reasoning for its low usage is clear on the [man page](https://docs.python.org/3/library/fpectl.html): this module is not built by default, and its usage is discouraged and dangerous. `zipapp` does something I didn't even know you could do in Python: run Python executables that have been zipped up into archives directly. `tracemalloc` lets debuggers sort through memory problems in their code, and it sort of makes sense to me that this probably doesn't make it into committed code that often. Finishing us out, `nis` is incredibly niche: it provides a wrapper around the Sun Network Information Service.

It's interesting to me that some of the least-used modules share some similarities with the most-used: they're all about system management. They're even experiments with new ways to approach system management. There's a lot that can be done with Python, but when it comes to the core library - the operating system is king.