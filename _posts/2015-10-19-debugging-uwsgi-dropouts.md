---
layout: post
title: Debugging uWSGI dropouts
---

On Friday night, our National Journal app suddenly stopped responding to requests. Our response time went straight through the roof, but this didn't correspond to any noticeable increase in load. In fact, our throughput (the requests per minute we respond to) had been declining up until the breakdown. We didn't have any noticeable spike in traffic that corresponded to this outage, so I suspect our `uwsgi` configuration may be to blame. Here's what the graph looked like:

![](/images/errors.png)

I'm going to tear through the `uwsgi` logs today to see if I can nail down the culprit. If my `uwsgi` threads are dying and not coming back, I'd expect to see a message like this:

	worker 1 killed successfully (pid: 17421)

that wasn't accompanied with a message like this:

	Respawned uWSGI worker 1 (new pid: 9438)

I've pulled the log files down from one of our application servers and will be going through it. I want to start by culling things down to only things that occurred in that 5:00-5:45 timeframe, so let's whittle it down with some `grep`. I'll use the `-m 1` flag to call only the first occurrence and the `-n` flag to show the line number.

	$ grep -m 1 -n "Oct 16 17:00:00" django-www.log

	763413:{address space usage: 3525341184 bytes/3362MB} {rss usage: 135106560 bytes/128MB} [pid: 2449|app: 0|req: 1197/17093] [IP ADDRESS] () {42 vars in 736 bytes} [Fri Oct 16 17:00:00 2015] GET /s/54699/1-easy-way-donald-trump-could-have-been-even-richer-doing-nothing => generated 304819 bytes in 178 msecs (HTTP/1.1 200) 5 headers in 263 bytes (6 switches on core 96)

	$ grep -m 1 -n "Oct 16 17:45:00" django-www.log
 
	768139:{address space usage: 3510857728 bytes/3348MB} {rss usage: 103940096 bytes/99MB} [pid: 11399|app: 0|req: 174/680] [IP ADDRESS] () {48 vars in 919 bytes} [Fri Oct 16 17:45:00 2015] GET /energy/scientists-go-beyond-science-to-explain-their-climate-terror-20140826?ref=facebook.com => generated 0 bytes in 31 msecs (HTTP/1.1 302) 3 headers in 226 bytes (1 switches on core 143)

Now I'm going to use `sed` to create a new file of only that range of lines from 763413 to 768139, to make parsing faster and easier. I'll drop this output into a new file called `outage.log`.

	$ sed -n 763413,768139p django-www.log > outage.log

Okay, now that I've whittled things down, I want to look for things indicating my workers died:

	$ grep -n "killed successfully" outage.log
	$ grep -n "Seeya" outage.log

Both of those didn't yield anything. Let's maybe instead look for signs of spawning:

	$ grep -n "spawn" outage.log

	999:DAMN ! worker 1 (pid: 2449) died, killed by signal 9 :( trying respawn ...
	1000:Respawned uWSGI worker 1 (new pid: 8359)
	1862:Fri Oct 16 17:28:18 2015 - HARAKIRI [core 151] [IP ADDRESS] - GET /member/energy/n2k-energy-solyndra-spawns-calls-for-more-probes-dems-ask-obama-to-hold-off-on-keystone-20111027 since 1445030637
	1882:Fri Oct 16 17:28:18 2015 - HARAKIRI [core 171] [IP ADDRESS] - GET /member/energy/n2k-energy-solyndra-spawns-calls-for-more-probes-dems-ask-obama-to-hold-off-on-keystone-20111027 since 1445030802
	1972:DAMN ! worker 3 (pid: 2977) died, killed by signal 9 :( trying respawn ...
	1973:Respawned uWSGI worker 3 (new pid: 9731)
	2324:DAMN ! worker 2 (pid: 2712) died, killed by signal 9 :( trying respawn ...
	2325:Respawned uWSGI worker 2 (new pid: 10063)
	2601:DAMN ! worker 4 (pid: 3240) died, killed by signal 9 :( trying respawn ...
	2602:Respawned uWSGI worker 4 (new pid: 10065)
	3006:DAMN ! worker 1 (pid: 8359) died, killed by signal 9 :( trying respawn ...
	3007:Respawned uWSGI worker 1 (new pid: 10593)
	4025:spawned uWSGI master process (pid: 11394)
	4026:spawned uWSGI worker 1 (pid: 11397, cores: 256)
	4027:spawned uWSGI worker 2 (pid: 11398, cores: 256)
	4029:spawned uWSGI worker 3 (pid: 11399, cores: 256)
	4030:spawned uWSGI worker 4 (pid: 11400, cores: 256)

NOW we're cooking. I'm going to chop things up a little bit more, since I can tell from this that we rebooted the app at line 4025.

	$ sed -n 1,4030p outage.log > outage2.log && mv outage2.log outage.log

And now let's look for something weird. I'm going to just dump out some of the things I've looked for.

	$ grep -n "17:23" outage.log
	$ grep -n "HARAKIRI" outage.log
	$ grep -n "spawn" outage.log

Then I came back to this and scrolled back up through the files:

	$ grep -n "17:23" outage.log

	1393:Fri Oct 16 17:23:00 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1395:Fri Oct 16 17:23:00 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1401:Fri Oct 16 17:23:08 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1404:Fri Oct 16 17:23:10 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1408:Fri Oct 16 17:23:15 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1409:Fri Oct 16 17:23:15 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1414:Fri Oct 16 17:23:16 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1417:Fri Oct 16 17:23:17 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1421:Fri Oct 16 17:23:20 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1424:Fri Oct 16 17:23:21 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1432:Fri Oct 16 17:23:32 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 
	1436:Fri Oct 16 17:23:38 2015 - uwsgi_response_write_body_do(): Broken pipe [core/writer.c line 331] during GET 

That maps _exactly_ back to the time that our application started spiking. I think I may have a breadcrumb.

... goes to Google ...

Maybe not. `uwsgi` throws out those broken pipe errors in the instance of a timeout, and it would make sense that things would be timing out around that time.

But what a second. I'm going to scroll up the log files until a few minutes _before_ the crash starts acting up to see if I can pinpoint what went wrong. Here's a sample line from that timeframe:

	{address space usage: 3521130496 bytes/3358MB} {rss usage: 167030784 bytes/159MB} [pid: 2712|app: 0|req: 1548/18272] [IP ADDRESS] () {40 vars in 668 bytes} [Fri Oct 16 17:17:50 2015] GET /columns/political-connections => generated 58615 bytes in 18558 msecs (HTTP/1.1 404) 2 headers in 95 bytes (2 switches on core 16)

That took us 18.5 seconds to generate a 404 page for a broken link. That's absurd. Right around the time that I read this line, one of our system administrators (who I've been live-updating as I worked) comes running around the corner to say: 

	> we didn't have uwsgi timeouts set on nginx!

Ahh. So `nginx` was timing out on sending and receiving data to and from `uwsgi`, but weren't *actually* timing out. We were just letting `uwsgi` spin into infinity. We fix that with these lines in our `nginx.conf`:

	location / {
		... stuff ...
		uwsgi_read_timeout 300;
	    uwsgi_send_timeout 300;
	    ... stuff ...
	}

We think that might be our ticket, allowing these dropped connections to actually timeout. We'll need a few days in production before I give the all-clear, but I think that might do it!