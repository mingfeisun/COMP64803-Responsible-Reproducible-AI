# Effective Python: AI-guided spintronics examples

Five original teaching demos inspired by *Effective Python* (2nd ed.). The synthetic Lorentzian is illustrative, not a complete spintronic-device model.

## Build and run in Docker

```bash
docker build -t effective-python-demo .
docker run --rm effective-python-demo python 01_pep8.py
docker run --rm effective-python-demo python 02_generators.py
docker run --rm effective-python-demo python 03_profiling.py
docker run --rm effective-python-demo python 04_environments.py
docker run --rm --cpus=2 effective-python-demo python 05_parallelism.py
```

For Item 83, the Dockerfile uses a pinned base image tag and `requirements.txt` records a NumPy version. For stronger reproducibility pin the image digest, lock all transitive dependencies, and record random seeds and hardware.

## Talking points

- **Item 2 — PEP 8:** Four-space indentation, snake_case, docstrings, readable formatting.
- **Item 30 — Generators:** Lazy production; `getsizeof` compares shallow object sizes, **not** full memory consumption. A generator can be exhausted.
- **Item 70 — Profiling:** Profile first; optimize measured bottlenecks. Timing varies between machines.
- **Item 83 — Virtual environments:** Docker packages system and Python dependencies; a Python `venv` isolates Python packages. Run `python -m venv .venv` on the host as a complementary demonstration.
- **Item 64 — Parallelism:** Process pools run independent CPU-bound tasks. Speedup is not guaranteed on restricted CPUs.
