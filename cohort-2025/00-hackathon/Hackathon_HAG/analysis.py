"""
analysis.py — plot harm trajectories from a completed experiment run.

Usage:
    python analysis.py 20260430_173957
    python analysis.py 20260430_173957 --show      # also open the plot interactively

Plots are saved to results/{run_id}/plots/
"""

import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_records(run_id: str) -> list[dict]:
    path = Path("results") / run_id / "raw_logs.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"No results found at {path}")
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------

STYLE = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.color": "#e0e0e0",
    "grid.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "sans-serif",
}


def harm_trajectory_plot(records: list[dict], run_id: str, out_dir: Path, show: bool):
    """
    Single-line plot: mean ± 1 std of harm score per turn across all benchmark items.
    Matches the style of Figure 2 in Hagendorff et al. (2025).
    """
    # Stack trajectories — shape (n_items, n_turns)
    trajectories = np.array([r["harm_trajectory"] for r in records])
    n_items, n_turns = trajectories.shape
    turns = np.arange(1, n_turns + 1)

    mean = trajectories.mean(axis=0)
    std  = trajectories.std(axis=0)

    attacker = records[0]["attacker_model"]
    target   = records[0]["target_model"]

    n_success = sum(r["attack_success"] for r in records)
    asr = 100 * n_success / n_items

    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(7, 4.5))

        ax.plot(turns, mean, color="#d62728", linewidth=2.2, label=target)
        ax.fill_between(turns, mean - std, mean + std,
                        color="#d62728", alpha=0.18)

        ax.set_xlim(1, n_turns)
        ax.set_ylim(0, 5.2)
        ax.set_xlabel("Turn", fontsize=12)
        ax.set_ylabel("Harm Score", fontsize=12)
        ax.set_title(f"Harm trajectory — Attacker: {attacker}", fontsize=13, pad=10)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        # Annotation box: ASR and item count
        info = f"n = {n_items} items\nASR = {n_success}/{n_items} ({asr:.0f}%)"
        ax.text(0.97, 0.97, info,
                transform=ax.transAxes,
                ha="right", va="top", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          edgecolor="#cccccc", linewidth=0.8))

        ax.legend(loc="upper right", bbox_to_anchor=(0.97, 0.80), fontsize=9,
                  framealpha=0.9, edgecolor="#cccccc")

        fig.tight_layout()

        out_path = out_dir / "harm_trajectory.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {out_path}")

        if show:
            plt.show()
        plt.close(fig)


def harm_trajectory_by_category(records: list[dict], run_id: str, out_dir: Path, show: bool):
    """
    One subplot per benchmark category, each showing mean ± std harm trajectory.
    """
    from collections import defaultdict

    by_cat: dict[str, list] = defaultdict(list)
    for r in records:
        by_cat[r["item_category"]].append(r["harm_trajectory"])

    categories = sorted(by_cat)
    n_cats = len(categories)
    ncols = min(3, n_cats)
    nrows = (n_cats + ncols - 1) // ncols

    attacker = records[0]["attacker_model"]
    target   = records[0]["target_model"]

    colors = plt.cm.tab10.colors

    with plt.rc_context(STYLE):
        fig, axes = plt.subplots(nrows, ncols,
                                 figsize=(5.5 * ncols, 4 * nrows),
                                 sharey=True)
        axes = np.array(axes).flatten()

        for idx, cat in enumerate(categories):
            ax = axes[idx]
            trajs = np.array(by_cat[cat])
            n_items = len(trajs)
            turns = np.arange(1, trajs.shape[1] + 1)
            mean = trajs.mean(axis=0)
            std  = trajs.std(axis=0)

            color = colors[idx % len(colors)]
            ax.plot(turns, mean, color=color, linewidth=2.0)
            ax.fill_between(turns, mean - std, mean + std,
                            color=color, alpha=0.18)

            n_success = sum(
                1 for r in records
                if r["item_category"] == cat and r["attack_success"]
            )
            asr = 100 * n_success / n_items

            ax.set_title(f"{cat}\n(n={n_items}, ASR={asr:.0f}%)", fontsize=10)
            ax.set_xlim(1, trajs.shape[1])
            ax.set_ylim(0, 5.2)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
            if idx % ncols == 0:
                ax.set_ylabel("Harm Score", fontsize=10)
            ax.set_xlabel("Turn", fontsize=10)

        # Hide unused axes
        for idx in range(n_cats, len(axes)):
            axes[idx].set_visible(False)

        fig.suptitle(
            f"Harm trajectories by category\nAttacker: {attacker}  |  Target: {target}",
            fontsize=12, y=1.01,
        )
        fig.tight_layout()

        out_path = out_dir / "harm_trajectory_by_category.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {out_path}")

        if show:
            plt.show()
        plt.close(fig)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Plot harm trajectories for an experiment run")
    parser.add_argument("run_id", help="Run ID under results/, e.g. 20260430_173957")
    parser.add_argument("--show", action="store_true", help="Open plots interactively")
    args = parser.parse_args()

    records = load_records(args.run_id)
    print(f"Loaded {len(records)} records from run {args.run_id}")

    out_dir = Path("results") / args.run_id / "plots"
    out_dir.mkdir(parents=True, exist_ok=True)

    harm_trajectory_plot(records, args.run_id, out_dir, args.show)

    categories = {r["item_category"] for r in records}
    if len(categories) > 1:
        harm_trajectory_by_category(records, args.run_id, out_dir, args.show)
    else:
        print(f"Only one category present ({next(iter(categories))}) — skipping per-category plot.")

    n_success = sum(r["attack_success"] for r in records)
    print(f"\nASR: {n_success}/{len(records)} ({100*n_success/len(records):.1f}%)")


if __name__ == "__main__":
    main()