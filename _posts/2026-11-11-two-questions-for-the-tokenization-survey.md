---
title: "2 papers challenging the tokenization survey"
description: "Recent papers question how we evaluate tokenizers and how we help underrepresented languages."
paper: tokenization-survey
role: scouting
task: hidden-gems
by: [IdoRavid]
---

The Survey paper is a substantial body of work covering many questions and issues regarding tokenizers. I looked for two recent papers that deal with, and challenge, assumptions and claims from the survery:

- **[Tokenizer Myths and Where To Find Them](https://arxiv.org/abs/2611.04215)** (Schaeffer & Koyejo, November 2026): 
Bits per byte (BPB), an evaulation metric for tokenizers, is defined as "agnostic" to the tokenization process. This paper claims that the BPB metric can favor particular tokenizers and vocabulary sizes even when the language models are untrained. This complicates the survey's use of BPB for cross-tokenizer comparison, as it is biased in a way and therefore less reliant.

- **[Language-Specific Effects of Tokenizer Choice in Multilingual Language Models](https://arxiv.org/abs/2610.12144)** (Meister, Altıntaş & Bosselut, October 2026): One key challenge that's addressed in the survey is multi-lingual tokenizations, and cross-lingual tokenization. The central claim is that tokenizers are biased towards lagnuages that are prominent in the dataset, and advocate twoards higher allocation of training resoursces to these low-frequency languages.
 This paper trys to reallocate more tokenizer training-data to lower-resource language. The result, across 123 models and 54 tokenizers, gives an overall HIGHER PBP. This might mean the PBP metric itself is problematic (as claimed in the paper above), or that, as the autorhs suspect,
 extra vocabulary entries may receive too little language-model training to learn useful embeddings.
