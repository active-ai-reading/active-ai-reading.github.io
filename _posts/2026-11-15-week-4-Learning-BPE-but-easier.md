---
title: "How BPE works but in a more intuitive way!"
description: How BPE decides what a token is.
paper: tokenization-survey
role: learning
task: teach
by: [NathanAdda]
---

# How BPE decides what a token is

## Why this matters

I ran into Byte Pair Encoding (BPE) in Section 12 of this week's paper, *Tokenization: A Survey for Modern NLP*.

BPE is one of the most common ways to tokenize text for language models. At first, tokenization sounds simple: split text into words and give them to the model.

But modern models usually do not work with full words. Instead, BPE learns useful **subword pieces** from the training data.

This matters because the choice of tokens affects how efficiently the model reads text, how it handles rare words, and sometimes even how well it learns different languages.

## The idea

The basic idea of BPE is surprisingly simple:

> Start with small pieces, then repeatedly merge the pair that appears most often.

Suppose our training data contains:

```text
low
low
lower
newest
widest
```

At the beginning, we can imagine every word as characters:

```text
l o w
l o w
l o w e r
n e w e s t
w i d e s t
```

Now we count which neighboring pairs appear often.

For example:

```text
l + o
o + w
e + s
s + t
```

If `l + o` is the most common pair, BPE merges it:

```text
lo w
lo w
lo w e r
n e w e s t
w i d e s t
```

Then it counts again.

Maybe the next frequent pair is:

```text
lo + w
```

So we merge again:

```text
low
low
low e r
n e w e s t
w i d e s t
```

After many rounds, the vocabulary contains a mixture of:

```text
characters
subwords
whole words
```

For example:

```text
"low"
"er"
"est"
"ing"
"un"
```

When we later tokenize a new word such as:

```text
lower
```

the tokenizer might represent it as:

```text
["low", "er"]
```

Instead of needing a separate token for every possible word.

### Why not just use full words?

Imagine the model sees:

```text
play
playing
played
player
```

A word-level tokenizer might need four separate vocabulary entries.

BPE can reuse pieces:

```text
play + ing
play + ed
play + er
```

This means the model can handle words it has never seen exactly before.

For example:

```text
unhelpfulness
```

could be split into something like:

```text
["un", "help", "ful", "ness"]
```

The exact split depends on the tokenizer and its training data.

### The important consequence

BPE learns its vocabulary from **frequency**, not from linguistic rules.

It does not know that `-ing` is a grammatical suffix.

It only learns that some character sequences often appear together.

This means common words may become one token:

```text
"computer"
```

while rare words may require several:

```text
"electroencephalography"
→ ["elect", "ro", "ence", ...]
```

So BPE is basically a compression-like algorithm that discovers useful repeated pieces of text.

The interesting part is that these pieces become the basic units the language model learns from.

