
from itertools import product
from math import comb
from time import perf_counter
import cProfile
import pstats


# BEFORE: Enumerate all tensor-product weight assignments
def weight_multiplicity_before(n, weight):
    return sum(
        sum(weights) == weight
        for weights in product((-1, 1), repeat=n)
    )


# AFTER: Use the binomial coefficient formula
def weight_multiplicity_after(n, weight):
    if abs(weight) > n or (n - weight) % 2:
        return 0

    k = (n - weight) // 2
    return comb(n, k)


# Verify mathematical correctness
# Both functions assume n is a nonnegative integer.
for n in range(11):
    for weight in range(-n - 2, n + 3):
        assert (
            weight_multiplicity_before(n, weight)
            == weight_multiplicity_after(n, weight)
        )

    # The sum of all weight multiplicities is dim(V^n) = 2^n
    assert sum(
        weight_multiplicity_after(n, weight)
        for weight in range(-n, n + 1)
    ) == 2**n

print("All weight multiplicity checks passed!")


# Compare execution times
n = 18
weight = 0

start = perf_counter()
before = weight_multiplicity_before(n, weight)
time_before = perf_counter() - start

start = perf_counter()
after = weight_multiplicity_after(n, weight)
time_after = perf_counter() - start

assert before == after == comb(18, 9)

print(f"\nWeight multiplicity in V^{n}:")
print(f"Before (enumeration): {before}")
print(f"After (binomial formula): {after}")

print(f"\nBefore runtime: {time_before:.6f} seconds")
print(f"After runtime:  {time_after:.6f} seconds")


# Item 70: Profile the original implementation
print("\nProfiling the original implementation:")

profiler = cProfile.Profile()

profiler.runcall(
    weight_multiplicity_before,
    n,
    weight
)

pstats.Stats(profiler).sort_stats(
    "cumulative"
).print_stats(10)


print("All profiling checks passed!")
