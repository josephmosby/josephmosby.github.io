---
layout: post
title: Open Source Search Technologies for Human Beings - Part 3
---

In the [first part](http://josephmosby.com/2014/03/24/open-source-search-technologies-for-human-beings-part-1.html) of this series, we talked about the nuts and bolts of search engines: how they create a nicely organized index of keywords and documents and use that index to find documents containing keywords. [Part 2](http://josephmosby.com/2014/03/25/open-source-search-technologies-for-human-beings-part-2.html) walked us through Lucene, an open source search engine written in Java that turns our Part 1 idea of a search engine into a computer program. With Part 3, we're going to build upon Lucene with Solr and Elasticsearch, two programs that use Lucene to create a fully-featured web search engine.

We saw that Lucene can do some basic indexing and searching, but it's fairly limited. It can only handle plain text documents well, it doesn't have any ability to connect to the web, and even the tiny little command-line application we used to "talk" to Lucene had to be built as a demonstration. Needless to say, Lucene just doesn't have what we need to serve as a web search engine. That's where Solr and Elasticsearch come in. They use Lucene as their core, but they tack on additional features in different ways to meet the needs of their customers. We'll take a first look at Solr, the federal government's legacy search engine, then follow it by showing the future with Elasticsearch.

### Solr

[Solr](https://lucene.apache.org/solr/) began as an enterprise search engine in 2004, and was designed for websites from the beginning. It was initially part of the closed source code owned by CNET, but was released as open source software when CNET donated the code to the Apache Software Foundation a a few years later. 