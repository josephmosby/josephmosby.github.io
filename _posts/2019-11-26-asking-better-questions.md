---
title: Asking better questions
layout: post
---

Here is a tough reality for most "data science" positions: nine times out of ten, the question that matters most doesn't need a cutting edge technology solution. It needs a dashboard, a nifty spreadsheet, or a simple report. 

Once upon a time, my data science team worked in a supercomputing environment for a whole year. We had access to petabytes of data to answer whatever questions we could ask around a general theme. I wrote beautiful stuff using the latest and greatest libraries and frameworks. I optimized aggressively, changing my code from Python with a shim to native languages. 

At the end of the day, the things that produced the most tangible outcomes for that particular project were some canned jobs and an interface for analysts to write some ad-hoc queries for follow-up on whatever the jobs produced. 

I had not initially been asking the right questions.

### Leverage

In a [now-moderately-famous tweetstorm](https://twitter.com/naval/status/1002106893265920000?s=20), venture capitalist summed up the power of code in a few sentences:

> Code and media are permissionless leverage. They're the leverage behind the newly rich. You can create software and media that works for you while you sleep. An army of robots is freely available - it's just packed in data centers for heat and space efficiency.

"Leverage" has become a bit of a watered-down term in the past decade or so of corporate-speak. More's the pity. It's now commonly used to denote simply "using something well" minus its original implication of "with some sort of amplification beyond what you could do on your own."

Stock traders have a notion of _margin_: a trader will take out a loan to purchase additional shares of stock than they could afford otherwise. If the price goes up, they pay back the loan and pocket the extra dollars. If the stock goes down, they're still on the hook for the loan amount. Their equity position is *leveraged*. The gains are highly amplified, but the losses are too.

Code is a form of leverage. It doesn't make ideas good or bad, but it amplifies them both alike. 

A bad question with code amplifying it becomes a much worse question.

### Bad questions

From 2014 through 2018, Amazon tried to roll their own AI-driven resume evaluator [that did not work out the way they intended](https://www.reuters.com/article/us-amazon-com-jobs-automation-insight/amazon-scraps-secret-ai-recruiting-tool-that-showed-bias-against-women-idUSKCN1MK08G). Their apparent question: "can we use the resumes for successful candidates over the past ten years to predict which resumes we'll like going forward?"

The results were unfortunate. From the article: 

> Top U.S. tech companies have yet to close the gender gap in hiring, a disparity most pronounced among technical staff such as software developers where men far outnumber women. Amazon’s experimental recruiting engine followed the same pattern, learning to penalize resumes including the word “women’s” until the company discovered the problem.

The good questions perhaps a few steps backwards in their decision process might have looked something like this:

1. When we look at engineers who have been successful at Amazon over several years, what attributes do they share? 
2. Are these attributes different across teams? 
3. Are there any apparent biases in these attributes? 
4. Do these attributes appear to align with the attributes we think we'll need over the next 5-10 years, or should we be looking for different ones?

These questions don't need "artificial intelligence." They need access to the Amazon performance review database, a little bit of SQL, and some forward thinking on the part of management. 

Amazon spent four years and untold amounts of engineering code to answer the question they probably didn't want to answer: yes, we've been biased in our hiring over the past ten years. Not how to hire better engineers going forward.

### Snake oil

Princeton computer science professor Arvind Narayanan recently [gave a talk](https://www.cs.princeton.edu/~arvindn/talks/MIT-STS-AI-snakeoil.pdf) on "AI snake oil" where he tangentially touched on the topic of bad questions. He breaks advances in AI into three rough categories:

1. Perception (content identification, speech to text, facial recognition)
2. Automating judgment (spam detection, essay grading, content recommendation)
3. Predicting social outcomes (predicting recidivism, predicting job performance)

In "perception" tasks, AI has advanced to the point of human accuracy. Given enough data (which is itself a challenge) and compute, AI can get the job done. In "judgment automation" tasks, AI can mostly get there, but there is a band where humans may disagree. If I train a content recommendation algorithm on one human, but then try it out on a slightly different human, I may get slightly different answers. That's not necessarily a problem, but it does mean that the data scientist needs to be concerned with how important that yes/no distinction is.

But with "predicting social outcomes," we see abundant quantities of snake oil - and therefore bad questions. Dr. Narayanan walks through past experiments in predicting recidivism, showing that artificial intelligence methods prove no better than random scoring. And, more perniciously, it predicts "re-arrest" rather than "recidivism," because that was what the available data tracked. 

So not only does the algorithm not work, but it also starts to equate "re-arrests" with "criminal activity." It doesn't ever consider if the arrested individuals were later tried and proven guilty or innocent. It assumes that if they were arrested, they must have committed some criminal activity.

Code as leverage. It doesn't make a question bad or good, but it does make a bad question worse.

### Good questions

If bad questions can be made into horrible questions with data science, how then do we ask good ones?

*Suggestion 1: When considering questions, figure out how to solve them with human intelligence before adding data science.*

Consider a data science task where we need to segment customers into groups based on likelihood of responding to a particular marketing message. This is commonly done with some sort of machine learning clustering task, but the need was first fulfilled by humans. You'd do focus groups that represented cross-sections of your populace, show them the marketing materials, then gauge responses. Clustering, at its best, is intended to identify _better_ cross-sections of the population, but the ultimate need here is the same. 

A human could perform a clustering task. The human would identify sensible numbers of groups (or, in this example, market segments). They'd consider the data available on each of their sample people and place that person into one of their groups. 

We can describe our task alongside a human approach to solving the issue - thus, we have a way to validate if anything we do in data science makes sense. Would a human make the same choices given the same data?

*Suggestion 2: Identify the discrete problem and describe an abstract solution before writing a single line of code.*

On the surface, our marketing problem looks simple. "Break these people into groups." But there's nuance there. 

"Break these people into groups" feels rough when we say it out loud, but that's how a lot of data science tasks actually start without foresight. Segmenting into groups that are all 100 people wide, or segmenting into groups by age alone, or by state of residence, would all meet that task's objective.

"Okay, okay," you say. "Break this population into groups based on likelihood of responding to marketing." But now I think: "does that mean 'all' marketing? Television versus radio versus online? What does response mean: they liked the ad or they actually went and bought something?"

"FINE." you now say. "Segment this population into groups based on their likelihood of purchasing a product after viewing online marketing." I continue to ask: "any product?" "Yes." "Can you show me how we can track this through all of our systems now - from the advertising release, on through viewing, on through final sale?" "Sure, it's like this."

"Segment this population into groups" --> "Segment this population into groups based on their likelihood of purchasing a product after seeing online marketing."

I have a discrete question now. What about my abstract solution?

Initially, this problem looked like a clustering problem (break into groups). After we refined the question, though, it starts to look like a classification problem. (Buys/does not buy product) We can start to say "my output should generate a 'likelihood to buy product' score for each customer. Then we'll place all of those on a line and group into 0-20%, 21-40%, etc.

All of that was done and written down without a single line of code. But now we know what we want.

*Suggestion 3: Map data to your proposed solution. Confirm that it's the right data.*

If we've confirmed our question and loosely confirmed our approach, our next thing to nail down is our data - which, in my anecdotal experience, tends to be where things break down most often. 

Let us re-imagine our earlier market segmentation problem. Assume that the organization tracks marketing impressions and clicks, and assume that the sales team captures data at the time of sale. Seems great on our surface, right? But - maybe our marketing team has one system that uses a specific Target ID for each prospect, and the sales system has a completely different numbering scheme for sales accounts.

"FINE." You say again. "I'll join them on first name / last name and email." But the sales team can't give you that information, because it's personally-identifiable information, and according to company policy it can't leave the sales system. Your project might be dead on arrival, but that's at least something you can find out (and hopefully fix) before your project gets started.

This problem is masked from many junior data scientists because so much pre-work goes in to getting it right. Kaggle competitions come with data. Managers _should_ do plenty of pre-work to make sure their team has what they need to get started. A big leap forward in the data scientist's career is realizing how to go get the data they need to solve the question that will have the largest impact to the business.

### Dashboards and spreadsheets

When I first began writing this post, I started with a simple premise: sometimes a simple dashboard or a spreadsheet is the best way to solve a problem. Sometimes, when we frame our question in the right way, that's all we might need. And that's okay. That's why the data scientists were brought in - to answer the need on the table, not try to rope in the niftiest new tech. 

But when we get to the point where knocking through those dashboards and spreadsheets becomes rote, automated, and easy - then we open the door for the really challenging problems.
