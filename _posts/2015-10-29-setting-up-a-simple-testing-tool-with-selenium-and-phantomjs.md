---
layout: post
title: Setting up a simple testing tool with Selenium and PhantomJS
---

Okay, this will be a short one, but I've just set up a minimalistic testing tool using Python, Selenium and PhantomJS and wanted to put it out there. Let's get cracking.

Start off by installing PhantomJS using Homebrew:

	$ brew install phantomjs

And then move on to add Selenium into the mix (assuming still that you're using Python):

	$ pip install selenium

And now let's build our first test case. I'm working as part of a Django app so I'll be using the Django `TestCase` object, but this will work very similarly with Python's core `unittest.TestCase`. 

	import os
	os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '127.0.0.1:9001'
	
	from django.test import LiveServerTestCase
	from selenium import webdriver

	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.PhantomJS()

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()

That's all it takes to get started. Honestly. Just install PhantomJS through Homebrew and Selenium through pip, and you're ready to get testing. Django's `LiveServerTestCase` needs a `DJANGO_LIVE_TEST_SERVER_ADDRESS`, so I've set one of those up as an environment variable. The `setUpClass()` and `tearDownClass()` methods are part of the `LiveServerTestCase` class, and are used to initialize behavior when the tests begin to run or to close things no longer needed after the test is completed. In this situation, we're using `setUpClass()` to set up our PhantomJS instance that we'll subsequently close in `tearDownClass()`.

With my particular test situation, I needed to execute some JavaScript on each page I planned to test. That JavaScript would return a variable, set to either 1 or 0 based on the state of an object on the page. Here's how we'll extend our code to do that:

	import os
	os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '127.0.0.1:9001'
	
	from django.test import LiveServerTestCase
	from selenium import webdriver

	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.PhantomJS()

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()

	def test_one_or_zero_on_link_one(self):
		self.driver.get('http://127.0.0.1:9001/linkone')
		should_be_zero = self.driver.execute_script('return case.a')
		self.assertEqual(should_be_zero, 0)

	def test_one_or_zero_on_link_two(self):
		self.driver.get('http://127.0.0.1:9001/linktwo')
		should_be_one = self.driver.execute_script('return case.a')
		self.assertEqual(should_be_one, 1)

I've now added two official tests to the mix. I'm asserting that on {DOMAIN}/linkone, there should be a JavaScript object called `case` with a property `a` that's set to zero. On {DOMAIN}/linktwo, that property should be set to one. In these two tests, I open the links up in PhantomJS (something you'll never see, by design). I then execute JavaScript on the pages and pick up the return values with `self.driver.execute_script()`. This allows me to tap some of the context of the page state through JavaScript.

My tests did not need anything much more complex than that, but I'm looking forward to using this in several other contexts in future tests. PhantomJS is wicked fast compared to running the same code using Selenium's Firefox or Chrome drivers. And being able to plug it into on-page JavaScript (maybe even tag-teaming with QUnit) makes it that much more appealing.