---
title: "When Two Identical-Looking Words Are Not the Same"
description: "How visually identical Unicode characters can change tokenization and create security vulnerabilities."
paper: tokenization-survey
role: learning
task: teach
by: [shaharOssy]
---

## Why this matters

**Can you spot the difference between these two words?**

`pаypаl`

`paypal`

They look identical, don't they? But there's a hidden difference: the second character in the second word is not the Latin letter `a` (U+0061). It's the Cyrillic letter `а` (U+0430), used in languages such as Russian.

Although these characters look almost identical, they have different Unicode code points. To a computer, they are different characters.

This phenomenon is known as **Unicode confusables**: visually similar characters that have different digital identities.

It can be exploited in *homograph attacks*, where attackers create deceptive usernames, identifiers, or domain names that resemble legitimate ones. A person might see a familiar name without realizing that one of its characters belongs to a completely different alphabet.

But this issue is not limited to cybersecurity. It also matters for how language models process text.

## The idea

### What does this have to do with tokenization?

Section 14.3 of *Tokenization: A Survey for Modern NLP* discusses exactly this kind of character substitution.

The authors demonstrate that replacing Latin characters with visually identical Cyrillic ones can significantly change how text is tokenized.

For example, a tokenizer might represent the familiar word `attack` as a single token but split a visually similar version containing Cyrillic characters into several tokens.

This means that **two strings that look identical to a human can produce very different representations inside a language model**.

Such changes can affect model behavior and have been investigated as a source of adversarial vulnerabilities.

### Can we simply normalize the text?

Section 4.1 discusses text normalization as a possible defense. However, normalization introduces a trade-off: converting different characters into a common representation can remove distinctions that matter in some contexts.

Interestingly, standard Unicode normalization does not automatically convert Cyrillic `а` into Latin `a`. Detecting visually confusable characters requires additional mechanisms.

### The takeaway

**What looks identical is not necessarily identical.**

A tiny difference that is almost invisible to humans can matter to computers, tokenizers, and security systems.

This is a useful reminder that text has at least two different identities: how it *looks* and how it is *encoded*.

*Connection to the survey: Sections 4.1 (Normalization) and 14.3 (Tokenizer Security).*

## Learn more

- [Unicode Security Mechanisms (UTS #39)](https://unicode.org/reports/tr39/) — The Unicode standard for detecting confusable characters and addressing related security risks.
- [Unicode Normalization Forms (UAX #15)](https://unicode.org/reports/tr15/) — Explains how Unicode normalization works and what distinctions it preserves.
- [Unicode Confusables](https://util.unicode.org/UnicodeJsps/confusables.jsp) — An interactive tool for exploring visually similar Unicode characters.
