from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def create_model():
    """Create and return a new RandomForestRegressor model."""
    return RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )

def evaluate_model(model, X_test, y_test):
    """Evaluate the model and return performance metrics."""
    y_pred = model.predict(X_test)
    
    return {
        "Prediction": y_pred.mean(),
        "MAE": mean_absolute_error(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "R²": r2_score(y_test, y_pred)
    }