---
title: "New abstract for LLM-JEPA"
description: reframing the novel contributions of the paper
paper: llm-jepa
role: writing
task: abstract
by: [IdoRavid]
---

## What I changed and why

The original abstract is fairly good, actually! In the sense that, at least, i understood some what they were trying to convery in the paper (as opposed to some previous papers we've read recently). Another benefit is that it's actually pretty short and to the point. Having said that, i felt that the abstract, and the paper as a whole, has some JEPA-optimistic bias (which i get!). I tried to rewrite it in a somewhat more balanced way.

## Yann (et al)'s version:

> Large Language Model (LLM) pretraining, finetuning, and evaluation rely on input-space reconstruction and generative capabilities. Yet, it has been observed in vision that embedding-space training objectives, e.g., with Joint Embedding Predictive Architectures (JEPAs), are far superior to their input-space counterpart. That mismatch in how training is achieved between language and vision opens up a natural question: can language training methods learn a few tricks from the vision ones? The lack of JEPA-style LLM is a testimony of the challenge in designing such objectives for language. In this work, we propose a first step in that direction where we develop LLM-JEPA, a JEPA based solution for LLMs applicable both to finetuning and pretraining. Thus far, LLM-JEPA is able to outperform the standard LLM training objectives by a significant margin across models, all while being robust to overfiting. Those findings are observed across numerous datasets (NL-RX, GSM8K, Spider, RottenTomatoes) and various models from the Llama3, OpenELM, Gemma2 and Olmo families.

## My Version:

> Nowadays, State-of-the-art LLMs are pretrained almost exclusively on a single task - autoregressive text prediction. This loss, powerful as it may be, does not explicitly influence the shape of the representation space. JEPA architerctures, which have shown some favorable results in Vision tasks, focus on shaping the representation space of the inputs. This paper aims to bridge the two. To do so, we offer a combined LLM-JEPA loss, along with small changes to transformer architecture and inputs. We show some gains ranging from modest to substantial, in various models and downstream tasks.

## Additional thoughts

The title is good, too, in my opinion. I intentionally removed some of the specifications of the implementation. Besides making it easier to read, my thought was that the readers belong to one of two crowds: (i) familiar with JEPA, in which case the combination is easier to imagine and would want to see the details directly, or (ii) unfamiliar with it, in which they need some background which the asbtract shouldn't supply. In both cases, leaving it less specific felt more natural to me.

