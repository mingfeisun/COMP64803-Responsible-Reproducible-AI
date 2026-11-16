"""The lecture: "You should always test your code". Run with:  pytest -v"""
import pytest

from zprime.cutflow import cutflow, format_cutflow
from zprime.events import make_events
from zprime.selection import CUTS, passes, select

GOOD = {"tau_pt": [50.0, 40.0], "tau_eta": [0.5, -1.0], "n_bjets": 1}


def test_good_event_passes():
    assert passes(GOOD, **CUTS)


@pytest.mark.parametrize("change", [
    {"tau_pt": [50.0, 10.0]},       # one tau too soft
    {"tau_eta": [0.5, 2.9]},        # one tau too close to the beam
    {"n_bjets": 0},                 # no b-jet
])
def test_each_cut_can_reject(change):
    assert not passes({**GOOD, **change}, **CUTS)


def test_cuts_must_be_named():
    with pytest.raises(TypeError):
        passes(GOOD, 30.0, 2.5, 1)


def test_mismatched_lists_are_an_error():
    with pytest.raises(ValueError):
        passes({**GOOD, "tau_eta": [0.5]}, **CUTS)


def test_same_seed_same_events():
    assert make_events(100, seed=3) == make_events(100, seed=3)
    assert make_events(100, seed=3) != make_events(100, seed=4)


def test_cutflow_only_goes_down():
    counts = [count for _, count in cutflow(make_events(5000))]
    assert counts[0] == 5000
    assert counts == sorted(counts, reverse=True)
    assert counts[-1] == len(select(make_events(5000), **CUTS))


def test_table_has_a_header_and_one_line_per_cut():
    assert len(format_cutflow(cutflow(make_events(100))).splitlines()) == 5
