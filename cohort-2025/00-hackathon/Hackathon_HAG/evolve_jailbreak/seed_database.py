#!/usr/bin/env python3
"""
Pre-seed the OpenEvolve MAP-Elites database with diverse jailbreak strategies.

Reads all seed prompts from seeds/ and injects them into a fresh OpenEvolve
database BEFORE evolution begins. All config comes from evolve_config.yaml.

Usage:
  python seed_database.py [--config evolve_config.yaml] [--output-dir openevolve_output]
"""

import argparse
import os
import sys
import uuid
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent.resolve()
DEFAULT_CONFIG = SCRIPT_DIR / "evolve_config.yaml"
SEEDS_DIR = SCRIPT_DIR / "seeds"

# Add parent dir to path so we can import evaluator helper functions
sys.path.insert(0, str(SCRIPT_DIR))
from evaluator import _calculate_stealth, _calculate_strategy_fingerprint

try:
    from openevolve.database import Program, ProgramDatabase
    from openevolve.config import Config, load_config
except ImportError:
    print("ERROR: openevolve not installed. Run: pip install openevolve")
    sys.exit(1)


def load_seeds() -> list[tuple[str, str]]:
    """Load all seed files. Returns list of (strategy_name, prompt_text)."""
    seeds = []
    for seed_file in sorted(SEEDS_DIR.glob("*.txt")):
        name = seed_file.stem
        strategy = name.split("_", 1)[1].replace("_", " ").title()
        prompt = seed_file.read_text().strip()
        seeds.append((strategy, prompt))
        print(f"  Loaded: {seed_file.name} — {len(prompt)} chars")
    return seeds


def estimate_metrics(prompt: str) -> dict:
    """Generate plausible initial metrics for a seed prompt using actual scoring functions."""
    stealth = _calculate_stealth(prompt)
    strategy = _calculate_strategy_fingerprint(prompt)

    prompt_lower = prompt.lower()
    technical_terms = [
        "step", "procedure", "method", "technique", "synthesize", "detailed",
        "instruction", "guide", "complete", "comprehensive", "specific"
    ]
    tech_score = sum(1 for kw in technical_terms if kw in prompt_lower) / len(technical_terms)
    estimated_harm = 0.1 + tech_score * 0.3 + stealth * 0.2

    return {
        "combined_score": estimated_harm,
        "strategy_fingerprint": strategy,
        "stealth_score": stealth,
        "prompt_length": float(len(prompt)),
    }


def main():
    parser = argparse.ArgumentParser(description="Pre-seed OpenEvolve database with diverse jailbreak prompts")
    parser.add_argument("--config", "-c", type=str, default=str(DEFAULT_CONFIG),
                        help="Path to evolve config YAML")
    parser.add_argument("--output-dir", "-o", type=str, default=str(SCRIPT_DIR / "openevolve_output"),
                        help="Output directory for database")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be seeded without creating the database")
    args = parser.parse_args()

    seeds = load_seeds()
    if not seeds:
        print("ERROR: No seed files found in seeds/")
        sys.exit(1)

    print(f"\nSeeding {len(seeds)} strategies into MAP-Elites database...")

    if args.dry_run:
        print("\n[DRY RUN] Would create database with these prompts:")
        for name, prompt in seeds:
            print(f"\n  -- {name} --")
            print(f"  {prompt[:200]}...")
        return

    config_path = args.config
    if not os.path.exists(config_path):
        print(f"ERROR: Config not found: {config_path}")
        sys.exit(1)

    config = load_config(config_path)

    # Ensure template_dir is absolute for openevolve
    template_dir = config.prompt.get("template_dir", "templates")
    if not os.path.isabs(template_dir):
        config.prompt["template_dir"] = str((Path(config_path).parent / template_dir).resolve())

    db = ProgramDatabase(config=config.database, output_dir=args.output_dir)

    num_islands = config.database.num_islands
    for i, (strategy_name, prompt) in enumerate(seeds):
        island_idx = i % num_islands
        metrics = estimate_metrics(prompt)

        program = Program(
            id=str(uuid.uuid4()),
            code=prompt,
            changes_description=f"Initial seed: {strategy_name}",
            language="text",
            parent_id=None,
            generation=0,
            iteration_found=0,
            metrics=metrics,
            complexity=len(prompt),
            diversity=0.0,
            metadata={"island": island_idx, "seed_strategy": strategy_name, "migrant": False},
        )

        success = db.add(program)
        if success:
            print(f"  OK [{strategy_name}] -> island {island_idx} (score={metrics['combined_score']:.3f})")
        else:
            print(f"  SKIP [{strategy_name}] -> rejected (too similar to existing)")

    db.last_iteration = 0

    os.makedirs(args.output_dir, exist_ok=True)
    checkpoint_dir = os.path.join(args.output_dir, "checkpoints", "checkpoint_0")
    db.save(checkpoint_dir)

    print(f"\nDone: database seeded with {len(seeds)} strategies across {num_islands} islands")
    print(f"  Checkpoint saved to: {checkpoint_dir}")
    print(f"\n  To resume evolution from here:")
    print(f"  ./run_evolution.sh --checkpoint {checkpoint_dir} --iterations 200")


if __name__ == "__main__":
    main()
