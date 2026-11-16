# Effective Python for MD research code

Five items from *Effective Python* (2nd ed., Brett Slatkin), each shown on a
small example from a molecular dynamics (MD) workflow. Every file runs on
its own.

| Item | File | What it shows |
|------|------|---------------|
| 52 Use subprocess to manage child processes | `item52_subprocess.py` | Run several simulations at once with a time limit. A crash or a hung run is reported, not ignored |
| 30 Consider generators instead of returning lists | `item30_generators.py` | Read a big trajectory one frame at a time: same answer, a tiny fraction of the memory |
| 64 Consider concurrent.futures for true parallelism | `item64_parallel.py` | Threads don't speed up Python number-crunching (GIL); processes do |
| 70 Profile before optimizing | `item70_profile.py` | cProfile finds the slow part; fix only that |
| 76 Verify related behaviors in TestCase subclasses | `item76_tests.py` | Test that energies and forces obey physics |

`fake_md.py` is a pretend simulation that `item52_subprocess.py` runs.

## Run on your own computer

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python item52_subprocess.py
python item30_generators.py
python item64_parallel.py
python item70_profile.py
python item76_tests.py
```

## Run in Docker

```bash
docker build -t effective-python .
docker run --rm effective-python

