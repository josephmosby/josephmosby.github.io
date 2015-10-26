---
layout: post
title: Pipes and such
---

In MIT's [text on the xv6](http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-828-operating-system-engineering-fall-2012/lecture-notes-and-readings/MIT6_828F12_xv6-book-rev7.pdf), pipes are described as "a small kernel buffer exposed to process as a pair of file descriptors, one for reading and one for writing." I think I understand file descriptors by now, but I don't quite know what a buffer is. Let me dig into that first with some Googling.

Wikipedia describes a buffer as "a region of a physical memory storage used to temporarily store data while it is being moved from one place to another." Cross-referencing this with other things I've previously learned about operating systems makes me think that buffers are probably also used for things like keyboard input - where we don't want to necessarily take the time for expensive writes to disk, so we just store in memory and wait until another program clears things out. Okay. Moving on.

This example code was provided by the text: 

	int p[2];
	char *argv[2];

	argv[0] = "wc";
	argv[1] = 0;
	
	pipe(p);

	if(fork() == 0) {
		close(0);
		dup(p[0]);
		close(p[0]);
		close(p[1]);
		exec("/bin/wc", argv);
	} else {
		write(p[1], "hello world\n", 12);
		close(p[0]);
		close(p[1]);
	}

And this compiles nicely with some tweaks for the OSX environment - but, as it never prints, we don't have a visual confirmation. 

Pipes and temporary files share some similarities in execution. This code would look the same way to the end user:

	$ echo hello world | wc
	$ echo hello world > /tmp/xyz; wc </tmp/xyz

But there are three key differences here. This would leave the `/tmp/xyz` file lying around, which we'd have to come back through and clean up later. It also expects there to be enough free disk space for the `/tmp/xyz` file, which could be extremely long. And finally, these processes could not easily send data back and forth with this approach, if `wc` needed to send data back to `echo`. 

And that's it for pipes. Next, on to the filesystem!
