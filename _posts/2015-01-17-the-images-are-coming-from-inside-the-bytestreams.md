---
layout: post
title: The images are coming from INSIDE the bytestreams
tags: code
---

Okay, let's first clarify that I've been working with digital images for longer than I'm comfortable with to just now learn how to do this. But that's neither here nor there. Obviously, images are streams of bytes just like every other piece of information stored on your computer. And obviously, there's got to be something inherent in the byte stream and how it's encoded that tells the computer how to open it. There's something that makes a PNG different from a TIFF, and the computer knows how the difference between the two. But how? How does a computer know when it's looking at a PNG or a TIFF when it starts to read the file? 

The answer, my friends, is in the byte stream. I just learned how to read it with mine own two eyes and I am very excited to share this knowledge with you. 

Open up a PNG file with your code-writing text editor of choice (I know this will work in Sublime). You'll have a massive eight-column byte stream open up in front of you, and you'll also notice that it starts with these characters: `8950 4e47 0d0a`. Those are hex codes, and they mean something very specific: `‰P NG \r\n`. This is the universal sign of a PNG file, and you'll find it on any PNG file that you open! 

Now do the same with a TIFF file. You'll notice the file starts with the following hex codes: `4d4d 002a 0000`. That stands for `MM NUL* NULNULNULNUL`. The MM, in this instance, signals the computer that we're working in a big-endian data format. We then have a null character and an asterisk - which also corresponds to the number 42. The 42 here is chosen for its "[deep philosophical significance](http://www.douglasadams.eu/en_h2g2_references.php)." If you see the byte order and 42, you've got a TIFF file!

Chances are that you won't want to visually inspect your image files to see what they are all the time, so Python has provided a helper library to do that: `imghdr`. It has one function:

	import imghdr

	print imghdr.what('snowman.tiff') # 'tiff'

The `what(filename)` function is used to detect file format. It can do so for the following image types: RGB, GIF, PBM, PPM, TIFF, RAST, XBM, JPEG, BMP, PNG. 

Go forth and read bytestreams!