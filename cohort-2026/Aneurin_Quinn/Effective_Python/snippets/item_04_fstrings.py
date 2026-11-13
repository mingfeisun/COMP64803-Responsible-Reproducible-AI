"""Item 4: Prefer Interpolated F-Strings Over C-style Format Strings and str.format.

Book: C-style `%` formatting has four problems:
  1. swapping the order/type of values breaks it (TypeError at runtime)
  2. small changes to values before formatting become hard to read
  3. using a value twice means repeating it
  4. the dictionary form fixes 1 and 3 but is very verbose
str.format fixes some of these but not 2 and 4. f-strings fix all four.

ML angle: every training script prints a progress line per epoch and
builds a run name from its hyperparameters.
"""

from toy_ml import LogisticRegression, batches, make_dataset, split


# --- One training-log line, three ways -------------------------------------

def log_c_style(epoch, train_loss, val_acc, lr):
    return "epoch %3d | loss %.4f | val acc %.1f%% | lr %.0e" % (
        epoch, train_loss, val_acc * 100, lr)


def log_str_format(epoch, train_loss, val_acc, lr):
    return "epoch {:3d} | loss {:.4f} | val acc {:.1f}% | lr {:.0e}".format(
        epoch, train_loss, val_acc * 100, lr)


def log_fstring(epoch, train_loss, val_acc, lr):
    return f"epoch {epoch:3d} | loss {train_loss:.4f} | val acc {val_acc:.1%} | lr {lr:.0e}"


# --- Other everyday uses ---------------------------------------------------

def run_name(model, lr, batch_size, seed):
    """Experiment / checkpoint name built from hyperparameters."""
    return f"{model}_lr{lr:g}_bs{batch_size}_seed{seed}"


def fmt_metric(value, places):
    """Book: expressions can go inside the format spec too."""
    return f"{value:.{places}f}"


def problem_1_demo():
    """Book problem #1: swap the tuple order and % fails at runtime."""
    loss, name = 0.1234, "val_loss"
    try:
        return "%-10s = %.4f" % (loss, name)
    except TypeError as err:
        return f"TypeError: {err}"


def accuracy(model, data):
    return sum(model.predict(x) == y for x, y in data) / len(data)


def main():
    print("=== Item 4: Prefer f-strings ===")
    args = (3, 0.41237, 0.8667, 1e-3)
    print("C-style    :", log_c_style(*args))
    print("str.format :", log_str_format(*args))
    print("f-string   :", log_fstring(*args))
    print("Swapped %  :", problem_1_demo())

    print("\nRun name:", run_name("logreg", 0.1, 32, 42))
    print("Precision as a variable:", fmt_metric(0.123456, places=3))

    print("\nTraining a toy classifier, logged with f-strings:")
    train, val, _ = split(make_dataset(n=1000))
    model, lr = LogisticRegression(), 0.1
    for epoch in range(1, 6):
        for batch in batches(train, 32):
            model.step(batch, lr)
        print("  " + log_fstring(epoch, model.loss(train), accuracy(model, val), lr))


if __name__ == "__main__":
    main()
