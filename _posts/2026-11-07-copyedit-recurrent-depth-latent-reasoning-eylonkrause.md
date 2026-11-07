---
title: "Copyediting Section 7 of Recurrent Depth"
description: "Section 7 is the most fun part of the paper, but it mixes what the authors saw with what they guess."
paper: recurrent-depth-latent-reasoning
role: writing
task: copyedit
by: [EylonKrause]
---

## What I changed and why

Section 7 is the most interesting part of the paper, but it's hard to tell what the authors saw from what they're guessing, and some claims go past the figures. The title says the patterns emerge at scale, but no smaller model is shown, and the text and the captions disagree on how widely orbits show up and what sliders are for. I named the patterns early, said once that this is a handful of examples, moved the guesses to the end and cut what the figures don't back, which took it from 568 words to under 400.

## Before and after

<div class="before-after">
  <div class="before" markdown="1">
<span class="label">Before</span>

[Paste Section 7 here]

  </div>
  <div class="after" markdown="1">
<span class="label">After</span>

**7 What the Model Does in Latent Space**

What is the model doing while it iterates? To get a first idea, we followed the trajectories $$\{\mathbf{s}_i\}_{i=1}^{r}$$ of every token in a handful of prompts. These are a few examples we picked by hand, so everything in this section is qualitative. Our training objective does nothing to pull the state toward a fixed point, unlike deep equilibrium models (Bai et al., 2019), so any structure in these trajectories is something the model learned on its own.

In these examples a token's state does one of three things. Figure 12 shows a few trajectories, projected onto the main PCA directions of the prompt. Many tokens simply converge to a fixed point. Others never settle and keep circling in an orbit. We see orbits on numbers in math problems, such as the "3" in a GSM8k question about a three-egg omelette (see also Figure 16), and on some words that shape the answer, such as "makes" and "thinks", but not on trivia questions. Some key tokens slide instead, drifting steadily in one direction, like the word "wrong" in an unsafe question.

How long a token takes to settle depends on its context and not only on the token. Figure 11 shows each token's distance from $$\mathbf{s}^*$$, its state after 128 iterations. The key words of the question and the first words of the answer take the longest, and the three identical dots in the prompt each behave differently. For some tokens, such as "school", the distance goes up and down instead of shrinking.

The starting point does not matter. When we restart the iteration from different random states $$\mathbf{s}_0$$, each token ends up in the same fixed point, orbit or slide (Appendix Figure 22). This is the path independence of Anil et al. (2022), which the random initial state was meant to encourage (Section 3.1).

What these patterns are for, we can only guess. The orbits on numbers might do the same job as the periodic patterns seen in transformers trained on arithmetic (Nanda et al., 2022). The sliders might count how many iterations have passed, or keep hold of a concept the model is still working on. A few examples cannot tell these apart, and we have not tested either idea.

  </div>
</div>

## The general rule

Say what you saw first and what you think it means second, in separate sentences. If you delete every guess, what's left should still describe the results correctly.
