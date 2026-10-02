from typing import Optional

import torch
from torch import nn

def train_step(model: nn.Module, opt: torch.optim.Optimizer,
               x: torch.Tensor, y: torch.Tensor) -> float:
    opt.zero_grad()
    loss = nn.functional.mse_loss(model(x), y)
    loss.backward()
    opt.step()
    return loss  # Bug 1: returns a Tensor, not a float (should be loss.item())

def best_epoch(losses: list[float]) -> Optional[int]:
    if not losses:
        return None
    return losses.index(min(losses))

model = nn.Linear(3, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)

try:
    losses = [train_step(model, opt, [1.0, 2.0, 3.0], torch.randn(1))]  # Bug 2: a list, not a Tensor
except TypeError as e:
    print(f"Bug 2 at runtime: {e}")
    losses = []

try:
    print(losses[best_epoch(losses)])  # Bug 3: best_epoch might return None
except TypeError as e:
    print(f"Bug 3 at runtime: {e}")