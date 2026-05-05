#!/usr/bin/env python3
"""
GamePlan Evolution Runner (Python entry point).

Reads all configuration from evolve_config.yaml — no .env file needed.

Usage:
  python run_evolution_direct.py --iterations 200
  python run_evolution_direct.py --config my_config.yaml --iterations 500

Requires: pip install openevolve openai pyyaml
"""

import argparse
import csv
import json
import os
import sys
import tempfile
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent.resolve()
DEFAULT_CONFIG = SCRIPT_DIR / "evolve_config.yaml"


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def set_env_from_config(config: dict) -> None:
    """Set environment variables needed by evaluator.py subprocess."""
    api = config["api"]
    models = config["models"]
    experiment = config["experiment"]

    os.environ["OPENROUTER_API_KEY"] = api["openrouter_key"]

    os.environ["EVOLVER_API_BASE"] = config["llm"]["api_base"]
    os.environ["EVOLVER_API_KEY"] = api["openrouter_key"]
    os.environ["EVOLVER_MODEL"] = models["evolver"]["name"]

    os.environ["TARGET_API_BASE"] = models["target"].get("api_base", api["openrouter_base"])
    os.environ["TARGET_API_KEY"] = api["openrouter_key"]
    os.environ["TARGET_MODEL"] = models["target"]["name"]
    os.environ["TARGET_MAX_TOKENS"] = str(models["target"].get("max_tokens", 4096))

    os.environ["JUDGE_API_BASE"] = models["judge"].get("api_base", api["openrouter_base"])
    os.environ["JUDGE_API_KEY"] = api["openrouter_key"]
    os.environ["JUDGE_MODEL"] = models["judge"]["name"]
    os.environ["JUDGE_MAX_TOKENS"] = str(models["judge"].get("max_tokens", 512))
    os.environ["GAMEPLAN_VERBOSE"] = "1" if experiment.get("verbose", False) else "0"


def write_resolved_config(config: dict, output_path: str) -> None:
    """Write an openevolve-compatible config with absolute paths."""
    resolved = dict(config)

    # Resolve template_dir relative to script dir
    template_dir = resolved.get("prompt", {}).get("template_dir", "templates")
    if not os.path.isabs(template_dir):
        resolved["prompt"]["template_dir"] = str((SCRIPT_DIR / template_dir).resolve())

    # Remove our custom sections that openevolve doesn't need
    for key in ["api", "models", "experiment"]:
        resolved.pop(key, None)

    with open(output_path, 'w') as f:
        yaml.dump(resolved, f, default_flow_style=False, sort_keys=False)


def _extract_top_k(output_dir: Path, k: int = 10) -> list[dict]:
    """Read latest checkpoint population and return top-k programs by combined_score."""
    ckpt_dir = output_dir / "checkpoints"
    if not ckpt_dir.is_dir():
        return []
    ckpts = sorted(
        [d for d in os.listdir(str(ckpt_dir)) if d.startswith("checkpoint_")],
        key=lambda d: int(d.split("_")[1]), reverse=True,
    )
    if not ckpts:
        return []
    programs_dir = ckpt_dir / ckpts[0] / "programs"
    if not programs_dir.is_dir():
        return []

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
    parser = argparse.ArgumentParser(description="GamePlan — Evolve jailbreak prompts via OpenEvolve")
    parser.add_argument("--config", "-c", type=str, default=str(DEFAULT_CONFIG),
                        help="Path to evolve config YAML")
    parser.add_argument("--iterations", "-i", type=int, default=None,
                        help="Number of evolution iterations (overrides config)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output directory for results")
    parser.add_argument("--checkpoint", type=str, default=None,
                        help="Resume from checkpoint directory")
    parser.add_argument("--log-level", type=str, default=None,
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--top-k", type=int, default=10,
                        help="Number of top programs to extract from population (default: 10)")
    args = parser.parse_args()

    config = load_config(args.config)
    set_env_from_config(config)

    iterations = args.iterations or config.get("max_iterations", 200)
    log_level = args.log_level or config.get("log_level", "INFO")

    print(f"Evolver: {config['models']['evolver']['name']} @ {config['llm']['api_base']}")
    print(f"Target:  {config['models']['target']['name']} @ {config['models']['target'].get('api_base', config['api']['openrouter_base'])}")
    print(f"Judge:   {config['models']['judge']['name']}")
    print(f"Iterations: {iterations}")
    print()

    # Write resolved config for openevolve
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
        resolved_config_path = tmp.name
    write_resolved_config(config, resolved_config_path)

    # Run OpenEvolve
    try:
        from openevolve.cli import main as openevolve_main
    except ImportError:
        print("ERROR: openevolve not installed. Run: pip install openevolve")
        sys.exit(1)

    sys.argv = [
        "openevolve",
        str(SCRIPT_DIR / "initial_jailbreak_prompt.txt"),
        str(SCRIPT_DIR / "evaluator.py"),
        "--config", resolved_config_path,
        "--iterations", str(iterations),
        "--log-level", log_level,
    ]
    if args.output:
        sys.argv.extend(["--output", args.output])
    if args.checkpoint:
        sys.argv.extend(["--checkpoint", args.checkpoint])

    exit_code = openevolve_main()

    # Cleanup
    try:
        os.unlink(resolved_config_path)
    except OSError:
        pass

    # Output results
    result_dir = Path(args.output or str(SCRIPT_DIR / "openevolve_output"))

    # Show best prompt
    best_file = result_dir / "best" / "best_program.txt"
    best_info_file = result_dir / "best" / "best_program_info.json"
    if best_file.exists():
        print("\n" + "=" * 70)
        print("  BEST JAILBREAK PROMPT:")
        print("=" * 70)
        print(best_file.read_text())
        print("=" * 70)

    # Write best prompt stats CSV
    if best_info_file.exists():
        with open(best_info_file) as f:
            info = json.load(f)
        metrics = info.get("metrics", {})
        stats = {
            "program_id": info.get("id", ""),
            "generation": info.get("generation", 0),
            "iteration_found": info.get("iteration", 0),
            "combined_score": metrics.get("combined_score", 0),
            "avg_harm": metrics.get("avg_harm", 0),
            "success_rate": metrics.get("success_rate", 0),
            "refusal_rate": metrics.get("refusal_rate", 1),
            "strategy_fingerprint": int(metrics.get("strategy_fingerprint", 0)),
            "stealth_score": metrics.get("stealth_score", 0),
            "prompt_length": metrics.get("prompt_length", 0),
        }
        stats_path = result_dir / "best_prompt_stats.csv"
        with open(stats_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(stats.keys()))
            writer.writeheader()
            writer.writerow(stats)
        print(f"\nBest prompt stats saved to: {stats_path}")

    # Write top-k prompts from population
    top_k = _extract_top_k(result_dir, k=args.top_k)
    if top_k:
        tk_path = result_dir / "top_k_prompts.csv"
        tk_fields = ["program_id", "generation", "iteration_found", "combined_score",
                     "avg_harm", "success_rate", "refusal_rate",
                     "strategy_fingerprint", "stealth_score", "prompt_length", "prompt_text"]
        with open(tk_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=tk_fields)
            writer.writeheader()
            writer.writerows(top_k)
        print(f"Top-{args.top_k} prompts saved to: {tk_path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
