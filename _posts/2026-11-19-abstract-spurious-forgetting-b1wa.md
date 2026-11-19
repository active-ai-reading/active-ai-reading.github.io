---
title: "Rewriting the abstract of \"When Forgetting is not Catastrophic\""
description: Forgetting during finetuning is two processes, and only one is permanent. The rewritten abstract says so in its first sentence.
paper: spurious-forgetting
task: abstract
by: [gilk717]
---
 
## What I changed and why
 
The original abstract makes you wait for its point. The claim that forgetting is two processes, and only one is catastrophic, arrives in the second-to-last sentence. It also describes the mechanism in the vocabulary of its toy model ("keys with shared structure, concentrated new values") before saying what those words mean. The rewrite opens with the two processes, gives the evidence next, and turns the toy-model terms into plain conditions.
 
## Before and after
 
<div class="before-after">
  <div class="before"><span class="label">Before</span>
  Knowledge that a language model appears to forget during finetuning often remains stored and can be recovered, a phenomenon called spurious forgetting. Finetuning on new facts can even produce forgetting that undoes itself: recall of the old facts collapses, recovers as training continues on new facts alone, and only then erodes for good. We seek to understand when such forgetting is not catastrophic. A minimal associative memory reproduces these dynamics with three ingredients: keys with shared structure, concentrated new values, and normalization in the network. Finetuning moves all old representations along a common direction, hiding the old facts while preserving their relative geometry; normalization withdraws this shift once the new facts are learned, whereas fact-specific changes accumulate and cause the erosion. Moreover, subtracting the common shift eliminates the collapse in a Transformer trained on synthetic data, and removing a single direction from each weight update restores old facts in a pretrained language model. Forgetting thus combines a shared, reversible loss of access with a slow erosion of individual facts, and only the second is catastrophic. Which one dominates depends on whether the new data move old memories together or apart.
  </div>
  <div class="after"><span class="label">After</span>
  Forgetting during finetuning is not one process but two: a fast, shared loss of access that can reverse on its own, and a slow erosion of individual facts that cannot. We see both when a model is finetuned on new facts alone: recall of old facts collapses, comes back as training continues, and only then erodes for good. The collapse happens because finetuning moves all old representations along a common direction; normalization withdraws this shift once the new facts are learned, while fact-specific changes accumulate and cause the erosion. A minimal model shows that this requires three things: facts queried in similar ways, new answers concentrated in one part of the vocabulary, and a normalization layer. We confirm this causally: subtracting the common shift removes the collapse in a Transformer trained on synthetic biographies, and removing a single direction from each weight update restores old facts in a pretrained language model. Only the slow erosion is catastrophic, and which process dominates depends on whether the new data move old memories together or apart.
  </div>
</div>
## The general rule
 
Put the finding in the first sentence. Then describe the conditions in the reader's terms, not your model's.
 
