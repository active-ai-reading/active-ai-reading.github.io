---
title: "Making the LLM-JEPA abstract clearer"
description: "Introduce JEPA, make its application to language concrete, and clarify what the experiments show."
paper: llm-jepa
task: abstract
by: [roey-magen]
---

## What I changed and why

The original abstract assumes familiarity with JEPA without explaining how it applies to language. I introduced its central mechanism, added a concrete instruction–code example, and clarified that the proposed loss supplements next-token prediction. I also replaced the broad claim of superiority in vision with a question about what embedding-space prediction can add to language modeling. I added details about the framework and its practical advantages. These details make the approach more concrete and explain why it is useful: readers can see how it reuses the existing model and improves performance without making inference more expensive.

## Before and after

<div class="before-after">
  <div class="before">
    <span class="label">Before</span>
    <p>Large Language Model (LLM) pretraining, finetuning, and evaluation rely on input-space reconstruction and generative capabilities. Yet, it has been observed in vision that embedding-space training objectives, e.g., with Joint Embedding Predictive Architectures (JEPAs), are far superior to their input-space counterpart. That mismatch in how training is achieved between language and vision opens up a natural question: can language training methods learn a few tricks from the vision ones? The lack of JEPA-style LLM is a testimony of the challenge in designing such objectives for language. In this work, we propose a first step in that direction where we develop LLM-JEPA, a JEPA based solution for LLMs applicable both to finetuning and pretraining. Thus far, LLM-JEPA is able to outperform the standard LLM training objectives by a significant margin across models, all while being robust to overfiting. Those findings are observed across numerous datasets (NL-RX, GSM8K, Spider, RottenTomatoes) and various models from the Llama3, OpenELM, Gemma2 and Olmo families. Code: <a href="https://github.com/rbalestr-lab/llm-jepa">https://github.com/rbalestr-lab/llm-jepa</a>.</p>
  </div>
  <div class="after">
    <span class="label">After</span>
    <p>Joint Embedding Predictive Architectures (JEPAs) learn representations by predicting one view’s embedding from another. This approach has shown promising results in representation learning for computer vision. While large language models (LLMs) are predominantly trained through next-token prediction, it remains unclear whether this objective alone produces representations that are readily predictable across semantically related inputs. This raises a natural question: can embedding-space prediction improve the representation learning and generalization capabilities of LLMs without sacrificing their generative abilities?</p>
    <p>We introduce LLM-JEPA, a training framework that combines the standard next-token prediction objective with an embedding prediction loss. Given two views of the same underlying information, such as a natural-language instruction and its corresponding code, the model learns to predict one view’s representation from the other. The LLM serves as both encoder and predictor, requiring no separate prediction network or additional computation at inference. LLM-JEPA improves performance over next-token prediction alone across datasets including NL-RX, GSM8K, and Spider, and model families including Llama3, OpenELM, Gemma2, and OLMo. It also shows greater resistance to overfitting during fine-tuning and improves downstream sentiment classification on Rotten Tomatoes after pretraining.</p>
  </div>
</div>

## The general rule

**Explain before you evaluate.** Give readers enough context to understand the method before presenting its results. A brief explanation and a concrete example make performance claims more meaningful.
