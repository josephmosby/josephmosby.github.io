---
layout: post
title: What does systemctl do?
---

In my [earlier post](http://josephmosby.com/2015/10/16/up-and-running-with-flask-on-a-brand-new-linode.html) on nginx and uWSGI, I used `systemctl` to kick off my app. I admittedly don't know much about systemctl (or about CentOS, if we're being totally honest), so I wanted to dig more into that.

My first round of looking for documentation took me to the Fedora project's [documentation on services and daemons](https://docs.fedoraproject.org/en-US/Fedora/15/html/Deployment_Guide/ch-Services_and_Daemons.html). (Turns out that [CentOS is ultimately a fork of Fedora](https://danielmiessler.com/study/fedora_redhat_centos/)) The official documentation seems like a good place to start here. It gives a nice description of how to check the status of my service, so I'm going to do that here.

	$ systemctl status dashboard.service
	dashboard.service - uwsgi instance to serve dashboard
	   Loaded: loaded (/etc/systemd/system/dashboard.service; enabled)
	   Active: active (running) since Sat 2015-10-17 04:32:57 UTC; 10h ago
	 Main PID: 14914 (uwsgi)
	   CGroup: /system.slice/dashboard.service
	           ├─14914 /var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini
	           ├─14916 /var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini
	           ├─14917 /var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini
	           ├─14918 /var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini
	           ├─14919 /var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini
	           └─14920 /var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini

	Oct 17 04:32:57 [INFO ABOUT MY LINODE] uwsgi[14914]: spawned uWSGI worker 5 (pid: 14920, cores: 1)
	Oct 17 04:33:00 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14920|app: 0|req: 1/1] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 722 b...re 0)
	Oct 17 04:33:00 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14919|app: 0|req: 1/2] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 713 b...re 0)
	Oct 17 04:33:00 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14920|app: 0|req: 2/3] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 680 b...re 0)
	Oct 17 04:35:56 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14920|app: 0|req: 3/4] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 722 b...re 0)
	Oct 17 04:35:56 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14916|app: 0|req: 1/5] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 713 b...re 0)
	Oct 17 04:35:59 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14920|app: 0|req: 4/6] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 680 b...re 0)
	Oct 17 04:37:15 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14920|app: 0|req: 5/7] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 722 b...re 0)
	Oct 17 04:37:16 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14919|app: 0|req: 2/8] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 713 b...re 0)
	Oct 17 04:37:16 [INFO ABOUT MY LINODE] uwsgi[14914]: [pid: 14916|app: 0|req: 2/9] [WHAT LOOKS LIKE AN IP ADDRESS] () {42 vars in 680 b...re 0)
	Hint: Some lines were ellipsized, use -l to show in full.

I masked out what I think would be identifying details that I don't want out there. The first commented-out section was my Linode's name, but the second was an IP address that I did not recognize. Maybe it's my IPv4 address? Maybe it's the Linode's hypervisor IP address? I think, though, that these logs may be from uWSGI and not from `systemctl`. I say this because the Fedora documentation doesn't have anything that looks like this in their [page about these logs](https://docs.fedoraproject.org/en-US/Fedora/15/html/Deployment_Guide/s1-services-running.html). I'm going to skip it for now. Most of the other information on Fedora's page here is about using the tool, which I've already done, so I'm going to move on to the raw man pages.

The man page for `systemctl` gives the following description for its use:

	systemctl — Control the systemd system and service manager

Okay, so `systemctl` is actually used to control the `systemd` tool. Maybe the documentation was a little sparse because `systemd` is where the money is. Still, let's go through the [man page](http://www.freedesktop.org/software/systemd/man/systemctl.html) to see what we can get here. I'm going to punch through the commands one by one to walk through what they can do.

	$ systemctl -t
	systemctl: option requires an argument -- 't'

Mer, that didn't go well. I didn't read the documentation enough. It requires a listing of unit types, which I can find here:

	$ systemctl -t help
	Available unit types:
	service
	socket
	target
	device
	mount
	automount
	snapshot
	timer
	swap
	path
	slice
	scope

	$ systemctl -t service

	UNIT                               LOAD   ACTIVE SUB     DESCRIPTION
	.... stuff ...
	crond.service                      loaded active running Command Scheduler
	dashboard.service                  loaded active running uwsgi instance to serve dashboard
	dbus.service                       loaded active running D-Bus System Message Bus
	.... stuff ...

Aha! There's my `dashboard` service, sandwiched right in between cron and something called `dbus`. It looks like it's loaded, active, and running, which is what I would expect. `$ systemctl --state=active` provides the same information, just a different way to cut the data.

	$ systemctl -t service --recursive

This doesn't work as expected on my machine. It may be live on Fedora, but disabled on CentOS or something like that.

	$ systemctl -t service --reverse

The man page says this should do the following: "Show reverse dependencies between units with list-dependencies, i.e. follow dependencies of type WantedBy=, RequiredBy=, RequiredByOverridable=, PartOf=, BoundBy=, instead of Wants= and similar." I remember having to type `WantedBy=` in my configuration earlier:

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

Okay, so I must have configured `dashboard.service` to start with some sort of a dependency: this `multi-user.target` thing. Let's see if I can find that.

	$ systemctl -t target

	UNIT                LOAD   ACTIVE SUB    DESCRIPTION
	... stuff ...
	local-fs.target     loaded active active Local File Systems
	multi-user.target   loaded active active Multi-User System
	network.target      loaded active active Network
	... stuff ...

It looks like these "targets" are super important. I didn't know you could even have a Unix system without multiple users, but it looks like that's something you have to manually turn on - and can turn off. Crazy.

There are two commands here that I don't want to fiddle with too much for now, because I plan to go down a `systemd` rabbit hole and these look like I could cause problems if I don't know what I'm doing. I'll circle back to them.

	$ systemctl --job-mode= ? 
	$ systemctl --fail 

The rest of the options here look like they're tied to actually starting and stopping services, rather than just managing them. Rather than try to imply what's going on with these, I want to jump down to the Commands section so I can start understanding what this utility can do.

	$ systemctl list-units

This does the same thing as just typing `systemctl`, and it dumps out an unfiltered list of running services and sockets and things.

	$ systemctl start [SOMETHING]
	$ systemctl stop [SOMETHING]
	$ systemctl restart [SOMETHING]

I used these last night, and they do exactly what I'd expect. They start, stop, and restart services. This one's new though:

	$ systemctl reload [SOMETHING]

When we type this, we can reload the configuration of a service without actually reloading the service itself. We could reload `nginx.conf` by typing `systemctl reload nginx`.

Now for what is the unexpectedly big kahuna:

	$ systemctl show dashboard

	Id=dashboard.service
	Names=dashboard.service
	Requires=basic.target
	Wants=system.slice
	WantedBy=multi-user.target
	Conflicts=shutdown.target
	Before=shutdown.target multi-user.target
	After=network.target systemd-journald.socket basic.target system.slice
	Description=uwsgi instance to serve dashboard
	LoadState=loaded
	ActiveState=active
	SubState=running
	FragmentPath=/etc/systemd/system/dashboard.service
	UnitFileState=enabled
	InactiveExitTimestamp=Sat 2015-10-17 04:32:57 UTC
	InactiveExitTimestampMonotonic=13928551290
	ActiveEnterTimestamp=Sat 2015-10-17 04:32:57 UTC
	ActiveEnterTimestampMonotonic=13928551290
	ActiveExitTimestamp=Sat 2015-10-17 04:31:52 UTC
	ActiveExitTimestampMonotonic=13863477373
	InactiveEnterTimestamp=Sat 2015-10-17 04:31:52 UTC
	InactiveEnterTimestampMonotonic=13863477373
	CanStart=yes
	CanStop=yes
	CanReload=no
	CanIsolate=no
	StopWhenUnneeded=no
	RefuseManualStart=no
	RefuseManualStop=no
	AllowIsolate=no
	DefaultDependencies=yes
	OnFailureIsolate=no
	IgnoreOnIsolate=no
	IgnoreOnSnapshot=no
	NeedDaemonReload=no
	JobTimeoutUSec=0
	ConditionTimestamp=Sat 2015-10-17 04:32:57 UTC
	ConditionTimestampMonotonic=13928549499
	ConditionResult=yes
	Transient=no
	Slice=system.slice
	ControlGroup=/system.slice/dashboard.service
	Type=simple
	Restart=no
	NotifyAccess=none
	RestartUSec=100ms
	TimeoutStartUSec=1min 30s
	TimeoutStopUSec=1min 30s
	WatchdogUSec=0
	WatchdogTimestampMonotonic=0
	StartLimitInterval=10000000
	StartLimitBurst=5
	StartLimitAction=none
	ExecStart={ path=/var/www/dashboard/venv/bin/uwsgi ; argv[]=/var/www/dashboard/venv/bin/uwsgi --ini dashboard.ini ; ignore_errors=no ; start_time=[Sat 2
	PermissionsStartOnly=no
	RootDirectoryStartOnly=no
	RemainAfterExit=no
	GuessMainPID=yes
	MainPID=14914
	ControlPID=0
	Result=success
	Environment=PATH=/var/www/dashboard/venv/bin
	UMask=0022
	LimitCPU=18446744073709551615
	LimitFSIZE=18446744073709551615
	LimitDATA=18446744073709551615
	LimitSTACK=18446744073709551615
	LimitCORE=18446744073709551615
	LimitRSS=18446744073709551615
	LimitNOFILE=4096
	LimitAS=18446744073709551615
	LimitNPROC=3934
	LimitMEMLOCK=65536
	LimitLOCKS=18446744073709551615
	LimitSIGPENDING=3934
	LimitMSGQUEUE=819200
	LimitNICE=0
	LimitRTPRIO=0
	LimitRTTIME=18446744073709551615
	WorkingDirectory=/var/www/dashboard
	OOMScoreAdjust=0
	Nice=0
	IOScheduling=0
	CPUSchedulingPolicy=0
	CPUSchedulingPriority=0
	TimerSlackNSec=50000
	CPUSchedulingResetOnFork=no
	NonBlocking=no
	StandardInput=null
	StandardOutput=journal
	StandardError=inherit
	TTYReset=no
	TTYVHangup=no
	TTYVTDisallocate=no
	SyslogPriority=30
	SyslogLevelPrefix=yes
	SecureBits=0
	CapabilityBoundingSet=18446744073709551615
	User=ghost
	Group=nginx
	MountFlags=0
	PrivateTmp=no
	PrivateNetwork=no
	SameProcessGroup=no
	IgnoreSIGPIPE=yes
	NoNewPrivileges=no
	KillMode=control-group
	KillSignal=15
	SendSIGKILL=yes
	SendSIGHUP=no
	CPUAccounting=no
	CPUShares=1024
	BlockIOAccounting=no
	BlockIOWeight=1000
	MemoryAccounting=no
	MemoryLimit=18446744073709551615
	DevicePolicy=auto
	ExecMainStartTimestamp=Sat 2015-10-17 04:32:57 UTC
	ExecMainStartTimestampMonotonic=13928551199
	ExecMainExitTimestampMonotonic=0
	ExecMainPID=14914
	ExecMainCode=0
	ExecMainStatus=0

I KNOW WHAT LIKE A TENTH OF THIS MEANS. THIS IS AWESOME.

I'm going to take a break here and digest some of the information gleaned from this little exercise. More to come!