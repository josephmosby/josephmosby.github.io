---
layout: post
title: Rosa&#39;s Cosas&#58; Building a Twilio app to match &#64;kingsthings
---

The Washington Post said it best: ["Larry King has a special way of tweeting."](http://www.washingtonpost.com/blogs/style-blog/wp/2015/03/19/larry-king-has-a-special-way-of-tweeting-the-broadcast-legend-who-just-cant-retire-talks-about-his-new-media-way-of-life/) He calls a special phone line and leaves a tweet on a voicemail, which is then transcribed by an assistant and posted to Twitter. Lacking an assistant, I decided to build something to allow [@lbrosa](https://twitter.com/lbrosa) to call in a tweet using Twilio's transcription functionality. 

Our workflow here is simple, but rather confusingly documented by Twilio's stock documentation. 

1. Call a Twilio number tied back to one of our app URLs dedicated for transcription.
2. Build a Twilio Response object that includes a Record verb that contains a `transcribeCallback` redirect parameter, which will be another URL in our app.
3. Twilio will record the call and hit our `transcribeCallback` URL with the transcription text once it's finished.
4. We take our transcribed text and post it to Twitter.

What does that look like in Django? What will we need?

	# requirements.txt

	Django==1.7.7
	twilio==3.7.3
	django-twilio==0.8.0
	tweepy==3.3.0

	# other dependencies that these libraries will install for you

The `twilio` library is put out by Twilio and contains some helper functions so you don't have to build raw XML to send back to them. `django-twilio` is here to help with Django's freakouts about POSTing data without CSRF tokens. And `tweepy` talks to Twitter. We'll see where they all fall into place in `views.py`.

	# views.py 
	# part 1

	from django_twilio.decorators import twilio_view
	from twilio import twiml

	@twilio_view
	def transcribe_incoming(request):

		r = twiml.Response()
		r.say("What is your tweet?")
		r.record(maxLength=30, transcribeCallback="/playback/")

		return r

This view will answer an incoming call to our app. We build a TwiML Response and attach two Twilio verbs to it: `<Say>` and `<Record>`. Our `<Say>` verb takes in some text that Twilio's robot voice will read back to the caller. Our `<Record>` verb takes in a `maxLength` in seconds for recording. It also contains a `transcribeCallback` parameter - the URL we'll POST data to once the transcription is completed. No need to include `transcribe="True"`, as `transcribeCallback` will assume that.

Our caller will record a tweet and then hang up, kicking off Twilio's transcription. Note that our app doesn't have anything to do here until Twilio finishes our transcription and then POSTs the response to `/playback/`. 

	# views.py
	# part 2

	from django.http import HttpResponse
	from django_twilio.decorators import twilio_view
	from twilio.rest import TwilioRestClient
	from django.conf import settings
	import tweepy

	@twilio_view
	def playback(request):

		transcribed = request.POST['TranscriptionText']
		sent_from = request.POST['From']
		body = "Tweet Sent: " + transcribed

		auth = tweepy.OAuthHandler(settings.TWITTER_CONS_KEY, settings.TWITTER_CONS_SECRET)
		auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)

		api = tweepy.API(auth)
		api.update_status(status=transcribed)

		client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

		msg = client.messages.create(to=sent_from, from_=settings.TWILIO_PHONE_NUM, body=body)

		return HttpResponse("A-OK", status=200)

Twilio includes the transcription text in the POST data as well as the number the user called from. We'll need both of those. We'll also need all of the Twilio and Twitter settings that you should keep secure. This app assumes that you've created a corresponding Twitter app that has Read and Write access to your account. No oAuth silliness - just the direct post to your account.

We follow the vanilla instructions for updating a status with `tweepy` using the `TranscriptionText` from the POST data. We're then going to send that text back to the user via SMS to give them a confirmation that everything proceeded as planned. We close the loop with a 200 Response back to Twilio.

URL patterns are up to you, but should probably look something like this: 

	# urls.py

	urlpatterns = patterns('',
	    url(r'^transcribe/$', 'callme.views.transcribe_incoming', name='transcribe_incoming'),
	    url(r'^playback/$', 'callme.views.playback', name='playback'),
    )

No admin console needed, no database. Just two quick little views. 

Have fun with this! I've created a [Github repo](https://github.com/josephmosby/rosascosaspublic/) for the project with the full Django app in case it's useful.