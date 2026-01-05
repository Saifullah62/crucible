# Crucible

Production-grade contrastive learning harness: curriculum training, tier-stratified evaluation, and adversarial mining.

## Quickstart (2 minutes, CPU)

```bash
# Install
pip install -r requirements.txt

# Run end-to-end demo on synthetic data
make quickstart
```

This trains for 500 steps on a synthetic minicorpus and generates scoreboards.

## Features

- **Curriculum Training**: Three-pool tier3 mixing with validated R75/15/10 ratios
- **Tier-Stratified Evaluation**: Separate frozen (retention) and organic (generalization) metrics
- **Production Capsules**: 3-seed runs with median selection, locked manifests
- **Parameter Sweeps**: Ratio sweeps, step sweeps, automated optimization
- **Documentation Guardrails**: Auto-generated CLI docs, drift detection in CI

## Usage

```bash
# Train with your data
python -m crucible.train --bundles data/bundles.jsonl --steps 10000

# Evaluate
python -m crucible.eval --eval evals/frozen.jsonl --results-root results/

# Build production capsule
python -m crucible.capsule \
    --bundles data/bundles.jsonl \
    --frozen-eval evals/frozen.jsonl \
    --organic-eval evals/organic.jsonl

# Run parameter sweep
python -m crucible.sweep ratio --bundles data/bundles.jsonl
```

## Project Structure

```
crucible/
├── qllm/                    # Core embedding model
├── crucible/                # CLI entrypoints (train, eval, capsule, sweep)
├── scripts/                 # Canonical training/eval scripts
├── experiments/             # Capsule builder, sweep runners
├── paradigm_factory/        # Bundle generation (code only)
├── examples/                # Synthetic minicorpus for demos
├── docs/crucible/           # Full documentation suite
└── tools/                   # Linters, truth extractor
```

## Data Convention

| Directory | Contents | Committed |
|-----------|----------|-----------|
| `data/` | Training bundles (`bundles.jsonl`) | No (gitignored) |
| `evals/` | Eval sets (`frozen.jsonl`, `organic.jsonl`) | No (gitignored) |
| `examples/` | Synthetic demo data | Yes |
| `results/` | Training outputs, scoreboards | No (gitignored) |

See [data/README.md](data/README.md) and [docs/crucible/SCHEMAS.md](docs/crucible/SCHEMAS.md) for formats.

## Documentation

Start with **[docs/crucible/INDEX.md](docs/crucible/INDEX.md)**:

| Doc | Purpose |
|-----|---------|
| [CURRENT_IMPLEMENTATION.md](docs/crucible/CURRENT_IMPLEMENTATION.md) | CLI flags (auto-generated, authoritative) |
| [QUICKSTART.md](docs/crucible/QUICKSTART.md) | Fastest end-to-end run |
| [METRICS.md](docs/crucible/METRICS.md) | Canonical formulas |
| [SCHEMAS.md](docs/crucible/SCHEMAS.md) | Bundle, eval, scoreboard formats |

**Rule**: When docs disagree, CURRENT_IMPLEMENTATION.md wins.

## Validated Recipe

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Tier3 Ratios | R75/15/10 | Pareto-optimal on frozen vs organic |
| Steps | 10,000 | Before overfitting cliff |
| Seeds | 3, median selection | Variance reduction without cherry-picking |

## CI Guardrails

- **Artifact Guard**: Fails PR if checkpoints, logs, or data files are committed
- **Drift Detection**: Fails if CLI docs don't match `--help` output
- **Quickstart Test**: Runs full pipeline on synthetic data

## Enterprise Features

Some features require a license (set `CRUCIBLE_ENTERPRISE_KEY`):
- Organic adversarial miner
- Capsule verification protocol
- Automated optimization

See [docs/crucible/COMMERCIAL.md](docs/crucible/COMMERCIAL.md) for details.

## Development

```bash
make help          # Show available commands
make quickstart    # Run demo
make lint          # Run linters
make docs          # Regenerate CLI docs
```

## License

MIT License - see [LICENSE](LICENSE)
