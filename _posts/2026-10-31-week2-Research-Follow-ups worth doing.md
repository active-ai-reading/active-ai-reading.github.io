---
title: "Research: Follow-ups worth doing  of Multi-Stream Attention Residuals"
description: Follow-ups worth doing - continue to explore the MSAR architecture 
paper: multi-stream-attention-residuals
role: research
task: Follow-ups worth doing
by: NettaShemesh103
---

<!-- FOLLOW-UPS -->
## Follow-ups worth doing

### 1. Does MSAR improve depth scaling?

**Question:**  
Does MSAR enable deeper networks to benefit more from additional layers compared to standard residual connections and AttnRes?

**Experiment:**  
Train Vanilla, AttnRes, and MSAR models with increasing numbers of layers while keeping the hidden dimension, training data, and optimization settings fixed across methods at each depth. Then compare training loss and downstream performance as depth increases.

**Why it's worth someone's time:**  
A central motivation of the paper is that information from early layers becomes harder to retrieve as networks grow deeper. However, the paper does not directly isolate the effect of depth itself. This follow-up would test whether MSAR actually improves depth scaling, rather than simply performing better at the model scales evaluated in the paper.