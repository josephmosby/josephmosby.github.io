---
layout: post
title: Python at Disney Animation
tags: product
---

I started off my technology career as a help desk support staffer at Belmont University in 2007 after being sick of working in the food industry. I learned how to code in Visual Basic for Applications by writing custom Excel functions to help me through my finance classes. I _finally_ and painstakingly learned some proper computer science through [MIT's OpenCourseWare](http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00-introduction-to-computer-science-and-programming-fall-2008/), where I picked up Python as my language of choice. I've learned a bit more computer science as a matter of course since then, but code to me has always been more about gluing together solutions and data than anything else.

Turns out, that's how Disney Animation sees it as well. 

	No one wants to use another limited DSL. [me: Domain-Specific Language] They just want Python.
	- Paul Hildebrandt, Software Engineer, Disney Animation

Disney movies require a lot of software programs used by several different teams. There's software to move characters' faces, software that simulates lights, and software that behaves as if it was a real camera. Like many graphics artists, Disney artists script a lot of their workflows to keep themselves from doing the same thing twice -- or two thousand times -- in repetition. Many of the commercial tools they use shipped with their own domain-specific languages, meaning that an artist could be compelled to learn four completely different scripting languages for four completely different software packages, even if all of the scripts were designed to do roughly the same thing. With Python embedded in their tools, that pain point has gone away. They can learn one language and trust that they'll be comfortable with its nuances regardless of how the software changes. 

	We paid $50 for the [San Francisco] county assessor's street and elevation maps. * pause * It's okay, we made a lot of money off Frozen.

So much of the work required for attacking details in building worlds is similar to GIS work that thousands of Pythonistas are already doing. [Big Hero 6](http://movies.disney.com/big-hero-6/) is set in "San Fransokyo", a mish-mash of San Francisco with Japanese culture, and the look and feel of San Francisco needed to be preserved. There's a reason that the movie's city looks like the Bay Area -- it's because it is! San Fransokyo is based on the actual street map and elevation of the real San Francisco, and much of that data analysis was done with Python.

	"Oh, so you guys crowdsourced crowds."

There's an entire team of people strictly dedicated to crowds of things. You have a shot in the middle of a city and there are cars on the streets and people milling around on the sidewalks. That's all crowd mechanics. Disney's crowd team released a character creator called "Denizen" (built with Python) and started letting their animators create characters on it. Those dreamed-up characters are now automatically brought into a crowd whenever one is needed. (I hope this means that Elsa is hanging around Big Hero 6 somewhere)

	"We don't always work in a correct world. We work in an art-directed world."

Scientifically, there's always a proper way that things are supposed to happen. Lights are supposed to behave in a certain way, as are wind and rain. That's just fine for the real world or for scientific modeling, but that isn't necessarily how an art director wants to capture a shot. The real world doesn't necessarily jibe with the feel of a movie. Python allows Disney technology teams to respond accordingly, with lightning quick software builds and easy customizability. 

It's been enlightening to have Disney Animation here at PyCon to learn about their workflow. Really, really inspiring stuff and great work coming out of it.  
