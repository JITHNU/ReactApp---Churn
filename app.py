#from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
from flask_cors import CORS  # Import CORS to handle cross-origin requests

# Load the trained model
model = joblib.load("churn_model.pkl")

# Define expected features
expected_features = ['SeniorCitizen', 'Tenure', 'MonthlyCharges', 'TotalCharges', 'Gender_Male',
                     'Partner_Yes', 'Dependents_Yes', 'PhoneService_Yes', 'MultipleLines_No phone service',
                     'MultipleLines_Yes', 'InternetService_Fiber optic', 'InternetService_No',
                     'OnlineSecurity_No internet service', 'OnlineSecurity_Yes', 'OnlineBackup_No internet service',
                     'OnlineBackup_Yes', 'DeviceProtection_No internet service', 'DeviceProtection_Yes',
                     'TechSupport_No internet service', 'TechSupport_Yes', 'StreamingTV_No internet service',
                     'StreamingTV_Yes', 'StreamingMovies_No internet service', 'StreamingMovies_Yes',
                     'Contract_One year', 'Contract_Two year', 'PaperlessBilling_Yes',
                     'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
                     'PaymentMethod_Mailed check']

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Churn Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON input from the request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Create a DataFrame with default values
        sample_data = pd.DataFrame([{feature: 0 for feature in expected_features}])
        
        # Update DataFrame with user-provided data
        for key in data:
            if key in sample_data.columns:
                sample_data[key] = data[key]

        # Ensure columns match training order
        sample_data = sample_data[expected_features]

        # Make prediction
        prediction = model.predict(sample_data)[0]
        result = "Churn" if prediction == 1 else "No Churn"

        return jsonify({"prediction": result})
    
    except Exception as e:
        print("Error:", str(e))  # Log error to console
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
