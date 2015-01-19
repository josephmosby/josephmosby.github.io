---
layout: post
title: Examining audio files with sndhdr
tags:
- pymod
---

In our [last installment](/2015/01/17/the-images-are-coming-from-inside-the-bytestreams.html), we cracked open some image files and looked at the raw bytestreams to assess what type of image file we were looking at. Python's `imghdr` module is designed to automate all of that at need. Python provides a companion library, `sndhdr`, to do the exact same thing for sound files. 

Did you know, for example, that all .aif files start with "FO RM," followed by characters indicating the file size, followed by "AIFF?" I didn't know that. MP3 files start with characters to synchronize the frames, followed by the MPEG version. Python is here to automatically check all of this for you.

	import sndhdr

	print sndhdr.what('snowman.mp3') # 'mp3'

Go forth and examine audio files, my friends.