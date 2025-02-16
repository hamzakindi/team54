def load_data(file_path):
    import pandas as pd
    data = pd.read_csv(file_path)
    return data

def handle_missing_values(data):
    # Fill missing values with the mean of the column
    return data.fillna(data.mean())

def normalize_data(data):
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    return pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

def split_data(data, target_column, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)