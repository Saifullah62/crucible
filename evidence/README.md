# Evidence Directory

Validated experimental results from the RAMP server sweep runs. These files document the empirical basis for the recommended R75/15/10 @ 10k recipe.

## Contents

### Scoreboards (sweep results)

| File | Description |
|------|-------------|
| `scoreboards/frozen_scoreboard.json` | Ratio sweep results on frozen eval |
| `scoreboards/organic_scoreboard.json` | Ratio sweep results on organic holdout |
| `scoreboards/organic_v2_scoreboard.json` | Step sweep results on organic v2 |
| `scoreboards/vet_sweep_scoreboard.json` | Vetting threshold sweep results |

### Evaluation Sets

| File | Size | Items | Description |
|------|------|-------|-------------|
| `frozen_eval_v23.jsonl` | 4.6MB | ~5000 | Frozen tier3 adversarial eval (known hard cases) |
| `organic_holdout_eval.jsonl` | 115KB | ~500 | Organic holdout v1 (mined adversarials) |
| `organic_holdout_v2_eval.jsonl` | 302KB | ~1200 | Organic holdout v2 (expanded mining) |

### Training Data

| File | Size | Items | Description |
|------|------|-------|-------------|
| `dress_rehearsal_bundles.jsonl` | 43MB | ~30k | Full dress rehearsal training bundles |

## Key Findings

### Ratio Sweep (R{legacy}/{organic}/{expanded})

From `scoreboards/frozen_scoreboard.json` and `scoreboards/organic_scoreboard.json`:

| Ratio | Frozen Tier3 | Organic Holdout | Notes |
|-------|--------------|-----------------|-------|
| R65/25/10 | ~85% | ~78% | Too much organic dilutes frozen |
| R70/20/10 | ~87% | ~80% | Better frozen, organic still good |
| **R75/15/10** | **~89%** | **~82%** | **Pareto optimal** |
| R80/15/5 | ~88% | ~79% | Reduced expanded hurts organic |
| R85/10/5 | ~86% | ~76% | Too little organic/expanded |

### Step Sweep

From `scoreboards/organic_v2_scoreboard.json`:

| Steps | Frozen | Organic | Notes |
|-------|--------|---------|-------|
| 5k | ~82% | ~78% | Undertrained |
| **10k** | **~89%** | **~82%** | **Sweet spot** |
| 20k | ~88% | ~75% | Overfitting cliff on organic |

## Usage

These files are committed as evidence of the validated recipe. For actual training/eval:

```bash
# Copy to standard locations
cp evidence/dress_rehearsal_bundles.jsonl data/bundles.jsonl
cp evidence/frozen_eval_v23.jsonl evals/frozen.jsonl
cp evidence/organic_holdout_v2_eval.jsonl evals/organic.jsonl

# Run production capsule
python -m crucible.capsule \
    --bundles data/bundles.jsonl \
    --frozen-eval evals/frozen.jsonl \
    --organic-eval evals/organic.jsonl
```

## Source

Synced from RAMP server (`gpu-swarm:~/QUANTUM_BWD/`) on 2026-01-05.
