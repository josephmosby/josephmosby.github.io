---
layout: post
title: Cooking My First Ever Drupal Theme From Scratch
---

About six months ago, I would have said that I was starting to figure Drupal out. I'll assure you now wthat I have no idea. I have picked up a few tricks here and there, though, and the Drupal templating system is starting to make some sense to me.

When I started building Drupal sites, I built them in [Zen](https://www.drupal.org/project/zen) or one of the many subthemes built off of it. Zen's philosophy is to anticipate much of what an experienced front-end developer would drop in to a non-Drupal site (such as Sass and Compass) and incorporate those into the base theme and subthemes from the beginning. Like most of the current popular Drupal themes, it's responsive and mobile-first. A theme structure with that many bells and whistles was too much for my back-end developer brain at the time, and I was scared off to other options.

[Omega](https://www.drupal.org/project/omega) is Zen's largest competitor. Version 3 of the framework provides a shiny graphical interface for creating responsive content regions, and I loved it. It was point-and-click web design! Omega happily produces five little stylesheets for you to use at different page widths and then does the rest of the work for you. Sure, my stylesheet file sizes would blow up trying to sift through the cruft Omega produces, but I didn't have to learn much about actual theming. Omega, [Delta](https://www.drupal.org/project/delta) and [Context](https://www.drupal.org/project/context) did it all for me.

My blissful ignorance came to an end when I revisited a site built by another development shop using Zen as a base theme. The horror! So many custom tpl.php files, so many PHP if statements and variables within those files! My complacent Drupal ignorance came crashing down around me. I was forced to battle with Drupal's theme engine, and I did not leave the fire unscathed. I arose, and now come with wisdom about battling the dragon for those who follow in my footsteps.

Let's talk about .info files.

### What does a .info file do, anyway?

Drupal's `.info` file is where all of the tools your theme will use are declared. It's not about content - we are miles away from content right now - it's about defining the tools we'll use to organize that content on a page. A sample `.info` file looks something like this: 

<script src="http://gist-it.appspot.com/github/josephmosby/base/blob/master/base.info"></script>

In the first blob we name our theme and specify the Drupal version (core) that it works with. In our second and third we add stylesheets and JavaScripts - our theme will pick up those files and add them into the `<head>` of any page with that theme. The directories are given relative to the theme's .info file. 

Our fourth blob contains the regions of our theme. I can place content into the `main_menu` region with this theme, the `content` region, or the `box_one` region. Though your theme must contain a `content` region, you can name the rest of them anything you like. Follow your heart. You'll be using these names later. 

Once we've created our `.info` file, we need to put it to use - we need to find a home for our content.

### What does a tpl file do?

Drupal uses these nifty files with `.tpl.php` extensions to build its pages, and most of them hang out like pitchers in a bullpen in the `modules/system` folder waiting for you to override them. Theoretically, we really only need one to build a new theme: the `page.tpl.php` file. Here's our example `page.tpl.php` file for this theme:

<script src="http://gist-it.appspot.com/github/josephmosby/base/blob/master/templates/page.tpl.php"></script>

Astute [Bootstrap](http://getbootstrap.com/) users may note that we're pulling in some Bootstrap elements here. We have `container` classes, with `row` classes within them, then some `col-md-6` classes, and then a little snippet of PHP code. This `<?php print render($page['sm_icons_top']); ?>` is where the magic happens. Drupal picks up anything that we've placed into the `sm_icons_top` region - whether it be a menu, a view, a block, etc. - and renders it into the page. You can see how that ultimately pans out in the HTML here:

<script src="https://gist.github.com/josephmosby/08851b82b4d14818bb75.js"></script>

You can see our `#top_menu`, our `row` class, and our `col-md-6` class followed by the block content Drupal popped into our page. That's the extremely basic purpose of `tpl.php` files: they provide homes in the HTML for certain content regions, we create blocks and drop them into those content regions through the administration tools, and finally our `tpls` take care of the rendering. Fantastic.

### But Drupal variables are weird...

All too true. I won't even profess to fully understand how to actually get at a specific piece of content, and Drupal's documentation is notoriously bad on the subject. I have figured out a few tricks though:

* In `page.tpl.php`, access the content in a specific region with `render($page['region-name'])`
* Make sure to render your metatags with `render($page['content']['metatags'])` or else some modules and libraries will behave strangely
* To access individual fields from `page.tpl.php`, use the syntax `print_r($node->field_fieldname['und'][0]['value'])`. This is not recommended behavior, but is occasionally necessary. The 'und' refers to the language (und is English... inexplicably), the '0' to the place in the array and the 'value' for the actual content.
* To call in a block, use `module_invoke('module', 'view', 'block-id')` where the 'module' is the module that produced the block (such as Webform or Views), the 'view' is the type of view (probably just block_view) and the 'block-id' is the machine name for the block

### I have IE-specific stylesheets and libraries that need conditional comments. Where do those come in?

I wondered this myself as Bootstrap requires some IE-specific libraries to be dropped in. The Internet yields a lot of solutions that don't really work for this but are worth mentioning anyway:

* Add them in your `.info` file. That won't help you with conditional comments but it is a solution.
* Add them with `drupal_add_css()` or `drupal_add_js()`. Same problem as above, though I suppose you could do some wizardry with detecting user agents and conditional logic.
* Add an element with `drupal_add_html_head()`. I can never get this to work.

The best solution I've found is to just add them directly into the `html.tpl.php` file. 

<script src="http://gist-it.appspot.com/github/josephmosby/base/blob/master/templates/html.tpl.php"></script>

You can see toward the bottom where I've added in those conditional libraries. It feels ugly, but that's the cleanest way I've discovered.

### What's next? 

I know that Drupal lets me get much more granular with my templating - down to the region, node and block level. I have no idea how to wrangle those templates yet, though, so those are next on my list. I'd also like to not have these hacky queries of the `$page` object that required me to guess how the object was structured half of the time. Till next time!
