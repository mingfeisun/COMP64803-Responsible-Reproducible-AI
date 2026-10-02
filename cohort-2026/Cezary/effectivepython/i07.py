import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(torch.randn(40, 3), torch.randn(40, 1))
loader = DataLoader(dataset, batch_size=8, shuffle=True)
model = nn.Linear(3, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)

# With range: doesn't even work here
# for i in range(len(loader)):
#     x, y = loader[i]  # TypeError: 'DataLoader' object is not subscriptable

# With enumerate
for step, (x, y) in enumerate(loader, start=1):
    opt.zero_grad()
    loss = nn.functional.mse_loss(model(x), y)
    loss.backward()
    opt.step()
    if step % 2 == 0:
        print(f"step {step}: loss {loss.item():.3f}")