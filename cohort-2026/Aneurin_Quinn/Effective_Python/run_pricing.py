"""Price an up-and-out barrier call with Wiener-Hopf Monte Carlo.

Compares three answers under Black-Scholes:
  * the exact closed-form price (continuous monitoring),
  * Wiener-Hopf Monte Carlo (WHMC), which samples the path maximum exactly,
  * plain grid Monte Carlo, which only checks the barrier at grid points.

Then chooses the simulation parameters from the results, checks the
small-number formulas, and saves a 300 dpi plot plus the run environment.

Usage:  python run_pricing.py [--paths N] [--seed S] [--strike K] [--barrier H] [--dpi D]
"""

import argparse
import importlib.metadata
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np

from whmc import (BarrierOption, Market, barrier_price, grid_mc_price, plot_convergence,
                  whmc_price, whmc_price_to_tolerance, wiener_hopf_factors)

MIN_PYTHON = (3, 10)                 # zip(strict=True) needs 3.10
STEPS = [4, 8, 16, 32, 64, 128, 256]  # doubling, so a log-scale plot is evenly spaced
TARGET_STDERR = 0.01                 # one cent on a ~3.33 price


# Reproducible environment ------------------------------------------------------

def check_python_version(minimum=MIN_PYTHON):
    if sys.version_info < minimum:
        raise RuntimeError(f"Python {'.'.join(map(str, minimum))}+ required, "
                           f"found {platform.python_version()}")


def run_metadata(seed):
    """Everything needed to reproduce the numbers: interpreter, libraries, seed."""
    return {
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "matplotlib": importlib.metadata.version("matplotlib"),
        "platform": platform.platform(),
        "seed": seed,
    }


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--paths", type=int, default=200_000, help="paths per convergence run")
    p.add_argument("--seed", type=int, default=2026, help="random seed (fixes every number)")
    p.add_argument("--strike", type=float, default=100.0)
    p.add_argument("--barrier", type=float, default=130.0)
    p.add_argument("--dpi", type=int, default=300, help="resolution of the saved PNG")
    p.add_argument("--outdir", type=Path, default=Path("results"))
    return p.parse_args(argv)


# Experiments ------------------------------------------------------------------------

def convergence_study(market, option, *, n_paths, seed):
    """Price with WHMC and grid MC at each step count in STEPS.

    Returns (steps, whmc estimates, grid estimates, (whmc s, grid s) timings).
    """
    rng = np.random.default_rng(seed)
    whmc_runs, grid_runs, timings = [], [], []
    for n in STEPS:
        t0 = time.perf_counter()
        whmc_runs.append(whmc_price(market, option, n_steps=n, n_paths=n_paths, rng=rng))
        t1 = time.perf_counter()
        grid_runs.append(grid_mc_price(market, option, n_steps=n, n_paths=n_paths, rng=rng))
        t2 = time.perf_counter()
        timings.append((t1 - t0, t2 - t1))
    return STEPS, whmc_runs, grid_runs, timings


def choose_steps(steps, estimates, exact):
    """Smallest step count whose bias is hidden by the Monte Carlo noise.

    More steps than this only costs time: the error is then dominated by the
    number of paths, not by the time discretisation.
    """
    for n, est in zip(steps, estimates, strict=True):
        if abs(est.price - exact) < 1.96 * est.stderr:
            return n
    return steps[-1]


def precision_checks(market):
    """Small-number formulas: the one-function version vs the naive one."""
    mu, sigma, q = market.drift, market.vol, 1e-14
    root = math.sqrt(mu**2 + 2 * q * sigma**2)
    naive_phi = (root - mu) / sigma**2
    stable_phi, _ = wiener_hopf_factors(mu, sigma, q)
    return [
        ("phi+ at q=1e-14", naive_phi, stable_phi),
        ("N(-10)", 0.5 * (1 + math.erf(-10 / math.sqrt(2))), 0.5 * math.erfc(10 / math.sqrt(2))),
        ("1 - exp(-1e-12)", 1 - math.exp(-1e-12), -math.expm1(-1e-12)),
    ]


def main(argv=None):
    check_python_version()
    args = parse_args(argv)
    market = Market()
    option = BarrierOption(strike=args.strike, barrier=args.barrier)
    exact = barrier_price(market, option)

    print(f"Up-and-out call: S0={market.spot:g}, K={option.strike:g}, H={option.barrier:g}, "
          f"r={market.rate:.0%}, sigma={market.vol:.0%}, T={market.maturity:g}y")
    print(f"Exact (closed form) price: {exact:.4f}\n")

    steps, whmc_runs, grid_runs, timings = convergence_study(
        market, option, n_paths=args.paths, seed=args.seed)

    print(f"{'steps':>5} | {'WHMC error':>11} | {'grid MC error':>13} | {'time WHMC / grid':>16}")
    print("-" * 56)
    rows = []
    for n, wh, gr, (t_wh, t_gr) in zip(steps, whmc_runs, grid_runs, timings, strict=True):
        print(f"{n:5d} | {wh.price - exact:+11.4f} | {gr.price - exact:+13.4f} | "
              f"{t_wh:6.2f}s / {t_gr:.2f}s")
        rows.append({"steps": n, "whmc": wh.price, "grid": gr.price,
                     "whmc_stderr": wh.stderr, "grid_stderr": gr.stderr})
    noise = 1.96 * whmc_runs[0].stderr
    print(f"(Monte Carlo noise: +/- {noise:.3f} at 95%)\n")

    # Choosing parameters: steps from the bias, paths from the target error
    n_steps = choose_steps(steps, whmc_runs, exact)
    adaptive = whmc_price_to_tolerance(market, option, n_steps=n_steps,
                                       target_stderr=TARGET_STDERR,
                                       rng=np.random.default_rng(args.seed + 1))
    print(f"Chosen steps: {n_steps} (smallest with bias inside the noise)")
    print(f"Chosen paths: {adaptive.n_paths:,} for stderr < {TARGET_STDERR} "
          f"-> price {adaptive}  (exact {exact:.4f})\n")

    print("Small numbers: naive formula vs one dedicated function")
    for name, naive, stable in precision_checks(market):
        print(f"  {name:<16} naive {naive:<24.17g} stable {stable:.17g}")

    files = plot_convergence(steps, [r["whmc"] - exact for r in rows],
                             [r["grid"] - exact for r in rows],
                             args.outdir / "convergence", dpi=args.dpi)
    out_json = args.outdir / "run.json"
    out_json.write_text(json.dumps({"metadata": run_metadata(args.seed), "exact": exact,
                                    "chosen": {"steps": n_steps, "paths": adaptive.n_paths},
                                    "convergence": rows}, indent=2))
    print(f"\nSaved {', '.join(str(f) for f in files)} ({args.dpi} dpi) and {out_json}")


if __name__ == "__main__":
    main()
