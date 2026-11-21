---
title: "Papers worth knowing this week"
description: Two recent papers exploring how language models can acquire new knowledge while preserving previously learned capabilities.
paper: spurious-forgetting
task: trending
by: [MatanBarTov]
---

This week's paper, *When Forgetting Is Not Catastrophic: On the Mechanics of Spurious Forgetting*, challenges the assumption that a decline in factual recall necessarily implies a loss of knowledge. Motivated by this distinction, I searched for recent papers investigating continual learning, knowledge retention, and the geometry of weight updates.

I used Hugging Face Daily Papers to estimate community interest, considering both total upvotes and average upvotes per day since submission to account for the different ages of the papers.

## 1. [The Surprising Effectiveness of Deleting Weights in LLM Post-Training](https://arxiv.org/abs/2611.10866)

**Published:** November 7, 2026

**Popularity:** [21 Hugging Face upvotes](https://huggingface.co/papers/2611.10866), averaging 2.10 upvotes per day since submission, and 129 GitHub stars.

**One-sentence summary:** The authors introduce Deletion Tuning, a method that matches full fine-tuning across three post-training regimes by selectively zeroing fewer than 0.05% of a language model's weights, while substantially reducing forgetting in reinforcement learning experiments.

## 2. [Continual Learning Mechanisms Compose for Long-Horizon Memorization](https://arxiv.org/abs/2609.06986)

**Published:** September 7, 2026

**Popularity:** [48 Hugging Face upvotes](https://huggingface.co/papers/2609.06986), averaging 0.73 upvotes per day since submission, and 25 GitHub stars.

**One-sentence summary:** By combining complementary continual learning mechanisms with merged LoRA, the authors improve average final knowledge retention from 1.2% to 34.9% across three datasets of 100 sequential memorization tasks.
