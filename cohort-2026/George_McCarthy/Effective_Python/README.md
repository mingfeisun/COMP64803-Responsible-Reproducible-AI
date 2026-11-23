# 6 cool things in marimo (COMP64803 talk)

A 10-minute live demo of marimo, a reactive Python notebook.

## Run with Docker

```bash
docker build -t marimo-talk .
docker run --rm -p 2718:2718 -v "$PWD/talk.py:/app/talk.py" marimo-talk
```

Then open http://localhost:2718. The volume mount means edits are saved back to `talk.py`.

## Run without Docker

```bash
uv run --with-requirements requirements.txt marimo edit talk.py --no-token
```

Or, with the local venv set up (`uv venv --python 3.12 && uv pip install -r requirements.txt`):

```bash
./edit.sh
```

## The six things

1. Reactive execution: no hidden state
2. UI widgets with no callbacks
3. Select points in a chart and get the data back in Python
4. SQL cells that query your dataframes
5. Explore and transform dataframes live, with no code
6. It's just a Python file: git, scripts, apps, and the browser

## marimo vs Jupyter: diff size

`talk.ipynb` is the same notebook written for Jupyter (ipywidgets plus plain duckdb), executed and saved with its outputs.

| | `talk.py` (marimo) | `talk.ipynb` (Jupyter) |
|---|---|---|
| File size | 3.4 KB, 148 lines | 92.7 KB, 1,240 lines |
| Diff after changing `n = 10` to `n = 11` and re-running | 2 lines | 658 lines |
