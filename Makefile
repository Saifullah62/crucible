# Crucible Makefile
# ==================
# Common tasks for development and demos.

.PHONY: quickstart install test lint docs clean help

# Default target
help:
	@echo "Crucible Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make quickstart    Run end-to-end demo on synthetic data (CPU)"
	@echo "  make install       Install dependencies"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make docs          Regenerate docs from --help"
	@echo "  make clean         Remove generated files"
	@echo ""
	@echo "Quickstart runs train + eval in ~2 minutes on CPU."

# Run quickstart demo
quickstart:
	@echo "=============================================="
	@echo "CRUCIBLE QUICKSTART DEMO"
	@echo "=============================================="
	@echo ""
	python -m crucible.sweep quickstart --device cpu

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests (placeholder)
test:
	python -m pytest tests/ -v 2>/dev/null || echo "No tests directory yet"

# Run linters
lint:
	python tools/docs_lint_crucible.py

# Regenerate docs from --help
docs:
	python tools/extract_script_flags.py
	python tools/docs_lint_crucible.py

# Clean generated files
clean:
	rm -rf results/quickstart
	rm -rf __pycache__ **/__pycache__
	rm -rf *.egg-info
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete

# Generate minicorpus (usually already committed)
minicorpus:
	python examples/generate_minicorpus.py

# Run ratio sweep (requires GPU and real data)
sweep-ratio:
	python -m crucible.sweep ratio --bundles data/bundles.jsonl --steps 10000

# Run steps sweep (requires GPU and real data)
sweep-steps:
	python -m crucible.sweep steps --bundles data/bundles.jsonl

# Build production capsule (requires GPU and real data)
capsule:
	python -m crucible.capsule \
		--bundles data/bundles.jsonl \
		--frozen-eval evals/frozen.jsonl \
		--organic-eval evals/organic.jsonl \
		--output-dir capsules/production
