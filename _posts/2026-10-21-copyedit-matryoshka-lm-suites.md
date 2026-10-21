---
title: "Editing the methods of <paper>"
description: sub-models are made of blocks
paper: matryoshka-lm-suites
role: writing
task: copyedit
by: AdamJaber03
---

<!-- Keep the sections that fit your task, delete the rest. -->

## What I changed and why

The original writing had 2 points that I found to be unclear: 
1. What is $e_{\theta_m}$? What's its dimension? whats its relation to $e_{\theta_{m-1}}$? I found the answers to be that while \theta_m contains \theta_{m-1}, the embedding layers are independent, and their dimension is the difference in dimension between different blocks.
2. The original writing "Each sub-model $T_{\theta_m}$ is a separate Transformer stack with its own hidden dimension (or width)" is I belive confusing; the following formulation from the main text indicates that the difference in dimension between a model and its direct sub-model is only within the new layers. I made this clearer by rewriting this using blocks where dimension is consistent, and those blocks are composed into different sub-models

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
<p> **Modeling** A Transformer [Vaswani et al., 2017] language model maps an input sequence $x \in [1, V]^L$ to output representations $o_\theta(x) \in \mathbb{R}^{L \times D}$ via an input embedding $e_\theta$ and a stack of Transformer blocks $T_\theta$ of hidden dimension $D$. A linear LM head $W$ maps each position's representation $o_\theta(x)$ to logits $l \in \mathbb{R}^V$, and the parameters $(\theta, W)$ are trained to minimize the next-token prediction cross-entropy loss. <\p>


A conventional suite of $M$ models uses $M$ independent parameter sets $\{(\theta_m, W_m)\}_{m=1}^{M}$. We instead enforce a strict nesting of parameters with the exception of the LM head:

$$
\theta_1 \subset \theta_2 \subset \cdots \subset \theta_M = \theta.
$$

Each sub-model $T_{\theta_m}$ is a separate Transformer stack with its own hidden dimension (or width) $D_m$, number of layers (or depth) $n_m$, and a LM head $W_m$. We require strictly increasing hidden dimensions $D_1 \le D_2 \le \cdots \le D_M$. Unlike standard early exiting, which assumes a fixed hidden dimension across exits, the Matryoshka design lets each sub-model use a width tailored to its size, giving more flexibility in the architectural design at every sub-model size compared to early-exit methods [Elhoushi et al., 2024]. Moreover, because $\theta_m \subset \theta_{m+1}$, running the full architecture produces all $M$ sub-model logits in a single forward pass while activating fewer parameters and writing less KV cache than $M$ independent forward passes, facilitating distillation during training and multi-model inference methods such as speculative decoding.
  </div>
  <div class="after"><span class="label">After</span>
<p> A Transformer [Vaswani et al., 2017] language model maps a token sequence $x \in [1, V]^L$ to output representations $o_\theta(x) \in \mathbb{R}^{L \times D}$: a learned embedding table $e \in \mathbb{R}^{V \times D}$ maps each token to a vector of width $D$, and a stack of Transformer layers $T_\theta$ of hidden dimension $D$ processes the result. A linear LM head $W \in \mathbb{R}^{V \times D}$ maps output representations $o_\theta(x)$ to next-token logits $l \in \mathbb{R}^{V \times L}$. $(e, \theta, W)$ are trained to minimize the next-token prediction cross-entropy loss. A conventional suite trains $M$ such models independently. </p>


<p> A Matryoshka suite instead stacks $M$ *blocks* and composes $M$ models of different sizes from them. Block $m$ consists of a stack $T_{\theta_m}$ of $n_m$ Transformer layers of width $D_m$, We require strictly increasing hidden dimensions $D_1 \le D_2 \le \cdots \le D_M$. Each block input is constructed using the previous block's output together with its own residual embedding table $e_m \in \mathbb{R}^{V \times (D_m - D_{m-1})}$ (where $D_0 = 0$) applied to the original token sequence $x$. *Sub-model* $m$ is the composition of blocks $1, \dots, m$, followed by its own LM head $W^m \in \mathbb{R}^{V \times D_m}$. It is therefore $N_m = n_1 + \cdots + n_m$ layers deep, and its layers do not share a single width: the first $n_1$ have width $D_1$, the next $n_2$ have width $D_2$, and so on up to its output width $D_m$. This dynamic width allows more flexibility in the architectural design compared to early-exit methods [Elhoushi et al., 2024], each block can use a width suited to the sub-model it completes. <\p>


<p> Using a Matryoshka suite, one forward pass through the largest sub-model passes every exit and yields the logits of all $M$ sub-models, while activating fewer parameters and writing less KV cache than $M$ forward passes through independent models. Additionally, this single-pass design reduces the overhead associated with distillation during training and multi-model inference methods such as speculative decoding. <\p>
  </div>
</div>

## The general rule

What rule did you apply that others could use in their own writing? (e.g. "Lead with the finding, not the method.")

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
