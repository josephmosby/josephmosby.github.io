---
layout: post
title: A Modest Proposal for Accessibility-Driven Web Development
---

I have never been a developer specifically tasked with making web applications accessible to users with disabilities, but I always manage to find myself engaged in conversations about web accessibility with my friends employed by government agencies here in Washington, D.C. There is always some new service or technology or design that government employees would love to bring in, but they're not legally allowed to because it's not "Section 508-compliant." This inevitably sparks a conversation about making technology accessible, and it's all too often sparked by non-developers who can't understand why developers just can't make their products accessible. It's one of the most misunderstood problems facing the accessibility community, and it shows no signs of being resolved any time soon. 

I would be remiss if I tried to solve the entire web accessibility problem in a blog post, but I can hopefully shed some light on how the problems start - now that I've had the opportunity to fix a few of my own.

Recently, my team was tasked to make some changes to a web site with a map that showed text content when a user hovered over it. I can't show the site itself, but [this page](https://www.mapbox.com/mapbox.js/example/v1.0.0/show-tooltips-on-hover/) gives a decent representation of what we added. It's a red-flag accessibility problem because it implies that sight is required to operate the web application, and not every possible user can see the screen. Some are navigating it through screen readers. I've had some training in how to spot these sorts of things, though, and I realized that we could easily just head off the user by placing `aria` tags within the map when a user stumbled upon it, and we could also place the tooltips in the HTML document such that a user could still read them. This was about five minutes worth of extra work, and all I needed to do was organize my HTML in such a way that a screen reader could figure it out. 

I can do this because I'm not just thinking about accessibility (which would have caused me to forego the map idea altogether), and I'm not just trying to hammer out a task in a hurry (which would have caused me to skip the HTML rearrangement). I've got time and training to notice the problem and creatively solve it. That happens at every level with our team at [APCO Worldwide](http://www.apcoworldwide.com). Our team members developing wireframes and user interfaces have accessibility in the back of their mind, our designers are thinking about color contrasts and font choices, and our developers are sorting through their HTML to make sure we don't make some sort of confusing error in our code. We're not accessibility professionals, we're creative professionals who happen to know that not every user has the same experience with a computer that we do.

We also plan our designs and our development in a holistic manner, and we iterate through multiple rounds of feedback to get it right. We decide who gets to have feedback and who doesn't. And we don't just say "yes" to any change that comes down the pipe: we weigh changes through our creative expertise before we implement them, and we push back on our clients if they make changes that will be problematic. If a client requests something that's going to impact the accessibility of the site (such as a color contrast issue or a font change), we discuss it internally and propose alternatives before we just start coding. 

### What Government Gets Wrong

Government has recently taken an interest in good design, which is all for the best. But it has focused heavily on simply hiring individual designers rather than *focusing on a creative process that emphasizes excellent, accessible design throughout.* This requires a commitment to a management style that is inherently at odds with how government develops and deals with IT solutions. 

Government tends to want to blame contractors for fleecing them, but I don't think that's the whole of the problem. We pull off accessible design and we're a contract-based shop. 

- management
- external products
