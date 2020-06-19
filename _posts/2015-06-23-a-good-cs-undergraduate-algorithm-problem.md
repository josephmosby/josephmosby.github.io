---
layout: post
title: A good CS undergraduate algorithm problem
tags: code
---

Okay, here's a question for an undergraduate algorithms class to solve. In a non-relational database, we have a users collection with user preferences for breaking news alerts. In a separate collection, we have news stories with tags and searchable content. We will run a scheduled job that will pair the two and send news alerts to users if a story that matches their alert preferences has been published in the last half hour. 

Given that we have approximately 50,000 users with an average of 5 alerts each and 500,000 stories with an average of 20 topics each and ten paragraphs of searchable content, how do we build this job in a way that it won't crash the database?

Example tables:

users:

	[
		{ 
			email: "jane.doe@example.com",
			alerts: [
				{
					type: "open-search",
					term: "Barack Obama"
				},
				{
					type: "topic",
					term: "politics"
				},
				{
					type: "topic",
					term: "congress"
				},
				{
					type: "open-search",
					term: "natural gas"
				},
				{
					type: "open-search",
					term: "solar power"
				}
			]
		},
		{ 
			email: "john.smith@example.com",
			alerts: [
				{
					type: "open-search",
					term: "Joe Biden"
				},
				{
					type: "topic",
					term: "politics"
				},
				{
					type: "open-search",
					term: "sunglasses"
				},
				{
					type: "topic",
					term: "house"
				},
				{
					type: "topic",
					term: "senate"
				},
				{
					type: "open-search",
					term: "solar power"
				}
			]
		},

		....
	]

stories:

	[
		{ 
			headline: "The Standard Lorem Ipsum passage",
			content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.......",
			tags: [
				{
					term: "Barack Obama"
				},
				{
					term: "president"
				},
				{
					term: "America"
				}
			]
		},
		{ 
			headline: "More lorem ipsum passages",
			content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.......",
			tags: [
				{
					term: "Joe Biden"
				},
				{
					term: "vice president"
				},
				{
					term: "Senate"
				}
			]
		},
	]

The end result should look something like:

alerts:

	[
		{ 
			email: 'john.doe@example.com',
			stories: [
				{ 
					headline: "More lorem ipsum passages",
					content: "Lorem ipsum dolor..."
				},
				{
					headline: "Another lorem ipsum passage",
					content: "Lorem ipsum dolor..."
				}
			]
		},
		{ 
			email: 'jane.smith@example.com',
			stories: [
				{ 
					headline: "Another lorem ipsum passage",
					content: "Lorem ipsum dolor..."
				},
				{
					headline: "The best of lorem ipsum",
					content: "Lorem ipsum dolor..."
				}
			]
		}
	]

Would love to hear your questions or solutions: josephmosby@gmail.com