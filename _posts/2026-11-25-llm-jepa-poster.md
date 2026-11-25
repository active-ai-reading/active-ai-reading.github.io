---
title: "Can predicting an answer’s representation help a language model generate better answers?"
description: "This poster explains how LLM-JEPA trains a language model to predict both the next token and a vector representing the answer."
paper: llm-jepa
task: extras
by: [yakovafgin]
---

{% include figure.liquid path="assets/img/posts/LLM-JEPA-web-poster.png" class="img-fluid rounded" avoid_scaling=true zoomable=true alt="LLM-JEPA training diagram and regular-expression results. Exact-match accuracy rises from 57.29% to 71.46% with the added vector prediction objective." caption="The blue arrow shows the vector predicted from the prompt. The orange arrow shows the vector the model gets from reading the reference answer. Training encourages the two arrows to point in the same direction." %}
