def plot_data_distribution(data):
    import matplotlib.pyplot as plt
    data.hist(bins=30, figsize=(10, 7))
    plt.tight_layout()
    plt.show()

def calculate_metrics(y_true, y_pred):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'f1_score': f1_score(y_true, y_pred, average='weighted')
    }
    return metrics

def log_message(message):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(message)