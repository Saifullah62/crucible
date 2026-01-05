"""
Crucible Sweep Module
=====================

Unified entrypoint for running parameter sweeps.

Usage:
    python -m crucible.sweep ratio --bundles ... --eval ...
    python -m crucible.sweep steps --bundles ... --eval ...
    python -m crucible.sweep full --config config.yaml

For available flags, run:
    python -m crucible.sweep --help
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def run_ratio_sweep(args):
    """Run tier3 ratio sweep (R50/25/25 through R90/5/5)."""
    script = PROJECT_ROOT / "experiments" / "run_ratio_sweep_overnight.sh"

    if not script.exists():
        # Fallback: run inline
        print("Running ratio sweep...")
        ratios = [
            (0.50, 0.25, 0.25),
            (0.60, 0.20, 0.20),
            (0.70, 0.15, 0.15),
            (0.75, 0.15, 0.10),  # Validated optimal
            (0.80, 0.10, 0.10),
            (0.90, 0.05, 0.05),
        ]

        for legacy, organic, expanded in ratios:
            cmd = [
                sys.executable,
                str(PROJECT_ROOT / "scripts" / "train_curriculum_v3.py"),
                "--bundles", args.bundles,
                "--steps", str(args.steps),
                "--tier3-legacy", str(legacy),
                "--tier3-organic", str(organic),
                "--tier3-expanded", str(expanded),
                "--device", args.device,
                "--output-dir", f"{args.output}/ratio_{int(legacy*100)}_{int(organic*100)}_{int(expanded*100)}",
            ]
            print(f"\n{'='*60}")
            print(f"Running: R{int(legacy*100)}/{int(organic*100)}/{int(expanded*100)}")
            print(f"{'='*60}")
            subprocess.run(cmd)
    else:
        subprocess.run(["bash", str(script)])


def run_steps_sweep(args):
    """Run training steps sweep (5k, 10k, 15k, 20k)."""
    print("Running steps sweep...")
    steps_values = [5000, 10000, 15000, 20000]

    for steps in steps_values:
        cmd = [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "train_curriculum_v3.py"),
            "--bundles", args.bundles,
            "--steps", str(steps),
            "--device", args.device,
            "--output-dir", f"{args.output}/steps_{steps}",
        ]
        print(f"\n{'='*60}")
        print(f"Running: {steps} steps")
        print(f"{'='*60}")
        subprocess.run(cmd)


def run_quickstart(args):
    """Run quickstart demo on synthetic data."""
    print("Running quickstart demo...")

    bundles = PROJECT_ROOT / "examples" / "minicorpus_bundles.jsonl"
    frozen = PROJECT_ROOT / "examples" / "minicorpus_frozen.jsonl"
    organic = PROJECT_ROOT / "examples" / "minicorpus_organic.jsonl"
    output = PROJECT_ROOT / "results" / "quickstart"

    # Check examples exist
    if not bundles.exists():
        print("Generating minicorpus...")
        gen_script = PROJECT_ROOT / "examples" / "generate_minicorpus.py"
        subprocess.run([sys.executable, str(gen_script)])

    # Train
    print("\n" + "="*60)
    print("PHASE 1: TRAINING (500 steps)")
    print("="*60)
    train_cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "train_curriculum_v3.py"),
        "--bundles", str(bundles),
        "--steps", "500",
        "--device", args.device,
        "--output-dir", str(output),
    ]
    result = subprocess.run(train_cmd)
    if result.returncode != 0:
        print("Training failed!")
        return 1

    # Eval frozen
    print("\n" + "="*60)
    print("PHASE 2: FROZEN EVAL")
    print("="*60)
    eval_cmd = [
        sys.executable,
        str(PROJECT_ROOT / "experiments" / "eval_capsules.py"),
        "--eval", str(frozen),
        "--results-root", str(output),
        "--device", args.device,
        "--out", str(output / "frozen_scoreboard.json"),
    ]
    subprocess.run(eval_cmd)

    # Eval organic
    print("\n" + "="*60)
    print("PHASE 3: ORGANIC EVAL")
    print("="*60)
    eval_cmd = [
        sys.executable,
        str(PROJECT_ROOT / "experiments" / "eval_capsules.py"),
        "--eval", str(organic),
        "--results-root", str(output),
        "--device", args.device,
        "--out", str(output / "organic_scoreboard.json"),
    ]
    subprocess.run(eval_cmd)

    print("\n" + "="*60)
    print("QUICKSTART COMPLETE")
    print("="*60)
    print(f"Results: {output}")
    print(f"Scoreboards: frozen_scoreboard.json, organic_scoreboard.json")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Crucible sweep runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Sweep Types:
  quickstart    Run demo on synthetic minicorpus (fastest)
  ratio         Sweep tier3 ratios (R50/25/25 through R90/5/5)
  steps         Sweep training steps (5k, 10k, 15k, 20k)

Examples:
  python -m crucible.sweep quickstart
  python -m crucible.sweep ratio --bundles data/bundles.jsonl --steps 10000
  python -m crucible.sweep steps --bundles data/bundles.jsonl
        """
    )

    subparsers = parser.add_subparsers(dest="sweep_type", help="Type of sweep to run")

    # Quickstart
    quick_parser = subparsers.add_parser("quickstart", help="Run demo on synthetic data")
    quick_parser.add_argument("--device", default="cpu", help="Device (cpu/cuda)")

    # Ratio sweep
    ratio_parser = subparsers.add_parser("ratio", help="Sweep tier3 ratios")
    ratio_parser.add_argument("--bundles", required=True, help="Training bundles")
    ratio_parser.add_argument("--steps", type=int, default=10000, help="Steps per run")
    ratio_parser.add_argument("--device", default="cuda", help="Device")
    ratio_parser.add_argument("--output", default="results/ratio_sweep", help="Output dir")

    # Steps sweep
    steps_parser = subparsers.add_parser("steps", help="Sweep training steps")
    steps_parser.add_argument("--bundles", required=True, help="Training bundles")
    steps_parser.add_argument("--device", default="cuda", help="Device")
    steps_parser.add_argument("--output", default="results/steps_sweep", help="Output dir")

    args = parser.parse_args()

    if args.sweep_type is None:
        parser.print_help()
        return 1

    if args.sweep_type == "quickstart":
        return run_quickstart(args)
    elif args.sweep_type == "ratio":
        return run_ratio_sweep(args)
    elif args.sweep_type == "steps":
        return run_steps_sweep(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
