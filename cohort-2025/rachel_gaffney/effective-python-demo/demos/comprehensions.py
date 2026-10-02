import pandas as pd
from data import X_TRAIN, X_TEST, X_TRAIN_TOP, X_TEST_TOP

"""Tip 4: Use comprehensions instead of loops
We compute variances and pick the top-K features using dict/list comprehensions."""

TOP_K = 10

def run_demo():
    X_train = pd.read_csv(X_TRAIN)
    X_test = pd.read_csv(X_TEST)

    # Dict comprehension for variances
    variances = {col: X_train[col].var() for col in X_train.columns}

    # List comprehension to select top-K by variance
    selected = [c for c, _ in sorted(variances.items(), key=lambda kv: kv[1], reverse=True)[:TOP_K]]

    pd.DataFrame(X_train[selected]).to_csv(X_TRAIN_TOP, index=False)
    pd.DataFrame(X_test[selected]).to_csv(X_TEST_TOP, index=False)

    print(f"✅ Selected top-{TOP_K} features and saved:")
    print(", ".join(selected))
