---
layout: post
title: Open Source Search Technologies for Human Beings - Part 3
---

In the [first part](http://josephmosby.com/2014/03/24/open-source-search-technologies-for-human-beings-part-1.html) of this series, we talked about the nuts and bolts of search engines: how they create a nicely organized index of keywords and documents and use that index to find documents containing keywords. [Part 2](http://josephmosby.com/2014/03/25/open-source-search-technologies-for-human-beings-part-2.html) walked us through Lucene, an open source search engine written in Java that turns our Part 1 idea of a search engine into a computer program. With Part 3, we're going to build upon Lucene with Solr and Elasticsearch, two programs that use Lucene to create a fully-featured web search engine.

We saw that Lucene can do some basic indexing and searching, but it's fairly limited. It can only handle plain text documents well, it doesn't have any ability to connect to the web, and even the tiny little command-line application we used to "talk" to Lucene had to be built as a demonstration. Needless to say, Lucene just doesn't have what we need to serve as a web search engine. That's where Solr and Elasticsearch come in. They use Lucene as their core, but they tack on additional features in different ways to meet the needs of their customers. We'll take a first look at Solr, the federal government's legacy search engine, then follow it by showing the future with Elasticsearch.

### Solr

[Solr](https://lucene.apache.org/solr/) began as an enterprise search engine in 2004, and was designed for websites from the beginning. It was initially part of the closed source code owned by CNET, but was released as open source software when CNET donated the code to the Apache Software Foundation a a few years later. Solr has since become an integral part of the Lucene ecosystem to the point that the two programs are now maintained by the same development team. 

Solr runs as an application server. Any program making use of a Solr server must make some sort of request to the server (such as adding documents to be indexed or querying for documents with "football" in the text). Solr will then respond to that request with search results, which the program can then display to the user, load into a web page or incorporate into a larger application. 

![Diagram of a program adding a file to the Solr index](/images/solr_doc_1.png)

The popularity of Solr for years brought it a lot of support from developer communities across many different languages and platforms. Solr proudly boasts support for PHP, Ruby, Python, Drupal, Wordpress, and a stack of other platforms that make adoption easy for users regardless of their existing technology stack. It's fast to set up, fast to run, and easy for an administrator to maintain through a web-based administrative interface.

That being said, Solr has a stack of limitations. It began as a centralized Java application, and it still requires a lot of familiarity with Java to run effectively. And all the Java in the world can't make up for the fact that Solr was built to be run from a central location. Elasticsearch took a different approach.

### Elasticsearch

[Elasticsearch](http://www.elasticsearch.org/) is the new kid on the block of open source search engines. [Shay Baron](https://twitter.com/kimchy) started writing the roots of Elasticsearch in 2004 with the Compass project, but soon realized that he would have to rewrite Compass to build it into a fully "scalable" system that could handle a substantial amount of search traffic at once without crashing. In 2010, Compass was rolled into the Elasticsearch project with all of the features needed to challenge Solr's dominance.

Elasticsearch (which I'll just abbreviate as ES from now on) was built from the ground up to be a distributed search platform rather than a centralized system like Solr. Whereas Solr has to handle each search request from a central hub, ES can split the workload over a cluster of search servers to speed up processing. Search starting to run slowly? Add more servers, no problem.

![Diagram of a program adding a file to the Elasticsearch index, which consists of many servers](/images/es_doc_1.png)

To be fair, Solr is now technically a distributed system as well through the addition of [Zookeeper](http://zookeeper.apache.org/). Zookeeper is a program designed to keep multiple servers in synchronization as a single Solr instance. It's an afterthought, though, and Solr still is not capable of handling many of the advanced distribution features that ES boasts by default. 

Elasticsearch also allows programmers to interact with a single RESTful API when they want to update and query the search engine. This is incredibly attractive to the average web developer who often did not study Java programming in school but interacts with RESTful APIs on a daily basis. With a single tailored request sent to ES' API, developers have search results ready to go without the need for a full-featured Java application.

Modern search engines also have a specific syntax for creating complex queries (for example, typing "site:apache.org Solr" will return any results for Solr on the Apache website only), and Elasticsearch is no different. The search engine also comes with a stack of plugins available and programming libraries written for many of the more esoteric languages to complement the common options available to both ES and Solr developers.

### Conclusion

Elasticsearch offers a number of benefits to web developers, and it's easy to see why the federal government is making moves to convert Solr instances into Elasticsearch ones. RESTful APIs and distributed clusters simply make perfect sense in a web environment. I'll be looking forward to seeing continued improvements in the federal government's search capabilities as they work through the upgrade.

-- special thanks to Kelvin Tan's great side-by-side breakdown of the technical differences between Solr and Elasticsearch here: [http://solr-vs-elasticsearch.com/](http://solr-vs-elasticsearch.com/)