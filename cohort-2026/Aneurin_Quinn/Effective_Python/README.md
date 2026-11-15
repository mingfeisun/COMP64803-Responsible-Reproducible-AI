# Effective Python: Pythonic Thinking — Aneurin Quinn

Five ways to write better Python from **Chapter 1 (Pythonic Thinking)** of
*Effective Python* (B. Slatkin, 2nd ed.), each rewritten with examples from
machine-learning research code: training loops, logging, evaluation and
hyperparameter sweeps.

| Item | Book's advice | ML example in the snippet | Snippet |
|---|---|---|---|
| 1 | Know which version of Python you're using | Fail early on the wrong interpreter; save Python/package versions with the seed | [`item_01_python_version.py`](snippets/item_01_python_version.py) |
| 4 | Prefer f-strings over `%` and `str.format` | Epoch log lines, run names from hyperparameters, the book's "swapped tuple" TypeError | [`item_04_fstrings.py`](snippets/item_04_fstrings.py) |
| 6 | Prefer unpacking over indexing | Ranking a hyperparameter sweep, `enumerate(loader)`, swap in a Fisher–Yates shuffle | [`item_06_unpacking.py`](snippets/item_06_unpacking.py) |
| 8 | Use `zip` to process iterators in parallel | Accuracy from predictions vs labels; `drop_last=True` makes plain `zip` score only 128 of 160 examples. Fixes: `zip_longest` (book), `strict=True` (Python 3.10+) | [`item_08_zip.py`](snippets/item_08_zip.py) |
| 10 | Prevent repetition with `:=` | Early stopping, `while batch := next_batch()`, choosing a training strategy with if/elif, pseudo-labelling with 1 model call per point instead of up to 3 | [`item_10_walrus.py`](snippets/item_10_walrus.py) |

All demos share [`toy_ml.py`](snippets/toy_ml.py): a dependency-free logistic
regression trained on two Gaussian blobs, so everything runs in seconds and is
fully reproducible.

The slides are in [`Pythonic_Thinking_AQ.pptx`](Pythonic_Thinking_AQ.pptx)
(10 slides, about 10 minutes, with speaker notes).

## Run the demos in Docker

```bash
docker build -t effective-python-aq .
docker run --rm effective-python-aq                                   # all five demos
docker run --rm effective-python-aq python snippets/item_08_zip.py    # a single item
docker run --rm effective-python-aq python -m pytest -q tests         # unit tests
```

## Run locally (Python 3.10+)

```bash
python snippets/run_all.py
pip install -r requirements.txt && python -m pytest -q tests
```

Every snippet keeps a "before" and an "after" version; the tests in
[`tests/test_snippets.py`](tests/test_snippets.py) check that both give the same
answer, and that the traps (silent `zip` truncation, swapped `%` arguments)
behave as described.
