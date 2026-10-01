
import torch
from torch import nn

def batches_list(n=10):
    return [torch.randn(32, 4) for _ in range(n)]  # builds all batches up front

def batches_gen(n=10):
    for _ in range(n):
        yield torch.randn(32, 4)                   # builds one batch at a time

model = nn.Linear(4, 1)

def train(batches, epochs=2):
    for epoch in range(epochs):
        steps = 0
        for x in batches:
            model(x).sum().backward()
            steps += 1
        print(f"epoch {epoch}: {steps} steps")

train(batches_list())  # epoch 0: 10 steps, epoch 1: 10 steps
train(batches_gen())   # epoch 0: 10 steps, epoch 1: 0 steps  <- silently exhausted!

class Batches:
    def __iter__(self):
        return batches_gen()  # a fresh generator every epoch

train(Batches())       # epoch 0: 10 steps, epoch 1: 10 steps