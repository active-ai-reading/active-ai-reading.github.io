---
title: "Literature review of Matryoshka Language Model Suites"
description: Ideas behind Matryoshka LM Suites and what it adds
paper: matryoshka-lm-suites
role: research
task: literature
by: [NicolasRW]
---

<!-- LITERATURE REVIEW -->
## The papers this builds on

{% cite godey2026matryoshka --style _bibliography/narrative-author-year.csl %} (hereafter GA26) introduce Matryoshka LM Suites, which combines nested models, knowledge distillation, and speculative decoding. Its new contribution is how these ideas are integrated to train a family of models.

The nesting principle draws on earlier work. {% cite kusupati2022matryoshka --style _bibliography/narrative-author-year.csl %} trained embeddings whose initial coordinates already form useful representations, allowing shorter vectors to be used when resources are limited. Building on this idea, {% cite devvrit2023matformer --style _bibliography/narrative-author-year.csl %} applied the nesting principle to Transformer feed-forward networks in MatFormer. Smaller versions use subsets of neurons and share their weights with larger versions. These choices can then be combined across layers to obtain additional sizes without retraining.

Within this line of work, GA26 changes how the models are nested. Larger models extend smaller ones with additional, wider Transformer layers. Its 500M model has 24 layers of width 1024; the 1.5B model adds 10 layers of width 2304; and the 3B model adds another five of width 4352. Smaller models therefore use fewer, narrower layers and smaller attention caches. In the original MatFormer formulation, attention dimensions and depth remain fixed, so reducing the feed-forward width does not shrink the KV cache.

MatFormer has also been adopted at larger scales. Gemma 3n (2025) used MatFormer, nesting a model with 2B effective parameters inside one with 4B {% cite gemma2025gemma3n %}. GA26’s trained comparison with MatFormer is limited to the 200M scale, while Appendix E compares theoretical resource costs at a 3B size. A direct comparison of model quality at larger scales remains an interesting question.

To train the nested models, GA26 also draws on knowledge distillation. {% cite bucilua2006compression --style _bibliography/narrative-author-year.csl %} demonstrated that small models could learn to imitate larger ensembles. Building on this approach, {% cite hinton2015distilling --style _bibliography/narrative-author-year.csl %} described combining supervision from correct labels with the teacher’s predicted probabilities. GA26 uses this loss form for next-token prediction. Its contribution here is the integration, where one shared training forward pass supplies the predictions needed for the largest model to teach all smaller models.

This agreement between models also benefits speculative decoding, which lets a small model propose several tokens that a larger model checks. This can accelerate generation while preserving the larger model’s output distribution {% cite leviathan2023speculative %}. Earlier work improved this process by training the small model to imitate the large one, i.e., by draft–verifier alignment through distillation {% cite zhou2024distillspec --style _bibliography/narrative-author-year.csl %}. GA26 combines these benefits within its model suite, since distillation encourages agreement during training, while shared layers reduce duplicated work during inference.

## The fields and concepts it connects to

The use of smaller models within a larger network also connects conceptually to the lottery ticket hypothesis {% cite frankle2019lottery --style _bibliography/narrative-author-year.csl %}. They showed that a large trained network contains much smaller sub-networks that, trained alone from the same starting weights, reach similar accuracy. Finding them, however,requires training the large network first and then pruning it. The resulting sub-networks are scattered sets of weights. MatFormer and GA26 design the
smaller networks in advance. The whole family is then trained together from
scratch, and each size can be extracted as a complete model.

Another related approach is elastic compression, which turns an already trained LLM into several smaller versions through additional training {% cite cai2024flextron %}. GA26 instead trains the different networks together from scratch, aiming to reduce the cost of creating new versions.

Finally, LoRA {% cite hu2021lora %} adapts a pretrained model by freezing its original weights and learning small, low-rank updates. Its connection to GA26 is the broader goal of reducing training costs through parameter reuse. However, LoRA’s updates still require the base model’s weights, whereas GA26 jointly trains complete models of different sizes with shared weights.  LoRA is therefore a related efficiency technique.

