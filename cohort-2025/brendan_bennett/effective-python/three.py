import numpy as np
import time

data = list(range(10000000))

start = time.perf_counter()
total_manual = 0
for x in data:
    total_manual += x
end = time.perf_counter()
print(f"Manual loop sum: {end - start:.4f} seconds")

start = time.perf_counter()
total_builtin = sum(data)
end = time.perf_counter()
print(f"Built-in sum():  {end - start:.4f} seconds")

arr = np.array(data)
start = time.perf_counter()
total_numpy = np.sum(arr)
end = time.perf_counter()
print(f"NumPy sum():     {end - start:.4f} seconds")
