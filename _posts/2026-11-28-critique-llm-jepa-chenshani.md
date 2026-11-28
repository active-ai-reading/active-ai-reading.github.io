---
title: "Critique of LLM-JEPA: Better Representations or Better Regularization?"
description: Examining whether improved performance reflects better semantic representations or an additional regularization effect.
paper: llm-jepa
task: critique
by: [chenshani-droid]
---

<!-- CRITIQUE -->
## Summary of the claims

LLM-JEPA combines next-token prediction with an additional training objective that predicts representations of related information. 
The authors claim that this approach improves performance, prevents overfitting, and encourages more structured internal representations without additional inference computation.

## Strengths

- **Simplicity:** The method requires no substantial architectural changes or additional inference computation.
- **Empirical diversity:** The authors evaluate multiple model families, datasets, and training settings.
- **Beyond accuracy:** The paper investigates the geometry of learned representations, attempting to explain the mechanism.
- **Computational efficiency:** JEPA-loss dropout offers a practical way to reduce additional training costs.

## Weaknesses

1. **Embedding alignment does not necessarily imply better representations.** Smaller singular values of the difference between text and code embeddings do not necessarily indicate lower rank or better semantic structure. In the extreme case, representation collapse would minimize these differences while eliminating semantic distinctions.

2. **Semantic learning or regularization?** Improved generalization and reduced overfitting may result from the addion to the objective acting as a regularizer. In my opinion, the paper does not really distinguish between these explanations.

3. **Fairness of comparisons.** LLM-JEPA receives additional hyperparameter tuning compared to standard fine-tuning. Furthermore, alternative loss functions in Table 3 are evaluated using the same loss weight, despite potentially different gradient magnitudes.

4. **Limited generalizability.** The strongest improvements are observed on tasks where the data already contains two related views, such as a text description and its corresponding code. However, for ordinary text, it is less clear how to create meaningful pairs. Therefore, it remains unclear whether LLM-JEPA would be equally effective for general language model pretraining.


## How it could have been improved

1. Measure embedding norms, effective rank, and variance to distinguish meaningful semantic alignment from partial representation collapse.

2. Compare against independently tuned regularization methods and introduce shuffled pair controls to investigate whether meaningful pairing is essential.

3. Independently tune competing objectives under comparable hyperparameter search budgets and report actual training costs.

4. Evaluate different view construction strategies, such as paraphrases, summaries, and masked text, alongside larger scale pretraining experiments.


## Verdict

**Worth publishing? Yes, with reservations.** The method is simple, practically relevant, and supported by promising empirical results. However, the evidence for improved performance is stronger than the evidence that improved semantic abstraction explains these gains.

**Worth pursuing? Yes.** Combining generative and representation learning objectives looks like a promising research direction. Future work should prioritize understanding whether the improvements arise from semantic alignment, regularization, or optimization effects, rather than simply demonstrating additional benchmark improvements.

