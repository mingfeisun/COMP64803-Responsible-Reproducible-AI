import pandas as pd

def load_data(filepath):
    """Loads data from a CSV file without specifying dtypes, which can cause type mismatches."""
    df = pd.read_csv(filepath)  # No dtype specification
    return df

def clean_data(df):
    """Cleans data by ensuring correct data types."""
    df['age'] = df['age'].astype(int)      # Convert age to integer
    df['height'] = df['height'].astype(float)  # Convert height to float
    df['weight'] = df['weight'].astype(int)    # Convert weight to integer
    return df
