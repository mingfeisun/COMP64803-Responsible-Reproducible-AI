"""Tests for the Wiener-Hopf Monte Carlo barrier pricer.

Monte Carlo checks use fixed seeds and a 4-standard-error tolerance, so they
are deterministic and only fail if the method is genuinely wrong.
"""

import json
import math
import struct
import sys
from decimal import Decimal, getcontext
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import run_pricing  # noqa: E402
from whmc import (BarrierOption, Market, barrier_price, bridge_mc_price,  # noqa: E402
                  grid_mc_price, plot_convergence, simulate_whmc, vanilla_call,
                  whmc_price, whmc_price_to_tolerance, wiener_hopf_factors)
from whmc.black_scholes import norm_cdf  # noqa: E402

MARKET = Market()
OPTIONS = [BarrierOption(100, 130), BarrierOption(90, 120),
           BarrierOption(100, 90, "down-and-out"), BarrierOption(85, 90, "down-and-out")]
IDS = [f"{o.kind}-K{o.strike:g}-H{o.barrier:g}" for o in OPTIONS]


# --- Wiener-Hopf factors ---------------------------------------------------

@pytest.mark.parametrize("q", [0.5, 4.0, 64.0])
def test_factors_are_roots_of_laplace_exponent(q):
    mu, sigma = MARKET.drift, MARKET.vol
    phi_plus, phi_minus = wiener_hopf_factors(mu, sigma, q)
    psi = lambda theta: mu * theta + 0.5 * sigma**2 * theta**2  # noqa: E731
    assert psi(phi_plus) == pytest.approx(q)
    assert psi(-phi_minus) == pytest.approx(q)
    # E[X at exponential time] = mu / q = E[max] - E[drop after max]
    assert 1 / phi_plus - 1 / phi_minus == pytest.approx(mu / q)


@pytest.mark.parametrize("mu", [0.03, -0.03])
@pytest.mark.parametrize("q", [1e-6, 1e-10, 1e-14])
def test_factors_accurate_for_tiny_q(mu, q):
    """Compare with a 50-digit Decimal reference: no catastrophic cancellation."""
    getcontext().prec = 50
    m, s, qq = Decimal(mu), Decimal(0.2), Decimal(q)
    root = (m * m + 2 * qq * s * s).sqrt()
    exact_plus, exact_minus = (root - m) / (s * s), (root + m) / (s * s)
    phi_plus, phi_minus = wiener_hopf_factors(mu, 0.2, q)
    assert phi_plus == pytest.approx(float(exact_plus), rel=1e-12)
    assert phi_minus == pytest.approx(float(exact_minus), rel=1e-12)


def test_factors_reject_bad_parameters():
    with pytest.raises(ValueError):
        wiener_hopf_factors(0.03, 0.2, q=0)


def test_single_exponential_step_moments():
    rng = np.random.default_rng(0)
    phi_plus, _ = wiener_hopf_factors(MARKET.drift, MARKET.vol, q=1.0)
    x_end, running_max = simulate_whmc(MARKET.drift, MARKET.vol, 1.0,
                                       n_steps=1, n_paths=400_000, rng=rng)
    assert running_max.mean() == pytest.approx(1 / phi_plus, rel=0.01)
    assert x_end.mean() == pytest.approx(MARKET.drift, abs=0.005)
    assert np.all(running_max >= np.maximum(x_end, 0.0))


# --- Closed form and small numbers -------------------------------------------

def test_norm_cdf_keeps_tiny_tail_probabilities():
    assert norm_cdf(-10) == pytest.approx(7.619853024160527e-24, rel=1e-12)
    assert 0.5 * (1 + math.erf(-10 / math.sqrt(2))) == 0.0  # the naive formula fails


def test_closed_form_limits():
    assert barrier_price(MARKET, BarrierOption(100, 1e6)) == pytest.approx(vanilla_call(MARKET, 100))
    assert barrier_price(MARKET, BarrierOption(100, 1e-6, "down-and-out")) == pytest.approx(
        vanilla_call(MARKET, 100))
    assert barrier_price(MARKET, BarrierOption(130, 120)) == 0.0          # strike above barrier
    assert barrier_price(MARKET, BarrierOption(90, 95)) < barrier_price(MARKET, BarrierOption(90, 120))


@pytest.mark.parametrize("option", OPTIONS, ids=IDS)
def test_closed_form_matches_brownian_bridge(option):
    est = bridge_mc_price(MARKET, option, n_steps=50, n_paths=200_000, rng=np.random.default_rng(1))
    assert abs(est.price - barrier_price(MARKET, option)) < 4 * est.stderr


# --- Monte Carlo methods ----------------------------------------------------

@pytest.mark.parametrize("option", OPTIONS, ids=IDS)
def test_whmc_matches_closed_form(option):
    est = whmc_price(MARKET, option, n_steps=128, n_paths=200_000, rng=np.random.default_rng(2))
    assert abs(est.price - barrier_price(MARKET, option)) < 4 * est.stderr


def test_grid_mc_overprices_knock_out():
    option = BarrierOption(100, 130)
    est = grid_mc_price(MARKET, option, n_steps=16, n_paths=100_000, rng=np.random.default_rng(3))
    assert est.price - barrier_price(MARKET, option) > 10 * est.stderr


def test_whmc_beats_grid_at_same_steps():
    option = BarrierOption(100, 130)
    exact = barrier_price(MARKET, option)
    wh = whmc_price(MARKET, option, n_steps=16, n_paths=100_000, rng=np.random.default_rng(4))
    gr = grid_mc_price(MARKET, option, n_steps=16, n_paths=100_000, rng=np.random.default_rng(4))
    assert abs(wh.price - exact) < abs(gr.price - exact) / 5


def test_same_seed_same_answer():
    option = BarrierOption(100, 130)
    a = whmc_price(MARKET, option, n_steps=8, n_paths=10_000, rng=np.random.default_rng(7))
    b = whmc_price(MARKET, option, n_steps=8, n_paths=10_000, rng=np.random.default_rng(7))
    assert a == b


# --- Choosing parameters ------------------------------------------------------

def test_sizes_are_keyword_only():
    """n_steps and n_paths are both ints; passing them by position is refused."""
    with pytest.raises(TypeError):
        whmc_price(MARKET, OPTIONS[0], 16, 1000, np.random.default_rng(0))


def test_bad_sizes_rejected():
    with pytest.raises(ValueError):
        whmc_price(MARKET, OPTIONS[0], n_steps=0, n_paths=1000, rng=np.random.default_rng(0))


def test_adaptive_stops_at_target():
    est = whmc_price_to_tolerance(MARKET, OPTIONS[0], n_steps=16, target_stderr=0.02,
                                  rng=np.random.default_rng(5), batch_size=10_000)
    assert est.stderr <= 0.02
    assert est.n_paths % 10_000 == 0
    assert math.isfinite(est.price)


def test_choose_steps_picks_first_inside_noise():
    exact = barrier_price(MARKET, OPTIONS[0])
    runs = [whmc_price(MARKET, OPTIONS[0], n_steps=n, n_paths=100_000, rng=np.random.default_rng(n))
            for n in run_pricing.STEPS]
    n = run_pricing.choose_steps(run_pricing.STEPS, runs, exact)
    chosen = runs[run_pricing.STEPS.index(n)]
    assert abs(chosen.price - exact) < 1.96 * chosen.stderr


# --- Graphs ------------------------------------------------------------------

def _png_size(path):
    with open(path, "rb") as f:
        header = f.read(24)
    return struct.unpack(">II", header[16:24])


def test_plot_saved_at_requested_resolution_and_as_vector(tmp_path):
    files = plot_convergence([4, 8, 16], [0.1, 0.05, 0.01], [1.0, 0.7, 0.5],
                             tmp_path / "conv", dpi=300)
    png, svg = files
    width, height = _png_size(png)
    assert width >= 6 * 300 and height >= 4 * 300  # figure inches x dpi
    assert svg.read_text().lstrip().startswith("<?xml")


# --- The script ----------------------------------------------------------------

def test_version_check():
    run_pricing.check_python_version((3, 0))
    with pytest.raises(RuntimeError):
        run_pricing.check_python_version((99, 0))


def test_script_runs_and_records_environment(tmp_path, capsys):
    run_pricing.main(["--paths", "2000", "--outdir", str(tmp_path), "--dpi", "100"])
    saved = json.loads((tmp_path / "run.json").read_text())
    assert saved["metadata"]["seed"] == 2026
    assert {"python", "numpy", "matplotlib"} <= saved["metadata"].keys()
    assert [row["steps"] for row in saved["convergence"]] == run_pricing.STEPS
    assert (tmp_path / "convergence.png").exists() and (tmp_path / "convergence.svg").exists()
    assert "Exact (closed form) price" in capsys.readouterr().out
