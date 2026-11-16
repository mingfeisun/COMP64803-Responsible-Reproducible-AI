"""Wiener-Hopf Monte Carlo (Kuznetsov, Kyprianou, Pardo & van Schaik, 2011).

Idea: instead of looking at the path on a fixed time grid (and missing
barrier crossings between grid points), stop the process at an
independent exponential time e_q with rate q. The Wiener-Hopf
factorisation says that at that time

    sup_{s <= e_q} X_s            ~ Exp(phi_plus)       (the maximum)
    X_{e_q} - sup_{s <= e_q} X_s  ~ -Exp(phi_minus)     (the drop after it)

and the two are independent. So one exponential "step" can be simulated
*exactly*, including its maximum, with two exponential random numbers.

Chaining n such steps with q = n / T reaches the random time
g_n ~ Gamma(n, rate n / T), which has mean T and concentrates at T as n
grows. The output (X_{g_n}, max_{s <= g_n} X_s) therefore converges to the
pair needed for barrier options, (X_T, max_{s <= T} X_s).

For Brownian motion with drift mu and volatility sigma (Black-Scholes in
log-space) the factors are explicit: they are the roots of
    mu * theta + sigma^2 theta^2 / 2 = q.
"""

import math

import numpy as np


def wiener_hopf_factors(mu, sigma, q):
    """Return (phi_plus, phi_minus) for X_t = mu t + sigma W_t killed at rate q.

    The textbook roots are (sqrt(mu^2 + 2 q sigma^2) -/+ mu) / sigma^2. One of
    them subtracts two nearly equal numbers when q is small, which throws
    away significant digits (catastrophic cancellation). We use the identity
    (root - mu)(root + mu) = 2 q sigma^2 to compute that root as a ratio of
    sums instead, so both factors are accurate for any q > 0.
    """
    if q <= 0 or sigma <= 0:
        raise ValueError(f"need q > 0 and sigma > 0, got q={q}, sigma={sigma}")
    root = math.hypot(mu, sigma * math.sqrt(2.0 * q))  # sqrt(mu^2 + 2 q sigma^2), no overflow
    if mu >= 0:
        return 2.0 * q / (root + mu), (root + mu) / sigma**2
    return (root - mu) / sigma**2, 2.0 * q / (root - mu)


def simulate_whmc(mu, sigma, maturity, *, n_steps, n_paths, rng, direction="up"):
    """Simulate n_paths paths of (X at the random horizon, running max or min).

    Parameters are keyword-only: n_steps and n_paths are both integers, and
    swapping them by position would run without error but give a wrong answer.

    direction="up" tracks the maximum (for up-and-out barriers);
    direction="down" tracks the minimum (for down-and-out barriers),
    using the dual factorisation (fall to the minimum first, then rise).

    Returns two arrays of shape (n_paths,), in log-price units (X_0 = 0).
    """
    if direction not in ("up", "down"):
        raise ValueError(f"direction must be 'up' or 'down', got {direction!r}")
    q = n_steps / maturity  # so the n exponential steps add up to T on average
    phi_plus, phi_minus = wiener_hopf_factors(mu, sigma, q)
    x = np.zeros(n_paths)
    extreme = np.zeros(n_paths)
    for _ in range(n_steps):
        if direction == "up":
            x += rng.exponential(1.0 / phi_plus, n_paths)    # climb to this step's maximum
            np.maximum(extreme, x, out=extreme)              # record it (exact, nothing missed)
            x -= rng.exponential(1.0 / phi_minus, n_paths)   # then fall back, independently
        else:
            x -= rng.exponential(1.0 / phi_minus, n_paths)   # fall to this step's minimum
            np.minimum(extreme, x, out=extreme)
            x += rng.exponential(1.0 / phi_plus, n_paths)
    return x, extreme
