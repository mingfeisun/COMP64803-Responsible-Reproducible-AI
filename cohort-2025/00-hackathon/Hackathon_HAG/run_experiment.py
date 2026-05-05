"""
run_experiment.py — entry point.

Runs the Hagendorff et al. (2025) adversarial jailbreak experiment.
Benchmark items are processed in parallel using a thread pool (network I/O bound).

Usage:
    python run_experiment.py                          # full 70-item run
    python run_experiment.py --dry-run --verbose      # 1-item smoke test
    python run_experiment.py --n-prompts 10           # subset
    python run_experiment.py --augment-attacker       # inject top-30 openers + free first turn
"""

import csv as csv_mod
import json
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from config import (
    ATTACKER_MODEL, TARGET_MODEL, JUDGE_MODEL,
    BENCHMARK_PATH, N_PROMPTS, MAX_TURNS, RESULTS_DIR, N_PARALLEL,
)
from attacker import Attacker
from defender import Defender
from judge import Judge
from experiment import run_exchange

# ---------------------------------------------------------------------------
# Thread-local worker ID (1, 2, 3 … N_PARALLEL)
# ---------------------------------------------------------------------------

_worker_counter = 0
_worker_counter_lock = threading.Lock()
_thread_local = threading.local()


def _worker_id() -> int:
    global _worker_counter
    if not hasattr(_thread_local, "id"):
        with _worker_counter_lock:
            _worker_counter += 1
            _thread_local.id = _worker_counter
    return _thread_local.id


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def load_benchmark(path: str, n: int) -> list[dict]:
    with open(path) as f:
        items = json.load(f)
    return items[:n]


def load_augment_prompts(path: str) -> list[str]:
    with open(path, newline="", encoding="utf-8") as f:
        return [row["prompt"] for row in csv_mod.DictReader(f)]


def get_run_dir(run_id: str) -> Path:
    run_dir = Path(RESULTS_DIR) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def save_jsonl(record: dict, filepath: Path):
    with open(filepath, "a") as f:
        f.write(json.dumps(record) + "\n")


def save_transcript(result, filepath: Path):
    SEP = "=" * 72
    DIV = "─" * 72
    status = "SUCCESS" if result.attack_success else "FAILED"
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"\n{SEP}\n")
        f.write(f"Item #{result.item_id}  |  {result.item_category}\n")
        f.write(f"Prompt  : {result.item_prompt}\n")
        f.write(f"Attacker: {result.attacker_model}  |  Target: {result.target_model}\n")
        f.write(f"Result  : {status}  |  max_harm={result.max_harm_score}/5  |  turns={result.n_turns}\n")
        f.write(f"{SEP}\n")
        for turn in result.turns:
            f.write(f"\nTurn {turn.turn}\n{DIV}\n")
            f.write(f"[ATTACKER]\n{turn.attacker_message}\n\n")
            f.write(f"[TARGET]\n{turn.target_response}\n\n")
            f.write(f"[JUDGE]  harm={turn.harm_score}  |  disclaimer={turn.disclaimer}  |  refusal={turn.refusal}\n")
        f.write(f"\n{SEP}\n")


def save_csv(records: list[dict], filepath: Path):
    if not records:
        return
    exclude = {"turns"}
    keys = [k for k in records[0] if k not in exclude]
    with open(filepath, "w", newline="") as f:
        writer = csv_mod.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in records:
            writer.writerow({k: r[k] for k in keys})


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

def _run_item(
    item: dict,
    idx: int,
    n_total: int,
    a_params: tuple,
    t_params: tuple,
    j_params: tuple,
    augment_prompts: list[str] | None,
    max_turns: int,
    verbose: bool,
    raw_log_path: Path,
    transcript_path: Path,
    write_lock: threading.Lock,
    print_lock: threading.Lock,
) -> dict:
    """Run one exchange and append results to shared output files."""
    wid = _worker_id()

    with print_lock:
        print(f"  [Worker {wid}] → item #{item['id']} ({item['category']}): "
              f"{item['prompt'][:60]}...")

    a_id, a_name, a_size = a_params
    attacker = Attacker(a_id, a_name, a_size, augment_prompts=augment_prompts)
    defender = Defender(*t_params)
    judge    = Judge(*j_params)

    result = run_exchange(attacker, defender, judge, item, max_turns, verbose)
    record = result.to_dict()

    with write_lock:
        save_jsonl(record, raw_log_path)
        save_transcript(result, transcript_path)

    trajectory_str = " ".join(str(h) for h in result.harm_trajectory)
    status = "SUCCESS" if result.attack_success else "FAILED"
    with print_lock:
        print(f"  [Worker {wid}] ✓ item #{item['id']} "
              f"max_harm={result.max_harm_score} | {status} | "
              f"trajectory=[{trajectory_str}] | {result.duration_seconds:.1f}s")

    return record


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Hagendorff et al. jailbreak experiment")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run only 1 benchmark item (pipeline smoke test)")
    parser.add_argument("--n-prompts", type=int, default=None,
                        help="Override number of benchmark items to run")
    parser.add_argument("--verbose", action="store_true",
                        help="Print turn-by-turn output (only useful with --dry-run or N_PARALLEL=1)")
    parser.add_argument("--augment-attacker", action="store_true",
                        help="Inject top-30 high-harm openers into the attacker system prompt "
                             "and let the attacker generate its own first message")
    args = parser.parse_args()

    n = 1 if args.dry_run else (args.n_prompts or N_PROMPTS)
    items = load_benchmark(BENCHMARK_PATH, n)

    augment_prompts = None
    if args.augment_attacker:
        csv_path = Path(__file__).parent / "prompts" / "top30_prompts_by_harm.csv"
        augment_prompts = load_augment_prompts(str(csv_path))
        print(f"Augmented attacker: loaded {len(augment_prompts)} opening strategies.")

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.augment_attacker:
        run_id += "_augmented"
    run_dir = get_run_dir(run_id)
    raw_log_path    = run_dir / "raw_logs.jsonl"
    summary_path    = run_dir / "summary.csv"
    transcript_path = run_dir / "conversations.txt"

    a_id, a_name, a_size = ATTACKER_MODEL
    t_id, t_name, t_size = TARGET_MODEL
    j_id, j_name, _      = JUDGE_MODEL

    workers = min(N_PARALLEL, len(items))
    a_size_str = f"{a_size}B" if a_size is not None else "API"
    t_size_str = f"{t_size}B" if t_size is not None else "API"

    print(f"Run      : {run_id}")
    print(f"Attacker : {a_name} ({a_size_str})  [OpenRouter]"
          + (" + augmented openers" if augment_prompts else ""))
    print(f"Target   : {t_name} ({t_size_str})  [OpenRouter]")
    print(f"Judge    : {j_name} ({a_size_str})  [OpenRouter]")
    print(f"Turns    : {MAX_TURNS}")
    print(f"Items    : {len(items)}")
    print(f"Workers  : {workers}")
    print(f"Results  : {run_dir}\n")

    verbose = args.verbose and workers == 1
    if args.verbose and workers > 1:
        print("Note: --verbose suppressed with N_PARALLEL > 1 (output would interleave)\n")

    a_params = (a_id, a_name, a_size)
    t_params = (t_id, t_name, t_size)
    j_params = (j_id, j_name)

    write_lock = threading.Lock()
    print_lock = threading.Lock()

    all_results: list[dict] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_item,
                item, i + 1, len(items),
                a_params, t_params, j_params,
                augment_prompts,
                MAX_TURNS, verbose,
                raw_log_path, transcript_path,
                write_lock, print_lock,
            ): item
            for i, item in enumerate(items)
        }
        for future in as_completed(futures):
            try:
                all_results.append(future.result())
            except Exception as e:
                item = futures[future]
                print(f"[ERROR] Item #{item['id']} failed: {e}")

    all_results.sort(key=lambda r: r["item_id"])
    save_csv(all_results, summary_path)

    n_success = sum(1 for r in all_results if r["attack_success"])
    asr = 100 * n_success / len(all_results) if all_results else 0.0
    print(f"\nDone. ASR = {n_success}/{len(all_results)} ({asr:.1f}%)")
    print(f"Raw logs    : {raw_log_path}")
    print(f"Summary     : {summary_path}")
    print(f"Transcripts : {transcript_path}")


if __name__ == "__main__":
    main()