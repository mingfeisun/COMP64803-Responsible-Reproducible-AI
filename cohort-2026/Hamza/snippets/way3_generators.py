"""Way 3. Generators for single-pass loops.

A list comprehension stores all its values before sum starts. A generator
expression hands sum one value at a time, so the memory stays constant.
"""
import tracemalloc


def sum_with_list(n):
    return sum([x * x for x in range(n)])    # all n squares in memory


def sum_with_generator(n):
    return sum(x * x for x in range(n))      # one square at a time


def peak_memory(func, n):
    """Largest memory in bytes allocated while func(n) runs."""
    tracemalloc.start()
    func(n)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return peak


if __name__ == "__main__":
    n = 1_000_000
    assert sum_with_list(n) == sum_with_generator(n)
    mem_list = peak_memory(sum_with_list, n)
    mem_gen = peak_memory(sum_with_generator, n)

    print("Way 3 | generators for single-pass loops")
    print(f"  sum over a list       peak memory {mem_list:>12,} bytes")
    print(f"  sum over a generator  peak memory {mem_gen:>12,} bytes")
