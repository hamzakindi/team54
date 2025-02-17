import logging
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.exceptions import NotFittedError
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

class ModelTrainer:
    def __init__(self, model, dataset_name=None):
        """
        Initialize ModelTrainer with a model and optional dataset name
        
        Args:
            model: sklearn model object
            dataset_name (str): Name of the dataset from data_dict
        """
        self.model = model
        self.dataset_name = dataset_name
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.is_fitted = False
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def check_data_prepared(self):
        """Check if data is prepared"""
        if any(x is None for x in [self.X_train, self.X_test, self.y_train, self.y_test]):
            raise ValueError("Data not prepared. Call prepare_data first.")
        return True

    def check_is_fitted(self):
        """Check if model is fitted"""
        try:
            # Try to make a prediction on a single sample
            self.model.predict(self.X_train[:1])
            self.is_fitted = True
            return True
        except (NotFittedError, AttributeError):
            self.is_fitted = False
            raise NotFittedError("Model must be trained before evaluation")

    def prepare_data(self, data_dict, dataset_name, target_column):
        """
        Prepare data from the data dictionary with proper handling of categorical features
        
        Args:
            data_dict (dict): Dictionary of datasets from load_data()
            dataset_name (str): Name of the dataset to use
            target_column (str): Name of the target column
        """
        try:
            from src.data.preprocessing import (
                handle_missing_values, 
                split_data,
                process_datetime_features
            )
            
            if dataset_name not in data_dict:
                raise KeyError(f"Dataset '{dataset_name}' not found")
            
            self.logger.info(f"Preparing dataset: {dataset_name}")    
            df = data_dict[dataset_name].copy()
            
            # Process datetime features first
            try:
                df = process_datetime_features(df)
                self.logger.debug("Datetime features processed")
            except Exception as e:
                self.logger.warning(f"Error processing datetime features: {str(e)}")
            
            # Handle missing values
            df = handle_missing_values(df)
            self.logger.debug("Missing values handled")
            
            # Identify numeric and categorical columns
            numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
            categorical_features = df.select_dtypes(include=['object', 'category']).columns
            categorical_features = categorical_features.drop(target_column) if target_column in categorical_features else categorical_features
            
            # Create preprocessing pipeline with updated OneHotEncoder parameters
            numeric_transformer = StandardScaler()
            categorical_transformer = OneHotEncoder(
                drop='first', 
                sparse_output=False,  # Updated from sparse to sparse_output
                handle_unknown='ignore'
            )
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_transformer, numeric_features),
                    ('cat', categorical_transformer, categorical_features)
                ],
                remainder='drop'
            )
            
            # Split data first
            self.X_train, self.X_test, self.y_train, self.y_test = split_data(
                df, target_column
            )
            
            # Fit and transform the training data
            self.X_train = preprocessor.fit_transform(self.X_train)
            self.X_test = preprocessor.transform(self.X_test)
            
            # Store the preprocessor for future transformations
            self.preprocessor = preprocessor
            self.dataset_name = dataset_name
            
            self.logger.info(f"Data prepared successfully. Training set shape: {self.X_train.shape}")
            
        except Exception as e:
            self.logger.error(f"Error preparing data: {str(e)}")
            raise

    def train(self):
        """Train the model on prepared data"""
        try:
            self.check_data_prepared()
            
            self.logger.info("Starting model training...")
            self.model.fit(self.X_train, self.y_train)
            self.is_fitted = True
            self.logger.info("Model training completed")
            
        except Exception as e:
            self.logger.error(f"Error during training: {str(e)}")
            raise

    def evaluate(self, X_test=None, y_test=None):
        """Evaluate model performance"""
        try:
            self.check_is_fitted()
            
            X = X_test if X_test is not None else self.X_test
            y = y_test if y_test is not None else self.y_test
            
            if X is None or y is None:
                raise ValueError("Test data not available")
            
            score = self.model.score(X, y)
            self.logger.info(f"Model evaluation score: {score:.4f}")
            return score
            
        except Exception as e:
            self.logger.error(f"Error during evaluation: {str(e)}")
            raise

    def save_model(self, filename):
        """Save trained model to file"""
        try:
            if not self.is_fitted:
                raise NotFittedError("Cannot save untrained model")
                
            save_path = Path(filename)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            joblib.dump(self.model, save_path)
            self.logger.info(f"Model saved to {save_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            raise

    def load_model(self, filename):
        """Load trained model from file"""
        try:
            load_path = Path(filename)
            if not load_path.exists():
                raise FileNotFoundError(f"Model file not found: {filename}")
                
            self.model = joblib.load(load_path)
            self.is_fitted = True
            self.logger.info(f"Model loaded from {load_path}")
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise

    def tune_hyperparameters(self, param_grid, X_train=None, y_train=None):
        """Perform grid search for hyperparameter tuning"""
        try:
            X = X_train if X_train is not None else self.X_train
            y = y_train if y_train is not None else self.y_train
            
            if X is None or y is None:
                raise ValueError("Training data not available")
            
            self.logger.info("Starting hyperparameter tuning...")
            grid_search = GridSearchCV(self.model, param_grid, cv=5, n_jobs=-1)
            grid_search.fit(X, y)
            
            self.model = grid_search.best_estimator_
            self.is_fitted = True
            
            self.logger.info(f"Best parameters: {grid_search.best_params_}")
            self.logger.info(f"Best score: {grid_search.best_score_:.4f}")
            
        except Exception as e:
            self.logger.error(f"Error during hyperparameter tuning: {str(e)}")
            raise