# Data Directory

Place your training bundles here. This directory is **gitignored** (except for this README) to prevent accidental commits of large data files or proprietary corpora.

## Expected Files

| File | Description | Required |
|------|-------------|----------|
| `bundles.jsonl` | Training bundles with tier labels | Yes |
| `bundles_v*.jsonl` | Versioned bundle files | Optional |

## Bundle Schema

Each line is a JSON object with the following fields:

```json
{
  "bundle_id": "unique_identifier",
  "anchor": "The sentence containing the polysemous word in context.",
  "positive": "A sentence or description matching the anchor's sense.",
  "negatives": [
    "A sentence with a different sense of the word.",
    "Another confusing negative example.",
    "..."
  ],
  "tier": "tier1|tier2|tier3_adversarial",
  "word": "the_polysemous_word",
  "anchor_sense": "description of the intended sense"
}
```

### Tier Definitions

| Tier | Description | Typical % |
|------|-------------|-----------|
| `tier1` | Easy cases, clear sense separation | 60% |
| `tier2` | Moderate difficulty, some ambiguity | 30% |
| `tier3_adversarial` | Hard cases, high-similarity negatives | 10% |

## Full Schema Reference

See **[docs/crucible/SCHEMAS.md](../docs/crucible/SCHEMAS.md)** for:
- Complete field specifications
- Validation rules
- Example bundles from each tier
- Scoreboard and capsule schemas

## Generating Bundles

Use the paradigm factory to generate bundles from raw sense data:

```bash
# See paradigm_factory/ for bundle generation scripts
python paradigm_factory/v2/generate_bundles.py --output data/bundles.jsonl
```

## Quick Demo

For a quick demo without your own data, use the synthetic minicorpus:

```bash
make quickstart
# Uses examples/minicorpus_bundles.jsonl
```
