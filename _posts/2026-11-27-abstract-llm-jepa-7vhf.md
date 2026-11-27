---
title: "Rewriting the abstract of LLM-JEPA"
description: One sentence that makes people want to click.
paper: llm-jepa
task: abstract
by: sprinzak
---

<!-- Keep the sections that fit your task, delete the rest. -->

## What I changed and why

The original abstract was good overall and conveyed the main message clearly. I added a brief explanation of how JEPA predicts the embedding of one view from another, along with a concrete example from language: a natural-language description paired with its corresponding code. This helps readers who are unfamiliar with JEPA understand the proposed approach on a first read.

## Before and after

<div class="before-after">
  <div class="before">
    <span class="label">Before</span>
    <p>Large Language Model (LLM) pretraining, finetuning, and evaluation rely on input-space reconstruction and generative capabilities. Yet, it has been observed in vision that embedding-space training objectives, e.g., with Joint Embedding Predictive Architectures (JEPAs), are far superior to their input-space counterpart. That mismatch in how training is achieved between language and vision opens up a natural question: can language training methods learn a few tricks from the vision ones? The lack of JEPA-style LLM is a testimony of the challenge in designing such objectives for language. In this work, we propose a first step in that direction where we develop LLM-JEPA, a JEPA based solution for LLMs applicable both to finetuning and pretraining. Thus far, LLM-JEPA is able to outperform the standard LLM training objectives by a significant margin across models, all while being robust to overfiting. Those findings are observed across numerous datasets (NL-RX, GSM8K, Spider, RottenTomatoes) and various models from the Llama3, OpenELM, Gemma2 and Olmo families.</p>
  </div>
  <div class="after">
    <span class="label">After</span>
    <p>Large language models (LLMs) are typically trained to predict the next token in a text sequence. In vision, training objectives defined in embedding space have outperformed input-space reconstruction in some settings. Joint Embedding Predictive Architectures (JEPAs) use this approach by predicting the embedding of one view from another. We introduce LLM-JEPA, a training objective that applies this principle to LLM pretraining and fine-tuning using paired views such as a natural-language description and its corresponding code. Across experiments on NL-RX, GSM8K, Spider, and Rotten Tomatoes, LLM-JEPA outperforms standard training objectives across models from the Llama 3, OpenELM, Gemma 2, and OLMo families and shows robustness to overfitting.</p>
  </div>
</div>

## The general rule

When an abstract borrows a method from another field, explain what the method does in one sentence and give a concrete example from the new setting.
