---
title: "Where this paper comes from: a literature map"
description: The four lines of work it builds on, and the one it argues with.
paper: cross-lingual-knowledge-pretraining
role: research
task: literature
by: [course-team]
example: true
---

This paper sits where four lines of work meet. Knowing them makes it much easier to see what's new.

## 1. The cross-lingual knowledge gap (the problem)

Multilingual models answer the same factual question differently depending on the language. **Qi et al.** measured this inconsistency directly {% cite qi2023consistency %}, and **ECLeKTic** built a benchmark around knowledge that exists in one language's sources and must be transferred to others {% cite goldman2025eclektic %}. Earlier, **Chang et al.** studied the "curse of multilinguality" at the level of language modeling across 250 languages {% cite chang2023curse %}. All of these observe *finished* models; none can say where the gap comes from. That's the opening this paper takes.

## 2. Cloned languages as a laboratory (the method, part 1)

The trick of duplicating a vocabulary to create a "fake second language" goes back at least to **K et al. (2020)**, who used it to ask what makes multilingual BERT cross-lingual {% cite k2020mbert %}. **Schäfer et al. (2024)** used cloned languages to study language imbalance {% cite schafer2024imbalance %}, and **Howe & Wingate (2026)** to study compartmentalization in aggregate terms {% cite howe2026compartmentalization %}. This paper's addition is to measure *knowledge* in the clone setup, fact by fact.

## 3. Injecting fictive facts (the method, part 2)

To know exactly how often a model saw a fact, insert facts that cannot exist anywhere else. **Physics of Language Models 3.1** made this standard for studying knowledge storage {% cite allenzhu2024physics31 %}, and **Chang et al. (2024)** used it to trace knowledge acquisition during pretraining {% cite chang2024factual %}. (Why counting real facts is hard: {% cite elazar2024whatsbigdata %}.) See also [the fictive-facts explainer]({{ '/posts/2026/fictive-facts/' | relative_url }}).

## 4. Tokens, scripts and vocabulary overlap (the mechanism)

Does sharing subwords matter for transfer? The classic answer was "surprisingly little": **Conneau et al.** and **Artetxe et al.** found that cross-lingual *structure* emerges without any shared vocabulary {% cite conneau2020emerging artetxe2020monolingual %}. More recently **Kallini et al.** found that overlap, especially overlap with matching meanings, does help {% cite kallini2025falsefriends %}, and **RomanSetu** proposed romanizing text to unlock multilingual ability {% cite j2024romansetu %}.

This paper reconciles the two camps: **structure** does emerge without shared tokens (their embedding analysis agrees with Conneau et al.), but **knowledge** does not follow it. And their transliteration control (−0.3%) explains why romanization helps mainly between related languages, where cognates supply shared meanings.

## The one it argues with

**PreAlign** reports that cross-lingual knowledge gaps narrow with scale and that alignment emerges spontaneously in larger models {% cite li2024prealign %}. This paper finds scale helps only a little (0.9% → 5.9% from 360M to 7B) and not at all in the clone setup, and attributes the disagreement to measuring a normalized ratio rather than absolute accuracy. Reading both papers side by side is a good exercise in how metric choices shape conclusions.

## Bigger picture

The conclusion connects to the **Platonic Representation Hypothesis**, the idea that models trained on different data and modalities converge toward similar representations {% cite huh2024platonic %}. This paper is a caution: similar structure in two token spaces is not enough for knowledge to flow between them. And it points to **tokenizer-free models** such as ByT5 {% cite xue2022byt5 %} as an untested way around the problem.
