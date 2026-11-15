"""Item 70: Profile a slow implementation, then compare an improvement."""

import cProfile
import pstats
from time import perf_counter


def lorentzian(frequency):
    return 1.0 / (1.0 + ((frequency - 5.0) / 0.4) ** 2)


def slow_sweep(count=100_000):
    return [lorentzian(i * 0.0001) for i in range(count)]


def fast_sweep(count=100_000):
    # Inlining a tiny operation removes Python function-call overhead.
    return [1.0 / (1.0 + ((i * 0.0001 - 5.0) / 0.4) ** 2)
            for i in range(count)]


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    slow_result = slow_sweep()
    profiler.disable()
    print("Slow implementation profile (top 8 by cumulative time):")
    pstats.Stats(profiler).sort_stats("cumulative").print_stats(8)

    for name, function in (("slow", slow_sweep), ("improved", fast_sweep)):
        start = perf_counter()
        result = function()
        elapsed = perf_counter() - start
        assert result == slow_result
        print(f"{name}: {elapsed:.4f} seconds")
