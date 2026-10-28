---
title: "MSAR Explainer Video"
description: Video explainer for Multi-Stream Attention Residuals.
paper: multi-stream-attention-residuals
role: communication
task: extras
by: [Tomeratia]
---

This short explainer video walks through the core idea of the Multi-Stream Attention Residuals (MSAR) paper.
Standard transformers pass each layer's output to the next via a single residual connection.
MSAR replaces this with a multi-head attention mechanism that lets each layer attend over the outputs of *all previous layers*, with different heads looking at the past through different lenses.
The result is richer gradient flow and better utilization of earlier representations.

{% include video.liquid path="assets/video/msar-explainer.mp4" class="img-fluid rounded z-depth-1" controls=true %}
