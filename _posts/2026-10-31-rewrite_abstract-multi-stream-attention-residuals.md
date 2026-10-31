---
title: "Rewriting the abstract of Multi-Stream Attention Residuals"
description: "MSAR's most compelling result, reaching the same training loss with substantially less compute, is buried at the end of the abstract. Here is a version that puts it first."
paper: multi-stream-attention-residuals
role: writing
task: abstract
by: [MatanBarTov]
---

<!-- Keep the sections that fit your task, delete the rest. -->

## What I changed and why

The original abstract explains the method clearly, but it follows a conventional structure: background, motivation, architecture, implementation details, and finally results. The most compelling finding, that **MSAR achieves a 1.58× iso-loss compute speedup over standard residual connections**, appears only in the final sentences.

This result is particularly interesting because MSAR improves the residual architecture without substantially increasing its computational cost. Yet the original abstract spends more space explaining architectural details than communicating the practical significance of the improvement.

My rewrite makes four changes:

1. **Lead with the quantitative result.** Open with the 1.58× iso-loss compute speedup to immediately establish why the paper matters.
2. **Explain the problem before introducing terminology.** Describe how standard residual connections accumulate information from previous layers, making earlier representations harder to retrieve selectively.
3. **Present the method as a simple progression.** Explain how MSAR creates different contextual views, independently retrieves information across depth, and combines the results, without overwhelming the reader with implementation details.
4. **Quantify both performance and overhead.** Include the improvement over AttnRes, the consistent gains across 12 benchmarks, and the negligible additional training FLOPs.


## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
  Attention Residuals (AttnRes) enables content-dependent retrieval over network depth, which can be viewed as single-stream softmax attention along the depth axis. Inspired by the success of multi-head attention along the sequence axis, we introduce Multi-Stream Attention Residuals (MSAR), an extension of AttnRes that generalizes this mechanism to multi-head depth attention, yielding substantial performance gains with minimal additional overhead. MSAR draws stream diversity from sequence context through multi-scale causal convolutions, allowing different heads to retrieve historical representations through distinct contextual views while preserving the integrity of the hidden representation. The retrieved streams are combined through lightweight adaptive mixing to generate the single-stream layer input. By retaining single-stream sources and expanding them on demand, MSAR supports multi-stream computation without requiring persistent multi-stream storage or communication. Across all 12 downstream benchmarks at the 18B and 28B MoE scales, MSAR consistently outperforms prior residual variants, including standard residual connections, manifold-constrained Hyper-Connections (mHC), and AttnRes. Scaling-law experiments yield an iso-loss compute speedup of 1.58× over the standard residual baseline, compared with 1.35× for AttnRes and 1.30× for mHC. These results make MSAR a promising residual architecture for large-scale pre-training.
  </div>
  <div class="after"><span class="label">After</span>
  Can changing how Transformer layers reuse earlier representations make language model pre-training substantially more compute-efficient? We show that Multi-Stream Attention Residuals (MSAR) achieves a **1.58× iso-loss compute speedup** over standard residual connections, outperforming previous alternatives such as AttnRes (1.35×) and mHC (1.30×). Standard residual connections accumulate layer outputs into a single representation, making it difficult for deeper layers to selectively retrieve earlier information. While AttnRes addresses this through attention over network depth, it relies on a single retrieval stream. MSAR extends this idea to multi-head depth attention: lightweight causal convolutions create multiple full-dimensional views of earlier representations, each independently attends to historical layers, and adaptive mixing combines the retrieved information. To avoid the cost of maintaining multiple streams, MSAR stores only single-stream summaries and expands them when needed. Evaluated on 18B and 28B MoE models, MSAR outperforms standard residuals, mHC, and AttnRes across all 12 downstream benchmarks, while adding only **0.5% training FLOPs** at the 28B scale. These results suggest that more selective access to earlier representations can improve both model quality and pre-training compute efficiency without substantially increasing architectural overhead.
  </div>
</div>

## The general rule

**Lead with the most compelling finding, not the method used to achieve it.** An abstract should immediately communicate why the research matters before explaining how it works. A concrete, quantitative result gives readers a reason to care about the proposed approach.

In particular, when a paper introduces a new architecture, the abstract should first establish its practical significance, then briefly explain the problem it addresses and the key idea behind the solution. Supporting numbers should make the improvement tangible, while technical implementation details can be left for the main text.

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
