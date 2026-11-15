# Slide 10: Unit Tests with pytest

import math
import pytest


def best_design(names, drags):
    pairs = list(zip(names, drags, strict=True))
    if not pairs or any(not math.isfinite(cd) or cd < 0 for cd in drags):
        raise ValueError("Invalid inputs")
    return min(pairs, key=lambda r: r[1])[0]


@pytest.mark.parametrize("names,drags,expected", [
    (["A", "B"], [0.012, 0.015], "A"),
    (["A", "B"], [0.015, 0.012], "B"),
    (["A"], [0.012], "A"),
    (["A", "B", "C"], [0.018, 0.015, 0.012], "C"),
    (["A", "B"], [0.012, 0.012], "A"),
])
def test_valid(names, drags, expected):
    assert best_design(names, drags) == expected


@pytest.mark.parametrize("names,drags", [
    ([], []),
    (["A", "B"], [0.012]),
    (["A"], [0.012, 0.015]),
    (["A"], [float("nan")]),
    (["A"], [-0.01]),
])
def test_invalid(names, drags):
    with pytest.raises(ValueError):
        best_design(names, drags)
