# Item 66: Use contextlib and with Statements

from contextlib import contextmanager
from time import perf_counter, sleep

@contextmanager
def timed():
    start = perf_counter()
    try:
        yield
    finally:
        print("Runtime:", round(perf_counter() - start, 3), "seconds")

with timed():
    sleep(0.1)  # Example simulation
