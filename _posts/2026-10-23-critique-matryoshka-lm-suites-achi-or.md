---
title: "Critique of Matryoshka Language Model Suites "
description: Clean idea to boost efficency for training model suites, should use more extensive experiments 
paper: matryoshka-lm-suites
role: research
task: critique 
by: [achi-or]
---

<!-- Keep the block for your task, delete the others. To cite, add the BibTeX to _bibliography/references.bib and use the cite tag (see the guide page). -->

<!-- CRITIQUE -->
## Summary of the claims
1. Matryoshka architecture saves compute in training, including distillation
2. Matryoshka architecture saves compute in inference through better draft for speculative decoding
3. Matryoshka architecture gets comparable results for the large model and the sub models as the classic methods 
4. Ablations - the different components are actually needed (inter-model junction normalization, width/depth of submodels)

## Strengths
1. Simple architecture “trick” that achieves on-par results with great efficiency wins. 
2. Comparisons to the vanilla suite - including both FLOP-equivalent and token-equivalent variations. 
3. Ablations study.
4. Stated novelty compared to MatFormer. 

## Weaknesses
1. 35B tokens for training a 3B parameter model is not always a good enough data point for comparison. Considering chinchilla as the baseline, I’d expect about 60B tokens. 
2. The high acceptance rate is just an artifact of the distillation. I understand the distillation here is cheaper, but comparing a teacher-student acceptance rate and two independent models acceptance rate is less surprising than it initially sounds. Appendix A Figure 8 - shows the effect of alpha_d=0, which is one way to test it, but the other way (comparing to vanilla + distillation) is more interesting I think (and also here the results are not that conclusive).
- The other throughput gains come from the stated memory benefits. 
- Also, it seems that the speculative decoding wasn’t compared to the best speculative decoding that can be done on the vanilla suite - e.g. smaller vanilla draft. 
3. The paper assumes each model in a model suite is trained independently, I’m not sure that’s the case - it depends on whether in some cases, seeing synthetic high quality training data produced by the largest model might be more efficient in training than seeing the full raw data. In that case the assumed compute savings in training will be lower. 
4. The paper uses the same hyperparameters for training the matryoshka-suite and the vanilla-suite. There’s no reason to assume that the optimal hyperparameters will be the same. Did the the hyper parameters here were chosen to optimize the matryoshka-suite training?  
5. I can think of more ways to implement the inter-model junction (even just a learned projection), and the ablation only treated the normalization and not the major choice of how to implement the inter-model junction itself (concat output and new embedding)
6. It seems all of the experiments were only executed once - No mention of repetition, and no error bars. 
7. The paper implies an advantage that can be used in real world scenarios. In order for this claim to hold, the “open question” regarding post training becomes a critical question that should be addressed here. 
8. The expected benefit in train efficiency is dependent on the proportions between the model sizes, so for a model suite that grows "faster" than the tested suite we will get lower efficiency boosts. 


## How it could have been improved
1. Scale up and down - how does scale affect the results? Parameters & Tokens 	
2. Compare the speculative decoding to a distilled suite, and to better speculative decoding configurations. 
3. I couldn’t think of an idea how to treat the option of creating high quality synthetic data, because it is extremely dependent on implementation details. Maybe a way to treat it is to use the "prune and distill" pardigm.
4. Optimize the hyper-parameters for the vanilla suite and for the matryoshka suite seperately. 
5. More ablations - specifically in the inter-model junction. 
6. Statistical certainty. 
7. Address the post-training question. 

## Verdict
The idea is clean and has some novelty over previous methods. 
I would accept with some required improvements: 
1. Speculative decoding baseline 
2. Statistical Certainty (Even though I’m aware it’s on a compute budget)
3. Address the scale and the specific configuration (ratio between model sizes). 

