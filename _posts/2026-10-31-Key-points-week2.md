---
title: "Key points of Multi Stream Attention"
description: They had a point, I'm sure it's buried in here somewhere.
paper: multi-stream-attention-residuals
role: writing
task: key-points
by: ItamarFruchter
---

## The general rule

Using technical jargon might make your abstract shorter - but it'll take twice as long to read.
Start the paper (abstract, intro) giving the readers some context on the problem you are trying to solve and on what is the state of solutions today, and **USE VISUALIZATIONS**.

{% include figure.liquid path="assets/img/papers/multi-stream-attention/XKCD_average_familiarity.png" class="img-fluid rounded z-depth-1" caption="Relevant XKCD: <a href='https://xkcd.com/2501/'>xkcd #2501, Average Familiarity</a> by Randall Munroe (CC BY-NC 2.5)." %}

Reading the abstract, a reader with no sufficient context on the innovations in the field (like myself) will be lost quickly (after being attacked by "content-dependent retrieval" and "single-stream softmax attention" in the first sentence, and the first architecture figure in page 7).

After doing some catching up, I think the main points of the paper could be described like so:

## 1. Residual streams could be upgraded to be non-uniform with attention
This is **not** a new contribution by the paper, but it is the main important context I was missing, and it's one of the more interesting things I learned going over this paper.
The credit for this idea (as far as I could tell) goes to Attention Residuals (AttnRes) {% cite kimi2026attnres %}, which builds on earlier ways of letting a layer read all previous layers directly {% cite huang2017densenet pagliardini2024denseformer xiao2025muddformer %}.

## 2. Attention over both depth AND tokens (/time)
A previous architecture - AttnRes - used attention on the residual stream of this same token. In this paper they expand this to both look across the different network layers as well as across each layer's reaction to the previous tokens (here - up to 12 previous tokens). Another expansion of this idea is the use of multi-headed attention here.
In this paper they use the convolution over the token history as the way to combine these. Here as well the idea isn't novel (Mixture-of-Depths Attention attends over both tokens and earlier layers {% cite zhu2026moda %}, and short convolutions over previous tokens appear in Primer and Canon layers {% cite so2021primer allenzhu2025canon %}), but the use of convolutions for inter-token mixing in the depth attention is new as far as I could tell.
{% include figure.liquid path="assets/img/papers/multi-stream-attention/figure2c.png" class="img-fluid rounded z-depth-1" caption="Figure 2c of the paper (CC BY 4.0): Block MSAR." %}

## 3. We made it work properly on production-sized models
Maybe the biggest contribution of the paper, in my view, is showing how they combined the first two points and using clever parametrization and caching they made it work on a large scale model, showing improvements over both vanilla architecture and previous attempts that scale to large models (not the biggest, but 18B and 28B are respectable models and not a model organism (even though this is the MoE total parameter count, not active)).
Caveat that should be stated here - this is a properly *sized* model but the compute budget for training is much much smaller than that of a "proper" production size LLM.

## How they could have done better
Maybe the paper isn't aimed at outsiders, but as one trying to read it - bringing me "up to speed" wouldn't have taken more than a few lines, written in simple english, and creating a more in depth view of their architectural suggestion (i.e figure 2, with a bit more focus on the architectural changes and most importantly - much earlier in the paper).
Additionally, I thing the framing of attention over both depth (of the network) and over previous tokens jointly is more helpful (at least to me).

The main contribution of this paper are it's results, which the paper presents in a very forward manner (abstract, first figure). They would be easier to understand given the context of the architectural changes.