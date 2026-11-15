---
title: "Why Do Language Models Read and Write in the Same Tokens?"
description: "Input and output tokenization serve different purposes. Should we really use the same tokenizer for both?"
paper: tokenization-survey
role: research
task: followups
by: [Reuvenspitz]
---

<!-- FOLLOW-UPS -->
## Follow-ups worth doing

While reading the survey, I noticed that several approaches already treat input and output tokenization differently. DPE (Section 3.6) processes characters while predicting subwords. Hong et al. (2024) modify the output vocabulary and convert generated tokens back into the input representation, while Huang et al. (2025) expand the effective input vocabulary (Section 12.1).

These approaches point to a simple question: **Why should the same tokenizer be optimal for both reading and writing?**

The two sides have different roles. Input tokenization determines how information is represented to the model, while output tokenization also determines what the model needs to predict at each step. It affects the learning objective and the number of autoregressive steps needed to generate text. There is no obvious reason why the same tokenization should be best for both.

Still, most autoregressive language models use a shared tokenizer. This is convenient because generated tokens become part of the input in the following steps. Separating the two sides would make the architecture more complicated. But perhaps this convenience comes at a cost.

A recent paper, [When Tokenization is Secretly Output Supervision](https://arxiv.org/abs/2609.01386) (Baeumel et al., 2026), provides an interesting starting point. The authors trained small models on three-digit addition, independently varying whether the input and output were tokenized as whole numbers or individual digits. Surprisingly, output tokenization had a much stronger effect on learning and performance than input tokenization.

This raises two possible follow-ups.

### 1. Does it depend on what the model is trying to do?

Perhaps output tokenization dominates in arithmetic because the main challenge is computing and generating the answer. But would the same happen in tasks where understanding the internal structure of the input is more important?

One way to investigate this would be to extend the experiment to natural language tasks, such as text infilling and character-level editing. We could use a shared vocabulary that supports both character-level and subword-level segmentation, and vary the input and output tokenization independently, as in the original experiment.

Comparing performance and generalization across different tasks could reveal whether the relative importance of the two sides changes with the task.

If it does, this would suggest that using a shared tokenizer involves a trade-off between different requirements. It might also help explain why intrinsic tokenizer metrics (Section 7) do not always predict downstream performance well.

### 2. What if the two sides used completely different tokenization methods?

The first experiment would still use different segmentations within a shared vocabulary. But perhaps we should consider a more fundamental separation.

For example, byte-level input could allow the model to handle arbitrary text without depending on a fixed subword vocabulary, while subword-level output could reduce the number of generation steps.

This connects to the discussion of hierarchical byte-level models in Section 9, where efficient decoding remains an important challenge.

A possible experiment would compare a standard subword model, a byte-level model, and a hybrid model with byte-level input and subword-level output, under similar computational budgets.

This would require more architectural changes, and the comparison would be harder to control. Still, it could help answer a broader question: **Instead of asking which tokenization method is best, should we ask which method is best for each side?**

### Final thought

Tokenization is usually treated as one design choice, but perhaps it is really two. Understanding the difference could change both how we design language models and how we evaluate tokenizers.
