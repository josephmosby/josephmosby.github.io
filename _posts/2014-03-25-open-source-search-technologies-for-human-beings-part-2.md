---
layout: post
title: Open Source Search Technologies for Human Beings - Part 2
---

In the [first part](http://josephmosby.com/2014/03/24/open-source-search-technologies-for-human-beings-part-1.html) of this series, we investigated the basics of how a search engine theoretically works. The process we described in part 1 didn't actually require a computer at all - any person could theoretically follow those exact same steps. Indeed, writers of complex research materials did so for decades before the first computers were invented. 

Though there is an entire profession based strictly around organizing and categorizing information and retrieving it at a later time (librarians), the average person doesn't want to be doing that on a daily basis. We've got computers for that, but that means we have to write a program to perform all of those steps we don't want to do ourselves. This brings us to [Lucene](https://lucene.apache.org/core/).

### Lucene

To quote exactly from the official manual: "Lucene is a high-performance, full-featured text search engine library written entirely in Java." Lucene performs all of the search engine features we described in part 1: it reads text-based documents, creates an index of those documents, and retrieves the documents based on search keywords. It does this quickly and efficiently with many features that make it appealing to computer programmers who wish to incorporate it into their applications. 

Let's take a quick tour of Lucene by playing around with its demo directly. 

	java org.apache.lucene.demo.IndexFiles /{path}/lucene-4.7.0/licenses

With this command, we first call the Java available on most of our personal computers. Lucene is written entirely in Java, a programming language popular with the federal government and many large commercial enterprises. We then call a Java-specific Lucene command - IndexFiles - and ask Lucene to index all the files in the "licenses" directory. This will produce an index of all of the legal software license documents that apply to the use of Lucene. When we do this, Lucene will happily print out a stack of messages letting us know that it's indexing:

```
Indexing to directory 'index'...
adding /{path}/lucene-4.7.0/licenses/ant-1.8.2.jar.sha1
adding /{path}/lucene-4.7.0/licenses/ant-LICENSE-ASL.txt
adding /{path}/lucene-4.7.0/licenses/ant-NOTICE.txt
... so on and so forth...
```

And now we have an index! Let's query it for a search term:

```
java org.apache.lucene.demo.SearchFiles
Enter query: 
GNU
Searching for: gnu
2 total matching documents
1. /{path}/lucene-4.7.0/licenses/javax.servlet-LICENSE-CDDL.txt
2. /{path}/lucene-4.7.0/licenses/servlet-api-LICENSE-CDDL.txt
```

I entered the SearchFiles command, and Lucene immediately prompted me for a search term. Thinking that I might find some reference to the [GNU Public License](https://www.gnu.org/copyleft/gpl.html) in a piece of open source software, I typed in "GNU" as my search term. Lucene found two files that contain the word "GNU" and returned them to me here. But if I try another term, it finds nothing at all:

```
java org.apache.lucene.demo.SearchFiles
Enter query: 
football
Searching for: football
0 total matching documents
```

There's a lot going on behind the scenes here with even this tiny demo app, but the basics are quite simple. Lucene has followed the exact same process for indexing and searching that we described in part 1. But what if we need to parse through an HTML or Word document rather than a simple text document? We'll need something a little bit more robust, which is where Solr and Elasticsearch come in... in [part 3](http://josephmosby.com/2014/03/25/open-source-search-technologies-for-human-beings-part-3.html). 
