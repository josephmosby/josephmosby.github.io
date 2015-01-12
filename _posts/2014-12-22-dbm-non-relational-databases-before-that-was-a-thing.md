---
layout: pymod
title: DBM - non-relational databases before that was a thing
tags:
- pymod
---

In 1970, databases were all the rage. Big stinkin' associative databases, mostly sold by IBM and running on a mainframe. A gentleman by the name of Edgar Codd was starting to beat the drum on this idea called a "relational" database, but IBM had no interest in cannibalizing the sales of its IMS software in favor of this new-fangled relational thingy. Until Larry Ellison started competing with IBM with his Oracle database, everybody was using these associative databases.

Everybody, of course, included AT&T. They commissioned their own DB engine, dubbed "DataBase Manager", in 1979. DBM stored data in a key-value array, restricted writes to a single process at a time, and used hash tables to implement the data structure. UC Berkeley would go on to release ndbm to support concurrency, and several other groups released their own open source clones to succeed the original dbm structure. 

With Python, you can have your very own dbm-style database using the `anydbm` module. Throw back to the seventies with this little guy: 

	import anydbm

	db = anydbm.open('mydb', 'c')

	db['home'] = 'www.josephmosby.com'
	db['docs'] = 'docs.python.org'

	for k, v in db.iteritems():
		print k, ': ', v

	db.close()

This snippet of code will open up a dbm-style database (and create it if it doesn't exist - note the 'c' flag), add some values in a key-value fashion, print those values back, and close the database. It's like a Python dictionary but you can store it. 

The next time you're working on a system from the 1980s that happens to know how to run Python scripts, please shoot me a note and let me know how awesome this `anydbm` module is!