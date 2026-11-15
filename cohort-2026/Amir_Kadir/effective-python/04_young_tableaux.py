
from itertools import islice
from math import factorial


# Identify removable corners of a Young diagram
def removable_corners(shape):
    for row, length in enumerate(shape):
        if (
            row == len(shape) - 1
            or length > shape[row + 1]
        ):
            smaller = list(shape)
            smaller[row] -= 1

            if smaller[row] == 0:
                smaller.pop(row)

            yield row, tuple(smaller)


# Insert n into the selected removable corner
def extend(tableau, row, n):
    rows = [list(r) for r in tableau]

    if row == len(rows):
        rows.append([])

    rows[row].append(n)
    return tuple(tuple(r) for r in rows)


# BEFORE: Construct and return all tableaux as a list
def tableaux_list(shape):
    if not shape:
        return [()]

    result = []

    for row, smaller in removable_corners(shape):
        for T in tableaux_list(smaller):
            result.append(
                extend(T, row, sum(shape))
            )

    return result


# AFTER: Generate tableaux lazily using yield
def tableaux_iter(shape):
    if not shape:
        yield ()
        return

    for row, smaller in removable_corners(shape):
        for T in tableaux_iter(smaller):
            yield extend(T, row, sum(shape))


# Independent check using the hook-length formula
def hook_length_count(shape):
    n = sum(shape)
    denominator = 1

    for row, length in enumerate(shape):
        for col in range(length):
            right = length - col - 1
            below = sum(
                next_length > col
                for next_length in shape[row + 1:]
            )
            denominator *= right + below + 1

    return factorial(n) // denominator


# Compare both implementations
for shape in [(3, 2), (5, 4)]:
    eager = tableaux_list(shape)
    lazy = list(tableaux_iter(shape))
    expected = hook_length_count(shape)

    assert eager == lazy
    assert len(eager) == expected

    print(f"Shape {shape}:")
    print(f"  Before (list): {len(eager)} tableaux")
    print(f"  After (generator): {len(lazy)} tableaux")
    print(f"  Hook-length formula: {expected}")


# Demonstrate partial consumption of a large generator
shape = (10, 10)

first_three = list(
    islice(tableaux_iter(shape), 3)
)

assert len(first_three) == 3

print(f"\nShape {shape}:")
print(f"Total possible tableaux: {hook_length_count(shape)}")
print(f"Tableaux actually requested: {len(first_three)}")
print("First tableau:", first_three[0])

print("\nAll Young tableaux checks passed!")

# Supporting Item 81: Measure memory usage with tracemalloc

import tracemalloc


def measure_peak_memory(computation):
    tracemalloc.start()

    try:
        result = computation()
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    return result, peak


shape = (10, 10)

# BEFORE: Construct the entire list to obtain one tableau
eager_first, eager_peak = measure_peak_memory(
    lambda: tableaux_list(shape)[0]
)

# AFTER: Generate only the first tableau
lazy_first, lazy_peak = measure_peak_memory(
    lambda: next(tableaux_iter(shape))
)

assert eager_first == lazy_first

print("\nItem 81: Memory profiling")
print(f"Shape: {shape}")
print(f"Eager peak memory: {eager_peak:,} bytes")
print(f"Lazy peak memory:  {lazy_peak:,} bytes")
print(f"Memory reduction factor: {eager_peak / lazy_peak:.2f}x")
