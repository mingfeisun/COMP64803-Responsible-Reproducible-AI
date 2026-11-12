"""Item 6: Prefer Multiple Assignment Unpacking Over Indexing.

Book: unpacking assigns several values in one statement, works on nested
iterables, swaps values without a temporary, and combined with enumerate
in a for loop removes almost all indexing.

ML angle: data loaders yield (inputs, targets) pairs, sweeps produce
((hyperparameters), (mean, std)) records, and data shuffling swaps items.
"""

import random

from toy_ml import LogisticRegression, batches, make_dataset, split

# Hyperparameter sweep: ((learning rate, batch size), (mean val acc, std over 5 seeds))
SWEEP = [
    ((0.1, 32), (0.912, 0.011)),
    ((0.01, 32), (0.874, 0.020)),
    ((0.1, 128), (0.905, 0.008)),
    ((1.0, 32), (0.861, 0.047)),
]


# --- Reporting sweep results -----------------------------------------------

def report_indexing(sweep):
    ranked = sorted(sweep, key=lambda r: r[1][0], reverse=True)
    lines = []
    for i in range(len(ranked)):
        r = ranked[i]
        lines.append(f"#{i + 1}: lr={r[0][0]} bs={r[0][1]} acc={r[1][0]:.3f}+/-{r[1][1]:.3f}")
    return lines


def report_unpacking(sweep):
    ranked = sorted(sweep, key=lambda r: r[1][0], reverse=True)
    lines = []
    for rank, ((lr, bs), (mean, std)) in enumerate(ranked, 1):
        lines.append(f"#{rank}: lr={lr} bs={bs} acc={mean:.3f}+/-{std:.3f}")
    return lines


# --- Swapping: Fisher-Yates shuffle (what random.shuffle does) ---------------

def shuffle_with_temp(items, seed):
    items, rng = list(items), random.Random(seed)
    for i in range(len(items) - 1, 0, -1):
        j = rng.randint(0, i)
        temp = items[i]
        items[i] = items[j]
        items[j] = temp
    return items


def shuffle_with_unpacking(items, seed):
    items, rng = list(items), random.Random(seed)
    for i in range(len(items) - 1, 0, -1):
        j = rng.randint(0, i)
        items[i], items[j] = items[j], items[i]  # swap, no temp
    return items


# --- A training loop -------------------------------------------------------

def train_one_epoch(model, data, batch_size, lr):
    """Return [(step, batch error rate before the update)]; unpacking everywhere."""
    history = []
    for step, batch in enumerate(batches(data, batch_size), 1):
        errors = sum(model.predict(x) != label for x, label in batch)
        history.append((step, errors / len(batch)))
        model.step(batch, lr)
    return history


def main():
    print("=== Item 6: Prefer unpacking over indexing ===")
    print("Indexing : r[0][0], r[1][0] ...")
    for line in report_indexing(SWEEP):
        print("  ", line)
    print("Unpacking: for rank, ((lr, bs), (mean, std)) in enumerate(...)")
    for line in report_unpacking(SWEEP):
        print("  ", line)

    train, val, test = split(make_dataset())  # unpack a returned tuple
    print(f"\nsplit() -> train={len(train)}, val={len(val)}, test={len(test)}")

    print("Shuffle with temp     :", shuffle_with_temp(range(8), seed=0))
    print("Shuffle with unpacking:", shuffle_with_unpacking(range(8), seed=0))

    print("\nOne epoch, batch error rate before each update:")
    for step, error_rate in train_one_epoch(LogisticRegression(), train, 32, lr=0.1):
        print(f"  step {step}: {error_rate:.0%}")

    try:
        lr, bs, extra = SWEEP[0]
    except ValueError as err:
        print(f"Shape changed? Unpacking fails loudly: {err}")


if __name__ == "__main__":
    main()
