---
title: "When Forgetting is not Catastrophic: On the Mechanics of Spurious Forgetting"
short: Spurious forgetting
authors: Vedant Palit, Florent Draye, Nicolas Zucchet, Zhijing Jin, Bernhard Schölkopf
year: 2026
arxiv: "2610.08718"
tldr: >
  (To be written by the class after week 5. Edit this file: one or two sentences someone can read in 10 seconds.)
tags: [forgetting, fine-tuning, plasticity, learning dynamics]
---

## For more reading

How training in one place changes what the model can do, or learn, somewhere else:

- [Learning Dynamics of Continual Learning: A Unified View of Data Attribution, Forgetting, and Plasticity Loss](https://arxiv.org/abs/2609.33620): how learning one token changes another prediction, and how updates slowly reduce what the model can learn later.
- [Can Scale Save Us From Plasticity Loss in Large Language Models?](https://arxiv.org/abs/2606.24752): a quick read. GPT-style models lose plasticity in a multilingual continual-learning setup, and larger models only delay when it starts.
- [Weight Decay Improves Language Model Plasticity](https://arxiv.org/abs/2602.11137): a base model that looks worse after pretraining can be better after fine-tuning.
- [Pre-training LLM without Learning Rate Decay Enhances Supervised Fine-Tuning](https://arxiv.org/abs/2603.16127) and [(How) Learning Rates Regulate Catastrophic Overtraining](https://arxiv.org/abs/2604.13627): learning-rate decay gives sharper minima that adapt and retain worse.
- [Sharpness-Aware Pretraining Mitigates Catastrophic Forgetting](https://arxiv.org/abs/2605.02105): flatter pretraining minima forget less after post-training.
- [Replaying pre-training data improves fine-tuning](https://arxiv.org/abs/2603.04964): replaying generic data helps the target task itself, not only retention.
- [Early Data Exposure Improves Robustness to Subsequent Fine-Tuning](https://arxiv.org/abs/2605.12705): how a capability is learned decides whether it survives later fine-tuning.
- [The Piggyback Hypothesis of Generalization](https://arxiv.org/abs/2606.06667): narrow fine-tuning spreads to unrelated prompts through the chat-template tokens.
