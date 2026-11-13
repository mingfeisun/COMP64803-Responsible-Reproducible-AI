"""pytest checks: each 'before' and 'after' version gives the same answer,
and the failure cases fail the way the slides say they do."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snippets"))

import item_01_python_version as item01  # noqa: E402
import item_04_fstrings as item04  # noqa: E402
import item_06_unpacking as item06  # noqa: E402
import item_08_zip as item08  # noqa: E402
import item_10_walrus as item10  # noqa: E402
import toy_ml  # noqa: E402


# --- Shared toy ML setup ---------------------------------------------------

def test_dataset_is_reproducible():
    assert toy_ml.make_dataset(seed=1) == toy_ml.make_dataset(seed=1)
    assert toy_ml.make_dataset(seed=1) != toy_ml.make_dataset(seed=2)


def test_training_reduces_loss():
    train, _, _ = toy_ml.split(toy_ml.make_dataset())
    model = toy_ml.LogisticRegression()
    before = model.loss(train)
    for batch in toy_ml.batches(train, 32):
        model.step(batch, 0.1)
    assert model.loss(train) < before


# --- Item 1 ----------------------------------------------------------------

def test_version_check_passes_and_fails():
    assert item01.check_python_version((3, 0)) >= (3, 0, 0)
    with pytest.raises(RuntimeError):
        item01.check_python_version((99, 0))


def test_run_metadata_records_seed_and_versions():
    meta = item01.run_metadata(seed=7, packages=("pytest", "surely-not-a-package"))
    assert meta["seed"] == 7
    assert meta["packages"]["surely-not-a-package"] == "not installed"
    assert meta["packages"]["pytest"] != "not installed"


# --- Item 4 ----------------------------------------------------------------

@pytest.mark.parametrize("args", [(1, 0.69, 0.5, 1e-3), (12, 0.0123, 0.9876, 3e-4)])
def test_three_formatting_styles_agree(args):
    expected = item04.log_c_style(*args)
    assert item04.log_str_format(*args) == expected
    assert item04.log_fstring(*args) == expected


def test_swapped_c_style_raises():
    assert item04.problem_1_demo().startswith("TypeError")


def test_run_name_and_precision():
    assert item04.run_name("mlp", 0.001, 64, 0) == "mlp_lr0.001_bs64_seed0"
    assert item04.fmt_metric(0.123456, 2) == "0.12"


# --- Item 6 ----------------------------------------------------------------

def test_unpacking_matches_indexing():
    assert item06.report_unpacking(item06.SWEEP) == item06.report_indexing(item06.SWEEP)


def test_swap_shuffles_agree_and_are_permutations():
    a = item06.shuffle_with_temp(range(20), seed=3)
    b = item06.shuffle_with_unpacking(range(20), seed=3)
    assert a == b and sorted(a) == list(range(20))


def test_split_sizes():
    train, val, test = toy_ml.split(list(range(100)))
    assert (len(train), len(val), len(test)) == (70, 15, 15)


# --- Item 8 ----------------------------------------------------------------

def test_zip_matches_indexing():
    preds, labels = [1, 0, 1, 1], [1, 1, 1, 0]
    assert item08.accuracy_zip(preds, labels) == item08.accuracy_indexing(preds, labels) == 0.5


def test_plain_zip_silently_truncates():
    # 2 predictions for 4 labels: plain zip scores only 2 examples and says 100%.
    assert item08.accuracy_zip([1, 1], [1, 1, 0, 0]) == 1.0
    assert item08.accuracy_zip_longest([1, 1], [1, 1, 0, 0]) == 0.5


def test_strict_zip_raises_on_mismatch():
    with pytest.raises(ValueError):
        item08.accuracy_strict([1, 1], [1, 1, 0])


def test_drop_last_loses_predictions():
    model, test_set = item08.train(epochs=1)
    assert len(item08.predict_all(model, test_set, 64, drop_last=True)) < len(test_set)


# --- Item 10 ---------------------------------------------------------------

@pytest.mark.parametrize("cfg", [{"gpus": 4}, {"gpus": 1, "gpu_mem_gb": 24},
                                 {"gpu_mem_gb": 8, "cpu_cores": 8}, {"cpu_cores": 0}])
def test_strategy_versions_agree(cfg):
    assert item10.strategy_walrus(cfg) == item10.strategy_nested(cfg)


def test_stream_versions_agree():
    data = toy_ml.make_dataset(n=50)
    assert item10.count_walrus(item10.make_stream(data, 8)) == \
        item10.count_loop_and_a_half(item10.make_stream(data, 8)) == 50


def test_pseudo_label_same_result_fewer_calls():
    train, _, test = toy_ml.split(toy_ml.make_dataset(n=400))
    model = toy_ml.LogisticRegression()
    for batch in toy_ml.batches(train, 32):
        model.step(batch, 0.1)
    unlabelled = [x for x, _ in test]

    model.calls = 0
    repeated = item10.pseudo_label_repeated(model, unlabelled)
    calls_repeated = model.calls
    model.calls = 0
    walrus = item10.pseudo_label_walrus(model, unlabelled)
    assert walrus == repeated
    assert model.calls == len(unlabelled) < calls_repeated


def test_early_stopping_stops():
    train, val, _ = toy_ml.split(toy_ml.make_dataset(n=400))
    _, epochs = item10.fit_early_stopping(toy_ml.LogisticRegression(), train, val, max_epochs=200)
    assert epochs < 200
