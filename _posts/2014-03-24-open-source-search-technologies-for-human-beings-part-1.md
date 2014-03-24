---
layout: default
title: Open Source Search Technologies for Human Beings - Part 1
---

Search is one of those features that's become so "baked in" to the way we experience the web that it's often an afterthought for us as users. We peck a few well-chosen words into the Google search bar, press enter, and end up where we needed to be. It's become a mental backup system to the point that we no longer even need to bookmark a link any more as long as we can remember the few keywords that will bring us back to the page. Though I develop websites every single day, I had never actually thought about the search technology that brings users to my page and allows them to find the content they wanted.

I was suddenly forced to confront my ignorance of search when I learned that the General Services Administration would be changing their search software from [Solr](https://lucene.apache.org/solr/) to [Elasticsearch](http://www.elasticsearch.org/). Having no idea how either of them worked, I started doing my homework immediately. 

### How Search Works

Though the specific implementations vary across platforms, the core of any text-based search technology is the same. The subject matter will be broken down into small components that can be stored in an index that references back to the document in question. The name is not accidental: this works in the same way as a word index that points back to pages at the back of a heavy research book. As we add more documents to the index, this process is repeated and the index size and complexity increases. 

In this example, our documents can be anything primarily composed of text. Web pages, Word documents or eBooks could all be comfortably fed into our search engine and happily indexed. Eventually, though, we'll need to retrieve that information if we want a fully functional search engine. An index of extremely well-organized keywords and documents won't do us any good if we never use it to retrieve the information we need. To do so, we'll "query" the index by feeding it a keyword. The search engine will then check its index for all documents that match that keyword and return us the corresponding list of document. If we add more than one keyword, the search engine will query the index to find documents that show up for each individual keyword then compare the results to bring us documents that contain all of our keywords. 

Let's take a quick visual walk through this process. Say we have a document (NFL.doc) that we'd like to index. Our document contains quite a bit of text about the NFL, all of which will be broken down and inserted into our index.

![Picture of a document that contains text about the NFL](/images/NFLdoc.png)

Our indexing process is going to examine the text of the document, split out the words, and point those words back to NFL.doc.

![Table of keywords that all correspond back to NFL.doc](/images/index1.png)

We'll then add these keyword/document pairings into our main index, which contains similar pairings for other documents.

![Table of keyword/document pairings that contains NFL and MLS references](/images/index2.png)

Our user will search for a term - in this case, football - and our search engine will return the documents that correspond to that term in our index.

![Input box prompting user to search. The user has entered "football" into the input box.](/images/search.png)

Our search engine will return a single result from the index. The search term "football" only corresponds to a single entry in the index, the NFL.doc document.

![Table showing a single keyword/document pairing that matches the word football with NFL.doc](/images/single_search_result.png)

And that's the core of a search engine to get us started! In Part 2 I'll talk a little bit about Lucene, the nuts and bolts of both Solr and Elasticsearch. In Part 3, I'll compare the two pieces of software to show how they each bring search technology to life for the web. 