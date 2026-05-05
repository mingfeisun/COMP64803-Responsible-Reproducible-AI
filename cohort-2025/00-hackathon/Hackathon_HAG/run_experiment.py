"""
run_experiment.py — entry point.

Runs the Hagendorff et al. (2025) adversarial jailbreak experiment:
    Attacker: Qwen2.5-32B  →  Target: Qwen2.5-1.5B

Saves results incrementally to JSONL (full logs) and CSV (summary).

Usage:
    # Full run (all 70 benchmark items)
    python run_experiment.py

    # Quick smoke test (1 item)
    python run_experiment.py --dry-run --verbose

    # Subset of benchmark
    python run_experiment.py --n-prompts 10 --verbose
"""

import json
import csv
import argparse
from datetime import datetime
from pathlib import Path

from config import (
    ATTACKER_MODEL, TARGET_MODEL, JUDGE_MODEL,
    BENCHMARK_PATH, N_PROMPTS, MAX_TURNS, RESULTS_DIR,
)
from attacker import Attacker
from defender import Defender
from judge import Judge
from experiment import run_exchange


def load_benchmark(path: str, n: int) -> list[dict]:
    with open(path) as f:
        items = json.load(f)
    return items[:n]


def get_run_dir(run_id: str) -> Path:
    run_dir = Path(RESULTS_DIR) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def save_jsonl(record: dict, filepath: Path):
    with open(filepath, "a") as f:
        f.write(json.dumps(record) + "\n")


def save_csv(records: list[dict], filepath: Path):
    if not records:
        return
    exclude = {"turns"}  # too verbose for CSV
    keys = [k for k in records[0] if k not in exclude]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in records:
            writer.writerow({k: r[k] for k in keys})


def main():
    parser = argparse.ArgumentParser(description="Hagendorff et al. jailbreak experiment")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run only 1 benchmark item (pipeline smoke test)")
    parser.add_argument("--n-prompts", type=int, default=None,
                        help="Override number of benchmark items to run")
    parser.add_argument("--verbose", action="store_true",
                        help="Print turn-by-turn output")
    args = parser.parse_args()

    n = 1 if args.dry_run else (args.n_prompts or N_PROMPTS)
    items = load_benchmark(BENCHMARK_PATH, n)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = get_run_dir(run_id)
    raw_log_path = run_dir / "raw_logs.jsonl"
    summary_path = run_dir / "summary.csv"

    a_id, a_name, a_size = ATTACKER_MODEL
    t_id, t_name, t_size = TARGET_MODEL
    j_id, j_name, _      = JUDGE_MODEL

    print(f"Run: {run_id}")
    print(f"Attacker : {a_name} ({a_size}B)  [port 8000]")
    print(f"Target   : {t_name} ({t_size}B)  [port 8001]")
    print(f"Judge    : {j_name}              [port 8000]")
    print(f"Turns    : {MAX_TURNS}")
    print(f"Items    : {len(items)}")
    print(f"Results  : {run_dir}\n")

    attacker = Attacker(a_id, a_name, a_size)
    defender = Defender(t_id, t_name, t_size)
    judge    = Judge(j_id, j_name)

    all_results = []

    for i, item in enumerate(items):
        print(f"[{i+1}/{len(items)}] #{item['id']} ({item['category']}): {item['prompt'][:70]}...")

        result = run_exchange(
            attacker=attacker,
            defender=defender,
            judge=judge,
            item=item,
            max_turns=MAX_TURNS,
            verbose=args.verbose,
        )

        record = result.to_dict()
        all_results.append(record)
        save_jsonl(record, raw_log_path)

        trajectory_str = " ".join(str(h) for h in result.harm_trajectory)
        status = "SUCCESS" if result.attack_success else "FAILED"
        print(f"  → max_harm={result.max_harm_score} | {status} | turns={result.n_turns} | trajectory=[{trajectory_str}] | {result.duration_seconds:.1f}s")

    save_csv(all_results, summary_path)

    n_success = sum(1 for r in all_results if r["attack_success"])
    asr = 100 * n_success / len(all_results) if all_results else 0.0
    print(f"\nDone. ASR = {n_success}/{len(all_results)} ({asr:.1f}%)")
    print(f"Raw logs : {raw_log_path}")
    print(f"Summary  : {summary_path}")


if __name__ == "__main__":
    main()
