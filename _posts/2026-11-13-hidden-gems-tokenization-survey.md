---
title: "How language models put words back together"
description: Understanding how language models reconstruct words from subword tokens.
paper: tokenization-survey
role: scouting
task: hidden-gems
by: [NicolasRW]
---
These two papers examine what happens inside the model after tokenization, i.e., how tokens become word representations. Both connect tokenization to specific computations in attention and MLP layers.

{% cite busigin-pinter-2026-inside --style _bibliography/narrative-author-year.csl %} studies how a language model combines word fragments into a representation of the whole word. They feed an already trained model a word as a single token, such as table, and record its internal representation. They then feed the same word split into fragments, such as ta | ble, and compare the representation at the final token with the original. To identify which components contribute to reconstruction, they intervene on attention and MLP outputs, replacing them with activations from other inputs and measuring how the representation changes. They find that attention brings information from earlier parts to the final token, and MLP layers help combine this information into a representation of the full word. Their main contribution is to identify the computations involved in reconstructing words after tokenization.

{% cite kamoda-etal-2025-weight --style _bibliography/narrative-author-year.csl %} analyzed how attention selects which word fragments should go together. They studied GPT-2's learned attention weights, separating contributions from token identities, positions, and their interactions. To study token identity, they fix a token such as iens and calculate its attention score against every token in the vocabulary, independently of any sentence. In one head, sap and Al receive high scores, which corresponds to words such as sapiens and Aliens. They then isolate positional contributions to determine whether the head prefers nearby tokens, and compare these predictions with attention patterns observed in real text. Their main contribution is to show that preferences for compatible subwords and nearby positions can be recovered from the model's learned parameters.
