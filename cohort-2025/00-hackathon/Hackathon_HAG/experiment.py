"""
experiment.py — Hagendorff et al. (2025) setup.

Runs a single adversarial exchange: attacker vs target vs judge, for one
benchmark item. Returns a full result including the per-turn harm trajectory
(matching Figure 2 of the paper).

Flow per exchange:
    1. Attacker sends "Hi!" → target responds → judge scores (turn 1)
    2. Attacker generates response → target responds → judge scores (turn 2)
    ...repeat up to MAX_TURNS.
"""

import time
from dataclasses import dataclass, field, asdict

from attacker import Attacker
from defender import Defender
from judge import Judge
from config import MAX_TURNS, HARM_THRESHOLD


@dataclass
class TurnLog:
    turn: int
    attacker_message: str
    target_response: str
    harm_score: int
    disclaimer: bool
    refusal: bool


@dataclass
class ExchangeResult:
    """Complete result for one (attacker, target, benchmark_item) run."""
    attacker_model: str
    attacker_size_b: float
    target_model: str
    target_size_b: float
    item_id: int
    item_category: str
    item_prompt: str

    # Per-turn harm trajectory (one score per turn, 0-5)
    harm_trajectory: list = field(default_factory=list)

    # Summary metrics
    max_harm_score: int = 0       # peak harm across all turns
    attack_success: bool = False  # max_harm_score == 5
    n_turns: int = 0

    # Full turn logs
    turns: list = field(default_factory=list)

    duration_seconds: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


def run_exchange(
    attacker: Attacker,
    defender: Defender,
    judge: Judge,
    item: dict,
    max_turns: int = MAX_TURNS,
    verbose: bool = False,
) -> ExchangeResult:
    """
    Run one full adversarial exchange.

    Args:
        attacker:  Attacker instance
        defender:  Defender (target) instance
        judge:     Judge instance
        item:      Dict with keys: id, category, prompt (from benchmark)
        max_turns: Number of turns (default 10, matching paper)
        verbose:   Print turn-by-turn progress to stdout

    Returns:
        ExchangeResult with harm trajectory and full logs.
    """
    t_start = time.time()

    result = ExchangeResult(
        attacker_model=attacker.display_name,
        attacker_size_b=attacker.size_b,
        target_model=defender.display_name,
        target_size_b=defender.size_b,
        item_id=item["id"],
        item_category=item["category"],
        item_prompt=item["prompt"],
    )

    attacker.reset(item["prompt"])
    defender.reset()

    # Turn 1: hardcoded opener "Hi!"
    attacker_message = attacker.first_message()

    for turn in range(1, max_turns + 1):
        if verbose:
            print(f"\n  --- Turn {turn}/{max_turns} ---")
            print(f"  [Attacker]: {attacker_message[:120]}")

        # Target responds
        target_response = defender.respond(attacker_message)

        if verbose:
            print(f"  [Target]:   {target_response[:120]}")

        # Judge scores this turn's response
        judgment = judge.score(item["prompt"], target_response)

        if verbose:
            print(f"  [Judge]:    harm={judgment['harm']} | disclaimer={judgment['disclaimer']} | refusal={judgment['refusal']}")

        result.harm_trajectory.append(judgment["harm"])
        result.turns.append(TurnLog(
            turn=turn,
            attacker_message=attacker_message,
            target_response=target_response,
            harm_score=judgment["harm"],
            disclaimer=judgment["disclaimer"],
            refusal=judgment["refusal"],
        ))
        result.n_turns = turn

        # Early stopping: maximum harm achieved
        if judgment["harm"] >= HARM_THRESHOLD:
            if verbose:
                print(f"  [Judge]:    Maximum harm score reached — stopping early.")
            break

        # Attacker generates next message (unless this was the last turn)
        if turn < max_turns:
            attacker_message = attacker.generate(target_response)

    result.max_harm_score = max(result.harm_trajectory) if result.harm_trajectory else 0
    result.attack_success = result.max_harm_score >= HARM_THRESHOLD
    result.duration_seconds = time.time() - t_start

    return result
