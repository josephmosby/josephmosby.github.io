---
layout: default
title: Creating a Mobile Content App with (Almost) Real Time Edits
--- 

It's not too often that we're asked to put together a native mobile app at [APCO Worldwide](http://www.apcoworldwide.com), but it does happen from time to time. We're a communications firm first and an app development firm second, and that means we have to plan for regular content additions, modifications and deletions that often need to happen immediately. We can't afford to recompile code and go through an app submission process every time someone needs to add a new story to an app, so we have to bake some flexibility into the system itself.

We also like to give our communications teams (copywriters, speechwriters, etc.) the ability to edit their own content on the fly when they need to. It's certainly easier for all parties concerned. Content changes don't have to be worked into a development queue, and developers don't need to go through the same quality control cycles over and over again if we build something flexible from the start. To this end, we've often opted to use Drupal for our CMS. We've trained our communications teams on how to use it and now have a predictable development pattern for the sites we build to deal with similar use cases. It gets hacky from time to time, but it works for a PR firm. 

One of our comms teams came to us in January with a content rich app idea that needed to be native on both iOS and Android. We knew it would require regular updates with a minimum amount of fuss, so we needed to find a way to feed content to the app rather than store it all locally. We also needed the application that populated that feed to have an interface that was familiar to our communications team. We knew we could solve the second problem with either Drupal or Wordpress, but what to do with the first?

Enter one of my new favorite ways to spend taxpayer money: the Drupal [Content API](https://drupal.org/project/contentapi) module. This project was put together jointly by the Federal Communications Commission and [Seabourne Consulting](http://seabourneinc.com/), and it does exactly what it sounds like: it makes a content API out of your Drupal website. There's a nice point-and-click interface in the Drupal administrative console that allows you to select the content types you'd like to feature in your API, the endpoints you'd like to use, and the fields you'd like to include, then voilà - an XML-formatted API appears. It's beautiful.

So we've now got a nice XML feed of all of the content that's going to populate this app happily displayed out there on the web. Our users can add, delete and modify entries and the XML feed will automatically update. 

Getting this data into the app was another story altogether. We followed these rough steps to build our system on both iOS and Android:
1. Connect to the API 
2. Download the main XML file, which lists all content 
3. Parse the XML file and check the IDs against our existing data present on the phone
4. Download any new or modified IDs
5. Lay out app for user content viewing

And that's pretty much it. I won't go into a detailed tutorial - I leaned heavily on another developer for much of the native app work - but I will share a few gotchas.

The Content API module takes a non-configurable approach to pagination. In the standard code, you get ten items per XML page, and that's it. I understand the rationale for why a government-sponsored content API would want to be careful on how much data it allowed out at any one time, but that wasn't going to work for this project. Around line 500 in `contentapi.module`, one finds the following code snippet:

```php
$limit = (isset($_GET['limit'])) ? (integer)$_GET['limit'] : 10;
...
$limit_cap = variable_get('contentapi_limit', 10);
```

Change those 10's to 200's and now we're talking. I am ashamed of the inelegance of this hack, but it got the job done.

Our second headache was XML parsing on Android. When we had the first working build up and running, it took five minutes to download the initial feed on a new installation. Android does a great job of background task management, but five minutes for a set of downloads that were mostly text was unacceptable. We did our homework, and it turns out that the [standard approaches for XML parsing are absolute garbage on Android](http://steveliles.github.io/comparing_java_xml_parsing_mechanisms_for_android.html). As [Steve Liles](http://twitter.com/steveliles) points out in the above post, it's far more efficient to swap in Java's SAX parser to manage your XML downloads. We got our full download time to about a minute - and given that we were also having to deal with PDFs and images, I'll take it. 

We had a lot of fun building this app and thinking through how to make it play nicely on multiple devices with an easy-to-use central administration console. We'd love for you to take a look at our [Android handiwork](https://play.google.com/store/apps/details?id=com.meetingsmeanbusiness.mmb). I'll share the iOS version once it finishes the Apple review cycle. Enjoy!