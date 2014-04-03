---
layout: post
title: Hacking Confirmation Emails on the Fly with Mailgun
---

I just finished slinging together some code for a confirmation email system for an email advocacy campaign using [CQRC Engage](http://corporate.cqrollcall.com/cqrcengage). Engage has a fairly simple set of tricks: it provides you with a Javascript-based widget to write a letter to your legislators, then submits that letter through whichever digital channel the legislator uses. As part of its process, it runs a check to find your particular legislator based on street address and postal code, then tailors the messages for that particular person. Engage doesn't have an email confirmation sent to you as part of your advocacy, so I built one.

Engage accepts letter submissions via that Javascript widget, then stores data about that advocate, the target, and the message itself in a database accessible via an API. This is all we need to begin constructing our confirmation email system. We're going to use [Mailgun](http://www.mailgun.com) for this task, which is an API-based system that accepts HTTP POST requests and turns them into emails at your command. Without further ado, let's start building.

I'm first going to build out a series of tiny classes that I'll use to power my app. In this case, we'll need four: one for the Advocate who sent a message, one for the Target, one for the Sent Message, and one for the Confirmation Email. They look something like this:

```python
class Advocate:
	def __init__(self, first_name, last_name, email):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		
class Target:
	def __init__(self, first_name, last_name, title):
		self.first_name = first_name
		self.last_name = last_name
		self.title = title
		
class SentMessage:
	def __init__(self, sender, recipients, message_subject, message_text):
		self.sender = sender # who should be an Advocate
		self.recipients = recipients # a list of Targets
		self.message_subject = message_subject
		self.message_text = message_text

class ConfirmationEmail:
	def __init__(self, sent_message):
		self.message_sent = sent_message
```

This is all stuff I'm going to extract from Engage without any further processing. I'm also going to go ahead and construct my confirmation email template using Jinja's syntax, which will accept data from these classes you see above.

```
<html>
	<head>
		<meta charset="UTF-8" />
	</head>
	<body>
		<p>Dear \{\{ first_name \}\} \{\{ last_name \}\}:</p>
		
		<p>\{\{ confirmation_leadin }}</p>
		
		\{% for recipient in recipients  \%}
			\{\{ recipient.first_name }} \{\{ recipient.last_name }}, \{\{ recipient.title }}
			<br />
		{% endfor %}
		
		<br />
		
		<p>SUBJECT: \{\{ message_subject }}</p>
		
		\{\{ message_text }}
	</body>
</html>
```

So far so good. You can see here that we've got a "confirmation_leadin" variable that doesn't seem to line up with any of our other tags. We added some introductory text into our emails as a "thank you" before including the text of the message and the list of targets it was sent to. Next step is to add on some basic work to begin converting the plain text messages out of Engage into HTML-based messages using [Markdown](https://pythonhosted.org/Markdown/reference.html). Then we'll use that, along with some of the data from our classes, to populate our Jinja template.

```python
# other lines truncated for brevity
class ConfirmationEmail: 
	def __init__(self, sent_message):
		self.message_sent = sent_message
		self.sanitized_message = markdown.markdown(sent_message.message_text, safe_mode='replace')
	
	def create_confirmation_text(self):
		self.confirmation_message = template.render( 
									{"first_name" : self.message_sent.sender.first_name,
								   	"last_name" : self.message_sent.sender.last_name, 
								   	"targets" : self.message_sent.recipients,
								   	"confirmation_leadin" : CONFIRMATION_LEADIN,
								   	"message_subject" : self.message_sent.message_subject,
								   	"message_text" : self.sanitized_message})
```

We're almost there! But now we just need to actually fire off that email, which requires a simple HTTP request using the [requests](http://docs.python-requests.org/en/latest/) library.

```python
# other lines truncated for brevity
class ConfirmationEmail: 
	def __init__(self, sent_message):
		self.message_sent = sent_message
		self.sanitized_message = markdown.markdown(sent_message.message_text, safe_mode='replace')
	
	def create_confirmation_text(self):
		self.confirmation_message = template.render( 
									{"first_name" : self.message_sent.sender.first_name,
								   	"last_name" : self.message_sent.sender.last_name, 
								   	"targets" : self.message_sent.recipients,
								   	"confirmation_leadin" : CONFIRMATION_LEADIN,
								   	"message_subject" : self.message_sent.message_subject,
								   	"message_text" : self.sanitized_message})
	
	def send_confirmation_message(self):
		return requests.post(MAILGUN_DOMAIN, auth=("api",API_KEY), 
								data={"from": DEFAULT_SENDER,
									  "to": [self.message_sent.sender.email],
									  "subject": CONFIRMATION_SUBJECT,
									  "html": self.confirmation_message})
```

We need one final bit to tie it all together - our script that checks the Engage system for new messages, downloads the data and then generates email templates out of it. I'm using pseudocode for some of the Engage API calls, but you'll get the general idea.

```python
if __name__ == "__main__":
	token = cq.login('user','password')
	actions = getActions(token)
	
	# store Actions to our owned database
	# the StoreActions formula was all written to check for anything already in the database and filter out those results
	
	conn = db.connect('db-location')	
	storeActions(conn, actions)
	
	# now we retrieve unconfirmed actions
	# this returns me a dictionary in the format { advocateId: {messageId: X, targets: [Y, Z, ...]}}  
	
	unconfirmed = cq.retrieveAllUnconfirmed(conn)
	
	for advocateId in unconfirmed.keys():
		advocate = cq.getAdvocate(token, advocateId)
		sender = Advocate(first_name = advocate["first_name"], last_name = advocate["last_name"], email = advocate["email"])
		recipients = []
		for targetId in unconfirmed[advocateId]["targets"]:
			target = cq.getTarget(token, targetId)
			recipients.append(Target(first_name = target["first_name"], last_name = target["last_name"], title = target["title"]))
		
		message_delivered = cq.getMessage(token, unconfirmed[advocateId]["messageId"])
		sent_message = SentMessage(sender = sender, recipients = recipients, message_subject = message_delivered["message_subject"], message_text = message_delivered["message_body"])
		
		confirmation_email = ConfirmationEmail(sent_message)
		confirmation_email.create_confirmation_text()
		
		confirmation_email.send_confirmation_email()
	 
	# then finally, mark those as confirmed in our database
	
	cq.markAsConfirmed(conn, unconfirmed.keys())
	
And that's it. We've built out a confirmation email system using Python - not very pretty, but it sure knows how to get the job done. Our final task is to run this puppy on a schedule using cron:

`$ env EDITOR=nano crontab -e`

```
*/3 * * * * /path/to/your/script
```

That will set up a cron job that runs every 3 minutes and executes our confirmation email script. We're ready to run this live, and -- barring anything catastrophic like a server crash -- it's relatively error proof. The script is designed to just fail silently and re-open every session if a script can't finish execution, so if a script misfires we'll just pick up those confirmation emails in the next batch three minutes later.

I'm a Mailgun convert after this. It's perfect for setting up simple email messages and automating them. The fact that I hacked this together in a few hours with most of that time dedicated to parsing through Engage's API documentation shows the ease of Mailgun's system. I'm all for it.