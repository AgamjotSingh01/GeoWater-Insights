import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = pd.read_csv(r'./data.csv', encoding='ISO-8859-1')

def generate_graph(y_test, y_pred):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.5, label="Predicted vs Actual")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], '--', color='red', label="Ideal Fit")
    plt.xlabel("Actual Groundwater Level (m bgl)")
    plt.ylabel("Predicted Groundwater Level (m bgl)")
    plt.title("Groundwater Level Prediction Performance")
    plt.legend()
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_image = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return encoded_image

def process_and_predict(state, district, block, rainfall_status, aquifer_type):
    df = data.query("`State_Name_With_LGD_Code` == @state and `District_Name_With_LGD_Code` == @district and `Block_Name_With_LGD_Code` == @block").copy()
    
    if rainfall_status.lower() == 'yes':
        post_monsoon_cols = [col for col in df.columns if 'Post-monsoon' in col]
        df_filtered = df.loc[:, post_monsoon_cols]
    elif rainfall_status.lower() == 'no':
        pre_monsoon_cols = [col for col in df.columns if 'Pre-monsoon' in col]
        df_filtered = df.loc[:, pre_monsoon_cols]
    else:
        return {"error": "Invalid rainfall status. Enter 'yes' for post-monsoon or 'no' for pre-monsoon."}
    
    required_cols = ['Aquifer', 'Latitude', 'Longitude']
    for col in required_cols:
        if col not in df.columns:
            return {"error": f"Missing required column: {col}"}
    
    additional_cols = df.loc[:, required_cols]
    df_filtered = pd.concat([additional_cols, df_filtered], axis=1)
    
    cols_to_convert = df_filtered.columns[3:]
    df_filtered[cols_to_convert] = df_filtered[cols_to_convert].apply(pd.to_numeric, errors='coerce')
    df_filtered.fillna(df_filtered.mean(numeric_only=True), inplace=True)
    
    well_condition_mapping = {
        'Abandoned': 0, 'Closed': 0, 'Filled up': 216, 'Dry': 0, 'dry': 0, 'DRY': 0,
        'Damage': 0, 'Collapsed': 0, 'filled up': 216, 'Filled Up': 216, 'buried': 0, 'Buried': 0
    }
    df_filtered.replace(well_condition_mapping, inplace=True)
    
    df_filtered = df_filtered[df_filtered['Aquifer'] == aquifer_type]
    df_filtered['Aquifer'] = df_filtered['Aquifer'].astype(str)
    df_filtered = pd.get_dummies(df_filtered, columns=['Aquifer'])
    
    num_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns
    scaler = MinMaxScaler()
    df_filtered.loc[:, num_cols] = scaler.fit_transform(df_filtered[num_cols])
    
    target_column = 'Post-monsoon_2022 (meters below ground level)' if rainfall_status.lower() == 'yes' else 'Pre-monsoon_2022 (meters below ground level)'
    
    if target_column in df_filtered.columns:
        X = df_filtered.drop(target_column, axis=1).values
        y = df_filtered[target_column].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        rf_model = RandomForestRegressor(n_estimators=100, max_depth=20, min_samples_split=5, min_samples_leaf=2, random_state=42)
        rf_model.fit(X_train, y_train)
        
        y_pred = rf_model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        graph = generate_graph(y_test, y_pred)
        
        return {
            "Prediction": float(np.mean(y_pred)),
            "MAE": float(mae),
            "MSE": float(mse),
            "R²": float(r2),
            "Graph": graph,
            "Groundwater_Level": [float(value) for value in y_pred]
        }
    else:
        return {"error": f"Target column '{target_column}' not found in the dataset."}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print(data)
    state = data.get('state')
    district = data.get('district')
    block = data.get('block')
    rainfall_status = data.get('rainfall_status')
    aquifer_type = data.get('aquifer_type')
    
    result = process_and_predict(state, district, block, rainfall_status, aquifer_type)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
