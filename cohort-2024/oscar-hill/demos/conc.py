from concurrent.futures import ProcessPoolExecutor
import time

def sleepy(n):
    time.sleep(1)
    return n

numbers = [1, 2, 3, 4, 5]

start = time.time()
results = list(map(sleepy, numbers))
end = time.time()
print(f"Non-concurrent version took {end-start:.3f}s.")

start = time.time()
pool = ProcessPoolExecutor(max_workers=5)
results = list(pool.map(sleepy, numbers))
end = time.time()
print(f"Concurrent version took {end-start:.3f}s.")
