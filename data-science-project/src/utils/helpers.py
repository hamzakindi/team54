def plot_data_distribution(data, dataset_name=None):
    """
    Plot distribution of data features
    
    Args:
        data: pandas DataFrame or dictionary of DataFrames
        dataset_name (str): If data is a dict, specify dataset to plot
    """
    import matplotlib.pyplot as plt
    
    if isinstance(data, dict):
        if dataset_name is None:
            raise ValueError("dataset_name must be specified when passing a dictionary")
        if dataset_name not in data:
            raise KeyError(f"Dataset '{dataset_name}' not found")
        df = data[dataset_name]
    else:
        df = data
        
    df.hist(bins=30, figsize=(10, 7))
    plt.suptitle(f'Data Distribution - {dataset_name if dataset_name else ""}')
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