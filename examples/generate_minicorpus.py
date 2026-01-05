#!/usr/bin/env python3
"""
Generate Mini Corpus for Quickstart Demo
=========================================

Creates a small synthetic dataset (200 bundles) to demonstrate
the Crucible harness end-to-end without requiring real data.

Usage:
    python examples/generate_minicorpus.py

Output:
    examples/minicorpus_bundles.jsonl   (160 train bundles)
    examples/minicorpus_frozen.jsonl    (20 frozen eval)
    examples/minicorpus_organic.jsonl   (20 organic eval)
"""

import json
import random
from pathlib import Path

# Polysemous words with their senses for synthetic data
POLYSEMOUS_WORDS = {
    "bank": [
        ("financial institution", "The bank approved my loan application."),
        ("river edge", "We had a picnic on the bank of the river."),
        ("aircraft maneuver", "The pilot executed a sharp bank to avoid the storm."),
    ],
    "bat": [
        ("flying mammal", "The bat emerged from the cave at dusk."),
        ("sports equipment", "He swung the bat and hit a home run."),
    ],
    "crane": [
        ("bird", "A crane stood motionless in the shallow water."),
        ("machine", "The crane lifted the steel beam into place."),
        ("neck movement", "She had to crane her neck to see the stage."),
    ],
    "spring": [
        ("season", "Flowers bloom in spring after the winter."),
        ("water source", "Fresh water bubbled up from the spring."),
        ("coil", "The spring in the mattress was broken."),
        ("jump", "The cat will spring at the slightest movement."),
    ],
    "bass": [
        ("fish", "He caught a large bass in the lake."),
        ("low frequency", "Turn up the bass on the speaker."),
        ("instrument", "She plays bass in a jazz band."),
    ],
    "lead": [
        ("metal", "The pipe was made of lead."),
        ("guide", "She will lead the team to victory."),
        ("clue", "The detective found a new lead."),
    ],
    "bark": [
        ("tree covering", "The bark of the oak tree was rough."),
        ("dog sound", "The dog's bark echoed through the yard."),
    ],
    "date": [
        ("calendar day", "What is today's date?"),
        ("fruit", "She added chopped dates to the recipe."),
        ("romantic meeting", "They went on a date to the cinema."),
    ],
    "fan": [
        ("cooling device", "The fan kept the room cool."),
        ("enthusiast", "He's a huge fan of classical music."),
        ("spread out", "She held the cards in a fan shape."),
    ],
    "jam": [
        ("fruit preserve", "She spread jam on her toast."),
        ("traffic", "We got stuck in a traffic jam."),
        ("music session", "The band had a jam session last night."),
    ],
}


def generate_bundle(word: str, senses: list, tier: str, bundle_id: int) -> dict:
    """Generate a single training bundle in train_curriculum_v3.py format."""
    # Pick anchor sense
    anchor_idx = random.randint(0, len(senses) - 1)
    anchor_sense, anchor_example = senses[anchor_idx]

    # Positive: same sense, different phrasing
    positive_templates = [
        f"The word '{word}' here means {anchor_sense}.",
        f"In this context, '{word}' refers to {anchor_sense}.",
        f"'{word}' is used to describe {anchor_sense}.",
    ]
    positive = random.choice(positive_templates)

    # Negatives: other senses
    negatives = []
    for i, (sense, example) in enumerate(senses):
        if i != anchor_idx:
            neg_templates = [
                f"The word '{word}' here means {sense}.",
                f"In this context, '{word}' refers to {sense}.",
                example,
            ]
            negatives.append({"text": random.choice(neg_templates)})

    # Pad negatives if needed (minimum 2)
    while len(negatives) < 2:
        negatives.append({"text": "Unrelated: The weather is nice today."})

    return {
        "bundle_id": f"mini_{bundle_id:04d}",
        "anchor": {"text": anchor_example},
        "positive": {"text": positive},
        "negatives": negatives[:5],  # Cap at 5 negatives
        "metadata": {
            "difficulty_tier": tier,  # Already in correct format
            "word": word,
            "anchor_sense": anchor_sense,
            "source": "synthetic_minicorpus",
        },
    }


def generate_eval_item(word: str, senses: list, item_id: int, eval_type: str) -> dict:
    """Generate a single eval item in eval_capsules.py format."""
    anchor_idx = random.randint(0, len(senses) - 1)
    anchor_sense, anchor_example = senses[anchor_idx]

    # For eval, we use cleaner formulations
    positive = f"'{word}' meaning: {anchor_sense}"

    negatives = []
    for i, (sense, _) in enumerate(senses):
        if i != anchor_idx:
            negatives.append(f"'{word}' meaning: {sense}")

    while len(negatives) < 2:
        negatives.append("Completely unrelated concept")

    return {
        "item_id": f"{eval_type}_{item_id:04d}",
        "anchor_text": anchor_example,
        "positive_text": positive,
        "negative_texts": negatives[:5],
        "word": word,
        "expected_sense": anchor_sense,
        "tier": "tier3_adversarial" if eval_type == "frozen" else "organic",
    }


def main():
    random.seed(42)  # Reproducible

    output_dir = Path(__file__).parent

    # Generate training bundles (160 total)
    bundles = []
    bundle_id = 0

    # Tier distribution: 60% tier1, 30% tier2, 10% tier3
    tier_counts = {"tier1_easy": 96, "tier2_medium": 48, "tier3_adversarial": 16}

    words = list(POLYSEMOUS_WORDS.keys())

    for tier, count in tier_counts.items():
        for _ in range(count):
            word = random.choice(words)
            senses = POLYSEMOUS_WORDS[word]
            bundle = generate_bundle(word, senses, tier, bundle_id)
            bundles.append(bundle)
            bundle_id += 1

    random.shuffle(bundles)

    # Write bundles
    bundles_path = output_dir / "minicorpus_bundles.jsonl"
    with open(bundles_path, "w") as f:
        for b in bundles:
            f.write(json.dumps(b) + "\n")
    print(f"Wrote {len(bundles)} bundles to {bundles_path}")

    # Generate frozen eval (20 items) - known hard cases
    frozen_items = []
    for i in range(20):
        word = words[i % len(words)]
        senses = POLYSEMOUS_WORDS[word]
        item = generate_eval_item(word, senses, i, "frozen")
        frozen_items.append(item)

    frozen_path = output_dir / "minicorpus_frozen.jsonl"
    with open(frozen_path, "w") as f:
        for item in frozen_items:
            f.write(json.dumps(item) + "\n")
    print(f"Wrote {len(frozen_items)} frozen eval items to {frozen_path}")

    # Generate organic eval (20 items) - held-out generalization
    organic_items = []
    for i in range(20):
        word = words[(i + 5) % len(words)]  # Offset to get different distribution
        senses = POLYSEMOUS_WORDS[word]
        item = generate_eval_item(word, senses, i, "organic")
        organic_items.append(item)

    organic_path = output_dir / "minicorpus_organic.jsonl"
    with open(organic_path, "w") as f:
        for item in organic_items:
            f.write(json.dumps(item) + "\n")
    print(f"Wrote {len(organic_items)} organic eval items to {organic_path}")

    print("\nMini corpus generated! Run quickstart with:")
    print("  make quickstart")
    print("  # or")
    print("  python -m crucible.train --bundles examples/minicorpus_bundles.jsonl --steps 500")


if __name__ == "__main__":
    main()
