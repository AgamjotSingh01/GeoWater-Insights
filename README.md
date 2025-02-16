# 🌍 Groundwater Level Prediction API

This project is a Flask-based API that leverages machine learning to predict groundwater levels based on historical data. It is designed to assist in water resource management, providing valuable insights for farmers, policymakers, and researchers.

## 🚀 Features
- **Machine Learning Model:** Predicts groundwater levels using historical data.
- **Flask API:** Handles requests and serves predictions efficiently.
- **React Frontend:** Provides an interactive UI for users.
- **Data Processing & Feature Engineering:** Cleans and prepares data for better model accuracy.
- **Time Series Forecasting:** Uses models like LSTM and CNN for predictive insights.
- **CSV-Based Data Handling:** Reads and processes data from `data.csv`.
- **CORS Enabled:** Ensures smooth frontend-backend communication.

## 🛠️ Tech Stack
- Python, Flask, Pandas, NumPy, Scikit-learn
- Machine Learning (Random Forest, LSTM, CNN)
- React (Frontend UI)
- REST API Integration

## 🔧 Setup Instructions
### Clone the repository:
```sh
git clone https://github.com/your-username/groundwater-prediction-api.git
cd groundwater-prediction-api
```

### Install dependencies:
For Flask backend:
```sh
pip install -r requirements.txt
```

For React frontend:
```sh
cd frontend
npm install
```

### Run the Flask server:
```sh
python app.py
```

### Start the React frontend:
```sh
npm run dev
```

## 📌 API Usage
Send a `POST` request to `/predict` with JSON data:
```json
{
  "state": "Uttar Pradesh_9",
  "district": "Baghpat_124",
  "block": "Pilana_893",
  "rainfall_status": "yes",
  "aquifer_type": "Unconfined"
}
```
The API will return a groundwater level prediction along with performance metrics.


## 📷 Screenshots

![ss1](https://github.com/user-attachments/assets/9910e06c-b155-4f32-a6e4-69f5108dbfbd)
<br>
![ss2](https://github.com/user-attachments/assets/b5e1989e-633c-4f19-abd2-4e2917ec337c)
<br>
![image](https://github.com/user-attachments/assets/fdca25bd-2b7f-4325-9f41-b20d8a039275)
<br>

## 📢 Contributions
Feel free to fork, contribute, and improve the project! 🚀

🔗 #MachineLearning #FlaskAPI #GroundwaterPrediction #AIForGood
