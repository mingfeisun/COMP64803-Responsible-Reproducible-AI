#!/usr/bin/env python3
"""
Extract top-k prompts from a completed evolution run.

Reads the latest checkpoint in a run directory and outputs the top-k
programs ranked by combined_score.

Usage:
  python extract_top_k.py --run ../../openevolve_output --top-k 20
  python extract_top_k.py --run results/run_TIMESTAMP/target-id --top-k 5 -o top5.csv
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path


def extract_top_k(run_dir: Path, k: int) -> list[dict]:
    """Read latest checkpoint population and return top-k programs by combined_score."""
    ckpt_dir = run_dir / "checkpoints"
    if not ckpt_dir.is_dir():
        print(f"ERROR: No checkpoints/ directory found in {run_dir}")
        sys.exit(1)

    ckpts = sorted(
        [d for d in os.listdir(str(ckpt_dir)) if d.startswith("checkpoint_")],
        key=lambda d: int(d.split("_")[1]),
        reverse=True,
    )
    if not ckpts:
        print(f"ERROR: No checkpoint_* directories found in {ckpt_dir}")
        sys.exit(1)

    programs_dir = ckpt_dir / ckpts[0] / "programs"
    if not programs_dir.is_dir():
        print(f"ERROR: No programs/ directory in latest checkpoint ({ckpts[0]})")
        sys.exit(1)

    programs = []
    for fname in os.listdir(str(programs_dir)):
        if not fname.endswith(".json"):
            continue
        with open(programs_dir / fname) as f:
            prog = json.load(f)
        m = prog.get("metrics", {})
        programs.append({
            "program_id": prog.get("id", ""),
            "generation": prog.get("generation", 0),
            "iteration_found": prog.get("iteration_found", 0),
            "combined_score": m.get("combined_score", 0),
            "avg_harm": m.get("avg_harm", 0),
            "success_rate": m.get("success_rate", 0),
            "refusal_rate": m.get("refusal_rate", 1),
            "strategy_fingerprint": int(m.get("strategy_fingerprint", 0)),
            "stealth_score": m.get("stealth_score", 0),
            "prompt_length": m.get("prompt_length", 0),
            "prompt_text": prog.get("code", ""),
        })

    programs.sort(key=lambda p: p["combined_score"], reverse=True)
    return programs[:k]


def main():
    parser = argparse.ArgumentParser(description="Extract top-k prompts from a completed evolution run")
    parser.add_argument("--run", "-r", type=str, required=True,
                        help="Path to the run directory (contains checkpoints/)")
    parser.add_argument("--top-k", "-k", type=int, default=10,
                        help="Number of top programs to extract (default: 10)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output CSV path (default: top_{k}_prompts.csv in run dir)")
    args = parser.parse_args()

    run_dir = Path(args.run).resolve()
    if not run_dir.is_dir():
        print(f"ERROR: Run directory not found: {run_dir}")
        sys.exit(1)

    output_path = args.output or str(run_dir / f"top_{args.top_k}_prompts.csv")

    programs = extract_top_k(run_dir, args.top_k)
    if not programs:
        print("No programs found in population.")
        sys.exit(1)

    fields = ["program_id", "generation", "iteration_found", "combined_score",
              "avg_harm", "success_rate", "refusal_rate",
              "strategy_fingerprint", "stealth_score", "prompt_length", "prompt_text"]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(programs)

    print(f"Extracted top {args.top_k} programs from checkpoint {run_dir}")
    print(f"Saved to: {output_path}")

    # Print summary table
    print(f"\n{'Rank':<5} {'Score':<10} {'Harm':<8} {'Success':<9} {'Gen':<5} {'Iter':<6} {'Strategy':<10} {'Stealth':<8} {'Length':<7}")
    print("-" * 75)
    for rank, p in enumerate(programs, 1):
        print(f"{rank:<5} {p['combined_score']:<10.4f} {p['avg_harm']:<8.2f} {p['success_rate']:<9.1%} "
              f"{p['generation']:<5} {p['iteration_found']:<6} {p['strategy_fingerprint']:<10} "
              f"{p['stealth_score']:<8.2f} {p['prompt_length']:<7}")


if __name__ == "__main__":
    main()
