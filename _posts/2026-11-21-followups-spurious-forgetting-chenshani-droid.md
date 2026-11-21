---
title: "3 Follow-Ups: Understanding and Preventing Spurious Forgetting"
description: Exploring how semantic structure, learned abilities, and training dynamics influence spurious forgetting.
paper: spurious-forgetting
task: followups
by: [chenshani-droid]
---

<!-- FOLLOW-UPS -->
## Follow-ups worth doing
The paper demonstrates that forgetting during fine-tuning does not necessarily imply a loss of knowledge. Instead, a common shift in internal 
representations can temporarily interfere with retrieving previously learned facts (Spurious Forgetting). This raises several questions about what determines forgetting, 
whether it extends beyond factual knowledge (like mathmatical or coding abilities), and how we might prevent it.

## 1. Does generalization come at the cost of remembering?

**Research question:** How does the semantic structure of newly learned knowledge affect spontaneous recovery?

In Section 5.1, the authors of the paper observe spontaneous recovery when the new facts are arbitrary associations, but not when they are semantically meaningful.
They suggest that a possible explanation for that is that shared information remains useful for predicting meaningful associations, potentially reducing the incentive to reverse the common shift (caused by fine-tuning).

However, the two datasets differ in more than just their semantic structure.

**Proposed experiment:** Construct a controlled dataset of subject-answer pairs and gradually increase the proportion of randomly shuffled answers. For example, assign fictional individuals hometowns that are consistent with their countries of origin, and progressively shuffle these assignments. This would allow us to vary the predictability of the answers while keeping the subjects, answer vocabulary, dataset size, and answer frequencies fixed.

Measure the magnitude of the common shift and the extent of spontaneous recovery at different levels of semantic structure, comparing models at similar new-fact accuracy.

**Why it is worth doing:** This experiment could help establish whether semantic structure itself determines the persistence of forgetting (we could see if there is a trend to the level of forgetting as semantic structure changes, rather than just comparing 2 extreme cases like the paper examined). It would also investigate a potentially counterintuitive trade-off between learning generalizable patterns and preserving access to previously learned knowledge.

## 2. Do language models forget abilities or just facts?

**Research question:** Does the mechanism of spurious forgetting extend beyond factual recall to more complex tasks and abilities?

The paper focuses on factual associations, but as we know, language models also acquire abilities such as mathematical reasoning, programming, and logical inference. It remains unclear whether the deterioration of these abilities during fine-tuning can arise from the same geometric mechanism.

**Proposed experiment:** Evaluate a pretrained language model on factual recall but also on mathematical reasoning, and programming tasks. Fine-tune it on an unrelated domain, such as history, and measure the deterioration of each capability. Then apply the SVD-based intervention introduced in Section 5.2 of the paper and evaluate the extent to which each capability recovers, without retraining on the original tasks.

Compare the model's performance before and after the SVD modification, and investigate whether removing other singular components (not only the dominant one) can also restore previously learned abilities.

**Why it is worth doing:** Recovering complex abilities through targeted low-rank weight interventions would provide evidence that the mechanism extends beyond associative memory. This could have practical implications for developing specialized language models without sacrificing previously acquired capabilities.

## 3. Can we prevent forgetting by changing the order of training?

**Research question:** What if we deliberately organize the training data so that the gradients are less aligned? Can controlling gradient alignment during fine-tuning reduce the common representational shift responsible for spurious forgetting?

The mechanism described in Section 3 of the paper suggests that shared structure across training examples produces aligned updates, which collectively shift old representations and interfere with the retrieval of knowledge. This raises the possibility of controlling the shift by organizing the training examples.

**Proposed experiment:** Fine-tune identical models on the same dataset using three mini-batch constructions:

- Random batching: standard random sampling.
- Homogeneous batching: grouping semantically similar examples together.
- Diverse batching: deliberately combining examples from different semantic groups.

The hypothesis is that diverse batches could reduce the alignment of interfering gradient components, thereby limiting the common shift.

Measure gradient similarity, the magnitude of the common shift, and accuracy on both old and new facts throughout training. Compare the strategies at matched new-fact accuracy to ensure that less forgetting is not simply a consequence of less learning.

**Why it is worth doing:** While the authors use SVD to recover old knowledge after forgetting has occurred, this approach aims to reduce forgetting in the first place. If it would be successful, then changing how training examples are grouped into mini-batches could help preserve old knowledge without modifying the model architecture, adding parameters, or retraining on old data.

