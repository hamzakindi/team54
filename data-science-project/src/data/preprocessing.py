from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

__all__ = [
    'load_data',
    'handle_missing_values',
    'normalize_data',
    'split_data',
    'process_datetime_features'
]

def load_data(csv_path=Path(r"C:\RnD\MedHack\archive\MedHack AI Hospital\csv")):
    """
    Load all CSV files from the specified directory into a dictionary.
    
    Args:
        csv_path (Path): Path to directory containing CSV files
    Returns:
        dict: Dictionary with filename stems as keys and DataFrames as values
    """
    data_dict = {}
    csv_files = list(csv_path.glob('*.csv'))
    
    for file in csv_files:
        try:
            data_dict[file.stem] = pd.read_csv(file)
            print(f"Successfully loaded: {file.name}")
        except Exception as e:
            print(f"Error loading {file.name}: {str(e)}")
    
    return data_dict

def handle_missing_values(data):
    """
    Fill missing values based on column data type:
    - Numeric columns: fill with mean
    - Categorical columns: fill with mode
    
    Args:
        data (pd.DataFrame): Input DataFrame
    Returns:
        pd.DataFrame: DataFrame with missing values handled
    """
    # Create a copy to avoid modifying original data
    df = data.copy()
    
    # Handle numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())
    
    # Handle categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
    
    return df

def normalize_data(data):
    """
    Normalize numerical data using MinMaxScaler while preserving categorical and datetime columns.
    
    Args:
        data (pd.DataFrame): Input DataFrame
    Returns:
        pd.DataFrame: Normalized DataFrame with original categorical and datetime columns
    """
    df = data.copy()
    
    # Identify column types
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Convert potential datetime strings to datetime
    for col in categorical_cols:
        try:
            df[col] = pd.to_datetime(df[col])
            datetime_cols = datetime_cols.append(pd.Index([col]))
            categorical_cols = categorical_cols.drop(col)
        except (ValueError, TypeError):
            continue
    
    # Handle datetime columns
    datetime_features = pd.DataFrame()
    for col in datetime_cols:
        datetime_features[f'{col}_year'] = df[col].dt.year
        datetime_features[f'{col}_month'] = df[col].dt.month
        datetime_features[f'{col}_day'] = df[col].dt.day
        datetime_features[f'{col}_hour'] = df[col].dt.hour
        datetime_features[f'{col}_minute'] = df[col].dt.minute
    
    # Normalize numeric columns
    if len(numeric_cols) > 0:
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    # Normalize extracted datetime features
    if not datetime_features.empty:
        datetime_scaler = MinMaxScaler()
        datetime_features = pd.DataFrame(
            datetime_scaler.fit_transform(datetime_features),
            columns=datetime_features.columns,
            index=df.index
        )
        df = pd.concat([df.drop(columns=datetime_cols), datetime_features], axis=1)
    
    return df

def split_data(data, target_column, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def process_datetime_features(df):
    """
    Convert datetime columns to numeric features
    
    Args:
        df (pd.DataFrame): Input dataframe
    Returns:
        pd.DataFrame: DataFrame with processed datetime features
    """
    datetime_columns = df.select_dtypes(include=['datetime64', 'object']).columns
    
    for col in datetime_columns:
        try:
            # Convert to datetime if not already
            df[col] = pd.to_datetime(df[col], errors='ignore')
            
            # If conversion successful, extract useful features
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[f'{col}_year'] = df[col].dt.year
                df[f'{col}_month'] = df[col].dt.month
                df[f'{col}_day'] = df[col].dt.day
                df[f'{col}_hour'] = df[col].dt.hour
                df[f'{col}_minute'] = df[col].dt.minute
                
                # Drop original datetime column
                df = df.drop(columns=[col])
        except Exception as e:
            continue
            
    return df