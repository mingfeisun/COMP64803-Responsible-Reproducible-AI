
import torch
from torch import nn

class Trainer:
    def __init__(self, model, lr):
        self.model = model  # still a plain attribute
        self.optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    @property
    def lr(self):
        return self.optimizer.param_groups[0]["lr"]

    @lr.setter
    def lr(self, value):
        if value <= 0:
            raise ValueError("lr must be positive")
        for group in self.optimizer.param_groups:
            group["lr"] = value

    @property
    def num_params(self):  # computed and read-only: no setter
        return sum(p.numel() for p in self.model.parameters())

t = Trainer(nn.Linear(3, 1), lr=0.1)
t.lr *= 0.5        # same syntax as before, but now it updates the optimizer
print(t.lr)        # 0.05
print(t.num_params)  # 4
try:
    t.lr = -1
except ValueError as e:
    print(f"Rejected: {e}")  # Rejected: lr must be positive

try:
    t.num_params = 10
except AttributeError as e:
    print(f"Rejected: {e}")