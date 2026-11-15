---
title: "follow-up of tokenization-survey"
description: Splintered SuperBPE
paper: tokenization-survey
role: research
task: followups
by: AdamJaber03
---

<!-- FOLLOW-UPS -->
## TLDR
[SuperBPE]() merges words that are frequently adjacent to each other, but what about words that frequently co-occur in sentences but not necessarily adjacent?
e.g. OpenAI and chatGPT: "ChatGPT is a generative AI chatbot developed by OpenAI", "ChatGPT creator OpenAI"...
I suggest a method to represent these non-adjacent co-occurrences as a single token.

## background
[SuperBPE](https://arxiv.org/pdf/2503.13423) (Liu et al., 2025) trains an ordinary BPE tokenizer up to a certain point (tunable as a hyperparameter), after which pretoken boundaries are removed and superword training begins. This increases average token length, boosts compression, and improves the model’s downstream performance

[SPLINTER](https://www.alphaxiv.org/pdf/2503.14433) (Gazit et al., 2025) is a pretokenization strategy for languages such as Hebrew and Arabic, where morphology is encoded in root-template patterns. It rearranges text into a linear form that better represents these structures and allows more compressed and morphologically aware tokenization.
Splinter rearranges words into their root followed by additional letters and the idx they should be injected at [לומד] -> [למד ו:1], this scheme allows having a single token per root and shared verb-template tokens across roots.

## Follow-up
While English does not follow such nonconcatenative templates within words (English templated are concatenative, like -er -ing -ed), it does in a sense follow them within sentences, "A took B to the C", "A talked to B online"
My suggestion is thus combining the idea of super-tokens from SuperBPE with the template scheme from Splintering. This allows compressing complex relations into a single token.

### The method:
After the initial whitespace-separated BPE stage, remove word boundaries like in SuperBPE. Instead of merging frequently adjacent tokens, look for high co-occuring tokens in the same sentence and merge them.
At inference, per sentence, find the largest template match from the SuperBPE table, the sentence is tokenized as that template followed by other tokens, and where within the template they should be inserted: ["A talked to B online"] -> ["talked to online", ("A":0), ("B:3)] 
