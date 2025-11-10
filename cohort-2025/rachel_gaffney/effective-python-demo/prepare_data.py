from sklearn.datasets import load_breast_cancer
import pandas as pd
import os

def main():
    os.makedirs("data", exist_ok=True)
    data = load_breast_cancer(as_frame=True)
    df = data.frame  # features + target in one DataFrame
    df.rename(columns={"target": "target"}, inplace=True)
    df.to_csv("data/cancer_data.csv", index=False)
    print("✅ Saved data/cancer_data.csv:", df.shape)

if __name__ == "__main__":
    main()