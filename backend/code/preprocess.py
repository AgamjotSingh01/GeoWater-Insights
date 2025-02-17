import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(file_path):
    """Load and return the dataset."""
    try:
        return pd.read_csv(file_path, encoding='ISO-8859-1')
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        raise

def process_data(data, state, district, block, rainfall_status, aquifer_type):
    """Process the data according to input parameters."""
    try:
        # Filter based on state, district, and block
        df = data.query("State_Name_With_LGD_Code == @state & District_Name_With_LGD_Code == @district & Block_Name_With_LGD_Code == @block")

        if df.empty:
            return None, "No data available for the given state, district, and block."

        # Filter columns based on rainfall condition
        if rainfall_status.lower() == 'yes':
            monsoon_cols = [col for col in df.columns if 'Post-monsoon' in col]
        elif rainfall_status.lower() == 'no':
            monsoon_cols = [col for col in df.columns if 'Pre-monsoon' in col]
        else:
            return None, "Invalid rainfall status. Enter 'yes' for post-monsoon or 'no' for pre-monsoon."

        df_filtered = df[monsoon_cols]

        # Select additional columns
        additional_cols = df[['Aquifer', 'Latitude', 'Longitude']]
        df = pd.concat([additional_cols, df_filtered], axis=1)

        # Convert columns to numeric and handle missing values
        df[df_filtered.columns] = df[df_filtered.columns].apply(pd.to_numeric, errors='coerce')
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

        # Well condition mapping
        well_condition_mapping = {
            'Abandoned': 0, 'Closed': 0, 'Filled up': 216, 'Dry': 0, 'dry': 0, 'DRY': 0,
            'Damage': 0, 'Collapsed': 0, 'filled up': 216, 'Filled Up': 216, 'buried': 0, 'Buried': 0
        }
        for col in df_filtered.columns:
            df[col] = df[col].replace(well_condition_mapping).astype(float)

        # Filter by Aquifer Type
        df = df[df['Aquifer'] == aquifer_type]

        if df.empty:
            return None, "No data available for the given aquifer type."

        # Convert categorical columns to dummies
        df = pd.get_dummies(df, columns=['Aquifer'])

        # Normalize numerical data
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        scaler = MinMaxScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])

        return df, scaler, None

    except Exception as e:
        logger.error(f"Error in process_data: {str(e)}")
        return None, None, str(e)

def prepare_features(df, rainfall_status):
    """Prepare features and target for model training."""
    try:
        target_column = 'Post-monsoon_2022 (meters below ground level)' if rainfall_status.lower() == 'yes' \
            else 'Pre-monsoon_2022 (meters below ground level)'
        
        if target_column not in df.columns:
            return None, None, f"Target column '{target_column}' not found in the dataset."
        
        X = df.drop(target_column, axis=1).values
        y = df[target_column].values
        
        return X, y, None
        
    except Exception as e:
        logger.error(f"Error in prepare_features: {str(e)}")
        return None, None, str(e)