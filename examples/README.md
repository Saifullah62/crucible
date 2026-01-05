# Examples

This directory contains synthetic data and configs for running the Crucible harness end-to-end.

## Quickstart Demo

Run the full pipeline on synthetic data (CPU, ~2 minutes):

```bash
make quickstart
```

Or step by step:

```bash
# 1. Generate synthetic minicorpus (already committed, but regenerate if needed)
python examples/generate_minicorpus.py

# 2. Train for 500 steps
python -m crucible.train \
    --bundles examples/minicorpus_bundles.jsonl \
    --steps 500 \
    --device cpu

# 3. Evaluate
python -m crucible.eval \
    --eval examples/minicorpus_frozen.jsonl \
    --results-root results/quickstart \
    --device cpu
```

## Files

| File | Description |
|------|-------------|
| `generate_minicorpus.py` | Script to generate synthetic bundles and evals |
| `minicorpus_bundles.jsonl` | 160 training bundles (60% tier1, 30% tier2, 10% tier3) |
| `minicorpus_frozen.jsonl` | 20 frozen eval items |
| `minicorpus_organic.jsonl` | 20 organic eval items |
| `quickstart_config.yaml` | Config for CPU demo runs |

## Data Format

See [docs/crucible/SCHEMAS.md](../docs/crucible/SCHEMAS.md) for the canonical bundle and eval schemas.

### Bundle Schema (training)

```json
{
  "bundle_id": "mini_0001",
  "anchor": "The bank approved my loan application.",
  "positive": "The word 'bank' here means financial institution.",
  "negatives": ["The word 'bank' here means river edge.", "..."],
  "tier": "tier1",
  "word": "bank",
  "anchor_sense": "financial institution"
}
```

### Eval Item Schema

```json
{
  "item_id": "frozen_0001",
  "anchor": "The bank approved my loan application.",
  "positive": "'bank' meaning: financial institution",
  "negatives": ["'bank' meaning: river edge", "..."],
  "tier": "tier3_adversarial"
}
```

## Using Your Own Data

1. Place training bundles in `data/bundles.jsonl`
2. Place eval sets in `evals/frozen.jsonl` and `evals/organic.jsonl`
3. Run with your data:

```bash
python -m crucible.train --bundles data/bundles.jsonl --steps 10000
python -m crucible.eval --eval evals/frozen.jsonl --results-root results/
```
