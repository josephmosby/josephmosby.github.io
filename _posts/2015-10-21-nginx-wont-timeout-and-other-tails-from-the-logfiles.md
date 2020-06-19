---
layout: post
title: nginx won't timeout, and other tails from the log files
tags: code
---

We had yet another instance of nginx allowing requests to spin into infinity, and now I'm starting to get a little frustrated with it. I'm going to take a different tack and see if I can sniff out the point when these requests start to blow up. To do this, I'm going to use the `awk` tool to find any and all requests that take longer than 3000 milliseconds, which is well beyond the tolerance point for my application. Most of our requests average out in the 100-150ms range, with long running requests taking 500ms. Let's dump some things out from the log files.

	cat django-www.log | awk '$33 > 3000 {print NR-1 ": " $0;}' > high.log

So what this little snippet will do is `cat` the entire log file out, then pipe the output through an `awk` command. The syntax of `awk` breaks the file up based on delimiters (I think space is the default), which you can then access by number. `$33`, in this case, is the 33rd character, which is our millisecond mark. If it's greater than 3000, I print the line number, the line itself, then dump all that out to a file called `high.log`.

Onward.

I don't know why this stuck out to me, but I gave the address space usage and the rss usage of my uwsgi threads a second look this time. Here's what they look like under normal traffic for a small sample.

	{address space usage: 3510480896 bytes/3347MB} {rss usage: 84557824 bytes/80MB} [pid: 5542|app: 0|req: 394/98579] 
	{address space usage: 3510046720 bytes/3347MB} {rss usage: 101765120 bytes/97MB} [pid: 5875|app: 0|req: 387/98580] 
	{address space usage: 3510497280 bytes/3347MB} {rss usage: 106389504 bytes/101MB} [pid: 6922|app: 0|req: 70/98581] 
	{address space usage: 3510497280 bytes/3347MB} {rss usage: 106500096 bytes/101MB} [pid: 6922|app: 0|req: 71/98582] 
	{address space usage: 3521171456 bytes/3358MB} {rss usage: 135237632 bytes/128MB} [pid: 4706|app: 0|req: 660/98583] 
	{address space usage: 3510046720 bytes/3347MB} {rss usage: 101765120 bytes/97MB} [pid: 5875|app: 0|req: 388/98584] 
	{address space usage: 3510480896 bytes/3347MB} {rss usage: 84557824 bytes/80MB} [pid: 5542|app: 0|req: 395/98585] 

The address space usage hovers at about 3.3GB, but the rss usage averages out around 100MB under normal traffic. Here's what it looks like when we spike:
	
	{address space usage: 3518722048 bytes/3355MB} {rss usage: 148234240 bytes/141MB} [pid: 28562|app: 0|req: 4128/36509]
	{address space usage: 3537321984 bytes/3373MB} {rss usage: 153063424 bytes/145MB} [pid: 28827|app: 0|req: 4137/36512]
	{address space usage: 3518103552 bytes/3355MB} {rss usage: 125833216 bytes/120MB}
	{address space usage: 3537321984 bytes/3373MB} {rss usage: 153255936 bytes/146MB} [pid: 28827|app: 0|req: 4138/36517]
	{address space usage: 3518722048 bytes/3355MB} {rss usage: 148992000 bytes/142MB} [pid: 28562|app: 0|req: 4137/36523]
	{address space usage: 3518722048 bytes/3355MB} {rss usage: 148992000 bytes/142MB} [pid: 28562|app: 0|req: 4137/36525]

Our address space usage is the same, but our rss usage is pushing over 142MB for almost every request. I want to dig more into this.

I stumbled upon this discussion thread on the `uwsgi` issues page from someone experiencing the same sort of performance degradation with almost the same sort of configuration that we have: `uwsgi`, `supervisord`, Django. The solution suggested here is to add `die-on-term=True` to our `uwsgi` config, but I want to look into that a little more before I just start adding things to our `uwsgi` config. (the issue thread is [here](https://github.com/unbit/uwsgi/issues/296))

The issue is distilled [here](http://uwsgi-docs.readthedocs.org/en/latest/ThingsToKnow.html) (second bullet). Before uWSGI 2.1, sending the `SIGTERM` signal to `uwsgi` means "brutally reload the stack", which is not convention. `SIGINT` or `SIGQUIT` has the same behavior in uWSGI that `SIGTERM` has in other applications. Searching for `supervisord SIGTERM` yielded this StackOverflow answer:

	supervisord will emit a SIGTERM signal when a stop is requested. Your child can very probably catch and process this signal (the stopsignal configuration can change the signal sent).

	http://stackoverflow.com/a/20299217/1020642

But my child CAN'T catch and process that signal. In fact, it [actually totally ignores it](https://github.com/unbit/uwsgi/issues/296#issuecomment-36086359). It trips over it and brutally reloads the stack if I'm running `uwsgi` prior to 2.1.

	$ uwsgi --version
	2.0.9

So to fix this bug, we either need to upgrade `uwsgi`, or send the `die-on-term` option, which will correct this behavior. Adding the `die-on-term` directive is the quicker and less potentially problematic version. This will go in our `uwsgi.ini` file:

	[uwsgi]
	... stuff ...
	processes=4
	threads=256
	harakiri=20
	max-requests=5000
	die-on-term=True # yay
	... stuff ...

And now we'll reload and give it a shot. 