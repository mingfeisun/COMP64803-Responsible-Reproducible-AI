import numpy as np
import cProfile, pstats, io

def process_events(events):
    results = []
    for event in events:
        result = np.sqrt(np.sum(event**2))  #compute feature
        results.append(result)
    return results

events = np.random.rand(10_000, 100)
output = process_events(events)

pr = cProfile.Profile()
pr.enable()
process_events(events)
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(5)
print(s.getvalue())
