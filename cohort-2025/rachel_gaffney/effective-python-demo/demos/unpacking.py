import pandas as pd
from sklearn.model_selection import train_test_split
from data import NORMALIZED_CSV, X_TRAIN, X_TEST, Y_TRAIN, Y_TEST

"""Tip 2: Prefer multiple assignment unpacking over indexing
We split data and unpack the result directly into four variables."""

def run_demo():
    df = pd.read_csv(NORMALIZED_CSV)
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train.to_csv(X_TRAIN, index=False)
    X_test.to_csv(X_TEST, index=False)
    y_train.to_csv(Y_TRAIN, index=False, header=["target"])
    y_test.to_csv(Y_TEST, index=False, header=["target"])

    print(f"✅ Train/Test split saved: {X_train.shape=} {X_test.shape=}")
