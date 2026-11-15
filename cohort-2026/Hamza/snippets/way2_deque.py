"""Way 2. Deques for queues.

Removing the first item of a list moves every other item one place to the
left, which costs O(n). A deque removes an item from either end in O(1).
"""
from collections import deque
import timeit


def serve_with_list(n):
    queue = list(range(n))
    return [queue.pop(0) for _ in range(n)]      # each pop shifts the rest


def serve_with_deque(n):
    queue = deque(range(n))
    return [queue.popleft() for _ in range(n)]   # nothing moves


if __name__ == "__main__":
    n = 50_000
    assert serve_with_list(n) == serve_with_deque(n) == list(range(n))
    t_list = timeit.timeit(lambda: serve_with_list(n), number=1)
    t_deque = timeit.timeit(lambda: serve_with_deque(n), number=1)

    print("Way 2 | deques for queues")
    print(f"  {n:,} pops from a list   {t_list * 1e3:8.2f} ms")
    print(f"  {n:,} pops from a deque  {t_deque * 1e3:8.2f} ms"
          f"   ({t_list / t_deque:,.0f}x faster)")
