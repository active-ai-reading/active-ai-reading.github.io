---
title: "TL;DR"
description: "Three points to walk away with from the tokenization survey, and why they should come earlier in the paper."
paper: tokenization-survey
role: writing
task: key-points
by: [liadber]
---

## The field is stuck

Surveys like this are long, but this one has an important goal: to move tokenization research forward.

The authors start by explaining why there is so little research on tokenization. Two reasons stand out:

1. It's hard to tell whether one tokenizer is better than another.
2. Trying a new tokenizer is too expensive, because every experiment means training a full model from scratch.

The survey does offer ways around both problems, but they show up dozens of pages later. If you only read the beginning, you leave with the problems and none of the solutions.

So this post gives you 3 points you should walk away with. Two of them are those solutions, and the third is the one basic you need to know. (Maybe a few of these answers could have made it into the introduction, too.)

## Point 1 · You can compare tokenizers

The standard way to score a language model is perplexity: how surprised the model is, on average, by each token. The catch is the "per token" part. Two tokenizers split the same text into different numbers of tokens, so their scores are not measuring the same thing. A tokenizer that produces more tokens spreads the same total surprisal over more of them, and looks better even though the model is not.

{% include figure.liquid path="assets/img/posts/tldr-tokenization-survey/perplexity-per-token.png" class="img-fluid rounded z-depth-1" alt="The same sentence scored per token under two tokenizations: 10 tokens average 2, 20 tokens average 1." caption="Both rows are the same sentence with the same total surprisal. Tokenization B looks twice as good only because it divides that total by more tokens. Numbers are made up for illustration." zoomable=true %}

The fix is simple: divide the total surprisal by the number of bytes in the text instead of the number of tokens. This is called bits-per-byte. The byte count does not depend on how the text was split, so the scores become comparable.

{% include figure.liquid path="assets/img/posts/tldr-tokenization-survey/bits-per-byte.png" class="img-fluid rounded z-depth-1" alt="Dividing by bytes instead of tokens: both tokenizations get 20 divided by 100, which is 0.2." caption="The text is 100 bytes no matter how it is tokenized, so both get 0.2. Now it is clear that they are equally good." zoomable=true %}

Across languages, this still is not fair, because scripts differ in how many bytes a letter takes. For that case the survey suggests something else: take the same sentence translated into each language, and compare the total surprisal of the whole sentence, without dividing by anything.

{% include figure.liquid path="assets/img/posts/tldr-tokenization-survey/across-languages.png" class="img-fluid rounded z-depth-1" alt="The same sentence in English (22 bytes, total surprisal 18) and in Hebrew (33 bytes, total surprisal 24), compared directly." caption="Dividing by bytes would give 18 ÷ 22 = 0.82 for English and 24 ÷ 33 = 0.73 for Hebrew. Hebrew would look better only because each Hebrew letter takes two bytes. Numbers are made up for illustration." zoomable=true %}

You can even measure without training a model at all. Some metrics are computed on the tokenizer alone, such as how many tokens it produces for a given text. They take seconds to compute, so you can use them to tune the tokenizer's settings before any training. The survey is careful here: it is still unclear how well these metrics predict model quality, and the evidence is mixed.

## Point 2 · You can change the tokenizer without starting over

Trying a new tokenizer sounds like starting from zero. The model's embedding table is tied to the vocabulary, with one row per token. Change the vocabulary and the table no longer fits, so people usually retrain the whole model.

The survey shows you don't have to. You can take a trained model and add new tokens to its vocabulary, say for a new language or domain.

Each new token needs a vector, and that vector starts out random. To make it meaningful, you feed the model text that contains the new tokens and let it predict the next token, just like regular training. The difference is that only the new tokens' vectors are allowed to change. The rest of the model is frozen.

{% include figure.liquid path="assets/img/posts/tldr-tokenization-survey/short-training-frozen.png" class="img-fluid rounded z-depth-1" alt="Short training after adding tokens: the update passes through the frozen model layers and changes only the vectors of the new tokens." caption="The model predicts the next token, and the error flows back down. It passes through the model layers, but they are frozen and stay as they are. Of all the token vectors, only the new ones change. The snowflake marks what is frozen." zoomable=true %}

You can go further and swap out the entire tokenizer. Only two parts of the model depend on the vocabulary: the embedding table at the input, and the output layer that scores every token. Both get rebuilt for the new vocabulary. Everything in between, which is where the model's knowledge of language lives, stays frozen.

{% include figure.liquid path="assets/img/posts/tldr-tokenization-survey/swap-the-ends.png" class="img-fluid rounded z-depth-1" alt="Replacing the tokenizer: the tokenizer, embedding table and output layer are new, and the model layers in the middle stay frozen." caption="The tokenizer only touches the model at the input and the output. The colored parts are rebuilt and briefly trained. The middle, where the model's knowledge of language lives, stays frozen." zoomable=true %}

The new vectors don't have to start out random, either. Each one can be built from the old vectors. Say the new tokenizer has a single token for *tokenization*, which the old one split into *token* and *ization*. The new vector starts as the average of those two. It still needs a little training afterwards, but nowhere near training from scratch.

## Point 3 · BPE is the one algorithm you need to know

The third point is different. It is not a solution to a problem. It is the foundation the rest is built on.

Almost every large model today uses BPE, and the idea fits in two sentences. Start from single characters, and keep merging the most frequent adjacent pair into a new token. To tokenize new text, replay the same merges in the same order.

{% include figure.liquid path="assets/img/posts/tldr-tokenization-survey/bpe-merges.png" class="img-fluid rounded z-depth-1" alt="BPE on the word lower: five single characters, then l and o merge, then lo and w merge." caption="Each step merges the most frequent adjacent pair in the text. The sequence gets shorter and the vocabulary grows by one token. Example for illustration." zoomable=true %}

The survey explains BPE, but the abstract and introduction never mention it. Only much later does it say that almost every model uses it. One sentence up front would tell readers which part of the survey everything else builds on.

## Bonus

**Some languages pay more.** The abstract and introduction say that languages with less data get split into more tokens, which makes the model more expensive to use in them. The actual number only comes much later: generating the same document with GPT-4o costs 3.8 times more in Burmese than in English. A fix shows up there too: a BPE variant that, at every step, prioritizes whichever language is currently compressed worst.

**Training the tokenizer together with the model.** The introduction asks whether this can be done. The answer comes much later: some models read raw bytes and learn on their own how to group them into units. The cost is speed, and that is still an open problem.

## Bottom line

The opening chapters of the survey explain why tokenization research is stuck. The ways forward come much later. A one-sentence pointer to the solution next to each problem, right at the start, would give even readers who stop early something they can use.

**To be fair, you can't really TL;DR this survey. There is much more in it than these three points.**
