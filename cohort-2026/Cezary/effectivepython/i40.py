import torch
from torch import nn

class Encoder(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.encoder = nn.Linear(3, 3)

class Head(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.head = nn.Linear(3, 1)

class Model(Encoder, Head):
    def __init__(self):
        Encoder.__init__(self)
        Head.__init__(self)  # re-runs nn.Module.__init__, erasing self.encoder

m = Model()
print(hasattr(m, "encoder"))                       # False
print(sum(p.numel() for p in m.parameters()))     # 4, only the head's parameters
print([cls.__name__ for cls in Model.__mro__])

class WithEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Linear(3, 3)

class WithHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.head = nn.Linear(3, 1)

class Model(WithEncoder, WithHead):
    def __init__(self):
        super().__init__()

m = Model()
print(hasattr(m, "encoder"))                       # True
print(sum(p.numel() for p in m.parameters()))     # 16, encoder (12) + head (4)
print([cls.__name__ for cls in Model.__mro__])
