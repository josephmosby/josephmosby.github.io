---
layout: post
title: An introductory look at Erlang
---

I wanted to take a step back from operating systems to consider how another programming language views the world. Operating systems in the Unix world require knowledge of C: something that expands my programming mind but often feels like the Python knowledge I already know, just at a lower level. I wanted to pick something totally new, and so I'm going with [Erlang](http://learnyousomeerlang.com/).

Erlang is an _imperative_ language: which means once you set a variable, it doesn't change. That means a statement like `i++` or `i += 1` won't work. I assume that Erlang has an elegant way of dealing with this, but I'm very early on in this book. Erlang does this to ensure that functions with the same parameters will always return the same results, regardless of the state elsewhere in the application. 

The language makes use of something called an "actor model." Each "actor" is a separate process in the Erlang virtual machine, calmly waiting for tasks but mostly sitting around doing nothing. Each process can do a very limited set of tasks. Each process is also totally segregated from other processes - without passing very transparent messages back and forth, processes don't have the ability to communicate. Erlang also appears to come with a standard library that's almost as fully featured as Python's: debugging tools, a web server, a database, all the tools I generally rely on to get programming work done. 

The _Learn You Some Erlang_ book also makes a point to call out overzealousness in the Erlang community. Erlang caught my eye because of its concurrency and scalability (or rather, people talking about Erlang's concurrency and scalability), but this book makes a point to calm those expectations a little bit. Just because you can divide everything up into actors doesn't mean you should. The authors point out that Erlang is fantastic for things like server-level software and is mostly terrible at things like image processing. Exceptions can be made, of course. As I'm interested in things like server-level software and not so interested in image processing, I'm excited to get under the hood. 

And with that, let's get started.

	$ brew install erlang
	$ erl

I continue on to the next chapter and discover this line:

	The Erlang shell has a built-in line editor based on a subset of Emacs, a popular text editor that's been in use since the 70s. If you know Emacs, you should be fine. For the others, you'll do fine anyway.

I am skeptical. I strongly dislike Emacs because every time I try to grok it, I trip over my feet and mostly destroy my entire program. Whatever, onward. Ctrl+A moves me to the beginning of a line, Ctrl+E to the end in Erlang-world. In the current version of Erlang compiled for OSX, it appears that Erlang opens you right into a shell. If I want to get out of it to enter some commands, I hit Ctrl+G. If I can't remember what I'm supposed to do once I get out of the shell, I hit `h`. If I want to see a listing of all my current jobs, I hit `j`... oh, and I bet this is like doing `ps -ef`, but for the virtual machine. Okay, now I want to get back into my shell... hmm. Struggling to that with the instructions given. I'm going to have to trust that I'll figure it out as time goes on. 

Calling it a day for there. I'll come back to it in earnest after I've digested a few things about the language.