import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import random

# Enforce Clarity with Keyword-Only and Positional-Only Arguments

def generate_data(N=100, random_state=42):
    """Generates random binary classification data."""
    np.random.seed(random_state)
    X = np.random.randn(N, 5)  # N samples, 5 features
    y = np.random.choice([0, 1], size=N)  # Binary target
    return X, y

def train_model(X, y, batch_size=32, epochs=10):
    """Trains a logistic regression model on the given data."""  

    model = LogisticRegression(max_iter=epochs, solver="saga", optimizer="sgd")
    model.fit(X, y)
    return model

def train_model_goodway(X, y, /, *, batch_size=32, epochs=10):
    """Trains a logistic regression model on the given data."""
    model = LogisticRegression(max_iter=epochs, solver="saga", optimizer="sgd")
    model.fit(X, y)
    return model

if __name__ == "__main__":

    input("Generate data ...")
    X, y = generate_data(N=100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # print(X_train, X_test, y_train, y_test)

    model = train_model(X_train, y_train, batch_size=64, epochs=100)

    input("↑ Normal behavior.")
    model = train_model(X_train, y_train, 100, 64)
    
    input("↑ Batch size, epochs swapped.")
    
    model = train_model_goodway(X_train, y_train, 100, 64)
    input("↑ Good practice.")
    
