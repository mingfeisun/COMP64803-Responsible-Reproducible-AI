from context_timer import Timer
import bisect 

# Searching a list! 
search_space = list(range(10000000))

goal = 974921
with Timer() as timer: 
    for i, val in enumerate(search_space):
        if val == goal:
            print(f'Indices:{i}') 
            print(f'Value:{val}') 

with Timer() as timer:
    bisect.