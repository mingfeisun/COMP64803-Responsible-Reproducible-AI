# Five Effective Python items, on a toy particle-physics selection

Small demo for COMP64803. It applies five items from *Effective Python*
(2nd ed., Brett Slatkin) to one job: preprocessing made-up collision events
into a training set for a signal-versus-background classifier. The code
filters the events, counts how many are left after each filter (a "cutflow"),
and builds one example input feature. No model is trained here.

| Item | Idea | Where |
| --- | --- | --- |
| 4 | f-strings over `%` formatting | `zprime/cutflow.py` |
| 7 | `enumerate` over `range(len(...))` | `zprime/cutflow.py` |
| 8 | `zip` to walk two lists together | `zprime/selection.py` |
| 27 | Comprehensions over `map` and `filter` | `zprime/selection.py` |
| 25 | Keyword-only arguments | `zprime/selection.py` |

Plain Python only; the one dependency is pytest. The events are random
numbers from a fixed seed, so nothing here is a physics result.

## Run it in Docker

```bash
docker build -t zprime-demo .            # build the image (once, and after edits)
docker run --rm zprime-demo              # run every demo
docker run --rm zprime-demo python -m zprime.demo item8   # run one demo
docker run --rm zprime-demo pytest -v    # run the tests
docker run --rm -it zprime-demo bash     # look around inside the container
```

To edit code on your laptop and re-run without rebuilding:

```bash
docker run --rm -v "$(pwd)":/app zprime-demo python -m zprime.demo cutflow
```

## Run it without Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m zprime.demo all
pytest -v
```
