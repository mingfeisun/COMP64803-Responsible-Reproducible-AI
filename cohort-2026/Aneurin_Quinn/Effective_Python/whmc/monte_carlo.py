"""Monte Carlo estimators for knock-out barrier calls.

* grid_mc_price   - the textbook method: exact GBM on a time grid, barrier
                    checked only at grid points (biased: misses crossings).
* whmc_price      - Wiener-Hopf Monte Carlo: the maximum is sampled exactly
                    over each random exponential step.
* bridge_mc_price - grid MC with a Brownian-bridge correction; used as an
                    independent check of the closed-form price in the tests.

All estimators take their simulation sizes as keyword-only arguments.
"""

import math
from dataclasses import dataclass

import numpy as np

from .wiener_hopf import simulate_whmc


@dataclass(frozen=True)
class Estimate:
    price: float
    stderr: float  # standard error of the mean, not the payoff spread
    n_paths: int

    def __str__(self):
        return f"{self.price:.4f} +/- {1.96 * self.stderr:.4f}"  # 95% interval


def _check_sizes(n_steps, n_paths):
    if n_steps < 1 or n_paths < 2:
        raise ValueError(f"need n_steps >= 1 and n_paths >= 2, got {n_steps}, {n_paths}")


def _summarise(discounted_payoffs):
    n = discounted_payoffs.size
    if n < 2:  # no spread yet: report "infinitely uncertain"
        return Estimate(float("nan"), float("inf"), n)
    return Estimate(float(discounted_payoffs.mean()),
                    float(discounted_payoffs.std(ddof=1) / math.sqrt(n)), n)


def _knock_out_payoff(market, option, x_end, extreme):
    log_barrier = math.log(option.barrier / market.spot)  # compare in log space, like the simulation
    alive = extreme < log_barrier if option.is_up else extreme > log_barrier
    payoff = np.maximum(market.spot * np.exp(x_end) - option.strike, 0.0)
    return math.exp(-market.rate * market.maturity) * payoff * alive


def _whmc_payoffs(market, option, *, n_steps, n_paths, rng):
    _check_sizes(n_steps, n_paths)
    x_end, extreme = simulate_whmc(market.drift, market.vol, market.maturity,
                                   n_steps=n_steps, n_paths=n_paths, rng=rng,
                                   direction="up" if option.is_up else "down")
    return _knock_out_payoff(market, option, x_end, extreme)


def whmc_price(market, option, *, n_steps, n_paths, rng):
    return _summarise(_whmc_payoffs(market, option, n_steps=n_steps, n_paths=n_paths, rng=rng))


def _grid_paths(market, *, n_steps, n_paths, rng):
    """Exact GBM log-prices at n_steps equally spaced times; shape (n_paths, n_steps + 1)."""
    _check_sizes(n_steps, n_paths)
    dt = market.maturity / n_steps
    increments = (market.drift * dt
                  + market.vol * math.sqrt(dt) * rng.standard_normal((n_paths, n_steps)))
    x = np.cumsum(increments, axis=1)
    return np.hstack([np.zeros((n_paths, 1)), x]), dt


def grid_mc_price(market, option, *, n_steps, n_paths, rng):
    x, _ = _grid_paths(market, n_steps=n_steps, n_paths=n_paths, rng=rng)
    extreme = x.max(axis=1) if option.is_up else x.min(axis=1)  # only sees grid points
    return _summarise(_knock_out_payoff(market, option, x[:, -1], extreme))


def bridge_mc_price(market, option, *, n_steps, n_paths, rng):
    """Grid MC weighted by the exact probability of not crossing between grid points."""
    x, dt = _grid_paths(market, n_steps=n_steps, n_paths=n_paths, rng=rng)
    b = math.log(option.barrier / market.spot)
    dist = (b - x) if option.is_up else (x - b)  # distance to the barrier, > 0 while alive
    left, right = dist[:, :-1], dist[:, 1:]
    # P(bridge crosses) = exp(-a) with a = 2 * left * right / (sigma^2 dt), so
    # P(no cross) = 1 - exp(-a). For small a that subtraction loses digits;
    # -expm1(-a) computes the same number in one accurate step.
    a = 2.0 * np.clip(left, 0, None) * np.clip(right, 0, None) / (market.vol**2 * dt)
    survive = np.where((left > 0) & (right > 0), -np.expm1(-a), 0.0).prod(axis=1)
    payoff = np.maximum(market.spot * np.exp(x[:, -1]) - option.strike, 0.0)
    return _summarise(math.exp(-market.rate * market.maturity) * payoff * survive)


def whmc_price_to_tolerance(market, option, *, n_steps, target_stderr, rng,
                            batch_size=20_000, max_paths=2_000_000):
    """Choose the number of paths automatically: simulate batches until the
    standard error is below target_stderr (or max_paths is reached)."""
    payoffs = np.empty(0)
    while ((estimate := _summarise(payoffs)).stderr > target_stderr
           and payoffs.size < max_paths):
        batch = _whmc_payoffs(market, option, n_steps=n_steps, n_paths=batch_size, rng=rng)
        payoffs = np.concatenate([payoffs, batch])
    return estimate
