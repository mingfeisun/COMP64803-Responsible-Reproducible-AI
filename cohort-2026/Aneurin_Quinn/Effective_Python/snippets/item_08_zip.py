"""Item 8: Use zip to Process Iterators in Parallel.

Book: zip walks several iterators together without indexing, and is lazy
so it works on huge or infinite inputs. BUT it silently truncates to the
shortest input; use itertools.zip_longest when lengths may differ.
Newer than the book (Python 3.10+): zip(..., strict=True) raises instead.

ML angle: predictions vs labels. If the eval loop used drop_last=True,
you have fewer predictions than labels, and plain zip quietly scores
only the examples that happen to line up.
"""

import itertools

from toy_ml import LogisticRegression, batches, make_dataset, split


def accuracy_indexing(preds, labels):
    correct = 0
    for i in range(len(preds)):
        if preds[i] == labels[i]:
            correct += 1
    return correct / len(preds)


def accuracy_zip(preds, labels):
    pairs = list(zip(preds, labels))
    return sum(p == y for p, y in pairs) / len(pairs)


def accuracy_zip_longest(preds, labels):
    """Book's fix: missing predictions become None and count as wrong."""
    pairs = list(itertools.zip_longest(preds, labels))
    return sum(p == y for p, y in pairs) / len(pairs)


def accuracy_strict(preds, labels):
    """Python 3.10+: refuse to score mismatched lengths at all."""
    return sum(p == y for p, y in zip(preds, labels, strict=True)) / len(labels)


def predict_all(model, data, batch_size, drop_last):
    preds = []
    for batch in batches(data, batch_size, drop_last=drop_last):
        preds.extend(model.predict(x) for x, _ in batch)
    return preds


def train(seed=0, epochs=5):
    data = make_dataset(n=400, seed=seed)
    train_set, _, test_set = split(data, (0.5, 0.1, 0.4))
    model = LogisticRegression()
    for _ in range(epochs):
        for batch in batches(train_set, 32):
            model.step(batch, 0.1)
    return model, test_set


def main():
    print("=== Item 8: Use zip to process iterators in parallel ===")
    model, test_set = train()
    labels = [y for _, y in test_set]

    preds = predict_all(model, test_set, batch_size=64, drop_last=False)
    print(f"Full eval: {len(preds)} predictions, {len(labels)} labels")
    print(f"  range(len()) accuracy: {accuracy_indexing(preds, labels):.3f}")
    print(f"  zip accuracy         : {accuracy_zip(preds, labels):.3f}")

    short = predict_all(model, test_set, batch_size=64, drop_last=True)
    print(f"\nBuggy eval (drop_last=True): {len(short)} predictions, {len(labels)} labels")
    print(f"  plain zip   -> scores {len(list(zip(short, labels)))} examples, "
          f"acc {accuracy_zip(short, labels):.3f}  (silently!)")
    print(f"  zip_longest -> scores {len(list(itertools.zip_longest(short, labels)))} examples, "
          f"acc {accuracy_zip_longest(short, labels):.3f}  (book's fix)")
    try:
        accuracy_strict(short, labels)
    except ValueError as err:
        print(f"  zip(strict=True) -> ValueError: {err}")

    print("\nzip is lazy, so it pairs a generator of batches with step numbers:")
    for step, batch in zip(itertools.count(1), batches(test_set, 64)):
        print(f"  step {step}: batch of {len(batch)}")


if __name__ == "__main__":
    main()
