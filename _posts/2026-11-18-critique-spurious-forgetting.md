---
title: "Critique of Spurious Forgetting paper"
description: The Spurious Forgetting paper offers a cool and intuitive explanation of this odd phenomena, but assumes rather strong assumptions that might not be reproducible or hold for real-sized LLMs.
paper: spurious-forgetting
role: research
task: critique
by: [IdoRavid]
---

This paper deals with an intriguing phenomena related to a common failure mode for large neural models (lagnuage models or others). Fine tuning is known to hurt capabilities in already-learend tasks. The phenomena described here, named "Spurious forgetting", deals with cases in which the original capabilities, namely information that was originally stored in the model, is still recoverable after forgetting. 

The paper tries to give an answer as to HOW This happens, and builds an interseting mathematical model that explains it.


## Strengths.

- Writing - it is well written. most sections provide, in my opionion, a clean and well seperated idea that one could understand. It is not overly simplified, but it maintains good balance between making the ideas accessible while not underselling the complexity.

- Mathematical model - the mathematical ideas that are suggested in the paper, namely the geometric representation of old and new facts during training, the effects of normalization, and the ingredients needed to replicate the phenomena - seemed all well established to me. Under the assumptions of the paper, they offer a plausible and intuitive explanation of the failure mode that causes this phenomena.


## Weaknesses

- Representability - the assumed minimal model seems somewhat different from the way an actual LLM functions:
 1.  The minimal model focuses only on MLP layers while abstracting attention. this might be a logical step, but  a clearer link  to a full attention head would be closer to a real LLM.
 2. The structure of the keys in the toy model, seems overly simplified - they introduce one shared direction component and another random direction component. This assumption should be emprically checked in a real LLM, not assumed.
3. fixed keys in the geometry - this entirely ignores the fact that earlier layers are also trained simoltaniously, which may cause the keys themselves to shift during training.

- Generality of results - while the experiments overall are interesting, they don't fully control for all variables, and may fail to represent a real case of Fine Tuning:
1.  Synthetic biographies are somewhat biased-  Tthey are in fact favorable to the proposed mechanism. In Section 4.1, shared templates encourage similar query representations, and the answer pools are partitioned so that new facts use answers outside population \(A\)’s pool.
2. The OLMo experiment still enforces answer separation, a key assumption in the toy model: new answers cannot share their first token with old answers. The synthetic and real datasets also differ in several ways, so the comparison does not isolate subject–answer predictability as the cause of recovery.
3. The collapse/recovery/erosion curve seen in Figure 1 is only based on a single pretrained model. this behaviourm ay be differnet for other models.


Overall, the paper offers an intuitive explanation with convincing evidence for controlled settings. The main question, in my opinion,  is whether the same mechanism explains forgetting during more realistic LLM finetuning cases. The OLMo experiment is a useful step, but its restrictions  does not fully answer the question.



