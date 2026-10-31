---
title: "Follow-ups on Multi-Stream Attention Residuals"
description: "Cutting memory bandwidth overhead via asymmetric residual stream allocation between Attention and MLP sublayers."
paper: multi-stream-attention-residuals
role: research
task: followups
by: shaharOssy
---

<!-- FOLLOW-UPS -->
## Follow-ups worth doing

### Asymmetric Multi-Stream Residuals Across Sublayer Types

* **The Question:**
  Can we significantly reduce the memory access bottleneck of MSAR by deploying multi-stream retrieval ($m=4$) exclusively before Attention sublayers, while keeping standard single-stream residuals before MLP sublayers?

* **The Experiment:**
  1. Train a 10B MoE model using the architecture and Pile training budget described in Table 2 and Appendix A.
  2. Evaluate four configurations under identical training tokens and compute budgets:
     * **Full MSAR (Default):** $m=4$ streams applied to both Attention and MLP sublayers.
     * **Asymmetric MSAR:** $m=4$ streams prior to Attention sublayers; MLP sublayers bypass multi-stream expansion and the $\mathcal{H}^{Pre}$ mixer entirely, relying on standard single-stream residual connections.
     * **Standard Baselines:** Vanilla residuals and Block AttnRes as reference baselines.
  3. Measure the final pre-training loss on Pile, downstream benchmark scores, and wall-clock training throughput (tokens/sec) alongside memory I/O cost.
  4. Visualize the learned Pre-Attn depth-attention weights (replicating Figure 4) to verify that restricting MLP sublayers to a single stream does not degrade the cross-depth diversity of Attention sublayers.

* **Why it's worth someone's time:**
  The authors identify memory access cost as the primary operational overhead of MSAR: Table 6 shows that forward-pass memory I/O reaches $21.5d$ per token per sublayer for Block MSAR, compared to only $5.5d$ for AttnRes and $3d$ for Vanilla. 
  However, the attention weight visualizations in Section D (Figure 4) reveal a striking contrast: Pre-Attention reads retrieve broadly across historical blocks and utilize diverse streams, whereas Pre-MLP reads focus almost entirely on the local diagonal (the immediate preceding sublayer). Allocating $m=4$ full retrieval streams to MLP sublayers incurs heavy memory traffic for operations that show little cross-depth diversity. An asymmetric design directly eliminates this inefficiency, potentially preserving MSAR's performance gains while drastically cutting memory bandwidth overhead.
