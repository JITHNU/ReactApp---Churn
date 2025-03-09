import streamlit as st
import requests

st.title("Customer Churn Prediction")

tenure = st.number_input("Tenure", min_value=0, step=1)
monthly_charges = st.number_input("Monthly Charges", min_value=0.0, step=0.1)
total_charges = st.number_input("Total Charges", min_value=0.0, step=0.1)
gender_male = st.checkbox("Male")
internet_fiber = st.checkbox("Fiber Optic Internet")
contract_one_year = st.checkbox("One Year Contract")
payment_electronic = st.checkbox("Electronic Check")

input_data = {
    "Tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "Gender_Male": int(gender_male),
    "InternetService_Fiber optic": int(internet_fiber),
    "Contract_One year": int(contract_one_year),
    "PaymentMethod_Electronic check": int(payment_electronic),
}

if st.button("Predict Churn"):
    response = requests.post("http://127.0.0.1:8080/predict", json=input_data)
    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result['prediction']}")
    else:
        st.error("Error: Unable to get prediction")
