---
title: "Follow-ups on Tokenization: A Survey for Modern NLP"
description: "Should input and output tokenization be optimized separately, and when would this be beneficial?"
paper: tokenization-survey
role: research
task: followups
by: [Reuvenspitz]
---

<!-- FOLLOW-UPS -->
## Follow-ups worth doing

### Background: Should input and output tokenization be designed separately?

The survey describes several approaches that treat input and output tokenization differently:

- **DPE (Section 3.6)** processes characters in the decoder while predicting subword tokens.
- **Hong et al. (2024)** modify the output vocabulary and retokenize generated text before feeding it back to the model, while **Huang et al. (2025)** expand the effective input vocabulary (Section 12.1).
- **Tao et al. (2024)** discuss the trade-off between vocabulary size, sequence compression, and the computational cost of the output softmax (Section 11.4).
- **Section 9.3** discusses the difficulty of efficient generation in byte-level models, where producing text byte by byte can be expensive.

These approaches raise a more general question: **Why should the same tokenizer be optimal for both input and output?**

Input tokenization determines how information is represented to the model. Output tokenization also determines the units the model must predict, how the prediction loss is computed, and how many autoregressive steps are needed. These are different roles with different costs, so there is no obvious reason why the optimal tokenization should be the same.

Most autoregressive language models nevertheless use a shared tokenizer. One important reason is practical: generated tokens become part of the input in the following steps, so using different tokenizers requires converting between the two representations.

A recent study, [When Tokenization is Secretly Output Supervision](https://arxiv.org/abs/2609.01386) (Baeumel et al., 2026), investigated this distinction in a controlled setting.

The authors trained small models on three-digit addition, independently varying whether input and output numbers were represented as whole tokens or as individual digits. They used a shared vocabulary that supports both representations, allowing a 2×2 comparison.

They found that output tokenization had a much stronger effect than input tokenization on performance, training dynamics, and internal representations.

This is an interesting result, but it is not clear whether it reflects a general property of tokenization or something specific to arithmetic tasks.

### Follow-up 1: When does each side matter?

**The question.** Does the relative importance of input and output tokenization depend on the type of task?

**The experiment.** Extend the controlled experiment of Baeumel et al. to several tasks with different requirements, including natural language tasks.

For example, we could compare text infilling with character-level editing or other text transformations. Some tasks may require more precise access to individual characters in the input, while others may be more sensitive to how the output is generated.

We could use a shared vocabulary supporting both fine-grained and subword-level tokenization, and independently vary the input and output segmentation, as in the original experiment. Importantly, both sides should have meaningful alternative tokenizations in each task.

We could also examine generalization to unseen examples or combinations, rather than comparing only accuracy on familiar patterns.

**Why it is worth doing.** This experiment could show whether the strong influence of output tokenization observed in arithmetic also appears in natural language tasks, or whether the importance of each side changes depending on the task.

It could also help explain why intrinsic tokenizer metrics (Section 7) do not always predict downstream performance well: different tasks may depend on different properties of the input and output representations.

The experiment would require more work than the original arithmetic setup, but small models and controlled tasks could make it feasible without training a large language model.

### Follow-up 2: Different methods, not just different granularities

**The question.** Could input and output benefit from fundamentally different tokenization methods, rather than simply different granularities within the same vocabulary?

For example, a model could process input at the byte level while generating output using subword tokens.

**The experiment.** One possibility would be to compare three models under similar computational budgets: a standard subword model, a byte-level model, and a hybrid model with byte-level input and subword-level output.

Byte-level input avoids dependence on a fixed subword vocabulary and can handle arbitrary text. On the other hand, generating one byte at a time requires many autoregressive steps.

A hybrid approach could potentially combine the flexibility of byte-level input with the efficiency of subword-level generation.

Generated subwords can be converted back into bytes, although integrating this efficiently into an autoregressive model would still require architectural changes.

**Why it is worth doing.** This connects to the discussion of hierarchical byte-level architectures in Section 9. It is a more ambitious experiment, and it would be harder to isolate the effect of tokenization from other architectural differences.

Still, it could help determine whether the best input representation and the best output representation should be designed independently.

Rather than asking whether byte-level or subword-level tokenization is better, we could ask which representation is better for each part of the model.

### Conclusion

Input and output tokenization serve different roles, but are usually treated as a single design choice. Understanding when they should differ could lead to better model designs and a more meaningful way to evaluate tokenization methods.
