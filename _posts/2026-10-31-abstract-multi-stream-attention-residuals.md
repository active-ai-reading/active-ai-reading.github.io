---
title: "Rewriting the abstract of Multi-Stream Attention Residuals"
description: "A new approach to Transformer residual connections that improves performance while reducing the computational cost of deep learning."
paper: multi-stream-attention-residuals
role: writing
task: abstract
by: [golombi]
---

## What I changed and why

The original abstract presents the technical details quite densely, making it difficult to immediately understand the motivation behind the method and what distinguishes it from previous approaches. I reorganized it to first introduce the problem, then explain the limitation of AttnRes and present MSAR as the proposed solution. I also improved the flow between the methodology, efficiency advantages, and experimental results.

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>

Attention Residuals (AttnRes) enables content-dependent retrieval over network depth, which can be viewed as single-stream softmax attention along the depth axis. Inspired by the success of multi-head attention along the sequence axis, we introduce Multi-Stream Attention Residuals (MSAR), an extension of AttnRes that generalizes this mechanism to multi-head depth attention, yielding substantial performance gains with minimal additional overhead. MSAR draws stream diversity from sequence context through multi-scale causal convolutions, allowing different heads to retrieve historical representations through distinct contextual views while preserving the integrity of the hidden representation. The retrieved streams are combined through lightweight adaptive mixing to generate the single-stream layer input. By retaining single-stream sources and expanding them on demand, MSAR supports multi-stream computation without requiring persistent multi-stream storage or communication. Across all 12 downstream benchmarks at the 18B and 28B MoE scales, MSAR consistently outperforms prior residual variants, including standard residual connections, manifold-constrained Hyper-Connections (mHC), and AttnRes. Scaling-law experiments yield an iso-loss compute speedup of 1.58× over the standard residual baseline, compared with 1.35× for AttnRes and 1.30× for mHC. These results make MSAR a promising residual architecture for large-scale pre-training.

  </div>
  <div class="after"><span class="label">After</span>

Deep Transformer models can struggle to effectively retrieve information from earlier layers, limiting the benefits of increasing network depth. Attention Residuals (AttnRes) address this challenge by using attention to retrieve information from previous layers, but rely on a single attention stream. We introduce Multi-Stream Attention Residuals (MSAR), which extends this approach by enabling multiple attention streams to independently retrieve information from previous layers. To create diverse streams without reducing the dimensionality of hidden representations, MSAR uses multi-scale causal convolutions that capture different ranges of sequence context. Each stream performs its own attention over previous layers, and the retrieved representations are combined through lightweight adaptive mixing to produce a single input for the next layer. Furthermore, MSAR generates additional streams only when needed, avoiding the need to store or communicate multiple persistent representations. Experiments at the 18B and 28B MoE scales demonstrate that MSAR consistently outperforms standard residual connections, manifold-constrained Hyper-Connections (mHC), and AttnRes across all 12 downstream benchmarks. Scaling-law experiments further show a 1.58× compute speedup over standard residual connections at equivalent training loss, compared with 1.35× for AttnRes and 1.30× for mHC. These results demonstrate that MSAR can improve the efficiency and performance of large-scale Transformer pre-training.

  </div>
</div>

## The general rule

Introduce the problem before describing the proposed method. Explain the limitations of existing approaches to establish why a new method is needed, then present the main contribution and how it addresses those limitations. Finally, highlight the most important experimental results. An abstract should communicate the motivation, novelty, and significance of a paper in a logical order without overwhelming readers with technical details.
