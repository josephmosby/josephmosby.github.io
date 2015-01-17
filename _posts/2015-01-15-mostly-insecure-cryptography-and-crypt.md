---
layout: post
title: Mostly insecure cryptography and crypt()
tags:
- pymod
---

In the 1970s, DES was all the rage. The Data Encryption Standard was the standard for encryption of federal government data and everything unclassified was expected to use it. The algorithm uses a 56-bit key size and some NSA-suggested substitution boxes to encrypt and decrypt data. It was great for the 1970s, but we knew it was susceptible to brute-force attacks then - and in the 1990s, DES was finally cracked. It's since been replaced by more robust cryptographic algorithms, but it remains a part of the legacy Unix codebase via the `crypt(3)` tool. 

Because you might need to one day access legacy systems where data is encrypted using `crypt(3)`, Python has provided a helpful little module with `crypt`. It has a single function: `crypt.crypt(word, salt)`, where the word represents the data to be encrypted and the salt is a two-character alphanumeric string. It's as easy as would be expected:

	import crypt

	print crypt.crypt('hello there', 'ht') # ht5gSI1o04H8I

And with just that simple function, we have an DES-encrypted password for use on a legacy Unix system. In case you ever need one.