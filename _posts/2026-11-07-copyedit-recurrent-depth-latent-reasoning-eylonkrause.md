---
title: "Copyediting Section 7: what the latent trajectories show, and what is a guess"
description: "The paper's most exciting section blends what its plots show with what the authors hope they mean, so I pulled the two apart."
paper: recurrent-depth-latent-reasoning
role: writing
task: copyedit
by: [EylonKrause]
---

## What I changed and why

Section 7 is the most exciting part of the paper, but it mixes what the plots show with what the authors think they mean, and it introduces its three patterns one example at a time across two figures. It also claims more than it shows: the title says the patterns emerge at scale, but no smaller model appears; the text says orbits go well beyond arithmetic, while Figure 16's caption limits them to math reasoning and thinking tokens; and the text and Figure 12's caption give sliders two different jobs. I named the patterns first, said once how much evidence there is, moved every interpretation into a last paragraph marked as untested, and kept the scope to what the captions say, which also cut the section from 568 words to about 420.

## Before and after

<div class="before-after">
  <div class="before" markdown="1">
<span class="label">Before</span>

[Paste Section 7 of the paper here: all six paragraphs, from the opening question through the Path Independence paragraph.]

  </div>
  <div class="after" markdown="1">
<span class="label">After</span>

**7 What the Model Does in Latent Space**

What happens to a token's state while the model iterates? For a first look, we follow the trajectories $$\{\mathbf{s}_i\}_{i=1}^{r}$$ of every token in a handful of prompts. The evidence here is qualitative: a few hand-picked examples, not a measurement over a dataset. Nothing in our training objective pulls the state toward a fixed point, unlike deep equilibrium models (Bai et al., 2019); we train only with truncated unrolling, so any structure in these trajectories is something the model learned by itself.

**Three patterns.** Figure 12 projects example trajectories onto the top principal directions of all the trajectories in a prompt. In the examples we looked at, a token's state does one of three things:

- **It converges.** Many tokens simply settle into a fixed point (top row).
- **It orbits.** Some states keep circling instead of settling. We see this on numbers in math problems, such as the "3" in a GSM8k question about a three-egg omelette (middle row, and Figure 16), and on some words that set the structure of the answer, such as "makes" or "thinks". We have not seen orbits on trivia questions.
- **It slides.** Some states drift steadily in one direction, such as the word "wrong" in an unsafe question (bottom row).

**How fast a token settles depends on its context.** Figure 11 plots each token's distance to $$\mathbf{s}^*$$, its state after 128 iterations. The key words of the question and the first tokens of the answer take the longest to settle, and the three identical dots in the prompt behave differently from one another. For some tokens, such as "school", the distance rises and falls instead of shrinking steadily.

**The patterns do not depend on the starting point.** When we restart the iteration from several random states $$\mathbf{s}_0$$, each token ends up in the same fixed point, orbit or slide (Appendix Figure 22). This is the path independence (Anil et al., 2022) that the random initial state was meant to encourage (Section 3.1).

**What this might mean.** These are hypotheses we have not tested. Orbits on numbers may play the role of the periodic number representations found in transformers trained on arithmetic (Nanda et al., 2022). Sliders could count how many iterations have passed, or hold a concept the model is still working through; a few examples cannot tell these apart. If either is right, the model organizes its computation through the geometry of its high-dimensional state, rather than step by step in discrete tokens as verbalized chain-of-thought does.

  </div>
</div>

## The general rule

Say what you saw before you say what it means, and keep the two in separate sentences. A quick test: delete every interpretation, and what is left should still be a complete and correct description of the results. When you have categories, name them before the examples, so the reader knows what each example is an example of.
