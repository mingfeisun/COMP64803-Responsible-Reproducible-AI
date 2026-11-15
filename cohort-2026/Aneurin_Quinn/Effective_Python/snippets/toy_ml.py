"""A tiny, dependency-free ML setup shared by the demos.

Two Gaussian blobs and a logistic-regression classifier trained with
mini-batch gradient descent. Pure Python (no NumPy / PyTorch) so the
Docker image stays small and every run is fully reproducible.
"""

import math
import random


def make_dataset(n=200, seed=0):
    """Return a shuffled list of ((x1, x2), label) pairs."""
    rng = random.Random(seed)
    data = []
    for i in range(n):
        label = i % 2
        centre = 0.8 if label else -0.8
        data.append(((rng.gauss(centre, 1.0), rng.gauss(centre, 1.0)), label))
    rng.shuffle(data)
    return data


def split(data, fractions=(0.7, 0.15, 0.15)):
    """Split into train / validation / test lists."""
    n_train = int(len(data) * fractions[0])
    n_val = int(len(data) * fractions[1])
    return data[:n_train], data[n_train:n_train + n_val], data[n_train + n_val:]


def batches(data, batch_size, drop_last=False):
    """Yield consecutive mini-batches, like a PyTorch DataLoader."""
    for start in range(0, len(data), batch_size):
        batch = data[start:start + batch_size]
        if drop_last and len(batch) < batch_size:
            return
        yield batch


class LogisticRegression:
    def __init__(self):
        self.w = [0.0, 0.0]
        self.b = 0.0
        self.calls = 0  # how many times the model has been evaluated

    def predict_proba(self, x):
        self.calls += 1
        z = self.w[0] * x[0] + self.w[1] * x[1] + self.b
        return 1.0 / (1.0 + math.exp(-z))

    def predict(self, x):
        return int(self.predict_proba(x) >= 0.5)

    def loss(self, data):
        """Mean binary cross-entropy."""
        eps = 1e-12
        total = 0.0
        for x, y in data:
            p = self.predict_proba(x)
            total -= y * math.log(p + eps) + (1 - y) * math.log(1 - p + eps)
        return total / len(data)

    def step(self, batch, lr):
        """One gradient-descent step on a mini-batch."""
        gw0 = gw1 = gb = 0.0
        for (x1, x2), y in batch:
            err = self.predict_proba((x1, x2)) - y
            gw0 += err * x1
            gw1 += err * x2
            gb += err
        n = len(batch)
        self.w[0] -= lr * gw0 / n
        self.w[1] -= lr * gw1 / n
        self.b -= lr * gb / n
