# Evals Directory

Place your evaluation sets here. This directory is **gitignored** (except for this README) to prevent accidental commits of proprietary eval data.

## Expected Files

| File | Description | Purpose |
|------|-------------|---------|
| `frozen.jsonl` | Frozen eval set | Retention: known hard cases that must not regress |
| `organic.jsonl` | Organic holdout | Generalization: unseen hard cases |

## Eval Item Schema

Each line is a JSON object:

```json
{
  "item_id": "unique_identifier",
  "anchor": "The sentence to retrieve the correct sense for.",
  "positive": "The correct sense description or example.",
  "negatives": [
    "An incorrect but plausible sense.",
    "Another confusing negative.",
    "..."
  ],
  "tier": "tier3_adversarial|organic",
  "word": "the_polysemous_word",
  "expected_sense": "description of correct sense"
}
```

## Two-Eval Strategy

The Crucible harness uses two eval sets to detect overfitting vs. generalization:

| Eval | What it measures | Healthy trend |
|------|------------------|---------------|
| **Frozen** | Retention of known hard cases | Improving or stable |
| **Organic** | Generalization to new hard cases | Improving |

**Warning signs:**
- Frozen improving but organic flat → memorization, not learning
- Organic improving but frozen dropping → catastrophic forgetting
- Both should improve together for healthy training

## Full Schema Reference

See **[docs/crucible/SCHEMAS.md](../docs/crucible/SCHEMAS.md)** for complete specifications.

## Quick Demo

For a quick demo without your own data:

```bash
make quickstart
# Uses examples/minicorpus_frozen.jsonl and minicorpus_organic.jsonl
```
