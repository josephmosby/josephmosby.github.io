---
layout: post
title: Up and Running with Flask on a Brand New Linode
---

Tonight, I'm building a minimalistic Flask app that will run on Linode. Flask is a relatively new framework for me. I've dealt with CentOS, nginx, and uwsgi at work, but I've never tried to get them installed on my own. Time to get started.

### Step 1: Install and configure nginx, round 1

I am skipping over the step where we create a CentOS 7 machine from the Linode dashboard. I can't think of a good way to explain that one without screenshots. Let's assume we have one, and let's install the necessaries on it.
	
	$ yum install epel-release
	$ yum install nginx

Okay! That was simple enough. Here we've installed nginx, which will allow us to serve up our web pages. I want to start here because I like the feedback of knowing that I'm serving up web pages from the very start.

I know that I plan to serve multiple sites off of this one server, so I need to adjust my domain and nginx configuration accordingly. In Namecheap, I've created 2 A records - dashboard.mosby.io and www.mosby.io - which I'll both point at this server's IP address. I'll let nginx sort out the parsing.

	# /etc/nginx/nginx.conf

	... # stuff here that you shouldn't remove

	http {

		... # more stuff here that you shouldn't remove

		server { 
			listen	80;
			server_name	www.mosby.io;
			root /var/www/main;
		}

		server {
			listen	80;
			server_name	dashboard.mosby.io;
			root /var/www/dashboard;
		}
	}

nginx has a configuration file called `nginx.conf` that we're going to modify to serve our sites. Here, we've said that any request incoming will either be for `www.mosby.io` or `dashboard.mosby.io`. If it's for `www`, we're going to serve content from `/var/www/main`. If it's for `dashboard`, we're going to serve content from `/var/www/dashboard`. We can test this out by creating two text files:

	# /var/www/main/index.html

	Hello, www.mosby.io!

AND

	# /var/www/dashboard/index.html

	Hello, dashboard.mosby.io!

Assuming that you've already pointed your two subdomain to your Linode's IP address, these will each display their respective content. Success!

### Step 2: Install Python3, Flask and uWSGI

This is the part I know least about this entire process. Let's start by installing Python 3, pip, and a version of `virtualenv` that's cool with all of this:
	
	$ yum install python34
	$ wget https://bootstrap.pypa.io/get-pip.py
	$ python3.4 get-pip.py

Now I'm going to move into my dashboard folder and create the application. 

	$ cd /var/www/dashboard
	$ virtualenv venv
	$ source venv/bin/activate

We've got a local instance of Python3 and pip now. Time to get uWSGI and Flask.

	$ pip install uwsgi flask

Wait hold on. uWSGI just crapped out on installation. I missed something. The scary error message looks like this:

	Command "/var/www/dashboard/venv/bin/python3.4 -c "import setuptools, tokenize;__file__='/tmp/pip-build-5a_chnf_/uwsgi/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-8zr4gl3_-record/install-record.txt --single-version-externally-managed --compile --install-headers /var/www/dashboard/venv/include/site/python3.4/uwsgi" failed with error code 1 in /tmp/pip-build-5a_chnf_/uwsgi

But that's not the root of the problem. I've got to scroll up the stack trace for that.

	In file included from plugins/python/python_plugin.c:1:0:
    plugins/python/uwsgi_python.h:2:20: fatal error: Python.h: No such file or directory
     #include <Python.h>

I don't have Python headers installed on this system! Let's see if I can do that.

	$ yum install python34-devel
	$ pip install uwsgi flask

Okay, that worked!

And now, let's convert our little test HTML from before into a Flask app. We're then going to remove the HTML file, which will let us confirm that we've actually set of Flask and uWSGI correctly when we see it again. I'm going to do some work here using the `vi` editor, but if you're not familiar with it, please replace the `vi` commands with `nano`. It's simpler.

	$ vi app.py

	from flask import Flask
	application = Flask(__name__)

	@application.route("/")
	def helloworld():
		return "Hello, dashboard.mosby.io on Flask!"

	if __name__ == "__main__":
		application.run(host='0.0.0.0')

	$ rm index.html
	$ python app.py

I can see that I've done it all right by going to my new homepage in my browser! Visiting dashboard.mosby.io:5000 will show me my updated page. 

### Step 3: Configure uWSGI Serving

We've got ourselves a basic skin of an application, so let's hook it up to nginx through uWSGI.

	$ uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi

It works! Exactly the same way it did when we ran the application directly. Let's build a `.ini` file so we can do this more repeatedly.

	$ vi dashboard.ini

	[uwsgi]
	module = wsgi

	master = true
	processes = 5

	uid = ghost
	socket = dashboard.sock
	chown-socket = ghost:nginx
	chmod-socket = 660
	vacuum = true

	die-on-term = true

This `ini` file does a few things for us. It points to the wsgi module, sets it in master mode, and spawns 5 processes of the app. It also ties to the uWSGI process to a Unix socket, and will remove (vacuum) that socket when the process stops.

I'm also specifying that the `ghost` user will own this process. (I've been doing all of this work as `root`, which is not a good practice for running the application) I now need to create the ghost user and add it to the nginx group.

	$ useradd ghost
	$ usermod -a -G nginx ghost

Verify that you did it right:

	$ id ghost

You should see the `ghost` user attached to the nginx group. Onward!

### Step 4: Start on Boot

When our server comes online, we want our uWSGI app to be available immediately. Let's start by creating a service file in our `/etc/systemd/system` directory.

	$ vi /etc/systemd/system/dashboard.service

	[Unit]
	Description=uwsgi instance to serve dashboard
	After=network.target

	[Service]
	User=ghost
	Group=nginx
	WorkingDirectory=/var/www/dashboard
	Environment="PATH=/var/www/dashboard/venv/bin"
	ExecStart=/var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini

	[Install]
	WantedBy=multi-user.target

There is black magic going on here that I need to dig into more. I don't know _why_ we do all of these things, but I do know that we're specifying the working directory, and the environment, and what should happen when we start things up. Which we'll do now.

	$ systemctl start dashboard
	$ systemctl enable dashboard

### Step 5: Proxy Requests from Nginx

Now it's time that we return to our `nginx.conf` file. We need to modify our dashboard server block to handle the uwsgi application.

	# /etc/nginx/nginx.conf

	... # stuff here that you shouldn't remove

	http {

		... # more stuff here that you shouldn't remove

		server { 
			listen	80;
			server_name	www.mosby.io;
			root /var/www/main;
		}

		server {
			listen	80;
			server_name	dashboard.mosby.io;
			
			location / {
				include uwsgi_params;
				uwsgi_pass unix:/var/www/dashboard/dashboard.sock;
			}
		}
	}

	$ nginx -t <-- test your configuration
	$ service nginx reload

And now we go to our browser and punch in dashboard.mosby.io, and... crap.

502 Bad Gateway. What did I do wrong here? That error means nginx can't talk to our application.

Ahh, I've been doing all this as root. Everything is currently owned by root, which means that neither `ghost` nor `nginx` can see my dashboard socket. Let's change that. 

	$ chown ghost:nginx /var/www/dashboard
	$ service nginx reload
	$ systemctl restart dashboard

And, we're back, folks!

That's a basic configuration for getting an Flask/uWSGI/nginx app up and running on a CentOS Linode box. If you decide to do something other than CentOS, most of it should still work, but the initialization service script will probably not. You can browse the repository for all of this [here](https://github.com/josephmosby/dashboard/tree/c776c8875f8eaf094e2c506e1c0aca91693b7323).
