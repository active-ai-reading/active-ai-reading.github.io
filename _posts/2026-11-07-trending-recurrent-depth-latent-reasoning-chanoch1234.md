---
title: "Recent work on recurrent-depth language models"
description: "Two recent papers explore how recurrent latent reasoning can become more adaptive and more stable."
paper: recurrent-depth-latent-reasoning
role: scouting
task: trending
by: [chanoch1234]
---

The paper of this week (3) shows how Huginn scales test-time computation by repeatedly applying a shared recurrent block. I found two papers that explore how this fixed recurrent process can be made more adaptive or more stable. 
To be honest I am not sure if the term "trending" is the most fitting. I enjoyed those papers and they both appeared at major conferences so I'm going to say it's okay.

{% include figure.liquid path="assets/img/posts/trending papers - MoDr architecture/modr-architecture.png" class="img-fluid rounded" caption="MoDr architecture. Source: Zhang et al., Mixture-of-Depth-Recurrent Transformers for Test-Time Reasoning." %}

**[MoDr: Mixture-of-Depth-Recurrent Transformers for Test-Time Reasoning](https://proceedings.iclr.cc/paper_files/paper/2026/hash/8a81180649011d1690e05c68bfeaa57c-Abstract-Conference.html)** replaces Huginn's single recurrent chain with a learnable hard-gated router over multiple LoRA-based branches, allowing different inputs to follow different latent reasoning paths.

**[STARS: Stabilizing Recurrent Dynamics for Test-Time Scalable Latent Reasoning](https://proceedings.mlr.press/v306/yang26t.html)** keeps the recurrent-depth setup but changes the training objective by regularizing the latent dynamics, making additional recurrences more stable and reducing the performance collapse that can occur at large test-time depths.
