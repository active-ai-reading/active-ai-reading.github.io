---
title: Suppressed, not erased, and automatic soundness check
description: "A probe finds edited facts still readable inside the model, plus one trending paper I kept anyway: an AI reviewer trained to judge soundness."
paper: spurious-forgetting
task: hidden-gems
by: achi-or
---
I suggest two papers - one is directly connected to this week's paper, and the other is connected to our course goals. 
I found the PaperCritique by browsing through hugging face's daily papers, and the "Suppresses Not Erased" by using AI engines to find papers that are related to this week's paper and choosing by intrest.  

- **[Suppressed, Not Erased: A Representational Trace of Edited Facts Survives Even Weight-Free Knowledge Editing](https://arxiv.org/abs/2609.18985)** (Srivastava & Chatterjee, 2026): 
A linear probe can still recover original facts from GPT-2-XL after a counter-fact editing. This is this week's gap between losing access and losing the fact, on the same CounterFact facts, but caused by deliberate editing rather than by learning new facts. It raises the question: is "the readout moved, the knowledge stayed" a general property of how these models store facts? 
It has some caveats - GPT-2-XL, only 50 edits, some of the methods have trivial results (If you only edit one layer, it's obvious the other layers still hold the original).


- **[PaperCritic: Training AI Reviewers to Assess the Soundness of Papers](https://arxiv.org/abs/2611.17834)** (Ryu et al., 2026): 
This is relevant to our course, but not specifically to this week. More over, it's a little trending, but it seemed close enough that it matters.  
The paper trains a 4B model to review papers, but they distinguish between the subjective part of the reviews, which they do not try to imitate, and the objective side - soundness of the claims. 
A main finding is that strong models produce many plausible concerns and few sound ones.
This paper also has some caveats - specifically it seems they are over dependent on GPT 5.4, to the point where some of the experiments are circular. 
  - **Why I kept it anyway:** this course is about reading papers actively and judging whether their claims hold, and PaperCritic turns exactly that into something measurable: what makes a critique point correct, and what makes it important. Its main finding is a useful warning for how we use AI to read papers in this course, including the post above. Worth reading even if it is not a hidden gem.
