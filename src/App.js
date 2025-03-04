import React, { useState } from "react";
import "./styles.css"; 

function App() {
  const [formData, setFormData] = useState({
    Tenure: "",
    MonthlyCharges: "",
    TotalCharges: "",
    Gender_Male: false,
    InternetService_Fiber_optic: false,
    Contract_One_year: false,
    PaymentMethod_Electronic_check: false
  });

  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    const { name, type, checked, value } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8080/predict", { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      setPrediction(result.prediction);
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Failed to connect to API. Check if it's running.");
    }
  };

  return (
    <div className="container">
      <h1>Churn Prediction App</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <label>Tenure:</label>
        <input type="number" name="Tenure" placeholder="Enter Tenure" step="any" onChange={handleChange} required />

        <label>Monthly Charges:</label>
        <input type="number" name="MonthlyCharges" placeholder="Enter Monthly Charges" step="any" onChange={handleChange} required />

        <label>Total Charges:</label>
        <input type="number" name="TotalCharges" placeholder="Enter Total Charges" step="any" onChange={handleChange} required />

        <div className="checkbox-group">
          <label>
            <input type="checkbox" name="Gender_Male" onChange={handleChange} /> Gender: Male
          </label>
          <label>
            <input type="checkbox" name="InternetService_Fiber_optic" onChange={handleChange} /> Internet Service: Fiber Optic
          </label>
          <label>
            <input type="checkbox" name="Contract_One_year" onChange={handleChange} /> Contract: One Year
          </label>
          <label>
            <input type="checkbox" name="PaymentMethod_Electronic_check" onChange={handleChange} /> Payment Method: Electronic Check
          </label>
        </div>

        <button type="submit" className="submit-btn">Predict</button>
      </form>

      {prediction && <h2 className="prediction-result">Prediction: {prediction}</h2>}
    </div>
  );
}

export default App;



