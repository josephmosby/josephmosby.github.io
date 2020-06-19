---
layout: post
title: Seeding a database with queues and threading
tags: code
---

Don't try this at home. There is no good reason to do this.

Moving on.

Let's say we wanted to seed a MongoDB database with a ton of records. And let's just say that we had a Django app connected to that Mongo database. We'd likely be using [django-nonrel](http://django-nonrel.org/) with its MongoDB connector. And let's again say that we have a models.py file that looks like this:

	# models.py

	from django.db import models
	from djangotoolbox.fields import ListField, EmbeddedModelField

	class Author(models.Model):
		name = models.CharField(max_length=60, blank=False)

	class Tag(models.Model):
		name = models.CharField(max_length=40, blank=False)

	class Article(models.Model):
		title = models.CharField(max_length=60, blank=False)
		subhead = models.CharField(max_length=140)
		date = models.DateField(auto_now=True)
		content = models.TextField()
		authors = ListField(EmbeddedModelField('Author'))
		tags = ListField(EmbeddedModelField('Tag'))

We've got some fairly standard models here - an Article with Tags and Authors embedded in. Now we'll need a seed file:
	
	# seed.py
	import os, sys, django
	import random
	from datetime import date, timedelta as td
	from time import sleep
	import Queue, threading

	sys.path.append('/path/to/my/project/mongotest/')
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mongotest.settings")

	from dbtest.models import Author, Tag, Article

Nothing too crazy worth noting here. I need to append my project folder to `sys.path` and configure the `DJANGO_SETTINGS_MODULE` environment variable so that my app `dbtest` is registered with the system. 

	# seed.py continued

	AUTHOR_FILE = 'authors.txt'
	TAG_FILE = 'tags.txt'
	CONTENT_FILES = ['text1.txt', 'text2.txt', 'text3.txt', 'text4.txt', 'text5.txt', 'text6.txt', 'text7.txt']
	TITLES = ['Numeric abstract base classes', 'The numeric tower', 'Notes for type implementors', 'Number-theoretic and representation functions', 'Decimal fixed point and floating point arithmetic', 'Rational numbers', 'Higher order functions and operations', 'Generate pseudo-random numbers', 'Functions creating iterators', 'Mapping operators to functions']
	DATE_DIFF = date(2014, 12, 31) - date(1999, 1, 1)

The contents of these files bear some explanation. I have an authors.txt file and tags.txt file that contain lists of authors and tags (presidents' names for authors and random words from Wikipedia for tags). I have seven textN.txt files that each contain lorem ipsum text. And I have some titles yanked from Python's `math` module. The `DATE_DIFF` is used to calculate days between January 1, 1999 and December 31, 2014. We'll use that last bit later.

	# seed.py continued

	def store_models(file):
	'''Initialize with tags and author names from text files.'''
		f = open(file)
		f_text = f.read().split('\n')
		for item in f_text:
			if file == 'tags.txt':
				new_tag = Tag(name=item)
				new_tag.save()
			elif file == 'authors.txt':
				new_author = Author(name=item)
				new_author.save()
			else:
				print('Whoa, not a file')
				return ""

	store_models(TAG_FILE)
	store_models(AUTHOR_FILE)

We continue this by creating a stack of tags and authors that we'll need later.

	# seed.py continued

	def prep_half_entry(q, contents, titles, dates):
		title = random.choice(titles)
		content = random.choice(contents)
		subhead = random.choice(titles) + " " + random.choice(contents)[:15]
		article_date = random.choice(dates)
		article = Article(title=title, subhead=subhead, content=content, date=article_date)
		article.save()
		q.put(article)

	def write_full_entry_to_db(q, tags, authors):
		sleep(0.05)
		article = q.get()
		authors_list = [random.choice(authors)]
		tags_list = [random.choice(tags)]
		article.authors.extend(authors_list)
		article.tags.extend(tags_list)
		article.save()

Here we have two functions that we're going to turn into lots of tiny little threads. The `prep_half_entry()` function takes four parameters: a queue and sets of contents, titles and dates. From there, it will haphazardly choose some titles, contents, subheads, and dates, and then save the article. It will then put that article on the Queue using the `q.put()` method - meaning we can access it from other threads. The `write_full_entry_to_db()` function expects to receive a Queue, a set of tags, and a set of authors. From there, it will pop the first Article it finds off the queue, then complete the entry with tags and authors. The `sleep(0.05)` is only in there to make the function stall so we can watch the queue grow.

	# seed.py continued

	q = Queue.Queue()
	contents = [open(x).read() for x in CONTENT_FILES]
	dates = [date(1999, 1, 1)+td(days=i) for i in range(DATE_DIFF.days + 1)]
	tags = Tag.objects.all()
	authors = Author.objects.all()

Here we build the Queue object a few other sources of data our functions need to complete their work. Remember that `prep_half_entry()` and `write_full_entry_to_db()` are just going to shuffle up entries to seed the DB.

	for i in range(0, 500):

		t_one = threading.Thread(target=prep_half_entry, args=(q, contents, TITLES, dates))
		t_two = threading.Thread(target=write_full_entry_to_db, args=(q, tags, authors))

		t_one.daemon = True
		t_two.daemon = True

		t_one.start()
		t_two.start()

		if q.qsize() >= 8:
			print q.qsize()

Here's where the magic happens. We're now going to spin up a thousand daemon threads and set them loose on this operation. `t_one` will be 500 threads of prepping half-completed entries and placing them in the queue. `t_two` will look for entries on the queue and finish them out before saving them to the database.

This sort of raw approach is suboptimal - if you'd like to do something like this at scale, use [Celery](http://www.celeryproject.org/). But it makes a cute little proof of concept.
