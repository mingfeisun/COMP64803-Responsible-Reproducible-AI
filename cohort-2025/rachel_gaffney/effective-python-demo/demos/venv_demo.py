import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from data import X_TRAIN_TOP, X_TEST_TOP, Y_TRAIN, Y_TEST

""""Tip 5: Use virtual environments for reproducibility
We show the pay-off: a clean, deterministic env that trains and evaluates a model."""

def run_demo():
    X_train = pd.read_csv(X_TRAIN_TOP)
    X_test = pd.read_csv(X_TEST_TOP)
    y_train = pd.read_csv(Y_TRAIN)["target"]
    y_test = pd.read_csv(Y_TEST)["target"]

    model = LogisticRegression(max_iter=500, n_jobs=None)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"✅ Model accuracy: {acc:.3f}")
    print("\nClassification report:\n", classification_report(y_test, preds, digits=3))
    print("\nThis ran inside a locked uv environment from pyproject/uv.lock.")