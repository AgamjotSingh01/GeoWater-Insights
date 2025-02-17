import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
import preprocess
import model
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model(data, state, district, block, rainfall_status, aquifer_type):
    """Train a model for the given parameters."""
    try:
        # Process data
        processed_data, scaler, error = preprocess.process_data(
            data, state, district, block, rainfall_status, aquifer_type
        )
        
        if error:
            return None, None, error
            
        # Prepare features
        X, y, error = preprocess.prepare_features(processed_data, rainfall_status)
        
        if error:
            return None, None, error

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Hyperparameter tuning with GridSearchCV
        param_grid = {
            'n_estimators': [100],
            'max_depth': [20],
            'min_samples_split': [5],
            'min_samples_leaf': [2]
        }
        
        rf_model = model.create_model()
        grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_
        
        return best_model, scaler, None

    except Exception as e:
        logger.error(f"Error in train_model: {str(e)}")
        return None, None, str(e)

def train_and_save_models():
    """Train models for all available combinations and save them."""
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')

    # Load data
    data = preprocess.load_data('data/data.csv')
    
    models = {}
    scalers = {}
    
    # Get unique combinations
    states = data['State_Name_With_LGD_Code'].unique()
    
    for state in states:
        logger.info(f"Processing state: {state}")
        state_data = data[data['State_Name_With_LGD_Code'] == state]
        districts = state_data['District_Name_With_LGD_Code'].unique()
        
        for district in districts:
            logger.info(f"Processing district: {district}")
            district_data = state_data[state_data['District_Name_With_LGD_Code'] == district]
            blocks = district_data['Block_Name_With_LGD_Code'].unique()
            aquifer_types = district_data['Aquifer'].unique()
            
            for block in blocks:
                for aquifer_type in aquifer_types:
                    for rainfall_status in ['yes', 'no']:
                        logger.info(f"Training model for {state}-{district}-{block}-{aquifer_type}-{rainfall_status}")
                        
                        trained_model, scaler, error = train_model(
                            data, state, district, block, rainfall_status, aquifer_type
                        )
                        
                        if error:
                            logger.warning(f"Error training model: {error}")
                            continue
                            
                        key = f"{state}_{district}_{block}_{aquifer_type}_{rainfall_status}"
                        models[key] = trained_model
                        scalers[key] = scaler
                        
                        logger.info(f"Successfully trained model for {key}")

    # Save models and scalers
    try:
        with open('models/rf_models.pkl', 'wb') as f:
            pickle.dump(models, f)
        
        with open('models/scalers.pkl', 'wb') as f:
            pickle.dump(scalers, f)
            
        logger.info("Successfully saved all models and scalers")
        
    except Exception as e:
        logger.error(f"Error saving models and scalers: {str(e)}")
        raise

if __name__ == "__main__":
    train_and_save_models()