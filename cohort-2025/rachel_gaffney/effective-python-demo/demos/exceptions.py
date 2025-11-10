import os
import pandas as pd
from data import X_TRAIN, Y_TRAIN

""""Tip 3: Prefer raising exceptions to returning None
We validate that required artifacts exist and are sane; otherwise, raise explicit errors."""

def assert_exists(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} is missing — run previous steps first.")

def assert_nonempty_dataframe(path: str):
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"{path} is empty.")
    return df

def run_demo():
    # Fail loudly if anything is wrong
    assert_exists(X_TRAIN)
    assert_exists(Y_TRAIN)
    X = assert_nonempty_dataframe(X_TRAIN)
    y = assert_nonempty_dataframe(Y_TRAIN)

    # Simple sanity check: matching lengths
    if len(X) != len(y):
        raise ValueError(f"Length mismatch: X={len(X)} vs y={len(y)}")

    print("✅ All required files present and valid.")

