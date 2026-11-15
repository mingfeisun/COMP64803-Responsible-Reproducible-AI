"""Item 64: Independent CPU-bound parameter sweeps with processes."""

from concurrent.futures import ProcessPoolExecutor
from math import sin
from time import perf_counter


def simulate(seed):
    """Independent synthetic CPU-heavy sweep; return a scalar summary."""
    total = 0.0
    for i in range(350_000):
        frequency = 4.0 + i * 0.000005
        response = 1.0 / (1.0 + ((frequency - 5.0) / 0.4) ** 2)
        total += response * sin(frequency + seed * 0.01)
    return total


if __name__ == "__main__":
    seeds = list(range(8))
    start = perf_counter()
    sequential = [simulate(seed) for seed in seeds]
    sequential_time = perf_counter() - start

    start = perf_counter()
    with ProcessPoolExecutor(max_workers=2) as pool:
        parallel = list(pool.map(simulate, seeds))
    parallel_time = perf_counter() - start

    assert all(abs(a - b) < 1e-9 for a, b in zip(sequential, parallel))
    print(f"Sequential: {sequential_time:.3f} s")
    print(f"2 processes: {parallel_time:.3f} s")
    print("Speedup depends on CPU resources and process overhead.")
