"""Black-Scholes model and closed-form prices for single-barrier calls.

Under the risk-neutral measure the stock is a geometric Brownian motion,
    S_t = S_0 exp(X_t),   X_t = mu t + sigma W_t,   mu = r - sigma^2 / 2.

Continuously monitored knock-out calls have closed-form prices
(Merton 1973; Reiner & Rubinstein 1991). We use them as the "exact"
answer that the Monte Carlo methods should reproduce.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Market:
    spot: float = 100.0
    rate: float = 0.05
    vol: float = 0.2
    maturity: float = 1.0

    @property
    def drift(self):
        """Drift of the log-price under the risk-neutral measure."""
        return self.rate - 0.5 * self.vol**2


@dataclass(frozen=True)
class BarrierOption:
    strike: float
    barrier: float
    kind: str = "up-and-out"  # or "down-and-out"

    def __post_init__(self):
        if self.kind not in ("up-and-out", "down-and-out"):
            raise ValueError(f"unknown barrier kind {self.kind!r}")

    @property
    def is_up(self):
        return self.kind == "up-and-out"


def norm_cdf(x):
    """Standard normal CDF.

    Written with erfc, not 0.5 * (1 + erf(x / sqrt 2)): for x far below 0 the
    "1 + erf" version adds a number very close to -1 to 1 and rounds to 0
    (e.g. N(-10) becomes 0.0 instead of 7.6e-24).
    """
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def vanilla_call(market, strike):
    s, r, v, t = market.spot, market.rate, market.vol, market.maturity
    vol_sqrt_t = v * math.sqrt(t)
    d1 = (math.log(s / strike) + (r + 0.5 * v**2) * t) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t
    return s * norm_cdf(d1) - strike * math.exp(-r * t) * norm_cdf(d2)


def _call_term(spot_weight, strike_weight, z, shift):
    """spot_weight * N(z) - strike_weight * N(z - shift).

    Every Reiner-Rubinstein building block has this one shape, so it is
    written once here instead of four times as a long inline expression.
    """
    return spot_weight * norm_cdf(z) - strike_weight * norm_cdf(z - shift)


def _reiner_rubinstein_terms(market, strike, barrier, eta):
    """The A, B, C, D building blocks of the Reiner-Rubinstein formulas (calls, no rebate)."""
    s, r, v, t = market.spot, market.rate, market.vol, market.maturity
    vol_sqrt_t = v * math.sqrt(t)
    mu = (r - 0.5 * v**2) / v**2
    shift = (1 + mu) * vol_sqrt_t

    x1 = math.log(s / strike) / vol_sqrt_t + shift
    x2 = math.log(s / barrier) / vol_sqrt_t + shift
    y1 = math.log(barrier**2 / (s * strike)) / vol_sqrt_t + shift
    y2 = math.log(barrier / s) / vol_sqrt_t + shift

    discounted_strike = strike * math.exp(-r * t)
    h_s = barrier / s
    reflected_spot = s * h_s ** (2 * (mu + 1))           # weights for the "mirror image" terms
    reflected_strike = discounted_strike * h_s ** (2 * mu)

    a = _call_term(s, discounted_strike, x1, vol_sqrt_t)
    b = _call_term(s, discounted_strike, x2, vol_sqrt_t)
    c = _call_term(reflected_spot, reflected_strike, eta * y1, eta * vol_sqrt_t)
    d = _call_term(reflected_spot, reflected_strike, eta * y2, eta * vol_sqrt_t)
    return a, b, c, d


def barrier_price(market, option):
    """Exact price of a continuously monitored knock-out call."""
    k, h = option.strike, option.barrier
    if option.is_up:
        if market.spot >= h or k >= h:
            return 0.0
        a, b, c, d = _reiner_rubinstein_terms(market, k, h, eta=-1)
        return a - b + c - d
    if market.spot <= h:
        return 0.0
    a, b, c, d = _reiner_rubinstein_terms(market, k, h, eta=1)
    return a - c if k > h else b - d
