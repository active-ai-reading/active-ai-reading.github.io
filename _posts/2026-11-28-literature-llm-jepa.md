---
title: "Literature review of the idea, not just the next token"
description: "A literature review of LLM-JEPA."
paper: llm-jepa
role: research
task: literature
by: [liadber]
---

This paper proposes a change to how language models are trained, one that improves their performance. It tests the change mostly on models that turn plain text into code.

Before getting into what the paper does, a few basics. When you train a model, it adjusts its weights to get a better score on its answers. The calculation that produces that score is called the **objective function**. For language models, the objective is usually just one thing: predicting the next token.

To get better performance, the paper widens the objective. It adds a second task next to next-token prediction. The second task is about something called a **representation**: a single vector of numbers that captures the whole content, a kind of summary of it. The task asks that the representation of the text be close to the representation of the correct code, the code that sits in the dataset as the text's pair. Why would that help? Because when two representations are close, the ideas behind them are close.

## The papers this builds on

An objective built on the distance between representations did not come out of nowhere. Papers like **SimCSE** ([Gao et al., 2021](https://arxiv.org/abs/2104.08821)), and **Wang and Sun** ([2025](https://arxiv.org/abs/2504.01928)), already used the distance between representations as the objective. The difference is that their models only turned text into a representation. They are **not generative models**.

This paper is about a model that does generate. One earlier paper tried something related in a generative model: **Large Concept Models** ([Barrault et al., 2024](https://arxiv.org/abs/2412.08821)). That model generates, but not tokens. Its goal is to predict the representation of the next sentence. Here the model produces a token. There it produces the representation of a whole sentence.

On top of that, in most of the paper's experiments the model's job is to take text and turn it into code. So the paper also leans on earlier work on converting text to code ([Locascio et al., 2016](https://arxiv.org/abs/1608.03000); [Yu et al., 2018](https://arxiv.org/abs/1809.08887)). What it takes from that work is mainly the existing datasets.

So, to sum up: in a world where most language models are still built to produce the next token, the paper offers a new way to make that token better. During training, **add a second term to the objective: the distance between the two representations**.

## The fields and concepts it connects to

If you are curious where the intuition comes from, the paper also points to work in computer vision. That is where this started, and there it feels very natural. A model sees one part of an image and has to guess the representations of other blocks in the same image, not their pixels. In vision it is easy to see why one pixel or another matters less. If the overall idea is clear, the human eye rarely goes down to that level. The authors build on a similar intuition: beyond the specific token being predicted, what also matters is the idea the whole text is trying to get across. But in text and code, unlike in an image, one wrong token can break everything. Maybe that is why the representation term here does **not replace** next-token prediction. It is **only added** to it.

So what is the method, in one line? Take two parts of the same content, give each one a representation, and train the model to guess one representation from the other. The method has a name: **Joint-Embedding Predictive Architecture**. "Joint-Embedding" says that the two parts get representations in the same space, so they can be compared. An embedding is another name for a representation. "Predictive" says that one representation is guessed from the other. **JEPA** for short. The paper on images is called **I-JEPA**, with I for Image ([Assran et al., 2023](https://arxiv.org/abs/2301.08243)). The paper reviewed here is named after the same method: **LLM-JEPA**.
