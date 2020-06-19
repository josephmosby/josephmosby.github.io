---
layout: post
title: Combining pickle and anydbm to form shelve
tags: code
---

Now that we've talked about both [pickle](http://josephmosby.com/2015/01/12/storing-objects-with-the-best-named-module-ever-pickle.html) and [anydbm](http://josephmosby.com/2014/12/22/dbm-non-relational-databases-before-that-was-a-thing.html), we can now talk about marrying the two with `shelve`. The `shelve` module brings `pickle` functionality to dbm-style databases, allowing us to store massive data entries in dictionary form without the expected performance hit. It's the middle option between a full-on database implementation and simple flat file storage. 

We create a new shelf like so:

	import shelve

	s = shelve.open('shelving', flag='c') # the open() method is a wrapper around anydbm.open()

	s['name'] = "Joe"

	s.close()

A shelf is created by using the `shelve` module's `open()` method, a wrapper around `anydbm.open()`. Once we have that shelf, we can treat it much like we would a dictionary. We save a value by specifying a dictionary key/value pair. Finally, we close the filestream. 

Reading data from the shelf is equally simple:

	import shelve

	s = shelve.open('shelving', flag='r')

	print s['name']

	s.close()

By default, a shelf does not save modifications to volatile object structure. We see this in the following example:

	import shelve

	s = shelve.open('shelving', flag='c') # the open() method is a wrapper around anydbm.open()

	s['name'] = {}

	s.close()

	s = shelve.open('shelving')

	s['name']['fname'] = 'Joe'
	s['name']['lname'] = 'Mosby'

	s.close()

	s = shelve.open('shelving')

	print s['name'] # will print {}

	s.close()

However, if we enable `writeback` when we open the shelf, we can make direct changes to an object. (warning: performance will take a hit as this will open a potentially massive object in memory)

	import shelve

	s = shelve.open('shelving', flag='c') # the open() method is a wrapper around anydbm.open()

	s['name'] = {}

	s.close()

	s = shelve.open('shelving', writeback=True)

	s['name']['fname'] = 'Joe'
	s['name']['lname'] = 'Mosby'

	s.close()

	s = shelve.open('shelving')

	print s['name'] # will print {'fname': 'Joe', 'lname': 'Mosby'}

	s.close()

And that's where we stand with `shelve`. Not too much to it - just a little persistence library built for a very niche database format.
