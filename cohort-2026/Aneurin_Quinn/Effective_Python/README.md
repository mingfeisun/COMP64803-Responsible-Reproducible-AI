# Effective Python: Pythonic Thinking — Aneurin Quinn

Five ways to write better Python, chosen from **Chapter 1 (Pythonic Thinking)** of
*Effective Python: 90 Specific Ways to Write Better Python* (B. Slatkin), with examples
drawn from my research area: uncertainty quantification (UQ) for multi-physics
fusion simulations.

| Item | Idea | Why it matters for UQ / simulation research | Snippet |
|---|---|---|---|
| 1 | Know which version of Python you're using | Results must be reproducible; record and check the interpreter | [`item_01_python_version.py`](snippets/item_01_python_version.py) |
| 4 | Prefer f-strings over `%` and `.format()` | Clear, correct logging of means, std devs and units | [`item_04_fstrings.py`](snippets/item_04_fstrings.py) |
| 6 | Prefer unpacking over indexing | Named fields instead of `run[2][0]` in nested results | [`item_06_unpacking.py`](snippets/item_06_unpacking.py) |
| 8 | Use `zip` to process iterators in parallel | Compare predictions vs. measurements; `strict=True` catches length bugs | [`item_08_zip.py`](snippets/item_08_zip.py) |
| 10 | Prevent repetition with `:=` | Cleaner solver / sampling loops with no duplicated calls | [`item_10_walrus.py`](snippets/item_10_walrus.py) |

The slides are in [`Pythonic_Thinking_AQ.pptx`](Pythonic_Thinking_AQ.pptx) (about 10 minutes).

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

Every snippet has a "before" and an "after" version; the tests in
[`tests/test_snippets.py`](tests/test_snippets.py) check that both give the same answer.
