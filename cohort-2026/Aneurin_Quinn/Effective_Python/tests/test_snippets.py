"""pytest checks that the 'before' and 'after' versions of each item agree."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snippets"))

import item_01_python_version as item01  # noqa: E402
import item_04_fstrings as item04  # noqa: E402
import item_06_unpacking as item06  # noqa: E402
import item_08_zip as item08  # noqa: E402
import item_10_walrus as item10  # noqa: E402


def test_version_check_passes_and_fails():
    assert item01.check_python_version((3, 0)) >= (3, 0, 0)
    with pytest.raises(RuntimeError):
        item01.check_python_version((99, 0))


def test_environment_report_keys():
    assert {"python", "implementation", "platform"} <= item01.environment_report().keys()


@pytest.mark.parametrize("name,stats", item04.RESULTS.items())
def test_all_three_formatting_styles_agree(name, stats):
    mean, std = stats
    expected = item04.c_style(name, mean, std)
    assert item04.format_method(name, mean, std) == expected
    assert item04.f_string(name, mean, std) == expected


def test_relative_uncertainty():
    assert item04.relative_uncertainty(10.0, 1.0) == "10.0%"


def test_unpacking_matches_indexing():
    assert item06.summarise_unpacking(item06.RUNS) == item06.summarise_indexing(item06.RUNS)


def test_bounds():
    assert item06.bounds([3, 1, 2]) == (1, 3)


def test_zip_matches_range():
    assert item08.residuals_with_zip(item08.MEASURED_K, item08.PREDICTED_K) == \
        item08.residuals_with_range(item08.MEASURED_K, item08.PREDICTED_K)


def test_zip_strict_catches_length_mismatch():
    with pytest.raises(ValueError):
        item08.residuals_with_zip([1.0, 2.0], [1.0])


def test_two_sigma_flags_only_outliers():
    flagged = item08.outside_two_sigma(
        item08.SENSORS, item08.MEASURED_K, item08.PREDICTED_K, item08.PRED_STD_K
    )
    assert flagged == ["TC-02"]
    assert item08.outside_two_sigma(["a"], [10.0], [0.0], [1.0]) == ["a"]


def test_fixed_point_versions_agree():
    a, _ = item10.fixed_point_without_walrus(math.cos, 1.0)
    b, _ = item10.fixed_point_with_walrus(math.cos, 1.0)
    assert a == pytest.approx(b)
    assert b == pytest.approx(math.cos(b), rel=1e-6)


def test_accepted_samples_respect_threshold():
    kept = item10.accepted_samples(500, threshold=1.0, seed=42)
    assert kept and all(y < 1.0 for y in kept)
