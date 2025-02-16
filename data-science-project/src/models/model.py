class ModelTrainer:
    def __init__(self, model, X_train, y_train):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self, X_test, y_test):
        return self.model.score(X_test, y_test)

    def save_model(self, filename):
        import joblib
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        import joblib
        self.model = joblib.load(filename)

    def tune_hyperparameters(self, param_grid, X_train, y_train):
        from sklearn.model_selection import GridSearchCV
        grid_search = GridSearchCV(self.model, param_grid, cv=5)
        grid_search.fit(X_train, y_train)
        self.model = grid_search.best_estimator_