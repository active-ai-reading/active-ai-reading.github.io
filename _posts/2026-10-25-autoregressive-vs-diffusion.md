---
title: "Why autoregressive and diffusion LMs can imitate each other (and why it still costs)"
description: "A claim from week 1, made easier to follow with a picture: the two model types can reach the same results, each at a cost."
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

**What is going on.** Both models were trained on the same text, where "It's raining outside today" appears with some frequency. The autoregressive model remembers that frequency *split into steps* ("after 'It's raining', 'outside' 80% of the time"). The diffusion model remembers it *as hole-filling* ("between 'It's' and 'outside', 'raining' 90% of the time"). Two different ways of storing the same fact. The fact (how often the sentence occurs) does not depend on the storage format, so anything one model can remember, the other can too.

**Why this is always possible, not just in the example.** Any distribution over sequences can be written as a product of "next given previous" terms. That is the chain rule of probability, not a property of neural networks. So whatever distribution a diffusion model produces, an autoregressive factorization of it exists, and a large enough autoregressive model can learn it. The other direction is easier: a masked diffusion model that unmasks exactly one position per round, left to right, *is* an autoregressive model. Autoregression is a special case of diffusion with a fixed unmasking order.

{% include figure.liquid path="assets/img/posts/autoregressive-vs-diffusion/table-tree.png" class="img-fluid rounded z-depth-1" caption="A tiny world with three possible sentences. Left: the table of probabilities, which is what any model produces in the end. Right: the same table as a tree of choices (first word, then second word given the first), which is what an autoregressive model learns. Divide the table to get the branches; multiply the branches to get the table back. Every table can be written as a tree." %}

**So what is the difference? The cost.** An autoregressive model imitating diffusion has to write out the rounds as text: first "▢ ▢ ▢ ▢", then "It's ▢ outside ▢", then the full sentence. Three drafts, word by word: 12 tokens instead of 4. A diffusion model imitating autoregression commits one position per round: 4 rounds instead of 2, and the parallelism is gone. Both can; both pay. There is also a cost you do not see immediately: what each one finds *easy* to learn. Local dependencies ("after 'It's' comes 'raining'") are cheap for autoregression; global structure ("a paragraph has an opening, a middle, an end") is cheap for diffusion. This is the "you wouldn't run it in polynomial time, you'd use the other one" remark from class.

**One caveat.** The equivalence is about ideal models with enough capacity and enough steps. Real models learn differently from the same data: autoregressive models train on correct text and then have to continue their own mistakes; parallel generation has the multimodality problem (each position picks something locally plausible, and together they do not fit). "What is possible" and "what actually happens" are two different levels, and the distinction comes up everywhere in this field.

**Why it matters for the course.** Most of the papers we will read are about autoregressive models, because that is what most research uses. The equivalence is the reason this is fine: what we learn about how one kind of model learns, remembers and fails carries over to the other. The architecture sets the cost, not what can be learned.
