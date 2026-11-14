---
title: "Rewriting the abstract of Tokenization - A Survey for Modern NLP"
description: A more concise and contribution centered rewrite of the abstract. 
paper: tokenization-survey # the filename of the paper in _papers/, without .md
role: writing
task: abstract 
by: [achi-or]
---

## What I changed and why

The abstract is very long, which is adequate for such a comprehensive survey, though I thought it can be more concise, 
and highlight the extra contributions the survey has other than systemization of knowledge. 
Also, the abstract spends many words on sub words vs. character, and it feels that those are considerations anyone slightly familiar with the concept of tokenization will know. 


## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
  While modern language models take raw text as their input and produce raw text as output,
they do not operate over text directly. Hidden in the very first step of language model
pipelines is tokenization, where raw text is converted to a sequence of tokens which the
model is designed to process.
The dominant approach to tokenization is subword tokenization, which uses tokens whose
granularity lies between that of characters (or bytes) and words. Subword tokenization is
ubiquitous in modern natural language processing (NLP) due to its advantages: compared
to word-level models, it solves the out-of-vocabulary problem while constraining the vocab
ulary size, reducing the number of embedding parameters and logits needed. Compared to
character-level models, it improves the inductive bias of models by packing more information
into a token while producing significantly shorter sequences.
While this technique is powerful, it is not without flaws. To name a few: it imposes a
rigid system for how tokens are built, and one system may not generalize across languages;
segmentation ambiguities create room for adversarial attacks; in multilingual settings, bal
ancing the token allocation between high- and low-resource languages must be done explic
itly; and the reliance on a static, pre-computed vocabulary means the tokenization process
is disjoint from the model’s training, preventing true end-to-end optimization. There is
substantial room for innovation in this domain, yet progress is contingent upon a clear un
derstanding of existing methodologies and current bottlenecks. This survey aims to serve
that purpose.
We present tokenization in the context of the modern large language model (LLM) era and
cover the breadth of areas that tokenization directly influences. We discuss algorithms,
techniques, pitfalls, theory, and practice, along with jumping-off points for prospective re
searchers and practitioners. We hope that this survey brings more attention to the field of
tokenization as an area in which much progress is still to be made.
  </div>
  <div class="after"><span class="label">After</span>
  Language models never see text. They see the output of a tokenizer: a pipeline of normalization, pretokenization, a vocabulary, and a segmentation algorithm that together decide what a model can represent. These choices underlie some of the most visible LLM failures, including brittle arithmetic and spelling, adversarial vulnerabilities, and a “token tax” that makes the same content cost more in many languages. Yet tokenization made up a small fraction of 2025 NLP and ML papers.
  We argue this neglect of tokenizers' research is structural: tokenizer ablations are costly and noisy at scale, perplexity is not comparable across tokenizers, and benchmarks typically freeze the tokenizer.
  This neglect is also visible through the confomism regarding choice of tokenizers - we complement the survey with a census of over 420k Hugging Face models and an audit of frontier tokenizers, open and closed. Together they reveal a monoculture: BPE with 100–275k vocabularies, and 94% of models reusing another model’s tokenizer exactly.
  We survey the field across the whole pipeline and model lifecycle: subword algorithms and pretokenization, writing systems and multilinguality, evaluation, non-canonical tokenizations, byte-level, latent and pixel-based alternatives, changing the tokenizer of a trained model, security, and theory. 
  We hope that this survey brings more attention to the field of tokenization as an area in which much progress is still to be made. Each section closes with open questions, and we identify evaluation as the main bottleneck to progress.
  </div>
</div>

## The general rule

I wanted the abstract to actually hold the contribution, and aim for someone that is somewhat familiar with the topic, 
not to start "from scratch" - it's redundant and doesn't allow to say what's importnat to the actual readers. 

## What I’m unsure about
1. Maybe the new abstract is too concentrated on the "other than SoK" parts, and misses the SoK centrality of this paper. 
2. Maybe I'm "jumping" ahead too much and the original abstract is better for "beginner readers"? 
3. The strctural claim appears in the papaer but i gave it a more central posistion and maybe I'm incorrect in understanding the papaer (hard to get a full grasp on such a msiive paper).
