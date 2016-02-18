---
layout: subpage
title: TIL
---

02-18-16: TIL how to query ELK for a specific set of servers for a particular
error code

	beat.name:*.secdom.tld AND message:*403

02-18-16: TIL how to run a script every five minutes straight from the command
line

	while script; do sleep 300; done
	# this is valid for any command that can be run from the shell

02-16-16: TIL how to jump to a particular line in Vim

	#42 # to jump to line 42

02-11-16: TIL how to split a pane in tmux and switch between the two panes

	Split the screen vertically: Ctrl-b %
	Switch between split panes: Ctrl-b o

