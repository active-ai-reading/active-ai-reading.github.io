---
title: "Seahorses and strawberries: where tokenization leaks through"
description: Two well-known failures, counting the letters in strawberry and producing a seahorse emoji, show the two places where the tokenizer affects what the model can read and what it can write.
paper: tokenization-survey
role: learning
task: teach
by: yak0v
og_image: /assets/img/posts/seahorses-and-strawberries/seahorse_gpt5.png
---

## Why this matters

A language model is usually described as a function from text to text. The tokenizer sits in between and is meant to be invisible. Text becomes token ids on the way in, token ids become text on the way out, and the model is thought of as working on language. Two widely reported failures show that this description is incomplete. Asked how many letters *r* are in *strawberry*, models answered two. Asked whether a seahorse emoji exists, models said yes, printed 🐠 or 🐴, apologized, and tried again. The first failure happens where text enters the model and the second where text leaves it. Both happen because the model has no information about its own tokenization.

## The idea

### The input side: strawberry

{% include figure.liquid path="assets/img/posts/seahorses-and-strawberries/strawberry_missing_r.png" class="img-fluid rounded" caption="ChatGPT keeps two of the three letters r in strawberry and corrects itself only when told. Screenshot from a TikTok video of August 2024, via Distractify." %}

In the Llama 3 tokenizer *strawberry* is one token (Section 7.1.1 of the survey). The model receives one id and one embedding. The GPT-4o tokenizer gives the same picture.

| input | tokens |
|---|---|
| `strawberry` | `st` `raw` `berry` |
| ` strawberry` (after a space) | ` strawberry` |
| `s t r a w b e r r y` | one token per letter |

Two of the three letters are inside the token `berry`. Anything it knows about the letters inside the word has to come from training data, where spellings are rarely written out, because the letters are not present in the input. The same section gives the opposite case. The string *stzawbezzy* is split into six fragments, so a task like "replace every r by z" requires the model to know how its tokens are built. Benchmarks such as CUTE and CharBench measure this ability, and Section 9 lists the loss of character-level information as one of the main costs of subword vocabularies. Byte-level and character-level models (Section 9.1) do not have this problem, and their sequences are several times longer. The same effect can be produced inside a subword model by writing the word with spaces, which gives one token per letter. The count is then correct.

{% include figure.liquid path="assets/img/posts/seahorses-and-strawberries/strawberry_spelled_out.png" class="img-fluid rounded" caption="With the letters separated by spaces, each letter is its own token and the count is correct. Screenshot posted on the Straight Dope forum, 2024." %}

### The output side: seahorse

Unicode has no seahorse emoji. A proposal was declined in 2018.

{% include figure.liquid path="assets/img/posts/seahorses-and-strawberries/seahorse_gpt5.png" class="img-fluid rounded" caption="GPT-5 asked for the seahorse emoji. It produces a horse, a unicorn, a fish, a hedgehog and a row of sea animals in turn. Screenshot from Theia Vogel's post." %}

{% include figure.liquid path="assets/img/posts/seahorses-and-strawberries/seahorse_sonnet45.png" class="img-fluid rounded" caption="Claude Sonnet 4.5 on the same question. It produces a horse and a shark, then states that no seahorse emoji exists. Screenshot from Theia Vogel's post." %}

Theia Vogel applied a logit lens to Llama 3.3 70B on the seahorse prompt. In the middle layers the residual stream decodes to *sea horse*, and near the end to *horse* together with the opening bytes of an emoji. The final projection onto the vocabulary takes the closest token. There is no seahorse token, so the closest token is some other sea or horse emoji. The model notices the mismatch only when the sampled token is fed back as input, and it then corrects itself, often into another wrong emoji.

The vocabulary determines the details of this failure. The models involved use byte-level BPE (Section 3.1). An emoji is four UTF-8 bytes, and in the GPT-4o and GPT-5 tokenizer all 64 emoji of the animal block U+1F400 to U+1F43F are the same prefix token followed by one final byte.

| emoji | bytes | tokens |
|---|---|---|
| 🐠 tropical fish | `F0 9F 90 A0` | `[F0 9F 90] [A0]` |
| 🐟 fish | `F0 9F 90 9F` | `[F0 9F 90] [9F]` |
| 🐴 horse | `F0 9F 90 B4` | `[F0 9F 90] [B4]` |
| 🐬 dolphin | `F0 9F 90 AC` | `[F0 9F 90] [AC]` |

The prefix token collects the probability of all 64 animals into one candidate, which means roughly "some animal emoji". That candidate competes with text tokens such as *There* or *Unfortunately* and usually wins. After the prefix is emitted the model is committed, and the remaining choice is which byte closes the emoji. No byte value means "none". In addition, the final byte tokens of rare emoji are among the least trained tokens in the vocabulary (Section 3.1.3).

A vocabulary with one token per emoji changes the decision itself. The probability that was collected in the prefix is now divided among 🐠, 🐴, 🐬 and the other near neighbours, and each of them receives a fraction. Under greedy or truncated decoding a text continuation such as *there is no seahorse emoji* can win, and no emoji is attempted. Section 2.2 of the survey discusses this difference between the probability of a string and the probability of a token sequence, and Section 14.5 on token healing describes the same prefix commitment from the prompt side. The effect depends on the decoding rule, because under sampling at temperature 1 the total probability of an emoji is unchanged, and the comparison assumes the same model with a different vocabulary. A vocabulary without emoji removes the loop, because the model outputs `<unk>` and cannot attempt an emoji. The belief that the emoji exists is unaffected by any of this. Asked only whether the emoji exists, GPT-5, Claude Sonnet 4.5 and Llama 3.3 70B said yes every time, in ordinary text.

### Under the tokenizers in the survey

The tokenizers covered in the survey lead to different behaviour in both cases. A word-level vocabulary stores *strawberry* as one unit, so the letters are hidden, and it usually has no emoji, so the model writes `<unk>` or plain text and the seahorse loop cannot start. Standard BPE and Unigram vocabularies also hide the letters, because *strawberry* becomes one to three tokens. If the vocabulary is built over characters and each emoji is a single character, the emoji is one token and the probability is divided among the candidates as described above. Byte-level BPE, used by GPT-2 to GPT-5 and Llama 3, hides the letters in the same way and splits each emoji into a shared prefix and a final byte, which is the setting of the observed loop. SuperBPE and BoundlessBPE produce longer tokens that can span several words, so even more letters are hidden inside single tokens. Stochastic tokenization, such as BPE-dropout and Unigram sampling (Section 3.7), shows the model the same word in several splits during training, including splits with single letters, which gives it a way to learn what is inside its tokens. It does not change which emoji exist in the vocabulary. Pure character-level and byte-level models (Section 9.1) see every letter, so the count can be read from the input. On the output side they write an emoji byte by byte, so the model commits to the emoji block after the first byte, which is an even earlier commitment than with byte-level BPE. Latent tokenization such as BLT's entropy patches (Section 9.2) keeps bytes at the input and output and groups them only inside the model. Letters are therefore visible, and the BLT authors report large gains on the CUTE character benchmarks over a subword model of similar size. The emoji is still produced byte by byte, so the seahorse case would behave as in a byte-level model. None of these choices removes the problem in both directions at once. Finer units help the model read letters, and coarser units for emoji help it avoid committing to an emoji it cannot complete.

### What the two cases share

In both cases the model has no view of the tokenizer. On the input side it cannot look inside a token, so letters are not observable. On the output side it cannot look at its vocabulary, so it can only find out whether a token exists by emitting one and reading it back. Training does not tell the model which strings are single tokens and which are split. The tokenizer therefore does more than encode text. It sets the resolution at which the model reads, the set of things it can write in one step, and the way probability is divided among them. These choices are made before training and are not revised afterwards.

## Learn more

- Theia Vogel, [Why do LLMs freak out over the seahorse emoji?](https://vgel.me/posts/seahorse/), October 2025. The logit lens analysis and the byte tokens of the fish emoji.
- Edman et al., [CUTE: Measuring LLMs' Understanding of Their Tokens](https://arxiv.org/abs/2409.15452), 2024. Character-level tasks including the strawberry family.
- Land and Bartolo, [Fishing for Magikarp](https://arxiv.org/abs/2405.05417), 2024. Detecting under-trained tokens, including unused byte tokens.
- Survey Sections 2.2 (string and token probabilities), 3.1 and 3.1.3 (byte-level BPE, undertrained tokens), 7.1.1 (character-level benchmarks), 9 (byte-level models) and 14.5 (token healing).
