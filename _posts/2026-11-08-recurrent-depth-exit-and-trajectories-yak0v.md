---
title: "Reproducing the exit rule and the latent trajectories on Huginn-0125"
description: Per-token exit trips, what the answer would be if the loop stopped early, and the latent trajectories of every token, measured on the released model.
paper: recurrent-depth-latent-reasoning
role: coding
task: reimplement
by: yak0v
og_image: /assets/img/posts/recurrent-depth-exit-and-trajectories/late_trajectories_all_tokens.png
---

## What was reimplemented

The authors released the trained model, [Huginn-0125](https://huggingface.co/tomg-group-umd/huginn-0125). Two parts of the paper were reproduced on it. The first is the adaptive exit rule from Section 6.1, which stops the recurrence for a token once the next-token distribution has stopped changing between consecutive trips. The second is the latent trajectory analysis from Section 7, where the hidden state of a token is plotted trip by trip in its two leading principal directions. Both were run on a single input: *Tom has 12 apples and buys 29 more. How many apples does he have now?*

## Setup

The model was run on a MacBook with an Apple M4 chip and 24 GB of memory. In bfloat16 it occupies about 8 GB. Each generated token took about 12 seconds at 64 trips, and the two prompts used in this post took under ten minutes in total.

## The code

The model exposes three methods that allow the recurrence to be driven step by step. `embed_inputs` runs the embedding and the prelude once and returns the vector $$e$$ for every position. `iterate_one_step` runs one trip through the core block. `predict_from_latents` applies the coda and the unembedding to a state and returns the logits. The loop below runs 64 trips and, after each one, computes the next-token distribution at every position and the KL divergence from the distribution one trip earlier, following the authors' KL exit criterion.

```python
emb, block_idx = model.embed_inputs(ids)          # prelude output e, computed once
x = model.initialize_state(emb)                    # random starting state s_0
prev = torch.full((S, V), -math.log(V))            # uniform distribution for the first comparison
for step in range(64):
    x, block_idx, _ = model.iterate_one_step(emb, x, block_idx=block_idx, current_step=step)
    lp = torch.log_softmax(model.predict_from_latents(x).logits[0].float(), -1)
    kl = (prev.exp() * (prev - lp)).sum(-1)        # one value per position
    # the first trip with kl < 5e-4 is the exit trip of that position; x is stored for the trajectory plots
    prev = lp
```

Generation runs this loop once per new token on the full sequence, without a KV cache. The next token is the most likely token at the last position at that position's exit trip. It is appended and the loop runs again. Decoding is greedy.

The full code is [here](https://github.com/active-ai-reading/active-ai-reading.github.io/tree/main/assets/code/recurrent-depth-exit-and-trajectories).

## Results

The model's answer is *Tom now has 12 + 29 = 41 apples.* The fourteen generated tokens exit between trip 7 and trip 28, with a mean of 14.6. The answer therefore used 205 trips through the core block, compared with 448 for a fixed budget of 32 trips per token.

Within the question, the exit trips are not uniform. The words *How*, *many* and *does* exit after 9 to 12 trips. The digits of 12 and 29 take 23 to 30 trips, and the digit *2* of *12* does not reach the threshold within 64 trips. In the answer, the first digit of 12 takes 28 trips and the plus sign 20, while *apples* takes 7.

### Output at each trip

For every answer position, the token that the coda would output after each trip was recorded. The figure shows these tokens for trips 1 to 32. Several positions change in the first ten trips. The answer digit is 1, 2, 5 and 3 on trips 1 to 5 and 4 from trip 6 onward. The position of the plus sign alternates between *+* and *apples* until trip 11. The position of *now* passes through *is*, *has*, *originally* and *initially* before trip 11. No position changes after trip 11, up to trip 64.

{% include figure.liquid path="assets/img/posts/recurrent-depth-exit-and-trajectories/answer_if_stopped_at_trip.png" class="img-fluid rounded" caption="Each row is one position of the answer. The cell at trip t is the token the coda would output if the loop stopped there: green where it equals the final token, red otherwise. The yellow tick marks the trip at which the exit rule stopped. No position changes after trip 11, so trips 33 to 64 are omitted." %}

The exit rule stopped every position after its last change, so the generated answer is identical to the one obtained with 64 trips. On this input the rule is conservative: all positions had settled by trip 11, and most exits came later.

### Latent trajectories

The figure below shows the hidden state of each token in the question on trips 33 to 64, projected onto the two leading principal directions of that token's own trajectory over those trips. Trips 1 to 32 are excluded because the state moves much more in the first trips than afterwards, and including them would compress the later trips into a single point.

{% include figure.liquid path="assets/img/posts/recurrent-depth-exit-and-trajectories/late_trajectories_all_tokens.png" class="img-fluid rounded" caption="One panel per token of the question. The dots are the token's latent state on trips 33 to 64, from dark to bright, projected on that token's own two leading principal directions. Green tokens exited before trip 20, yellow tokens at trip 20 or later, and the red token did not exit." %}

In this window, the state of most tokens moves along a closed or spiral path rather than converging to a point. The step length per trip is roughly constant from trip 25 onward, at about 1/300 of the first step. The tokens that exited earliest show the most regular loops. The paper reports orbits for selected tokens in Figure 10; on this input the same behaviour appears for most of the sentence.

## Discussion

The number of trips a token uses before the exit rule fires varies between 7 and 35 within one short input, and the longest counts occur on the digits and on the tokens where the answer's format is decided. The hidden state continues to move after the output has stopped changing, which is consistent with the authors' choice of a criterion on the output distribution rather than on the state.

These results come from one prompt, one random initial state and greedy decoding. They illustrate the mechanisms described in the paper but do not measure the model's accuracy or the savings from adaptive exit in general.
