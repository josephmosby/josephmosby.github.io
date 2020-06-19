---
layout: post
title: What does systemd do?
tags: code
---

I mentioned in an [earlier post](http://josephmosby.com/2015/10/17/what-does-systemctl-do.html) that `systemctl` appeared to be tied to `systemd`, which looked like a much more important program. In this post, I'm going to explore `systemd` and see what it does.

Turns out, it does a LOT. And people are super unhappy about it.

I loosely knew the Unix philosophy, which essentially states that programs should be tiny and do very little, rather than one program taking on monolithic functionality. Doug McIlroy, a former head of the Bell Labs Computing Sciences Research Center, summarized it thus:
	
	This is the Unix philosophy: Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface.

`systemd` does way more than this. It does a bajillion things, and it does them well, but it still does a bajillion things rather than just one. 

At its core, `systemd` is a Linux init system. It's designed to kick off programs - every single program that runs on a Unix system. As such, it's the first process spawned when a system boots:

	$ ps -ef | grep "systemd"
	root         1     0  0 00:40 ?        00:00:04 /usr/lib/systemd/systemd --system --deserialize 21
	root      1636     1  0 00:40 ?        00:00:00 /usr/lib/systemd/systemd-journald
	root      1649     1  0 00:40 ?        00:00:00 /usr/lib/systemd/systemd-udevd
	dbus      2488     1  0 00:40 ?        00:00:01 /bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
	root      2490     1  0 00:40 ?        00:00:00 /usr/lib/systemd/systemd-logind
	root     15732 15713  0 16:36 pts/3    00:00:00 grep --color=auto systemd

PID 1! The maker of all other services in a Unix operating system! I never knew what PID 1 would be, but there it is: `systemd`. This post is going to be heavy, I think. And I'll probably leave myself asking more questions. I'm not really grokking anything in-depth from the [Wikipedia page](https://en.wikipedia.org/wiki/Systemd) for `systemd`, so off I go to the [man pages](http://www.freedesktop.org/software/systemd/man/systemd.html). 

`systemd` has an entire "Concepts" page devoted to it, which is extremely useful. It states that `systemd` has a concept of units - our services, sockets, and other objects we used earlier. `nginx` is a unit. `dashboard` is a unit. Now we get some meat about what those units can be, and I'm just going to copy and paste the list here.

1. Service units, which start and control daemons and the processes they consist of.

2. Socket units, which encapsulate local IPC or network sockets in the system, useful for socket-based activation. 

3. Target units are useful to group units, or provide well-known synchronization points during boot-up.

4. Device units expose kernel devices in systemd and may be used to implement device-based activation.

5. Mount units control mount points in the file system.

6. Automount units provide automount capabilities, for on-demand mounting of file systems as well as parallelized boot-up.

7. Snapshot units can be used to temporarily save the state of the set of systemd units, which later may be restored by activating the saved snapshot unit.

8. Timer units are useful for triggering activation of other units based on timers.

9. Swap units are very similar to mount units and encapsulate memory swap partitions or files of the operating system.

10. Path units may be used to activate other services when file system objects change or are modified.

11. Slice units may be used to group units which manage system processes (such as service and scope units) in a hierarchical tree for resource management purposes.

12. Scope units are similar to service units, but manage foreign processes instead of starting them as well. 

I still don't know what a target unit is, so I'm going to move into the man page for `systemd.target` for a moment. This line is helpful from those pages: "They exist merely to group units via dependencies (useful as boot targets), and to establish standardized names for synchronization points used in dependencies between units." I think I've got it now - if you want to smash together a bunch of units into one (like you'd need to do for a multi-user system), you use a target unit.

`systemd` also manages the dependencies of units, and that's where those `Requires`, `Conflicts`, `After`, and `Before` lines came into play earlier. From my dashboard service's `systemctl show` output:

	Requires=basic.target
	Wants=system.slice
	WantedBy=multi-user.target
	Conflicts=shutdown.target
	Before=shutdown.target multi-user.target
	After=network.target systemd-journald.socket basic.target system.slice

My service Requires `basic.target`, Conflicts with `shutdown.target`, must be before `shutdown.target` and `multi-user.target`, and must come after `network.target`, `systemd-journald.socket`, `basic.target`, and `system.slice`. I'm not sure what most of these mean, but it does make sense that my web program should be loaded after the `network` has been loaded.

`systemd` states that it loads information about unit configuration from system directories and user directories, which I can find by typing the following commands in:

	$ pkg-config systemd --variable=systemdsystemunitdir
	/usr/lib/systemd/system

	$ pkg-config systemd --variable=systemduserunitdir
	/usr/lib/systemd/user

Let's go see what's in those:
	
	$ cd /usr/lib/systemd/system
	$ ls

Ooh, I see a bunch of files that look like the `.service` files I was tinkering around with last night but didn't understand! Let's inspect a few.

	$ cat sound.target
	#  This file is part of systemd.
	#
	#  systemd is free software; you can redistribute it and/or modify it
	#  under the terms of the GNU Lesser General Public License as published by
	#  the Free Software Foundation; either version 2.1 of the License, or
	#  (at your option) any later version.

	[Unit]
	Description=Sound Card
	Documentation=man:systemd.special(7)
	StopWhenUnneeded=yes

	$ cat halt.target
	#  This file is part of systemd.
	#
	#  systemd is free software; you can redistribute it and/or modify it
	#  under the terms of the GNU Lesser General Public License as published by
	#  the Free Software Foundation; either version 2.1 of the License, or
	#  (at your option) any later version.

	[Unit]
	Description=Halt
	Documentation=man:systemd.special(7)
	DefaultDependencies=no
	Requires=systemd-halt.service
	After=systemd-halt.service
	AllowIsolate=yes

	[Install]
	Alias=ctrl-alt-del.target

	$ cat crond.service
	[Unit]
	Description=Command Scheduler
	After=syslog.target auditd.service systemd-user-sessions.service time-sync.target

	[Service]
	EnvironmentFile=/etc/sysconfig/crond
	ExecStart=/usr/sbin/crond -n $CRONDARGS
	KillMode=process

	[Install]
	WantedBy=multi-user.target

So these `.service` and `.target` files are all part of the configuration that `systemd` requires. The `crond.service` configuration isn't `crond` itself, it's a file that tells `systemd` how to start and manage `crond`. I'm getting it now!

`systemd` can also receive certain signals, such as `SIGTERM`, `SIGINT`, and `SIGRTMIN+15`, which are more black magic to me. I'm not sure how I would send those signals to `systemd`, but maybe those things aren't for me in the way I think of them.

I think that's a good start into `systemd`, but I can tell I'm just scratching the surface with it. Next up: this [blog post](http://0pointer.de/blog/projects/systemd.html) on the origins of `systemd` and the `systemd` [homepage](http://www.freedesktop.org/wiki/Software/systemd/).
