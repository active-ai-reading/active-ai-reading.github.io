---
title: "Copyediting Section 7 of Recurrent Depth"
description: "Section 7 interleaves observation and speculation about the model's latent trajectories; this edit separates the two."
paper: recurrent-depth-latent-reasoning
role: writing
task: copyedit
by: [EylonKrause]
---

## What I changed and why

Section 7 is intriguing because it is where the paper looks directly at what the recurrence does to a token's latent state as the model iterates. With that being said, the section does not separate what the authors observed from what they infer, and several claims extend beyond the figures: the title attributes the patterns to scale although no smaller model is shown, and the text and captions disagree on how widely orbits occur and what sliders are for. I introduced the three patterns up front, stated the evidence base once, moved the interpretations to a closing paragraph and removed claims the figures do not support, reducing the section from 568 to under 400 words.

## Before and after

<div class="before-after">
  <div class="before" markdown="1">
<span class="label">Before</span>

Finally, what is the model doing while recurring in latent space? To understand this question better, we analyze the trajectories 
{
𝐬
i
}
i
=
1
r
 of the model on a few qualitative examples. We are especially interested in understanding what patterns emerge, simply by training this model at scale. In comparison to previous work, such as Bai et al. (2019), where the training objective directly encodes a prior that pushes trajectories to a fixed point, we only train with our truncated unrolling objective.

Figure 11 shows the norm distance 
‖
𝐬
i
−
𝐬
∗
‖
 between each 
𝐬
i
 in a trajectory and an approximate limit point 
𝐬
∗
 computed with 128 iterations. We show the sentence top to bottom and iterations from left to right. We clearly see that convergence behavior depends on context. We see that key parts of the question, and the start of the model response, are “deliberated” much more in latent space. The context dependence can also be seen in the different behavior among the three identical tokens representing each of the three dots. Also note that the distance to 
𝐬
∗
 does not always decrease monotonically (e.g. for school); the model may also trace out complicated orbits in its latent trajectory while processing information, even though this is not represented explicitly in our training objective.

We look at trajectories for select tokens in more detail in Figure 12. We compute a PCA decomposition of latent trajectories over all tokens in a sequence, and then show several individual trajectories projected onto the first six PCA directions. See the appendix for more examples. Many tokens simply converge to a fixed point, such as the token in the top row. Yet, for harder questions, such as in the 2nd row5, the state of the token quickly falls into an orbit pattern in all three pairs of PCA directions. The use of multi-dimensional orbits like these could serve a similar purpose to periodic patterns sometimes observed in fixed-depth transformers trained for arithmetic tasks (Nanda et al., 2022), but we find these patterns extend far beyond arithmetic for our model. We often also observe the use of orbits on tokens such as “makes” (see Figure 16) or “thinks” that determine the structure of the response.

Aside from orbits, we also observe the model encoding particular key tokens as “sliders”, as seen in the middle of the bottom row in Figure 12 (which is the token “wrong”, from the same message as already shown in Figure 11). In these motions the trajectory noticeably drifts in a single direction, which the model could use to implement a mechanism to count how many iterations have occurred.

The emergence of structured trajectories in latent space gives us a glimpse into how the model performs its computations. Unlike the discrete sequential chain of reasoning seen in verbalized chain-of-thought approaches, we observe rich geometric patterns including orbits, convergent paths, and drifts - means to organize its computational process spatially. This suggests the model is independently learning to leverage the high-dimensional nature of its latent space to implement reasoning in new ways.

Path Independence.
We verify that our models maintain path independence, in the sense of Anil et al. (2022), despite their complex, learned dynamics, which we discussed prior (see also the additional examples in Appendix Figure 22). When re-initializing from multiple starting states 
𝐬
0
, the model moves in similar trajectories, exhibiting consistent behavior. The same orbital patterns, fixed points, or directional drifts emerge regardless of initialization.

  </div>
  <div class="after" markdown="1">
<span class="label">After</span>

**What Patterns Emerge in Latent Space**

What does the model compute while it iterates in latent space? We examine the trajectories $$\{\mathbf{s}_i\}_{i=1}^{r}$$ of every token in a small set of hand-picked prompts, so the analysis in this section is qualitative. Unlike deep equilibrium models (Bai et al., 2019), our training objective does not pull the state toward a fixed point, so any structure in these trajectories is learned by the model rather than imposed by the objective.

In these examples, each token's state follows one of three patterns. Figure 12 shows selected trajectories projected onto the leading PCA directions of the prompt. Many tokens converge to a fixed point. Others enter an orbit and keep circling instead of converging. We observe orbits on numbers in math problems, such as the "3" in a GSM8k question about a three-egg omelette (see also Figure 16), and on some tokens that shape the response, such as "makes" and "thinks", but not on trivia questions. A third group, which we call sliders, drifts steadily in one direction, for example the token "wrong" in an unsafe prompt.

Convergence speed depends on context, not only on the token itself. Figure 11 plots each token's distance to $$\mathbf{s}^*$$, its state after 128 iterations. The key words of the question and the first tokens of the response converge most slowly, and three identical dot tokens in the same prompt behave differently. For some tokens, such as "school", the distance oscillates rather than decreasing monotonically.

These patterns do not depend on the initial state. Restarting the iteration from different random states $$\mathbf{s}_0$$ yields the same fixed point, orbit or slide for each token (Appendix Figure 22), consistent with the path independence (Anil et al., 2022) that the random initialization is designed to promote (Section 3.1).

The function of these patterns remains speculative. Orbits on numbers may serve a role similar to the periodic representations found in transformers trained on arithmetic (Nanda et al., 2022). Sliders could act as a counter of elapsed iterations, or hold a concept the model is still processing. A handful of examples cannot distinguish between these possibilities, and we do not test either hypothesis here.

  </div>
</div>

## The general rule

Separate observation from interpretation. Report what the evidence shows first, and present any interpretation afterwards, explicitly marked as a hypothesis. A useful check is that deleting every interpretive sentence should still leave a complete and accurate description of the results.
