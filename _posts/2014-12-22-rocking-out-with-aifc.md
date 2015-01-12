---
layout: post
title: Rocking out with aifc
tags:
- pymod
---

In 1985, Electronic Arts (then publishing such games as [The Bard's Tale](http://en.wikipedia.org/wiki/The_Bard%27s_Tale_(1985_video_game))) convened a group of engineers, software developers, and computer manufacturers to define a data interchange format for graphics, audio, and text. The aim was to create a file format with accompanying objects, data structures and interfaces that would be interchangeable across platforms for the budding gaming audience. This was a bold new time in data storage, when Apple had just invented a wonderful little tool called the "clipboard." 

A few years later, Apple defined a fork of the EA IFF 85 standard with the Audio Interchange File Format, which allowed for multiple channels of audio with customizable sample rates and widths. The data was stored in Motorola 68000 format, which used big-endian order (most significant bytes first). `.aiff` and its compressed brother `.aifc` were the audio standard on iTunes for decades.

The `aifc` [module](https://docs.python.org/2.7/library/aifc.html#module-aifc) for Python is used to read and write `aiff` files on OS X. If you're looking into using Python in the professional audio world, `aifc` should be in your toolkit. It's a fairly simple module to navigate. I downloaded some sample AIFF files from [here](http://www-mmsp.ece.mcgill.ca/documents/AudioFormats/AIFF/Samples.html) to play around with.

	import aifc

	tune = aifc.open('sample1.aif')

	print tune.getparams()

In the sample file I'm using, this will yield a tuple with values `(2, 1, 8000, 23493, 'NONE', 'not compressed')`. That tuple indicates that we have two channels (stereo sound), one byte per sample, a framerate of 8000 frames per second, 23493 frames, and no compression.

Now, if I wanted to create an AIFF object with these parameters, I'd do something like the following:

	import aifc

	tune = aifc.aiff()

	tune.setnchannels(2)
	tune.setsampwidth(1)
	tune.setframerate(8000)
	tune.setnframes(23493)
	tune.setcomptype('NONE')

And then I could write data to the file as needed with `aifc.writeframes(data)`. 

That's all there is to it! Obviously we haven't done much with this particular module - that needs far more libraries to support audio creation and playback. We'll see those later on.