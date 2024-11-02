import random
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from collections import namedtuple

def generate_data(N=20):
    """Generates random binary classification data."""

    y_true = [random.choice([0, 1]) for _ in range(N)]
    y_pred = [random.choice([0, 1]) for _ in range(N)]

    print(f"y_true:{y_true}")
    print(f"y_pred:{y_pred}")

    return y_true, y_pred

# incorrect practice

def compute_metrics(y_true, y_pred):
    """Return some metrics of interest"""

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    return accuracy, precision, recall, f1

# best practice: use dictionary/named tuple

def compute_metrics_goodway(y_true, y_pred):
    """Return some metrics of interest"""

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred)
    }
    
    return metrics

if __name__ == "__main__":
    input("")
    y_true, y_pred = generate_data()

    # dangerous practice
    input("")
    accuracy, precision, recall, f1 = compute_metrics(y_true, y_pred)
    print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

    # dangerous practice trigger a bug that can be spotted
    input("")
    precision, accuracy, recall, f1 = compute_metrics(y_true, y_pred)
    print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

    # good practice
    input("")
    metrics = compute_metrics_goodway(y_true, y_pred)
    print(f"Accuracy: {metrics['accuracy']}, Precision: {metrics['precision']}, 
          Recall: {metrics['recall']}, F1 Score: {metrics['f1_score']}")
