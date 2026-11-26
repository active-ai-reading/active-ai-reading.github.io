"""CPU reimplementation of the training comparison in LLM-JEPA Figure 3 (right)."""

import argparse
import csv
import json
from dataclasses import dataclass, fields
from pathlib import Path
from time import perf_counter

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


SEEDS = (82, 23, 37, 84, 4)
CHECKPOINTS = (0, 25, 50, 100, 150, 200, 250, 300)
CONDITIONS = {"next_token": 0.0, "llm_jepa": 1.0}
BATCH_SIZE = 16
LEARNING_RATE = 0.003
SYNTH_TEST_SIZE = 256
PAD, BOS, SEP, EOS = range(4)


@dataclass
class Batch:
    lm_ids: torch.Tensor
    labels: torch.Tensor
    prompts: torch.Tensor
    prompt_lengths: torch.Tensor
    text_ids: torch.Tensor
    code_ids: torch.Tensor
    regexes: np.ndarray

    def __getitem__(self, indices):
        return Batch(*(getattr(self, field.name)[indices] for field in fields(self)))


def read_synth(path):
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            messages = json.loads(line)["messages"]
            views = {message["role"]: message["content"] for message in messages}
            yield views["user"].split(), views["assistant"]


def make_synth_data(train_path, test_path):
    train = list(read_synth(train_path))
    train_prompts = {tuple(prompt) for prompt, _ in train}
    eligible = [row for row in read_synth(test_path) if tuple(row[0]) not in train_prompts]
    if not train or len(eligible) < SYNTH_TEST_SIZE:
        raise ValueError("Expected the published NL-RX-SYNTH train and test splits.")
    rng = np.random.default_rng(2026)
    indices = np.sort(rng.choice(len(eligible), size=SYNTH_TEST_SIZE, replace=False))
    test = [eligible[index] for index in indices]
    print(f"NL-RX-SYNTH: {len(train)} training rows, {len(eligible)} eligible test rows, {len(test)} sampled.", flush=True)
    return encode_data(train, test)


def encode_data(train, test):
    words = {word for prompt, _ in train for word in prompt}
    characters = {char for _, regex in train for char in regex}
    vocabulary = {token: index for index, token in enumerate(sorted(words | characters), start=4)}
    unknown_word = len(vocabulary) + 4
    regex_length = max(len(regex) for _, regex in train + test)
    prompt_length = max(len(prompt) + 2 for prompt, _ in train + test)
    context = prompt_length + regex_length + 1

    def encode(examples):
        def padded(rows, width):
            return torch.tensor([row + [PAD] * (width - len(row)) for row in rows])

        text = [[BOS] + [vocabulary.get(word, unknown_word) for word in prompt] for prompt, _ in examples]
        code = [[vocabulary[char] for char in regex] for _, regex in examples]
        prompts = [tokens + [SEP] for tokens in text]
        labels = [tokens + [EOS] for tokens in code]
        return Batch(
            padded([prompt + label for prompt, label in zip(prompts, labels)], context),
            padded(labels, regex_length + 1),
            padded(prompts, context),
            torch.tensor([len(prompt) for prompt in prompts]),
            padded(text, prompt_length - 1),
            padded([[BOS] + tokens for tokens in code], regex_length + 1),
            np.array([regex for _, regex in examples]),
        )

    return encode(train), encode(test), unknown_word + 1, context


class Decoder(nn.Module):
    """One causal self-attention head, a feed-forward layer, and final RMS normalization."""

    def __init__(self, vocab_size, context, width=32):
        super().__init__()
        self.token = nn.Embedding(vocab_size, width)
        self.position = nn.Embedding(context, width)
        nn.init.normal_(self.token.weight, std=0.2)
        nn.init.normal_(self.position.weight, std=0.2)
        self.attention = nn.MultiheadAttention(width, num_heads=1, bias=False, batch_first=True)
        self.feed_forward = nn.Sequential(
            nn.Linear(width, 2 * width, bias=False),
            nn.Tanh(),
            nn.Linear(2 * width, width, bias=False),
        )
        self.norm = nn.RMSNorm(width, eps=1e-5, elementwise_affine=False)
        self.lm_head = nn.Linear(width, vocab_size, bias=False)
        self.register_buffer("future", torch.ones(context, context, dtype=torch.bool).triu(diagonal=1))

    def forward(self, tokens):
        length = tokens.shape[1]
        x = self.token(tokens) + self.position.weight[:length]
        attention, _ = self.attention(x, x, x, attn_mask=self.future[:length, :length], need_weights=False)
        x = x + attention
        return self.norm(x + self.feed_forward(x))


def next_token_loss(model, batch):
    # The separator predicts the first regex character. Regex characters predict
    # the remaining characters and EOS. Padded positions contribute no loss.
    rows, label_positions = (batch.labels != PAD).nonzero(as_tuple=True)
    positions = batch.prompt_lengths[rows] - 1 + label_positions
    hidden = model(batch.lm_ids[:, :-1])
    logits = model.lm_head(hidden[rows, positions])
    return F.cross_entropy(logits, batch.labels[rows, label_positions])


def last_states(model, token_ids):
    last = token_ids.count_nonzero(dim=1) - 1
    return model(token_ids)[torch.arange(len(token_ids)), last]


def view_embeddings(model, batch):
    # The views share a decoder but cannot attend to each other.
    return last_states(model, batch.text_ids), last_states(model, batch.code_ids)


def greedy_outputs(model, batch):
    tokens = batch.prompts.clone()
    predictions = torch.full_like(batch.labels, PAD)
    live = torch.arange(len(tokens))
    positions = batch.prompt_lengths - 1
    for step in range(batch.labels.shape[1]):
        if live.numel() == 0:
            break
        query_positions = positions[live]
        hidden = model(tokens[live, : query_positions.max().item() + 1])
        logits = model.lm_head(hidden[torch.arange(len(live)), query_positions])
        next_ids = logits.argmax(dim=-1)
        predictions[live, step] = next_ids
        positions[live] += 1
        tokens[live, positions[live]] = next_ids
        live = live[next_ids != EOS]
    return predictions


@torch.inference_mode()
def evaluate(model, batch):
    text, code = view_embeddings(model, batch)
    distances = 1 - F.normalize(text, dim=-1) @ F.normalize(code, dim=-1).T
    wrong_regex = torch.from_numpy(batch.regexes[:, None] != batch.regexes[None, :])
    generated = greedy_outputs(model, batch)
    return {
        "next_token_loss": next_token_loss(model, batch).item(),
        "paired_cosine_distance": distances.diagonal().mean().item(),
        "wrong_cosine_distance": distances[wrong_regex].mean().item(),
        "exact_match": (generated == batch.labels).all(dim=1).sum().item() / len(generated),
    }


def train_run(train, test, vocab_size, context, seed, condition, weight):
    torch.manual_seed(seed)
    model = Decoder(vocab_size, context)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    rng = np.random.default_rng(seed + 1000)
    measurements = []
    training_losses = []
    started = perf_counter()

    def record(step):
        model.eval()
        measurements.append({"seed": seed, "condition": condition, "step": step, **evaluate(model, test)})
        model.train()

    record(0)
    for step in range(1, CHECKPOINTS[-1] + 1):
        batch = train[rng.integers(len(train.regexes), size=BATCH_SIZE)]
        optimizer.zero_grad()
        ntp = next_token_loss(model, batch)
        with torch.set_grad_enabled(bool(weight)):
            text, code = view_embeddings(model, batch)
            pred = 1 - F.cosine_similarity(text, code, dim=-1).mean()
        loss = ntp + weight * pred if weight else ntp
        training_losses.append({
            "seed": seed, "condition": condition, "step": step,
            "next_token_loss": ntp.item(), "jepa_loss": pred.item(),
        })
        loss.backward()
        optimizer.step()

        if step in CHECKPOINTS:
            record(step)

    seconds = perf_counter() - started
    return [dict(row, run_seconds=round(seconds, 3)) for row in measurements], training_losses


def check(train, test, vocab_size, context):
    assert len(test.regexes) == SYNTH_TEST_SIZE
    assert set(map(tuple, train.text_ids.tolist())).isdisjoint(map(tuple, test.text_ids.tolist()))

    torch.manual_seed(11)
    model = Decoder(vocab_size, context)
    batch = test[[0, 7]]
    edited = batch.lm_ids.clone()
    edited[:, 4:] = EOS
    with torch.no_grad():
        torch.testing.assert_close(model(batch.lm_ids)[:, :4], model(edited)[:, :4])
        changed = test[[0, 7]]
        changed.text_ids = changed.text_ids.flip(0)
        assert not torch.equal(batch.text_ids, changed.text_ids)
        _, original_code = view_embeddings(model, batch)
        _, changed_code = view_embeddings(model, changed)
        torch.testing.assert_close(original_code, changed_code)

    text, code = view_embeddings(model, batch)
    distance = 1 - F.cosine_similarity(text, code, dim=-1).mean()
    gradients = torch.autograd.grad(distance, (text, code))
    assert all(gradient.isfinite().all() and gradient.norm() > 0 for gradient in gradients)
    print("Data split, causality, view isolation, and JEPA gradients to both views passed.")


def plot(training_losses, path):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    series = (
        ("next_token", "next_token_loss", "#235789", "-", "Baseline (NTP)"),
        ("llm_jepa", "next_token_loss", "#ad6200", "-", "LLM-JEPA (NTP)"),
        ("next_token", "jepa_loss", "#b2393c", "--", "Baseline (JEPA loss)"),
        ("llm_jepa", "jepa_loss", "#087a54", "--", "LLM-JEPA (JEPA loss)"),
    )
    window_size = 5
    steps = np.arange(window_size, CHECKPOINTS[-1] + 1, window_size)
    fig, axis = plt.subplots(figsize=(7, 3.7), layout="constrained")
    for condition, metric, color, linestyle, label in series:
        values = [row[metric] for row in training_losses if row["condition"] == condition]
        windows = np.reshape(values, (len(SEEDS), len(steps), window_size))
        axis.semilogy(steps, windows.mean(axis=(0, 2)), color=color, linestyle=linestyle, label=label)
    axis.set(xlabel="Optimizer update", ylabel="Training loss (log scale)", xlim=(0, CHECKPOINTS[-1]))
    axis.grid(axis="y", alpha=0.22)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(ncol=2, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.02))
    fig.savefig(path, dpi=180, facecolor="white")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("llm-jepa-nl-rx-synth-results"))
    parser.add_argument("--check", action="store_true", help="Validate the data split and gradients without training.")
    parser.add_argument(
        "--synth-files", nargs=2, type=Path, required=True, metavar=("TRAIN_JSONL", "TEST_JSONL"),
        help="Paths to the authors' NL-RX-SYNTH train and test files.",
    )
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    train, test, vocab_size, context = make_synth_data(*args.synth_files)
    if args.check:
        check(train, test, vocab_size, context)
        return

    measurements = []
    training_losses = []
    for seed in SEEDS:
        for condition, weight in CONDITIONS.items():
            run, losses = train_run(train, test, vocab_size, context, seed, condition, weight)
            measurements.extend(run)
            training_losses.extend(losses)
            print(f"{seed} {condition}: {run[-1]['run_seconds']:.2f} s", flush=True)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, rows in (("curves.csv", measurements), ("training-losses.csv", training_losses)):
        with (args.output_dir / filename).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    plot(training_losses, args.output_dir / "learning-curves.png")


if __name__ == "__main__":
    main()
