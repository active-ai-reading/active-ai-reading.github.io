---
title: "copyedit 4.1"
description: One sentence that makes people want to click.
paper: tokenization-survey
role: writing
task: copyedit
by: ohad-agadi
---

<!-- Keep the sections that fit your task, delete the rest. -->

## What I changed and why

I chose to rewrite the beginning of section 4.1, due to it being overly formal and complex.

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
  One common preprocessing step is to normalize the input text into a standardized form before tokenization.
This may involve removing unwanted artifacts, mapping equivalent surface forms to a common representation, or applying lossy simplifications intended to reduce superficial variation in the data. Common
surface-level transformations include:
    ... (good examples)
  These normalizations are often used to unify minor typographical differences across scripts for easier processing or to clean up erroneous text. Invisible character removal is also important for tokenizer safety, as
control characters can be used to inject token breakpoints to alter a model’s output while leaving the surface
form of the text unchanged (see also Section 14.3; Boucher et al., 2022).
  </div>
  <div class="after"><span class="label">After</span>
  Before tokenization, text is often normalised into a standard format, Such that artifacts, escape or control characters do not exist. This is to prevent mapping of two visually similar text to different tokens and consequently different embeddings.
  ... (examples)
  Further more, control characters can be used to inject token breakpoints to alter a model’s output. Removing such "invisible characters" helps circumvent that safety risk. 
  </div>
</div>

## The general rule

Use simple words to convey a simple idea.

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
