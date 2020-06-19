---
layout: post
title: Where did my application go? and other tails from the log files
tags: code
---

I woke up this morning to yet another fun little situation from my application. As opposed to the prior set of errors, where response times were creeping up into the uncomfortably high range, this is exactly the opposite: the application stops responding to anything. Here's what that graph looks like in New Relic:

![](/images/errors2.png)

At 7:11AM, my application simply dies, according to New Relic. Into the breach!

I think that I likely only need about a hundred thousand lines of my logs to get back to the timeframe in question, so let's cull those out and locate anything happening in the 7:10-7:19 timeframe:

	$ tail -100000 django-www.log > outage.log
	$ grep -m 1 -n "07:1" django-www.log

	2825:{address space usage: 3589083136 bytes/3422MB} {rss usage: 318144512 bytes/303MB} [pid: 8510|app: 0|req: 4874/239423] [IP ADDRESS] () {50 vars in 1552 bytes} [Mon Oct 19 13:07:10 2015] GET /petro/s/90050/hillary-clinton-won-wont-always-be-this-way => generated 42453 bytes in 302 msecs (HTTP/1.1 200) 3 headers in 250 bytes (2 switches on core 17)

Whoops, too far. Let me slice this up a little bit more and back it up a few minutes.

	$ tail -30000 outage.log | grep -m 1 -n "Oct 20 07:10"

	13411:{address space usage: 3518570496 bytes/3355MB} {rss usage: 126271488 bytes/120MB} [pid: 11089|app: 0|req: 4972/319841] [IP ADDRESS] () {44 vars in 751 bytes} [Tue Oct 20 07:05:01 2015] GET /2012/04/the-land-of-hope-and-dreams.php => generated 58612 bytes in 41 msecs (HTTP/1.1 404) 2 headers in 95 bytes (2 switches on core 230)

Okay, so I'm going to slice out the last 16,589 lines, which will start me close to the beginning of the outage:

	$ tail -16589 django-www.log > outage.log
	$ sed -n 1,3500p outage.log > temp.log && mv temp.log outage.log

Let's get started. I'm going to look for the point where my app started throwing 500 errors.

	$ grep -m 20 -n "HTTP/1.1 500" outage.log

That prints out the first 20 lines of my application throwing 500 errors, and a lot of them are on things that I know shouldn't 500. I'm going to dig into my Sentry error logging to see what the problem is, and...crap.

At some point, I or one of my teammates accidentally removed the Sentry and Raven configuration from our Django app, so we haven't actually captured any of these errors. Awesome. This might be a dead end for now. I'm going to add the configuration lines back into the app:

	INSTALLED_APPS = (
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'raven.contrib.django.raven_compat'
	    ... other apps ...
	)

	import raven
    RAVEN_CONFIG = {
        'dsn': 'RAVEN KEY HERE',
    }

That's a frustrating dead end, but it's something we should have caught. I'm adding a simple test case into our test suite to make sure it doesn't happen again.

	from django.test import TestCase
	from django.core.management import call_command

	class TestRavenUp(TestCase):

		def test_raven_up(self):
			stdout_backup = sys.stdout
			sys.stdout = open('/tmp/raven_up', 'w')
			call_command('raven', 'test')

			f = open('/tmp/raven_up', 'r')
			config = f.read()
			f.close()

			sys.stdout = stdout_backup
			self.assertTrue('[MUH SERVER NAME]' in config)
			self.assertTrue('[MUH APPLICATION KEY]' in config)

			print('Inspect [MUH SENTRY SERVER] to note that event has been logged.')

			os.remove('/tmp/raven_up')

That will spit out a test event to Sentry if we have everything configured appropriately. Hopefully I'll have an update with error logs the next time it happens (but I hope it doesn't happen again).