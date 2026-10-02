# Use cProfile rather than profile
# because it has less of an impact
# on the performance of the program
# being profiled.
from cProfile import Profile
from pstats import Stats

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def factorial_wrapper(n):
    return factorial(n)

profiler = Profile()
profiler.runcall(lambda: factorial_wrapper(950))

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()
stats.print_callers()
