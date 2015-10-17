---
layout: post
title: How are PIDs assigned?
---

I want to take a moment to step through the `ps` command and how PIDs are assigned, because I want to walk through the first 10 processes kicked off when CentOS boots. I assume that PIDs are assigned based on the order in which they're created, but I'm not 100% certain on that. Let's take a look.

Wikipedia states:

	In Unix-like operating systems, new processes are created by the fork() system call. ... Process ID 1 is usually the init process primarily responsible for starting and shutting down the system. ... Process IDs are usually allocated on a sequential basis, beginning at 0 and rising to a maximum value which varies from system to system.

So PID 1, our `systemd` process, is created first (though there's a PID 0 which comes before), and all of the other processes follow sequentially. This makes things easier, as now I can (hopefully) get a listing of the first ten things CentOS does on boot. I wasn't looking for anything more formal than this, so let's move on.

I don't quite know how to get information on a specific process by giving its ID, so let's just try something out:

	$ ps 1
	PID TTY      STAT   TIME COMMAND
    1 	?        Ss     0:04 /usr/lib/systemd/systemd --system --deserialize 21

That was simple enough. There's `systemd`, just as I expected. Let's look at some others.

	$ ps 2
	PID TTY      STAT   TIME COMMAND
    2 	?        S      0:00 [kthreadd]

    $ ps 3
    PID TTY      STAT   TIME COMMAND
    3 	?        S      0:00 [ksoftirqd/0]

    $ ps 4
    # BLANK

    $ ps 5
    PID TTY      STAT   TIME COMMAND
    5 	?        S<     0:00 [kworker/0:0H]

    $ ps 6
    PID TTY      STAT   TIME COMMAND
    6 	?        S      0:00 [kworker/u2:0]

    $ ps 7
    PID TTY      STAT   TIME COMMAND
    7 	?        S      0:00 [rcu_sched]

    $ ps 8
    PID TTY      STAT   TIME COMMAND
    8 	?        S      0:00 [rcu_bh]

    $ ps 9
    PID TTY      STAT   TIME COMMAND
    9 	?        S      0:00 [migration/0]

    $ ps 10
    PID TTY      STAT   TIME COMMAND
   	10 	?        S<     0:00 [khelper]

Well, I couldn't get 10 commands (#4 was out), but I did get 9:

1. `systemd`
2. `kthreadd`
3. `ksoftirqd/0`
4. `kworker/0:0H`
5. `kworker/u2:0`
6. `rcu_sched`
7. `rcu_bh`
8. `migration/0`
9. `khelper`

Let's take a look into what they do to see if they do anything interesting. `systemd` we know.

`kthreadd` is the "kernel thread daemon," and it's actually not controlled by `systemd`. It's controlled by the kernel itself. I'm not familiar enough with the kernel (yet) to do any interesting work with this, but I can see from a `ps -ef` command that the rest of our listed processes are spawned by this one. 

	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 00:40 ?        00:00:04 /usr/lib/systemd/systemd --system --deserialize 21
	root         2     0  0 00:40 ?        00:00:00 [kthreadd]
	root         3     2  0 00:40 ?        00:00:00 [ksoftirqd/0]
	root         5     2  0 00:40 ?        00:00:00 [kworker/0:0H]
	root         6     2  0 00:40 ?        00:00:00 [kworker/u2:0]
	root         7     2  0 00:40 ?        00:00:00 [rcu_sched]
	root         8     2  0 00:40 ?        00:00:00 [rcu_bh]
	root         9     2  0 00:40 ?        00:00:00 [migration/0]
	root        10     2  0 00:40 ?        00:00:00 [khelper]

That PPID thread - right there in the middle - indicates that each of the following PIDs was spawned by `kthreadd`. So we'll obviously need to come back and explore this one in more detail.

Next on the list is `ksoftirqd`, which "is a per-cpu kernel thread that runs when the machine is under heavy soft-interrupt load." [docs here](http://www.ms.sapientia.ro/~lszabo/unix_linux_hejprogramozas/man_en/htmlman9/ksoftirqd.9.html) Again, I'm not 100% certain on how this works, but I'm bookmarking [this page](https://lwn.net/Articles/520076/) for future reference.

The next two are inherently related: they're `kworker` kernel processes. They handle work for system calls, rather than user calls. 

`rcu_sched` and `rcu_bh` are apparently a bit more arcane, given the lack of easy-to-find information about them. RCU stands for "Read-Copy-Update", and it's a synchronization mechanism. I'll be digging more into this later, but I'm bookmarking [this article](http://lwn.net/Articles/262464/) for future reference.

The `migration` process is also a kernel process, and it distributes the load across processor cores.

Finally (and perhaps fortuitously) we have `khelper`. This process is used to make calls to user processes from within the kernel, allowing the kernel and user processes to talk to each other.

So we've got our first ten processes. What does this `ps` process output tell us about them? Let's take a second look at our sample data:

	UID        PID  PPID  C STIME TTY          TIME CMD
	root         1     0  0 00:40 ?        00:00:04 /usr/lib/systemd/systemd --system --deserialize 21

The first column here is the user who kicked off the process: in this case, it's the root user. The PID is our process ID, and the PPID is the PID of the parent that spawned the process. C is used for CPU scheduling information. STIME is the time the process started. TTY is the terminal associated with the process. TIME is the CPU time the process has used. And CMD is the command itself. There are loads more options that we could incorporate here, but this is the default configuration for CentOS machines.

I think `ps` will need its own set of digging (like many other Unix utilities), so I'm going to stop here. Here are my open questions kicked off from this exercise:

1. What does the kernel thread daemon do?
2. What is a software interrupt?
3. What is the read-copy-update mechanism?