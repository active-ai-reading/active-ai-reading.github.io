---
title: "Does learning to write a regex also align its embedding?"
description: "A CPU reimplementation of Figure 3’s training-loss comparison on NL-RX-SYNTH."
paper: llm-jepa
role: coding
task: reimplement
by: [Shueyr]
---

## What I reimplemented

I reimplemented the right panel of Figure 3 with a small Transformer trained on NL-RX-SYNTH, the paper’s English-to-regex dataset. [Paper, §3.3 and Figure 3](https://arxiv.org/abs/2509.14252v2)

I measured next-token prediction (NTP) loss and JEPA loss, which measures the cosine distance between independently encoded prompts and regexes. The baseline trained on NTP alone and still tracked JEPA loss. The second condition trained on both losses. Each condition ran for 300 updates with five matched seeds.

## The code

[Experiment script]({{ '/assets/code/llm-jepa-figure-3.py' | relative_url }})

## Results

{% include figure.liquid path="assets/img/posts/llm-jepa-figure-3/nl-rx-synth-learning-curves.png" class="img-fluid" alt="A single log-scale plot showing next-token and JEPA training losses for both conditions on NL-RX-SYNTH." caption="Training losses on a shared log scale, following Figure 3 (right). Each point averages five consecutive minibatches across five seeds. NTP is next-token cross-entropy." %}

## What I learned

Adding JEPA lowered the embedding loss from 1.277 in the baseline to 0.013 over the final five updates. NTP loss fell in both conditions and finished higher with JEPA (0.635 vs. 0.492 nats). The paper’s NTP curves nearly overlap. [Paper, Figure 3](https://arxiv.org/abs/2509.14252v2)
