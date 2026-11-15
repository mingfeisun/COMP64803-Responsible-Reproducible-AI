"""Way 5. Binary search on sorted lists.

Counting the values below t by looking at each value costs O(n). On a sorted
list, bisect_left gives the same count by halving the range, in O(log n).
"""
from bisect import bisect_left
import random
import timeit


def count_below(values, t):
    return sum(1 for v in values if v < t)       # looks at every value


def count_below_sorted(sorted_values, t):
    return bisect_left(sorted_values, t)         # about log2(n) steps


if __name__ == "__main__":
    rng = random.Random(0)                       # fixed seed, same data
    scores = sorted(rng.uniform(0, 100) for _ in range(100_000))
    thresholds = range(1, 101)                   # 100 queries

    def scan():
        return [count_below(scores, t) for t in thresholds]

    def search():
        return [count_below_sorted(scores, t) for t in thresholds]

    assert scan() == search()
    t_scan = timeit.timeit(scan, number=1)
    t_search = timeit.timeit(search, number=1)

    print("Way 5 | binary search on sorted lists")
    print(f"  100 counts by scanning  {t_scan * 1e3:8.3f} ms")
    print(f"  100 counts with bisect  {t_search * 1e3:8.3f} ms"
          f"   ({t_scan / t_search:,.0f}x faster)")
