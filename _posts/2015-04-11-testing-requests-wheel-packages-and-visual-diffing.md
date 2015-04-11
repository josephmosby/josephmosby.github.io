---
layout: post
title: Testing requests, wheel packages, and visual diffing
---

	No matter how many unit tests you write, you'll never write a test for "is there a pony on the page?"
	- Dan Vanderkam, on an animated pony GIF appearing in Google production

I do not consider myself to be a very good tester. I am aware that I should write tests, but I am only vaguely certain of what I am supposed to be testing, and I am even less certain about which packages I'm supposed to use to test. Should I bust out `unittest`? Do I use Django's testing harness? And so Saturday became a day of testing for me. 

[Ian Cordasco](https://github.com/sigmavirus24) opened the door with an extremely scary question: how do you test web applications that expect access to the internet? We can't fake a web service (because then we'd have to test two separate things) and we can't just feed it expected data (because that's not a test). How do we isolate the two? 

Cordasco mentions a stack of libraries facilitate mock web services:
- [responses](https://pypi.python.org/pypi/responses/0.3.0)
- [httpretty](https://pypi.python.org/pypi/httpretty)
- [requests-mock](https://pypi.python.org/pypi/requests-mock)
- [mock](https://docs.python.org/3/library/unittest.mock.html)

These do many of the same functions with varying degrees of complexity, but the core principle is the same: _you cannot assume access to the internet in a predictable fashion when doing unit tests._ I have some digging to do into these libraries.

On a more niche use case, [Olivier Grisel](https://github.com/ogrisel) introduced me to wheel packages this afternoon. A [wheel package](https://packaging.python.org/en/latest/distributing.html#wheels) is a special package distribution format for Python packages that allows lightning fast installation and distribution. It's easy enough to use [TravisCI](https://travis-ci.org/) for deployment testing on *nix-based systems, but what about for Windows packages? Grisel and his team use [AppVeyor](http://www.appveyor.com/) to package scikit-learn on Windows systems. The tests can be automated, and the speed can't be beaten.

And finally, the pony.

[Dan Vanderkam](https://github.com/danvk)'s co-worker once accidentally shipped a pony to production. He didn't mean to - he was testing perfectly valid code and testing CSS animations at the time. The code passed peer review and all of the unit and integration tests. It just so happened to have a pony on it. And so his colleague was compelled to write [dpxdt](https://github.com/bslatkin/dpxdt) (pronounced "depicted") to do automated visual diff testing of new builds. `dpxdt` generates and stores screenshots of releases, then compares the two pixel-by-pixel to spot changes. If something breaks, `dpxdt` ships with a number of ways to showcase the changes.

There's _so much_ out there for testing. Special thanks to these presenters for bringing their slices of it to PyCon. 
