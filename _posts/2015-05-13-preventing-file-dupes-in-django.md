---
layout: post
title: Preventing file dupes in files uploaded through Django
tags: code
---

Many Django applications make use of uploaded files that should never be re-uploaded again after they've been uploaded once. An example of this in action might be an image (one image embedded in a blog post might not be a big deal for a small site, but news sites often deal with licensed high-definition images used across several stories) or a large PDF with associated metadata (once the metadata is keyed in once, users shouldn't be asked to do so again). Let's talk about two design patterns to handle files, and ways we can deal with duplicates in each one. 

### The Attachment

With the Attachment design pattern, a file is part of the model as a Django [FileField](https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.FileField). This is useful if the file to be attached is known ahead of time and will be of a semi-predictable type (for example, a press release for a scheduled report that will be in PDF format). Two or three additional users may be writing blog posts on the report, and each of them plan to attach the report as well. We don't want to store a stack of extra copies of the file on the server - so how can we de-dupe them?

Our post is set up like so:

	from django.db import models

	class ReportPost(models.Model):
		file = models.FileField()
		file_sha1 = models.CharField(max_length=40)
		post_text = models.TextField()

		... etc ...

Our `ReportPost` has space for an uploaded file. We also have a `sha1` field here. Django can't automatically detect a duplicate file (`unique` is not supported for `FileFields` or any derivatives), so we need to take the SHA-1 text hash of the file in order to check if it's been uploaded already. We'll take care of that in the `ModelAdmin` for this model.

	from django.contrib import admin
	import hashlib

	def generate_sha(file):
		sha = hashlib.sha1()
		file.seek(0)
		while True:
			buf = file.read(104857600)
			if not buf:
				break
			sha.update(buf)
		sha1 = sha.hexdigest()
		file.seek(0)

		return sha1

	class ReportPostAdmin(admin.ModelAdmin):
		... stuff ...

		def save_model(self, request, obj, form, change):
			sha = generate_sha(obj.file)
			obj.file_sha1 = sha
			match_qs = ReportPost.objects.filter(file_sha1=sha)
			if match_qs.count() > 0:
				obj.file = match_qs[0].file

			obj.save()
				
We derive a SHA-1 hash for this file by reading in the first 100 megabytes of data and hashing it. In our `ModelAdmin.save_model` method, we store that SHA-1 with our model instance. We also run a query against the database for any model instances with that exact same SHA-1 (indicating a match), and replace our instance of the file with the previously uploaded file. 

### The File as Object

With this design pattern, files are part of a larger object that gives them relevance. Images in a newsroom app, for example, come with credits, licensing information, and various data about how often the image is used. In order to store that metadata about that image, we need a file object.

	# models.py

	class ImageObject(models.Model):
		caption = models.CharField(max_length=140)
		credits = models.CharField(max_length=140)
		image_file = models.ImageField()
		file_sha1 = models.CharField(max_length=40, unique=True)

	# admin.py

	class ImageObjectAdmin(admin.ModelAdmin):
		... stuff ...

		def save_model(self, request, obj, form, change):
			sha = generate_sha(obj.file)
			obj.file_sha1 = sha
			obj.save()

With this example, we add some uniqueness to our model, which gives us the ability to easily enforce that each image file will only have one set of metadata. Our app will throw an `IntegrityError` if a user tries to save a duplicate SHA-1 hash. We'll need to handle that `IntegrityError` and redirect our user to the previously uploaded image. We can do that using a new middleware object.

Middleware objects in Django quietly do their thing 99.9% of the time, and you'll never think twice about them. They're there for session authentication or CSRF enforcement - things that most of us take for granted. But you can easily add your own middleware with ease by adding a `middleware.py` file to your application and registering it with `settings.py`:

	# settings.py

	MIDDLEWARE_CLASSES = (
		'django.contrib.sessions.middleware.SessionMiddleware',
		... stuff ...
		'our_image_app.middleware.RedirectOnSHAViolation',
	)

And then in `our_image_app/middleware.py`:

	# middleware.py

	from django.db import IntegrityError
	from django.http import HttpResponseRedirect
	from utils import generate_sha # same func as before
	from our_image_app.models import ImageObject

	class RedirectOnSHAViolation():
		def process_exception(self, request, exception):
			if type(exception) == IntegrityError:
				if "our_image_app/imageobject" in request.path:
					sha1 = generate_sha1(request.FILES['image_file'])
					img = ImageObject.objects.get(file_sha1=sha1)
					return HttpResponseRedirect('/admin/our_image_app/imageobject/') + str(img.id))

I never said it was pretty.

Django's middleware system expects to see a class with a `process_exception` method that's really, really stupid. The middleware knows it has a request that caused an error, but that's about all that it knows. We have to do two checks to make sure that we're handling the right error here. First, we check that the `type` of error is `IntegrityError`. We have to run this check first because every single error in our app could potentially hit this method, so we need to filter for only certain types. Once I've confirmed that, I check to see if the `IntegrityError` came from the `ImageObject` model within `our_image_app` - and since `ImageObject` only has one unique field, I know an `IntegrityError` here must be a duplicate file. Once I've ascertained all of that, then I need to find the file I should have used and redirect the user there instead.

### Conclusions

SHA-1 hashes provide an easy way to compensate for Django FileFields' inability to enforce uniqueness by default. Handling those errors can be a bit messy, but we can create some custom middleware to handle any problems or extend our admin's built-in methods to help us out.

_Props to [@spiggy](https://twitter.com/spiggy), who had the original idea of using SHAs to look for duplicate files._