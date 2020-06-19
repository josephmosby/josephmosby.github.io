---
layout: post
title: Cloning Postgres to Mongo in real time with Django
tags: code
---

Django comes baked with one major setback: it can't properly support non-relational databases. A few attempts to rectify this problem have been made, but none of them can handle Django's administration menu at the same time. So if your application simultaneously requires the speed of a non-relational database and the ease of the administration menu, you're going to need to figure out a way to run two databases - one relational, one not - and keep the two in sync. We're going to do that very thing with Postgres and MongoDB here.

You will need: 

* [pymongo](http://api.mongodb.org/python/current/)
* [Django signals (part of Django core)](https://docs.djangoproject.com/en/1.7/topics/signals/)

PyMongo provides us a convenient API to access MongoDB, while signals will allow us to perform certain actions upon saving a model. We begin by importing all of the necessaries and creating receiver functions to handle our signals:

	# models.py 

	from django.db import models
	from django.db.models.signals import post_save, post_delete
	from django.dispatch import receiver

	class MyModel(models.Model):
		pass

	@receiver(post_save)
	def save_mongo_instance(sender, **kwargs):
		pass

	@receiver(post_delete)
	def delete_mongo_instance(sender, **kwargs):
		pass

We use the `@receiver` decorator to indicate what event should trigger the `save_mongo_instance()` and `delete_mongo_instance()`. Our functions will fire immediately after a model saves to or deletes from our Postgres database (indicated by the post_save and post_delete parameters). These functions must also take in a sender (the Model triggering the method) and a fungible number of `kwargs`. One of these `kwargs` will be the specific Model *instance* we just saved or deleted.

These receiver methods will fire on *every* save or delete, regardless of the model that called it. If I have foreign key relationships, it won't make sense for me to save all of those into the database as their own Documents - I should be nesting those within other Documents. I need some way to dictate which models should and should not be saved as their own Documents in a Mongo collection.

	# models.py 

	class MyModel(models.Model):
		mongoable = True

	@receiver(post_save)
	def save_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

	@receiver(post_delete)
	def delete_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

I've added a property to `MyModel` that indicates it is "mongoable" (I made that word up). If `mongoable` is set to `True`, we'll save it to the Mongo database - otherwise we'll ignore the save event by returning out of the function.

Now we need to get the instance. 
	
	# models.py 

	@receiver(post_save)
	def save_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

	@receiver(post_delete)
	def delete_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

We extract the instance information - the specific data we just saved to Postgres - by pulling it out of the `kwargs` sent to our receiver function. Now we must parse them out! I created a helper utility to do this very thing and placed it in the `utils` directory of my Django project, so it looks something like this:

	mongoproject/
	|
	|--mongoproject/
		|
		|--settings.py
		|
	|--mongoapp/
		|
		|--__init__.py
		|--models.py
		|
	|--utils/
		|
		|--__init__.py
		|--mongo_clone.py

I've also modified `settings.py` to add my Mongo connection info:

	# settings.py

	MONGO_DB_HOST = 'localhost'
	MONGO_DB_PORT = 27017

And my mongo_clone.py utility looks [like this](https://gist.github.com/josephmosby/7ac22f01ccf738e94d7a):

	# mongo_clone.py

	import pymongo
	from django.db.models import Model
	from django.db.models.fields.files import ImageFieldFile
	from django.conf import settings

	def get_mongo_db():
		client = pymongo.MongoClient(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT)
		db = client.test
		return db

	def convert_fields(model):
		"""
		Recursive function to iterate over all fields in a Model.
		If the field is a ForeignKey, ManyToManyField or OneToOneField, 
		go into the model and recursively store fields.
		"""
		fields = model._meta.get_all_field_names()
		update_fields = {}

		for field in fields:
			try: 
				field_value = getattr(model, field)
				if getattr(field_value, 'all', None):
					"""
					Branch for a ManyToManyField.
					Iterate over each Model in and append data to a list.
					Add list to dictionary.
					"""
					fk_list = []

					for fk_model in field_value.all():
						fk_list.append(convert_fields(fk_model))

					update_fields[field] = fk_list

				elif isinstance(field_value, Model):
					"""
					Branch for a ForeignKey or OneToOneField.
					Create data for the Model and add to dictionary.
					"""

					update_fields[field] = convert_fields(field_value)

				elif isinstance(field_value, ImageFieldFile):
					"""
					Serialize an ImageField.
					"""
					try:
						update_fields[field] = field_value.path
					except ValueError:
						"""
						ValueError occurs if there is no actual File (i.e., is null).
						"""
						update_fields[field] = ""

				else:
					"""
					Branch for a standard field.
					Add data to the dictionary.
					"""

					if field == "id":
						update_fields["pg_" + model._meta.verbose_name + "_id"] = field_value
					else:
						update_fields[field] = field_value

			except AttributeError:
				"""
				ManyToManyFields will throw an AttributeError when trying to reference the parent.
				"""
				pass
				
				
		return update_fields

Let's walk through the branches of `convert_fields()` one by one. The function is designed to turn a Model into a dictionary of key/value pairs, iterating through each field and recursively digging into ForeignKeys and ManyToManyFields to created nested dictionaries. Our first two lines of the function create the primary dictionary and find the field names of the model.

We then begin a try/except block. Django ForeignKeys and ManyToManyFields store data in the Postgres database about their parent, but it's not specified directly in my Model. We deal with that by passing on an `AttributeError`. Next we loop through all fields.

It's perhaps most useful here to skip down directly to the `else` branch of this if/else statement. This is for our standard text and date fields - anything we can easily serialize. Our recursive function will always end up here. We'll continue to go deeper and deeper into our relationships as we're building our nested dictionaries for ForeignKeys, but once we have an object that has no relationships, we'll simply be serializing its fields with this branch.

Immediately above that branch is our test for an `ImageField`, which can't be neatly serialized. We tackle this by finding the path of the ImageFieldFile and attaching that to our dictionary.

Our first bit of recursion comes when we hit the branch above that, when we deal with ForeignKeys. Our FK model will be attached to the original model's ForeignKey field - but at the end of the day, it's just a standard model with fields that we could parse out with our bottom branch. We'll recursively call our `convert_fields` function on the model to do just that.

Our top branch deals with ManyToManyFields, which come through as a `Manager`. Managers are tough to detect, but they do have an `all()` method that no other field should have. We'll look for that method to find a ManyToManyField, then we're just looping through every attached Model and appending their keys to the dictionary.

Now we call our helper method as part of our receiver:
	
	# models.py 

	from utils.mongo_clone import get_mongo_db, convert_fields

	@receiver(post_save)
	def save_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

		update_fields = convert_fields(instance)

	@receiver(post_delete)
	def delete_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

And we'll save all this to the database by connecting to our DB and using a find_and_modify transaction:

	# models.py 

	from utils.mongo_clone import get_mongo_db, convert_fields

	@receiver(post_save)
	def save_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

		update_fields = convert_fields(instance)
		db = get_mongo_db()

	    mongo_instance = db.test.find_and_modify(query={"pg_instance_id": instance.id},
	                                            update={"$set": update_fields},
	                                            upsert=True,
	                                            full_response=True,
	                                            new=True)

	@receiver(post_delete)
	def delete_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

Deleting is far easier. All we have to do here is find the Mongo ID that corresponds to the deleted Postgres ID:

	# models.py 

	from utils.mongo_clone import get_mongo_db, convert_fields

	@receiver(post_save)
	def save_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

		update_fields = convert_fields(instance)
		db = get_mongo_db()

	    mongo_instance = db.test.find_and_modify(query={"pg_instance_id": instance.id},
	                                            update={"$set": update_fields},
	                                            upsert=True,
	                                            full_response=True,
	                                            new=True)

	@receiver(post_delete)
	def delete_mongo_instance(sender, **kwargs):

		if not sender.mongoable:
			return

		instance = kwargs.get('instance')

		db = get_mongo_db()

    	mongo_instance = db.test.remove( {"pg_instance_id": instance.id })

And we're cooking. We're still querying the original Postgres database - for now - but we'll fix that soon enough.