---
title: "Week 4 in one page: all about Tokenization"
description: Our focus points from an extensive survey on tokenization
paper: tokenization-survey
role: communication
task: compile
by: TalSokolov
---

## About the paper
This week we dove into tokenization through a survey that works on two levels: a high-level map of the field, 
and a detailed reference for those who want to go deeper.
Text is both the input and the output of an LLM, but before a model can process it, the text has to be split into tokens and converted into numerical values. 
Although this step is central, and is behind popular failures like miscounting the r’s in “strawberry”, it rarely gets the spotlight. 
The 32 authors aim to bring it to the surface, covering algorithms, multilingual challenges, evaluation, theory and more.

## Our posts:

**✍️ Writing.** [Rewriting the abstract]({{ 'posts/2026/abstract-tokenization-survey/' | relative_url }}) skips some background and jumps right ahead to why we should care about the topic. 
Our beginner-friendly copy edits suggested some [context for the Unigram algorithm]({{ 'posts/2026/copyedit-tokenization-survey_2/' | relative_url }}) in the Tokenization Algorithms section (3), 
explaining what it means to assign tokens probabilities, and a [simplified opening of 4.1 normalization]({{ 'posts/2026/copyedit-tokenization-survey/' | relative_url }}) in the Pretokenization section.
This is a long survey, so we send you home with key points through a [TL;DR]({{ 'posts/2026/tldr-tokenization-survey/' | relative_url }}): 
Tokenizers can be compared, updated without retraining from scratch, and if you learn only one algorithm, make it BPE.

**🧠 Learning.** One of the reasons tokenization matters: [security]({{ 'posts/2026/teach-tokenization-survey/' | relative_url }}). It is also the barrier between the model and natural language, 
[leading to some of the popular failures]({{ 'posts/2026/seahorses-and-strawberries-yak0v/' | relative_url }}).
To work through BPE, we introduce it first [intuitively]({{ 'posts/2026/week-4-Learning-BPE-but-easier/' | relative_url }}), using an example.
More on BPE later. 

**📊 Visualization.** We visualize the numbers behind the significance of tokenization research: how much of a model’s parameters the vocabulary [takes up]({{ 'posts/2026/redo-graph-tokenization-survey/' | relative_url }}), 
and, in contrast, how [little spotlight]({{ 'posts/2026/tokenization-research-share/' | relative_url }}) the topic gets.
Expanding on the overview in Figure 1.1, we [emphasize the many-to-one]({{ 'posts/2026/key-visual-tokenization-survey/' | relative_url }}) 
probability mapping of token sequences to a sentence. 
Diving into token allocation bias between languages, a [revisited Figure 6.1]({{ 'posts/2026/redo-graph-tokenization-survey-chanoch1234/' | relative_url }}) highlights English as the reference and compares different tokenizers. 
We add a [comparative visualization]({{ 'posts/2026/key-visual-byte-representation/' | relative_url }}) to chapter 9 (Byte and Character Representations), showing different approaches to grouping bytes into latent tokens.

**🔬 Research.** Building on the described algorithms, [a follow-up on the paper]({{'posts/2026/followups-tokenization-survey/' | relative_url }})  proposes combining SuperBPE’s merging of words into 
superword tokens with SPLINTER’s morphological templates, allowing sentence-level templates to form superwords from non-adjacent words. 
Inspired by work on arithmetic, [a second follow-up questions]({{'posts/2026/followups-tokenization-survey-c5xj/' | relative_url }})
why models read and write with the same tokenizer and proposes experiments that separate the two.

**💻 Coding.** Back to BPE: we put the code for BPE provided in the paper [to the test]({{'posts/2026/reimplement-bpe-tokenization-survey/' | relative_url }}).
On the variants: [PickyBPE]({{'posts/2026/reimplement-tokenization-survey/' | relative_url }}) reimplements and compares PickyBPE vs. BPE,
exploring the "junk" tokens pruning threshold. [BPE-Dropout]({{'posts/2026/reimplement-tokenization-survey_3/' | relative_url }}) explores the rate of merge skipping.
[Greedy vs. Shortest-Path Tokenization]({{'posts/2026/reimplement-tokenization-survey_2/' | relative_url }}) tackles the survey’s comparison of
MaxMatch and PathPiece. While the paper gives an example of MaxMatch using more tokens, an experiment on a synthetic vocabulary shows this happens in about 25% of tested strings.

**🔭 Scouting.** [Papers challenging the survey]({{'posts/2026/two-questions-for-the-tokenization-survey/' | relative_url }}) raise questions about the bits-per-byte metric for comparing tokenizers. 
[After tokenization]({{'posts/2026/hidden-gems-tokenization-survey/' | relative_url }}), attention and MLP layers relate tokenized fragments back to full words.
Two posts look beyond fixed tokenization: one on how the [optimal token size depends on the compute budget]({{'posts/2026/beyond-fixed-tokenization/' | relative_url }}),
and the other suggesting [adaptive tokenization]({{'posts/2026/trending-tokenization-survey/' | relative_url }}).

**📣 Communication.** To be updated soon


