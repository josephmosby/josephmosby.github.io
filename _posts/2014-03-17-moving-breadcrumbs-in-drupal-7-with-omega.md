---
layout: post
title: Moving Breadcrumbs in Drupal 7 with Omega
---

I recently had a client site that required me to move my Drupal breadcrumbs from one Omega zone to another, and I was absolutely stumped on how to do it. After much hacking around with template files with no success, I finally stumbled upon [this post](http://www.webbykat.com/2012/09/moving-breadcrumbs-zone-content-region-content-omega-drupal-7) by Katharine Ruhl (who I learned was a DC resident while writing this post, awesome) where she described moving her breadcrumbs from the content zone to the content region. I adapted her approach to move my breadcrumbs to a new zone entirely. 

First things first - I'm assuming you're running Drupal 7 with Omega 3.x, and this tutorial is from that vantage point. To get things started off, we dive into the default Omega theme folder and pull out the zone--content.tpl.php file. That file will look a lot like this:

```php
<?php if ($wrapper): ?><div<?php print $attributes; ?>><?php endif; ?>  
  <div<?php print $content_attributes; ?>>    
    <?php if ($breadcrumb): ?>
      <div id="breadcrumb" class="grid-<?php print $columns; ?>"><?php print $breadcrumb; ?></div>
    <?php endif; ?>    
    <?php if ($messages): ?>
      <div id="messages" class="grid-<?php print $columns; ?>"><?php print $messages; ?></div>
    <?php endif; ?>
    <?php print $content; ?>
  </div>
<?php if ($wrapper): ?></div><?php endif; ?>
```

Drop that folder into the templates folder of your new theme, but rename it zone--preface.tpl.php (substitute preface for the zone of your choosing, natch). This will alert the preface zone that it should expect breadcrumbs. Don't be distracted by the `<?php print $content; ?>` statement - Drupal uses that `$content` variable for every zone, not just the content zone. 

You're going to need to strike the `$messages` section out of this, as we don't need our Drupal error messages to pop up in two sections. Modify your new zone--preface.tpl.php file so it looks like this: 

```php
<?php if ($wrapper): ?><div<?php print $attributes; ?>><?php endif; ?>  
  <div<?php print $content_attributes; ?>>    
    <?php if ($breadcrumb): ?>
      <div id="breadcrumb" class="grid-<?php print $columns; ?>"><?php print $breadcrumb; ?></div>
    <?php endif; ?>    
    <?php print $content; ?>
  </div>
<?php if ($wrapper): ?></div><?php endif; ?>
```

Next, make a second copy of the zone--content.tpl.php file, place it in your theme's template folder, but keep the name the same this time. We're going to now strike the breadcrumb logic out of our new zone--content file so we don't have double breadcrumbs. 

```php
<?php if ($wrapper): ?><div<?php print $attributes; ?>><?php endif; ?>  
  <div<?php print $content_attributes; ?>>     
    <?php if ($messages): ?>
      <div id="messages" class="grid-<?php print $columns; ?>"><?php print $messages; ?></div>
    <?php endif; ?>
    <?php print $content; ?>
  </div>
<?php if ($wrapper): ?></div><?php endif; ?>
```

And that's all we need to do for the templates! We've now overridden two template files - the zone--preface file to add the breadcrumbs to that zone, and the zone--content file to remove them from that one. We diligently clear our caches, only to note that our breadcrumbs have totally disappeared and we're now getting an "Undefined variable $breadcrumb" error at the top of our pages. 

Omega appears to have the `$breadcrumb` variable hard-coded into the content zone, so we need to write an extra function to alert our `zone--preface.tpl.php` file to expect a `$breadcrumb`. Create a file in the preprocess folder of your theme and name it `preprocess-zone.inc`. Omega will see this as extra logic that it needs to incorporate before processing the theme. Type this function into that file:

```php
<?php

function thisisyourthemename_alpha_preprocess_zone(&$vars) {
	$theme = alpha_get_theme();

	if ($vars['zone'] == 'preface') {
		$vars['breadcrumb'] = $theme->page['breadcrumb'];
	}
}

?>
```

The logic here is relatively straightforward. We declare a `$theme` variable that pulls in our existing theme data. We then add `'breadcrumb'` as a new variable within the theme - but only for the preface zone. 

And that's it! Clear your caches, save configuration and hit refresh. You'll find that the breadcrumb trail is now happily appearing in your preface zone, ready to be styled however you like. 