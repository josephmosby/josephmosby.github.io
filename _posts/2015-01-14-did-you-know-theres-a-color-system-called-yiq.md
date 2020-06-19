---
layout: post
title: Did you know there's a color system called YIQ?
tags: code
---

I certainly didn't. YIQ is used if you're building software that's going to transmit over NTSC (broadcast television). YIQ contains information about the luminance and chrominance of colors. Luminance, as we might expect, can be measured on a spectrum from totally white to totally black. [Chrominance is the color information in a signal](http://wolfcrow.com/blog/understanding-luminance-and-chrominance/). These two values merge together in the YIQ data format, where Y represents luminance information, and I and Q represent chrominance information.

In the event that you are ever building software that must make use of the YIQ color format but you're really only great at dealing with RGB, Python is happy to accommodate you! The `colorsys` module provides color format conversions between RGB, YIQ, HLS and HSV. It works about how you'd expect:

	import colorsys

	print colorsys.rgb_to_yiq(82, 0, 99)

	print colorsys.yiq_to_rgb(35.49, 17.52, 47.91)

	print colorsys.rgb_to_hls(82, 0, 99)

	print colorsys.hls_to_rgb(0.833, 49.5, -1.020619)

	print colorsys.rgb_to_hsv(82, 0, 99)

	print colorsys.hsv_to_rgb(0.833333333, 1, 99)

And that's it - just those six functions for all of the color conversions you'll ever need when dealing with coordinate-based color systems.