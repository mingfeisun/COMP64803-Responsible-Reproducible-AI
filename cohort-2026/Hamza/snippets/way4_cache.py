"""Way 4. Caching for repeated calls.

Plain recursion computes the same Fibonacci numbers again and again. The
decorator @cache stores each result the first time and reuses it afterwards.
"""
from functools import cache
import timeit


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@cache
def fib_cached(n):
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


if __name__ == "__main__":
    n = 30
    assert fib(n) == fib_cached(n) == 832_040
    t_plain = timeit.timeit(lambda: fib(n), number=1)
    fib_cached.cache_clear()                  # start again from an empty cache
    t_cached = timeit.timeit(lambda: fib_cached(n), number=1)

    print("Way 4 | caching for repeated calls")
    print(f"  plain recursion  {t_plain * 1e3:8.3f} ms")
    print(f"  with @cache      {t_cached * 1e3:8.3f} ms"
          f"   ({t_plain / t_cached:,.0f}x faster)")
    print(f"  {fib_cached.cache_info()}")
