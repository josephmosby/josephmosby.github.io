---
layout: post
title: A brand new code review and integration workflow
tags: code
---

I've been fortunate to join the [National Journal](http://www.nationaljournal.com/) with a stack of brand new product managers and developers. As we form a new product team, we also need to address some of the operational nuances of bringing our team together. Part of that process includes defining and standardizing our workflow for code review, testing, and integration.

Our process starts by branching master off into a specific feature branch, with the intention that we'll push a set of changes through the review and testing process as a single set of commits that only pertain to that feature. 

We keep our feature branches local (though publishing a branch to GitHub isn't a problem). Once we're ready for our code to go to peer review, we execute the following commands to bring it into the review branch:

	$ git checkout review
	$ git merge feature-branch
	$ git pull origin review

We're approaching the code review process with a simple checklist, inspired by principles from Atul Gawande's [The Checklist Manifesto](http://www.amazon.com/Checklist-Manifesto-How-Things-Right/dp/0312430000/ref=sr_1_1/185-7726352-5707960?s=books&ie=UTF8&qid=1424833091&sr=1-1&keywords=the+check+list+manifesto) and Guido van Rossum's [PEP 8 guidelines](https://www.python.org/dev/peps/pep-0008/) for Python code. 

1. My code is indented with tabs.
2. Classes follow the CapWords naming convention and functions follow the lowercase_underscore convention.
3. Every public class and function has an associated docstring describing what the item does.
4. Any unusual or complex functions and algorithms have an associated comment describing the rationale for the approach. Any use of Exceptions is documented with comments.
5. The file does not have any code that is commented out, nor does it have any "TODOs".
6. All print() functions that go to the development console have been removed.
7. The code has associated tests.

Our checklist is only seven items long. We chose to leave off some items from PEP 8 compliance because we believe these items encompass the heart of good, readable Python code that our team can agree on as we're developing at a rapid pace. Holding up code that deals with a priority ticket because someone's lines have too many characters is not justifiable, but stopping a bugfix because it's undocumented most certainly is. 

In addition to these checklist items, we talk through our logical approach to solving the problem, the necessity of certain functions or exceptions, and possible scenarios that might cause failures. If the peer reviewer is satisfied with the code, we execute the following commands to merge our changes with testing:

	$ git checkout testing
	$ git pull origin review
	$ git pull origin testing

The testing branch is used by our functional testers to determine that everything's working properly. The app should work perfectly at this stage - if it doesn't, it's headed back to the review pipeline. No one commits directly to testing, so any conflicts will be resolved during the commit to review. If the testers are satisfied, we prepare for the move to production with the following commands:

	$ git checkout staging
	$ git pull origin testing
	$ git pull origin staging

To recap: 

![Git workflow](/images/review_workflow.svg)

1. Create local branch of master for the feature.
2. Complete work in branch and merge to review. 
3. Peer review changes and pull review into testing.
4. Test changes and pull into master.

What do we have left to do? 

1. Proper integration into our production environment. We're looking at something like [TravisCI](https://travis-ci.com/) or [CircleCI](https://circleci.com/) to manage our build process. 
2. Write tests for all the code that was written before we standardized on a review process. 
3. Write a PEP 8 linter to condense the style review. 
4. Bonus: it might be nice to have a simple push-button approach to move everything between branches. 

This is getting us started. We're still workshopping it, but it's standardizing us on an approach and getting our team in line.