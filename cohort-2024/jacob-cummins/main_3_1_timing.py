from main_3_1_code import fibonacci, fibonacci_number_matcher


#out = fibonacci_number_matcher(n=100000, contains=3)
#out = fibonacci_number_matcher(n=30000, contains=666)
#out = fibonacci_number_matcher(n=30000, contains=666)

#print(out)

test = lambda: fibonacci_number_matcher(n=30000, contains=666)
from cProfile import Profile
profiler = Profile()
profiler.runcall(test)

from pstats import Stats
stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()
#stats.print_callers()


# As we can see, the most amount of time is spent iterating through the sequence trying to find matches.