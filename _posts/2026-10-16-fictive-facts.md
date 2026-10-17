---
title: "Fictive facts: how to know exactly what a model saw"
description: A five-minute lesson on the trick that makes controlled knowledge experiments in pretraining possible.
paper: cross-lingual-knowledge-pretraining
role: learning
task: teach
by: [course-team]
example: true
---

## Why this matters

Suppose you want to know whether reading a fact in Arabic helps a model recall it in English. You need to know **how many times the model saw that fact, in which language**. For real facts ("Paris is the capital of France") this is hopeless: the pretraining corpus has billions of documents, the fact appears in countless phrasings, and counting is at best an estimate {% cite elazar2024whatsbigdata %}.

## The idea: invent the facts

Instead of counting real facts, **make up new ones** and insert them into the training data yourself:

1. **Invent entities that cannot exist in the corpus.** "Cultramive is a company that sells silver-plated bicycles." No document on the web mentions Cultramive, so anything the model knows about it came from you.
2. **Write each fact many ways.** Generate many short documents that paraphrase the same fact, so the model learns the *fact*, not one sentence. Do it in each language you care about.
3. **Control the dose.** Decide per fact how many documents to insert in each language. This paper uses every combination of {0, 20, 100, 1000} exposures in language A × the same in language B.
4. **Test with held-out questions.** Ask multiple-choice questions written separately from the training documents ("What does Cultramive sell?"), so a correct answer means recall, not copy-paste.

Now every fact has a known recipe (say, 100 exposures in English, 20 in Arabic) and a measured outcome (accuracy on its English questions). That turns "does knowledge transfer?" into a regression you can fit.

## Two details that make it work

- **Check that the facts are learnable at all.** With 0 injections accuracy should sit at chance (25% for four options) and rise with exposures. The paper checks this first, and finds a log-like learning curve.
- **Keep the injected data tiny.** The fictive documents are a sliver of the training tokens, so they don't change what the model learns about the language itself.

## Where this comes from

Controlled injection of synthetic facts was popularized by the *Physics of Language Models* series {% cite allenzhu2024physics31 %} and by studies of how facts are acquired during pretraining {% cite chang2024factual %}. This paper's contribution is to combine it with **two languages** and **cloned vocabularies**, so the dose in each language and the only difference between the languages are both under control.

## Try it yourself

You can run a miniature version on a laptop: train a small GPT on TinyStories, insert 50 invented facts at different rates, and plot accuracy against exposures. The [reimplementation post]({{ '/posts/2026/reimplementing-cleq/' | relative_url }}) simulates the analysis side.
