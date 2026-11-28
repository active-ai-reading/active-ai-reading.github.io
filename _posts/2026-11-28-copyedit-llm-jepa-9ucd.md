---
title: "Rewriting the abstract of LLM-JEPA"
description: The abstract spends five sentences clearing its throat before telling you what it did — here's a version that leads with the finding, the mechanism, and a number.
paper: llm-jepa
task: copyedit
by: dan22333
---

<!-- Copyedit of Huang, LeCun & Balestriero, "LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures", arXiv:2509.14252. -->

## What I changed and why

The original abstract buries its lede: four of its nine sentences are field-level framing (vision beats language, a rhetorical question, "a testimony of the challenge") before the reader learns what the paper actually built, and the single most important idea — that you get a JEPA objective for a *generative* LLM by treating a (text, code) pair as two **views** of the same knowledge — never appears in the abstract at all. The result is also unquantified ("a significant margin") when Figure 1 has clean numbers to offer. I rewrote it to open on the mechanism and the finding, fold the motivation into one sentence, kill the rhetorical question, add a concrete number, and fix the hedging ("Thus far, LLM-JEPA is able to outperform") and the "overfiting" typo.

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
  Large Language Model (LLM) pretraining, finetuning, and evaluation rely on input-space reconstruction and generative capabilities. Yet, it has been observed in vision that embedding-space training objectives, e.g., with Joint Embedding Predictive Architectures (JEPAs), are far superior to their input-space counterpart. That mismatch in how training is achieved between language and vision opens up a natural question: can language training methods learn a few tricks from the vision ones? The lack of JEPA-style LLM is a testimony of the challenge in designing such objectives for language. In this work, we propose a first step in that direction where we develop LLM-JEPA, a JEPA based solution for LLMs applicable both to finetuning and pretraining. Thus far, LLM-JEPA is able to outperform the standard LLM training objectives by a significant margin across models, all while being robust to overfiting. Those findings are observed across numerous datasets (NL-RX, GSM8K, Spider, RottenTomatoes) and various models from the Llama3, OpenELM, Gemma2 and Olmo families.
  </div>
  <div class="after"><span class="label">After</span>
  Vision models learn far better representations when trained to predict in embedding space — as Joint Embedding Predictive Architectures (JEPAs) do — than in input space, yet LLMs are still trained almost entirely by reconstructing tokens. We bring JEPA to language with LLM-JEPA, which adds an embedding-space prediction loss alongside the usual next-token objective: whenever a dataset gives two <em>views</em> of the same knowledge — e.g., a natural-language description and the regex or SQL it specifies — we train the model to predict one view's representation from the other. This keeps the LLM's generative ability intact while sharpening its representations. Across the Llama3, Gemma2, OpenELM, and Olmo families and four datasets (NL-RX, GSM8K, Spider, RottenTomatoes), LLM-JEPA beats standard finetuning by large margins — e.g., it lifts Llama3 on NL-RX-SYNTH from 37% to 52% accuracy — and resists overfitting, with encouraging early results for pretraining too. Code: github.com/rbalestr-lab/llm-jepa.
  </div>
</div>

## The general rule

**Lead with the mechanism and the finding; demote the motivation to one sentence — and put a number in.** An abstract reader is deciding whether to keep reading, so the first two sentences should tell them *what you did*, *how it works*, and *roughly how much it helped*. Framing about the state of the field is a toll you make the reader pay, not the product; pay it once and move on. And never pose a rhetorical question ("can language learn a few tricks from vision?") when you can just state the answer you found.
