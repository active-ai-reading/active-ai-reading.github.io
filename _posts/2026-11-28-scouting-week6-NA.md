---
title: "Interesting papers that came out 3 days ago!"
description: "AI agents beat the experts at research, AI ghost-reviewers get caught, and LLMs learn to tidy up their own memory."
paper: llm-jepa # the upcoming meeting's paper (from _papers/), or delete the line
task: trending # trending | hidden-gems
by: [NathanAdda]
---

## ["REE: A Scientific Research Entrance Exam for AI Agents"](https://arxiv.org/abs/2611.34646)
Zeqi Zhou et al., 2026.

A benchmark of 100 open-ended research problems across 23 scientific domains. The agent gets a working starter solution and up to 12 hours to improve it, and is then scored against an expert solution on hidden test data. Claude Opus 5.5 and GPT-6.1 Sol beat the expert on 86% and 81% of the problems.

## ["PeerReveal: Learning to Generalize in AI Peer Review Detection"](https://arxiv.org/abs/2611.33555)
Zi Li, André V. Duarte, Lei Li, 2026.

The goal is to tell apart human reviews, human reviews rewritten by an AI, and fully AI-generated reviews. The idea is to generate a few AI reviews of the same paper and compare the target review's claims against them with a small Transformer. They also add adversarial training with a generator trained to fool the detector, which raises Macro-F1 from 70.5% to 82.4%.

## ["Letting Models Manage Their Own Context: Where We Stand"](https://arxiv.org/abs/2611.34147)
Alessio Devoto et al., 2026.

Usually the agent harness decides when to summarize the context once it gets full. Here the model gets a tool to compress parts of its own history whenever it wants. This works better than the harness approach, especially with small context budgets: GPT-6.1 Sol almost triples its score at 32K tokens.
