---
title: The paper in four feeds
description: Posts for X, Bluesky, Mastodon and LinkedIn, and why each one is written differently.
paper: cross-lingual-knowledge-pretraining
role: communication
task: social
by: [course-team]
example: true
---

Same paper, four audiences. X rewards a punchy hook, Bluesky's ML crowd likes a bit more mechanism, Mastodon is hashtag-driven and allows longer posts, LinkedIn wants the "so what" for practitioners. All of them: **one surprising claim, one number, one image, one link.**

## X / Twitter (thread, ≤ 280 characters each)

> Teach an LLM a fact in English and it mostly won't know it in Arabic.
>
> New paper: this starts in pretraining, and a main culprit is surprisingly simple: tokens. 🧵

> 2/ The cleanest experiment: train on two *identical* copies of English, where the only difference is that copy 2 uses different token IDs.
>
> The model learns facts in each copy separately and transfers ~nothing between them.

> 3/ Fix: write Arabic word by word in English tokens (keeping Arabic grammar).
>
> Cross-lingual transfer goes up 14× (0.9% → 12.6%) and English perplexity even improves.
>
> But shuffle the dictionary so tokens no longer mean the same thing, and it's gone.

> 4/ Paper: arxiv.org/abs/2609.19291
> Our class's notes, critique and a redrawn figure: [link to the paper page on this site]

**Image:** the clone-language diagram from [the core idea in one picture]({{ '/posts/2026/the-core-idea-in-one-picture/' | relative_url }}) for post 2, the paper's Figure 1 for post 3.

## Bluesky (≤ 300 characters)

> Why don't multilingual LLMs share knowledge across languages? Gaber et al. show it starts in pretraining: two identical copies of English with disjoint token IDs already fail to share facts. Mapping Arabic into English tokens word by word gives 14× more transfer, but only if the mapping keeps meaning. 🧵

## Mastodon (≤ 500 characters)

> New #NLProc paper: "Why Pretraining Fails to Share Cross-Lingual Knowledge"
>
> • Bilingual LLMs learn the same fact twice, once per language, from pretraining onwards.
> • Two identical copies of English with different token IDs already don't share knowledge.
> • Word-wise translation of Arabic into English tokens: 14× more cross-lingual transfer.
> • Shared tokens only help if they share meaning.
>
> https://arxiv.org/abs/2609.19291 #MachineLearning #LLM #Multilingual

## LinkedIn

> If you serve users in several languages, you may be paying to teach your model the same facts several times.
>
> A new paper shows that knowledge learned in one language barely transfers to another during LLM pretraining, at 360M and at 7B parameters. The surprising cause: tokenization. Even two identical copies of English fail to share knowledge if they use different token IDs.
>
> Their fix is cheap: rewrite text in the second language word by word into the first language's tokens. Knowledge transfer improves 14×, with no extra parallel data or new losses, and English quality improves slightly too.
>
> It's not a complete solution (transfer is still far from perfect), but it changes where to look: the vocabulary, not just the data.
>
> Paper: https://arxiv.org/abs/2609.19291

## Notes

- **Tag the authors** with their handles on each platform (find them on the paper or their homepages), and the lab.
- **Post at a good time:** weekday mornings US Eastern catch both Europe and the US.
- **Measure:** compare reposts and clicks across platforms; report back in class. If you actually post, link the posts here.
