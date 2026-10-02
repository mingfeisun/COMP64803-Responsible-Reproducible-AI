def compute_accuracy(predictions, targets):
    if len(predictions) == 0:
        return None
    
    correct = (predictions.argmax(dim=1) == targets).sum().item()
    return correct / len(predictions)


def evaluate_model(model, dataloader):
    accuracies = []
    for batch_x, batch_y in dataloader:
        mask = batch_y < 5
        filtered_x = batch_x[mask]
        filtered_y = batch_y[mask]
        
        preds = model(filtered_x)
        acc = compute_accuracy(preds, filtered_y)
        if acc is not None:
            accuracies.append(acc)
    
    return sum(accuracies) / len(accuracies) if accuracies else 0.0


def compute_accuracy_safe(predictions, targets):
    if len(predictions) == 0:
        raise ValueError(
            "Cannot compute accuracy on empty batch. "
        )
    
    correct = (predictions.argmax(dim=1) == targets).sum().item()
    return correct / len(predictions)

def evaluate_model_safe(model, dataloader):
    total_correct = 0
    total_samples = 0
    
    for batch_x, batch_y in dataloader:
        mask = batch_y < 5
        filtered_x = batch_x[mask]
        filtered_y = batch_y[mask]
        
        if len(filtered_x) == 0:
            continue
        
        preds = model(filtered_x)
        acc = compute_accuracy_safe(preds, filtered_y)
        
        total_correct += acc * len(filtered_y)
        total_samples += len(filtered_y)
    
    return total_correct / total_samples if total_samples > 0 else 0.0
