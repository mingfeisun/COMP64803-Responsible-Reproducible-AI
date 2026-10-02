import time
import torch
from functools import lru_cache

def timed(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

@timed
def train_step(model, x, y):
    output = model(x)
    loss = torch.nn.functional.mse_loss(output, y)
    loss.backward()
    return loss.item()


@lru_cache(maxsize=None)
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(100))


@torch.no_grad()
def evaluate(model, dataloader):
    for x, y in dataloader:
        pred = model(x)

