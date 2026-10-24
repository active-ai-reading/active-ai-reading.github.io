---
title: "critique of matryoshka paper (GA26)"
permalink: /posts/2026/critique-matryoshka-lm-suites-ga26/
description: The narative about saving on parameters is diluted by a secondary point about cheap distiliation.
paper: matryoshka-lm-suites
role: research
task: critique
by: [ohad-agadi]
---

<!-- Keep the block for your task, delete the others. To cite, add the BibTeX to _bibliography/references.bib and use the cite tag (see the guide page). -->

<!-- CRITIQUE -->
## Summary of the claims
The paper tells a story about training a suite of stand-alone models more efficiently by stacking them and training end-to-end.
It then makes a point about distiliation in this setup being cheap. 

## Strengths
I felt the article was short, concice and readable. 

## Weaknesses
It is not clear if distilation is crucial to performance.
The main figure could include less information.

## How it could have been improved
Show or talk about results for a vanilla-matryshuka setup(no purple arrows). If that makes sense, show a simpler figure of the architecture and make your main claim about efficiency (3.2B instead of 5.2B. 38%~ less params -> roughly the same in compute. perhaps you don't need a figure?).
Otherwise, in the case the purple arrows are crucial, express that. 

## Verdict
I liked the paper. The technique was clear even for a novice AI reader (myself). 
The technique itself is cool.

