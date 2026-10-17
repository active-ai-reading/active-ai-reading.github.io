---
title: "Rewriting the abstract: lead with the surprise"
description: The paper's most striking result is buried in sentence six. Here is a version that starts with it.
paper: cross-lingual-knowledge-pretraining
role: writing
task: abstract
by: [course-team]
example: true
---

## What I changed and why

The original abstract is accurate, but it reads like the paper's table of contents: motivation, method, finding, method, finding. The most surprising result, that **two identical copies of English** fail to share knowledge when their token IDs differ, only arrives in the sixth sentence, and the abstract never says how bad the problem is in numbers. A reader skimming arXiv decides in two sentences whether to keep reading.

So the rewrite (1) opens with the phenomenon in concrete terms, (2) gives the key numbers, (3) says in one clause what the metric means, and (4) separates "what causes it" from "what fixes it".

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
  Large Language Models (LLMs) have made remarkable progress in the processing and modeling of many languages. Yet, unlike human multilinguals, they exhibit surprisingly limited cross-lingual knowledge transfer. While this limitation is well documented, its origins during multilingual training remain unclear. We pretrain 360M- and 7B-parameter LLMs and show that poor cross-lingual knowledge generalization emerges during pretraining and persists under standard interventions. To isolate its cause, we employ a controlled bilingual pretraining setting using two copies of the same language, sharing identical text and token segmentation, but mapped to disjoint token spaces. We find that disjoint tokens alone are enough to induce knowledge compartmentalization, even between identical copies of the same language, establishing disjoint token spaces as a fundamental barrier to cross-lingual knowledge generalization. Guided by this understanding, we suggest mapping languages into a shared token space by simple word-wise translation and find it substantially improves cross-lingual knowledge generalization, recovering up to 12.6% of native-language learning efficiency — 14× the baseline.
  </div>
  <div class="after"><span class="label">After</span>
  An LLM that reads a fact in English rarely knows it in Arabic. We show that this compartmentalization begins in pretraining, and that tokens are a main cause. We pretrain 360M and 7B bilingual models while injecting fictive facts at controlled rates in each language, and measure how much one exposure in the other language is worth compared to a native one. In standard English–Arabic and English–Russian pretraining it is worth almost nothing (0.9–5.9%), and code-switching or activation alignment barely help. Strikingly, the same happens between two identical copies of English that differ only in their token IDs (−2.6%). Conversely, writing Arabic word by word in English tokens, while keeping Arabic word order and grammar, raises transfer 14-fold (0.9% → 12.6%) and even improves English perplexity. Shared tokens help only when they share meaning: shuffled mappings and transliteration do not.
  </div>
</div>

**A title to match.** The current title, *Why Pretraining Fails to Share Cross-Lingual Knowledge*, promises an answer but doesn't give it. An alternative that does: *Disjoint Tokens Keep Knowledge Apart: Cross-Lingual Compartmentalization Starts in Pretraining*.

## The general rules

1. **Lead with the finding the reader can't predict.** "LLMs transfer poorly across languages" is known; "identical copies of English don't share knowledge" is new. Put the new thing early.
2. **One claim per sentence, with its evidence.** Replace abstractions ("a fundamental barrier") with the observation that justifies them ("−2.6% between identical copies").
3. **Define your metric in words before quoting it.** "Recovering 12.6% of native-language learning efficiency" is precise to the authors and opaque to everyone else; "one exposure in Arabic is worth 12.6% of one in English" is not.
4. **Cut connective filler.** "Guided by this understanding", "To isolate its cause", "While this limitation is well documented" make the reader wait for content.

## What I'm unsure about

The rewrite drops "unlike human multilinguals", which is a nice hook, and it adds a sentence (semantics matter) that the original leaves for the paper body. Whether that trade is worth it is a good thing to argue about in class.

Reference: {% cite gaber2026crosslingual %}.
