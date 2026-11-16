"""Item 64: Consider concurrent.futures for true parallelism.

Counts neighbouring atoms in many configurations, three ways:
  - one after another (serial)
  - with threads    -> no faster: the GIL lets only one thread run Python at once
  - with processes  -> faster: each process is a separate Python on its own core

Run: python item64_parallel.py
"""
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

CUTOFF = 0.1
N_CONFIGS = 96
N_ATOMS = 500


def make_atoms(seed):
    """Random atom positions in a 1 x 1 x 1 box."""
    rng = random.Random(seed)
    return [(rng.random(), rng.random(), rng.random()) for _ in range(N_ATOMS)]


def count_neighbours(atoms):
    """Slow on purpose: checks every pair of atoms with plain Python loops."""
    count = 0
    for i in range(len(atoms)):
        xi, yi, zi = atoms[i]
        for j in range(i + 1, len(atoms)):
            xj, yj, zj = atoms[j]
            if (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2 < CUTOFF**2:
                count += 1
    return count


def timed(label, run):
    start = time.time()
    counts = run()
    seconds = time.time() - start
    print(f"{label:<12} {seconds:5.2f} s   (total neighbours: {sum(counts)})")
    return seconds


# This `if` is required for processes on macOS and Windows: each worker
# re-imports this file, and must not re-run the code below.
if __name__ == "__main__":
    configs = [make_atoms(seed) for seed in range(N_CONFIGS)]
    cores = os.cpu_count()
    print(f"{N_CONFIGS} configurations of {N_ATOMS} atoms, {cores} CPU cores")

    serial = timed("serial", lambda: list(map(count_neighbours, configs)))

    with ThreadPoolExecutor(max_workers=cores) as pool:
        threads = timed("threads", lambda: list(pool.map(count_neighbours, configs)))

    with ProcessPoolExecutor(max_workers=cores) as pool:
        processes = timed("processes", lambda: list(pool.map(count_neighbours, configs)))

    print(f"speed-up: threads {serial / threads:.1f}x, processes {serial / processes:.1f}x")
