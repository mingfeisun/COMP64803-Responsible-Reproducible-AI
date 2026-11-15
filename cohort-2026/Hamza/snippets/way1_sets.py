"""Way 1. Sets for membership tests.

The test `x in a_list` compares x with the elements one by one, which costs
O(n). The test `x in a_set` finds x through its hash, in O(1) on average.
"""
import timeit


def count_hits(items, queries):
    """Number of queries that are among the items."""
    return sum(1 for q in queries if q in items)


if __name__ == "__main__":
    ids = list(range(100_000))
    ids_set = set(ids)                    # built once, in O(n)
    queries = range(0, 200_000, 200)      # 1,000 queries, half of them absent

    assert count_hits(ids, queries) == count_hits(ids_set, queries) == 500
    t_list = timeit.timeit(lambda: count_hits(ids, queries), number=1)
    t_set = timeit.timeit(lambda: count_hits(ids_set, queries), number=1)

    print("Way 1 | sets for membership tests")
    print(f"  1,000 lookups in a list  {t_list * 1e3:8.2f} ms")
    print(f"  1,000 lookups in a set   {t_set * 1e3:8.2f} ms"
          f"   ({t_list / t_set:,.0f}x faster)")
