---
title: "How autoregressive and diffusion LMs imitate each other, and why it is inefficient"
description: "A claim from week 1, made easier to follow with pictures: each model type can do what the other does, and what it costs to do so."
paper: cross-lingual-knowledge-pretraining
role: learning
task: teach
by: [liadber]
---

## Why this matters

In week 1 it was claimed that diffusion and autoregressive models are equivalent: each can reach the same results as the other, only at a higher cost. To make the claim easier to follow, here is a simple illustration.

## The idea

Both model types do one thing: they assign a probability to every possible sentence. The difference is only in *how* they produce a sentence from that distribution.

{% include figure.liquid path="assets/img/posts/autoregressive-vs-diffusion/side-by-side.png" class="img-fluid rounded z-depth-1" caption="The same sentence generated twice. Left: autoregressive, one word at a time, each step seeing only what came before. Right: masked diffusion, all positions guessed at once, the confident ones committed, the rest re-guessed in the next round. The numbers are made up; the shape is not." %}

**What is going on.** An autoregressive model is a function that answers one question: given the words so far, what comes next? A masked diffusion model answers a different one: given a sentence with holes, what goes in each hole? Both learned from the same text, so both know the same facts, for example how often "It's raining outside today" occurs. They only take the question in a different shape.

**Why this is always possible, not just in the example.** Any distribution over sequences can be written as a product of "next given previous" terms. That is the chain rule of probability, not a property of neural networks. So whatever distribution a diffusion model produces, an autoregressive factorization of it exists, and a large enough autoregressive model can learn it. The other direction is easier: a masked diffusion model that unmasks exactly one position per round, left to right, *is* an autoregressive model. Autoregression is a special case of diffusion with a fixed unmasking order.

{% include figure.liquid path="assets/img/posts/autoregressive-vs-diffusion/table-tree.png" class="img-fluid rounded z-depth-1" caption="A tiny world with three possible sentences. Left: the table of probabilities, which is what any model produces in the end. Right: the same table as a tree of choices (first word, then second word given the first), which is what an autoregressive model learns. Divide the table to get the branches; multiply the branches to get the table back. Every table can be written as a tree." %}

**So what is the difference? The cost.** Since the model is just a function and the generation loop around it is ordinary code, imitating the other model means writing a different loop around the same weights, and the price is the number of calls. To get what diffusion gets in one call, a table of candidates for every position, the autoregressive loop has to ask about every possible beginning: 3 calls for position 2, 9 for position 3, 27 for position 4. In our tiny world that is 44 calls instead of 2; with a real vocabulary it is not feasible. The other direction is cheaper but still wasteful: diffusion commits one position per call, left to right, computing all positions every time and discarding most of them. Four calls instead of two, and its parallelism is gone. This is the "you wouldn't run it in polynomial time, you'd use the other one" remark from class.

{% include figure.liquid path="assets/img/posts/autoregressive-vs-diffusion/four-runs-en.png" class="img-fluid rounded z-depth-1" caption="Four ways to produce the same sentence, all starting from four holes. Under each model call: how many calls it cost, and what came out (taken, left as a hole, or computed and discarded). Column height is the price." %}

**One caveat.** The equivalence is about ideal models with enough capacity and enough steps. Real models learn differently from the same data: autoregressive models train on correct text and then have to continue their own mistakes; parallel generation has the multimodality problem (each position picks something locally plausible, and together they do not fit). "What is possible" and "what actually happens" are two different levels, and the distinction comes up everywhere in this field.

**Why it matters for the course.** Most of the papers we will read are about autoregressive models, because that is what most research uses. The equivalence is the reason this is fine: what we learn about how one kind of model learns, remembers and fails carries over to the other. The architecture sets the cost, not what can be learned.
