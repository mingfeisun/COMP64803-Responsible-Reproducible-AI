import pandas as pd
from data import CSV_PATH, NORMALIZED_CSV

"""Tip 1: Write helper functions instead of complex expressions
We encapsulate normalization, making preprocessing reusable and readable."""

def minmax_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize numeric columns to [0, 1] range; leave non-numeric intact."""
    num = df.select_dtypes(include="number")
    den = (num.max() - num.min()).replace(0, 1)  # avoid divide-by-zero
    scaled = (num - num.min()) / den
    out = df.copy()
    out[scaled.columns] = scaled
    return out

def run_demo():
    df = pd.read_csv(CSV_PATH)
    features = df.drop(columns=["target"])
    target = df["target"].copy()

    # Use helper function
    normalized = minmax_normalize(features)
    normalized["target"] = target

    normalized.to_csv(NORMALIZED_CSV, index=False)
    print(f"✅ Normalized features saved to {NORMALIZED_CSV}")
    print(normalized.head(3).to_string(index=False))
