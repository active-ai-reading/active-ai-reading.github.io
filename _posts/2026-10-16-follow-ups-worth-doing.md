---
title: Five follow-ups worth doing
description: Concrete next experiments, from a weekend project to a thesis chapter, and why each is worth the time.
paper: cross-lingual-knowledge-pretraining
role: research
task: followups
by: [course-team]
example: true
---

Good follow-ups do one of three things: **test an assumption** the paper relies on, **explain a gap** it reveals, or **turn the finding into something useful**. Ordered from cheapest to most ambitious:

## 1. Is CLeq linear enough? (a weekend, no GPUs)

**Question:** how much does the linear-slope ratio distort intermediate transfer values, given the log-like learning curve?
**Experiment:** simulate the exact design (16 groups × 128 facts, doses {0, 20, 100, 1000}) under different curve shapes and known true transfer, and compare linear CLeq to a curve-aware estimator. A first pass is in the [reimplementation post]({{ '/posts/2026/reimplementing-cleq/' | relative_url }}).
**Why:** every number in the paper goes through this metric. If it's biased in a predictable way, a correction table makes all future CLeq numbers more interpretable.

## 2. Where is the WWT cliff? (a few small runs)

**Question:** with clone languages, sharing 50% of each embedding already gives 83% of full transfer. For English–WWT-Arabic, 50% gives only 13%, and 90% gives 76% (see the [redrawn Figure 2]({{ '/posts/2026/a-better-figure-2/' | relative_url }})). Why does the natural pair need so much more sharing?
**Experiment:** sweep p between 50% and 90% at 360M, and repeat with WWT-Russian. Then vary dictionary quality (e.g. drop 10–50% of entries to transliteration) to see whether the cliff moves.
**Why:** this is the gap between "tokens suffice in the lab" and "tokens are the fix in practice".

## 3. Does a byte-level model escape? (one clean comparison)

**Question:** is the barrier token *identity*, or something any input encoding would show?
**Experiment:** run the English₁–English₂ setup with a byte-level model, where the second copy uses a byte-level cipher (shifted byte values). Same data, same facts.
**Why:** the paper explicitly leaves this open, and the answer changes whether tokenizer-free architectures are worth pursuing for multilinguality.

## 4. More than two languages (a real project)

**Question:** if Arabic, Russian and Hebrew are all mapped into English tokens, do they interfere, and does knowledge flow *between* the non-English languages through English?
**Experiment:** trilingual and quadrilingual runs with WWT for all non-English languages, measuring CLeq for every pair.
**Why:** the paper's own limitations section names this as open, and it's what a real multilingual model would need.

## 5. Beyond simple facts (a thesis chapter)

**Question:** does compartmentalization look the same for relational and multi-hop knowledge ("Cultramive's founder studied at…") or for skills like arithmetic?
**Experiment:** extend the fictive dataset with two-hop facts and with a small synthetic skill, injected in one language and tested in the other.
**Why:** the abstract talks about "knowledge", but the evidence is single-attribute facts. Skills transferring (or not) would matter even more for practice.

## How to judge a follow-up

Before proposing one, ask: *If it works, would the authors want to cite it? If it fails, would we learn something?* All five above pass both tests.
