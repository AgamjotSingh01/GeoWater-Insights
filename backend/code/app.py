from flask import Flask, request, jsonify
import pandas as pd
import pickle
import preprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load models and scalers
try:
    with open('models/rf_models.pkl', 'rb') as f:
        models = pickle.load(f)
    with open('models/scalers.pkl', 'rb') as f:
        scalers = pickle.load(f)
    print("Models and scalers loaded successfully!")
except Exception as e:
    print(f"Error loading models: {str(e)}")
    models = None
    scalers = None

# Load dataset
try:
    data = pd.read_csv('data/data.csv', encoding='ISO-8859-1')
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    data = None

@app.route('/get_locations', methods=['GET'])
def get_locations():
    """Get all available locations from the dataset."""
    try:
        if data is None:
            return jsonify({"error": "Dataset not loaded"}), 500

        locations = data[['State_Name_With_LGD_Code', 'District_Name_With_LGD_Code', 'Block_Name_With_LGD_Code']].drop_duplicates()
        result = locations.to_dict('records')
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_districts/<state>', methods=['GET'])
def get_districts(state):
    """Get districts for a given state."""
    try:
        if data is None:
            return jsonify({"error": "Dataset not loaded"}), 500

        districts = data[data['State_Name_With_LGD_Code'] == state]['District_Name_With_LGD_Code'].unique().tolist()
        return jsonify(districts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_blocks/<state>/<district>', methods=['GET'])
def get_blocks(state, district):
    """Get blocks for a given state and district."""
    try:
        if data is None:
            return jsonify({"error": "Dataset not loaded"}), 500

        blocks = data[
            (data['State_Name_With_LGD_Code'] == state) & 
            (data['District_Name_With_LGD_Code'] == district)
        ]['Block_Name_With_LGD_Code'].unique().tolist()
        return jsonify(blocks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_aquifer_types', methods=['GET'])
def get_aquifer_types():
    """Get all available aquifer types."""
    try:
        if data is None:
            return jsonify({"error": "Dataset not loaded"}), 500

        aquifer_types = data['Aquifer'].unique().tolist()
        return jsonify(aquifer_types)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Make groundwater level predictions."""
    try:
        if models is None or scalers is None:
            return jsonify({"error": "Models not loaded"}), 500
        if data is None:
            return jsonify({"error": "Dataset not loaded"}), 500

        # Get input data
        input_data = request.get_json()
        
        if not input_data:
            return jsonify({"error": "No input data provided"}), 400

        required_fields = ['state', 'district', 'block', 'rainfall_status', 'aquifer_type']
        for field in required_fields:
            if field not in input_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Extract parameters
        state = input_data['state']
        district = input_data['district']
        block = input_data['block']
        rainfall_status = input_data['rainfall_status']
        aquifer_type = input_data['aquifer_type']

        # Filter data based on location and aquifer type
        filtered_data = data[
            (data['State_Name_With_LGD_Code'] == state) &
            (data['District_Name_With_LGD_Code'] == district) &
            (data['Block_Name_With_LGD_Code'] == block) &
            (data['Aquifer'] == aquifer_type)
        ]

        if filtered_data.empty:
            return jsonify({"error": "No data available for the given parameters"}), 404

        # Get the appropriate model and scaler
        model_key = 'post_monsoon' if rainfall_status.lower() == 'yes' else 'pre_monsoon'
        model = models[model_key]
        scaler = scalers[model_key]

        # Process the data
        processed_data, _, target_column = preprocess.process_data(filtered_data, rainfall_status)

        if processed_data is None:
            return jsonify({"error": "Error processing data"}), 500

        # Make prediction
        X = processed_data.drop(target_column, axis=1)
        prediction = model.predict(X)

        # Prepare response
        response = {
            "prediction": float(prediction.mean()),
            "location": {
                "state": state,
                "district": district,
                "block": block
            },
            "aquifer_type": aquifer_type,
            "season": "Post-monsoon" if rainfall_status.lower() == 'yes' else "Pre-monsoon"
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    status = {
        "status": "healthy",
        "models_loaded": models is not None,
        "scalers_loaded": scalers is not None,
        "dataset_loaded": data is not None
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)