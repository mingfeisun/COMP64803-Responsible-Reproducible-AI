"""Item 10: Prevent Repetition with Assignment Expressions (the walrus :=).

Book: `:=` assigns AND evaluates in one expression (Python 3.8+). Use it to
  - fetch a value and test it in the same `if`
  - replace deep if/else nesting with a flat if/elif chain (switch/case)
  - replace the `while True: ... if not x: break` "loop-and-a-half"
Wrap it in parentheses when it is part of a bigger expression.

ML angle: early stopping, picking a device/strategy from a config, reading
a data stream, and pseudo-labelling without calling the model twice.
"""

from toy_ml import LogisticRegression, batches, make_dataset, split


# --- 1. Assign and test in one `if`: early stopping ------------------------

def fit_early_stopping(model, train, val, lr=0.1, max_epochs=50, patience=3):
    best, bad_epochs, epochs_run = float("inf"), 0, 0
    for epoch in range(1, max_epochs + 1):
        for batch in batches(train, 32):
            model.step(batch, lr)
        epochs_run = epoch
        if (val_loss := model.loss(val)) < best - 1e-3:
            best, bad_epochs = val_loss, 0
        elif (bad_epochs := bad_epochs + 1) >= patience:
            break
    return best, epochs_run


# --- 2. switch/case: choose a training strategy from a config ----------------

def strategy_nested(config):
    gpus = config.get("gpus", 0)
    if gpus >= 2:
        return f"DistributedDataParallel on {gpus} GPUs"
    else:
        mem = config.get("gpu_mem_gb", 0)
        if mem >= 16:
            return f"single GPU, batch 256 ({mem} GB)"
        else:
            cores = config.get("cpu_cores", 1)
            if cores:
                return f"CPU with {cores} workers"
            else:
                return "nothing available"


def strategy_walrus(config):
    if (gpus := config.get("gpus", 0)) >= 2:
        return f"DistributedDataParallel on {gpus} GPUs"
    elif (mem := config.get("gpu_mem_gb", 0)) >= 16:
        return f"single GPU, batch 256 ({mem} GB)"
    elif cores := config.get("cpu_cores", 1):
        return f"CPU with {cores} workers"
    else:
        return "nothing available"


# --- 3. do/while: consume a data stream until it is empty ------------------

def make_stream(data, batch_size):
    it = batches(data, batch_size)
    return lambda: next(it, [])  # returns [] when exhausted


def count_loop_and_a_half(next_batch):
    seen = 0
    while True:
        batch = next_batch()
        if not batch:
            break
        seen += len(batch)
    return seen


def count_walrus(next_batch):
    seen = 0
    while batch := next_batch():
        seen += len(batch)
    return seen


# --- 4. Pseudo-labelling: confident predictions, model called once -----------

def pseudo_label_repeated(model, unlabelled, threshold=0.95):
    return [(x, round(model.predict_proba(x)))
            for x in unlabelled
            if max(model.predict_proba(x), 1 - model.predict_proba(x)) >= threshold]


def pseudo_label_walrus(model, unlabelled, threshold=0.95):
    return [(x, round(p))
            for x in unlabelled
            if max(p := model.predict_proba(x), 1 - p) >= threshold]


def main():
    print("=== Item 10: Prevent repetition with := ===")
    train, val, test = split(make_dataset(n=400))
    model = LogisticRegression()
    best, epochs = fit_early_stopping(model, train, val)
    print(f"Early stopping: best val loss {best:.4f} after {epochs} epochs")

    for cfg in ({"gpus": 4}, {"gpus": 1, "gpu_mem_gb": 24}, {"cpu_cores": 8}):
        print(f"Config {cfg} -> {strategy_walrus(cfg)}")

    print(f"Streamed {count_walrus(make_stream(test, 16))} test examples "
          "with `while batch := next_batch():`")

    unlabelled = [x for x, _ in test]
    model.calls = 0
    kept = pseudo_label_repeated(model, unlabelled)
    calls_before = model.calls
    model.calls = 0
    kept_walrus = pseudo_label_walrus(model, unlabelled)
    print(f"\nPseudo-labelling {len(unlabelled)} points, kept {len(kept_walrus)} confident ones")
    print(f"  without := : {calls_before} model calls")
    print(f"  with :=    : {model.calls} model calls (same result: {kept == kept_walrus})")


if __name__ == "__main__":
    main()
