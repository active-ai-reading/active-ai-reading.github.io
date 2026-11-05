---
title: "Literature Review: Recurrent Depth and Latent Reasoning"
description: How recurrent networks, looped Transformers, and implicit reasoning lead to test-time scaling in latent space.
paper: recurrent-depth-latent-reasoning
role: research
task: literature
by: [roey-magen]
---

## The papers this builds on

Recurrent computation offers a way to increase a network's effective depth while reusing its parameters. *Universal Transformers* introduced repeated, shared self-attention transformations across depth {% cite dehghani2019universal %}. Subsequent work showed that recurrent networks trained on simple problems could solve harder instances by performing more iterations at inference time {% cite schwarzschild2021algorithm %}. However, additional iterations can also degrade performance. {% cite bansal2022overthinking --style _bibliography/narrative-author-year.csl %} addressed this "overthinking" problem through input recall and progressive training.

These ideas connect to algorithmic reasoning and in-context learning. {% cite giannou2023looped --style _bibliography/narrative-author-year.csl %} demonstrated theoretically how looped Transformers can execute iterative algorithms, while {% cite yang2024looped --style _bibliography/narrative-author-year.csl %} showed that trained looped Transformers can match standard Transformers on several in-context learning tasks using substantially fewer parameters.

{% cite geiping2025latent --style _bibliography/narrative-author-year.csl %} bring recurrent-depth modeling to a 3.5-billion-parameter language model trained on approximately 800 billion tokens. Their model repeatedly applies a shared Transformer block to hidden representations. Randomized training depths and stabilization techniques enable performance gains from additional inference-time iterations, especially on mathematics and coding tasks. Its central contribution is demonstrating this approach at substantial language-model scale, without requiring specialized reasoning supervision.

## The fields and concepts it connects to

A related research direction moves reasoning away from explicit text: {% cite deng2024implicit --style _bibliography/narrative-author-year.csl %} gradually internalize chain-of-thought (CoT) steps; {% cite cheng2024compressed --style _bibliography/narrative-author-year.csl %} compress reasoning into continuous representations; and {% cite hao2025continuous --style _bibliography/narrative-author-year.csl %} feed hidden states back as subsequent input embeddings. Concurrently, {% cite saunshi2025latent --style _bibliography/narrative-author-year.csl %} provide theoretical and empirical evidence for looped Transformers' reasoning capabilities.

Together, these connections position recurrent depth as a complementary route to test-time scaling alongside explicit CoT. My main takeaway is that Geiping et al. establish the feasibility of large-scale recurrent reasoning; establishing when it offers the best accuracy–compute trade-off remains a separate question.
