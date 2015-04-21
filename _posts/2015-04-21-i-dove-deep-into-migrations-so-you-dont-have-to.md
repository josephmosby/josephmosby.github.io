---
layout: post
title: I dove deep into a Django migration so you don&#39;t have to
---

It is 2015. I expect to be able to forget my webapp database exists once I plug my credentials into a configuration file. From then on out it should be nothing more than feeding query terms into functions and getting lists back.

*AND YET.*

Back in the old days of Django, you had to cut all your database changes yourself. If you made schema changes to an app after you had run `syncdb`, you had to go figure out how to manage the changes with `ALTER TABLE` statements. Then Ruby on Rails came along with its cute little migrations that did all the hard work for you. `south` came along to help Django do the same, and then we finally just decided to roll `south` into Django core. If you make a change to a model, you run `manage.py makemigrations && manage.py migrate` and everything's happy. 

Well, until you've got crazy errors spitting out of your console because your relationships changed on three apps at once and two developers working on different portions of the project established a bunch of weird subclassing and EVERYTHING is going to pieces. 

And then we must deal with migrations. Let us begin.

A sample migration file (for a model called `Post`) looks something like this:

	# -*- coding: utf-8 -*-
	from __future__ import unicode_literals
	from django.db import models, migrations

	class Migration(migrations.Migration):

		dependencies = []

		operations = [
			migrations.CreateModel(
				name='Post',
				fields=[
					('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
					('publication_date', models.DateTimeField(blank=True, null=True)),
					('title', models.CharField(max_length=255)),
					('content', models.TextField()),
				],
				options={},
			),
		]

When `manage.py migrate` is run, Django will read this migration file, see the operations and depencies in the `Migration` class, and execute appropriate transactions against the target database. 

Now, let's say that we had an `Author` model (to track `Post` authors) and establish a `ForeignKey` here back to the `Author`. This migration would then look something like this:

	 # -*- coding: utf-8 -*-
	from __future__ import unicode_literals
	from django.db import models, migrations

	class Migration(migrations.Migration):

		dependencies = [
			('authors', '0001_initial'),
		]

		operations = [
			migrations.CreateModel(
				name='Post',
				fields=[
					('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
					('publication_date', models.DateTimeField(blank=True, null=True)),
					('title', models.CharField(max_length=255)),
					('content', models.TextField()),
					('author', models.ForeignKey(to='authors.Author'))
				],
				options={},
			),
		]

What's changed? We've added our first dependency! We can't have a `ForeignKey` in the database unless we have an `authors` table. `manage.py migrate` will sniff out this migration, then go check to make sure it's run against the database _before_ we run this `Post` migration. We can then make use of the `authors` foreign key in our model. 

When Django runs those migrations, it will execute the proper SQL commands against your database backend of choice (which you can see if you run `manage.py sqlmigrate`), then store a record of the migration in a special `django_migrations` table. This is how Django checks to see if a migration has been run already. If you've already got data and schema present in your database (but no migrations), `manage.py migrate --fake` will generate a migration file and add it to this table, but won't do any further work to the database. 

I can think of at least one "gotcha" with all this, as it's causing all sorts of trouble for my team at the moment. It's possible to attach widgets to objects that include `ForeignKey` relationships. This can really, really trip migrations up. We've had to solve it by migrating everything _except_ the field that includes the foreign key, then manually migrating things in order, but even that's a grab bag. 

But aside from that, migrations aren't that scary! Don't go coding your own, though.

_but if you did you could do it just by running `manage.py makemigrations --empty yourappname` and go from scratch_