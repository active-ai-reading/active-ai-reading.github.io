---
title: "The Authors' Path of Matryoshka Language Model Suites"
description: Background about the authors' of Matryoshka LM Suites and their recent research.
paper: matryoshka-lm-suites
role: research
task: authors
by: [shniki]
---

## Get to Know the Authors
### Nathan Godey
Nathan Godey is a Post-doctoral Associate working in Yoav Artzi's lab at Cornell University. 
Godey's research is mostly driven by understanding and improving the representations of language models.

### Yoav Artzi
Yoav Artzi is a Professor at Cornell University and a Visiting Researcher at Google DeepMind.
His lab, Cornell Language, Interaction, and Learning (LIL), primarily focuses on natural language modeling, processing, and learning.

## Matryoshka LM and the Rest of Their Research
Godey's PhD thesis revolves around improving language models, whether by optimizing training time, generation time, memory usage, or perplexity. These principles are reflected on all of Godey's work, especially on his recent work with Artzi. The two develop new architectures, as well as pinpointing architectural bottlenecks such as the LM head.

### Some New Architectures
* The **Matryoshka LM suite** cuts training time (among other optimizations) for a family of similar models of different sizes.
* **Copy-Paste LMs** introduce new types of tokens <copy> and <sink> and create a pointer mechanism to yield better models (improved performance across training time, generation time, memory usage, and perplexity).
* Continuous-query limited memory language models (**CO-LMLM**) achieve lower perplexity than models trained on significantly more data.  Instead of relying solely on the model's parameters, the mechanism retrieves data from an external unstructured knowledge base triggered by a special <FACT> token.
* Implement **Memory sharing in Loop Transformers (LT)** to reduce perplexity.
