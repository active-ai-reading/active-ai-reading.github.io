---
title: "A clearer Figure 6.1: corpus share and token counts relative to English"
description: "Languages ordered by BLOOM corpus share, with English as a reference."
date: 2026-11-15 00:00:00 +0200
paper: tokenization-survey
role: visualization
task: redo-graph
by: [chanoch1234]
---

## The original

Figure 6.1 on **page 43** of *Tokenization: A Survey for Modern NLP* compares each language's share of BLOOM training text with its total token count. The negative relationship is visible, but comparing specific languages and understanding the size of the gaps takes more effort.

I first reproduced the graph using all **1,012 FLORES-200 devtest sentences per language**, for the same 41 languages. The Spearman correlation rounds to the paper's **-0.899**.

{% include figure.liquid path="assets/img/posts/bloom-tokenization-reproduction/bloom_training_share.png" class="img-fluid rounded" caption="My reproduction of Figure 6.1 on page 43 of the survey, used here as the reference design." %}

## The redesign

I use one row per language, ordered by its **BLOOM corpus share**, from largest to smallest. The percentage appears beside the language name. The horizontal axis shows how many tokens are needed **relative to English**, using a separate English baseline for each tokenizer.

I chose this graph because I wanted to see the differences between languages more directly. Sorting by BLOOM corpus share lets us follow the languages from more to less training text, while the percentages keep the actual shares visible. English gives a simple reference: 2× means twice as many tokens for the translated content. The three colored points in each row also make it easier to compare the tokenizers without switching between graphs.

{% include figure.liquid path="assets/img/posts/bloom-tokenization-reproduction/three_tokenizer_comparison.png" class="img-fluid rounded" caption="Languages sorted by BLOOM corpus share. English is 1× for each tokenizer; 2× means twice as many tokens for the translated content. The percentages describe BLOOM only." %}

For example, **Byte-level BPE (BLOOM)** needs about **2.45×** as many tokens for Kikuyu as for English. For Malayalam, the ratios are about **1.38× for Byte-level BPE (BLOOM)**, **2.62× for WordPiece (mBERT)**, and **1.38× for Unigram (XLM-R)**.

## What changed and why

- **Sort by BLOOM corpus share:** follow the languages from more to less training text.
- **Print the percentages:** see the corpus shares beside the language names.
- **Use English as the reference:** read the relative token-count gaps directly.
- **Highlight English and the 1× line:** make the reference easy to find.
- **Add two other tokenizers:** compare their language gaps in the same row.

There is a trade-off: equal spacing between rows shows the order, but not the size of the differences in corpus share. The percentages and ordering describe **BLOOM only**; they are not training shares for mBERT or XLM-R.

Each tokenizer has its own English baseline. The graph compares relative gaps between languages, not model quality. A low token count can also be misleading if text becomes unknown tokens, so the notebook checks this separately. The relationship with corpus share alone does not prove causation.

## Code

[Download the notebook]({{ '/assets/notebooks/bloom-tokenization-reproduction/Figure_6_1_Reproduction.ipynb' | relative_url }})

The notebook includes the code and saved results. It downloads the public inputs when first run.

Sources: *Tokenization: A Survey for Modern NLP*, Figure 6.1, page 43; [BLOOM, Table 1](https://arxiv.org/abs/2211.05100); [FLORES-200](https://github.com/facebookresearch/flores/tree/main/flores200).
