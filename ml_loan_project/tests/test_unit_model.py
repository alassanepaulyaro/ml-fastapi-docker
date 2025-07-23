import joblib
import numpy as np
import pandas as pd
import pytest

@pytest.fixture(scope="module")
def model_and_scaler():
    model = joblib.load("random_forest_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

def test_model_predict_shape(model_and_scaler):
    model, scaler = model_and_scaler
    X_sample = pd.DataFrame([{
        'Gender': 1, 'Married': 1, 'Dependents': 0, 'Education': 1,
        'Self_Employed': 0, 'ApplicantIncome': 5000, 'CoapplicantIncome': 2000,
        'LoanAmount': 120, 'Loan_Amount_Term': 360, 'Credit_History': 1, 'Property_Area': 2
    }])
    X_scaled = scaler.transform(X_sample)
    prediction = model.predict(X_scaled)
    assert prediction.shape == (1,), "Model prediction should return a single value."

def test_model_predict_values(model_and_scaler):
    model, scaler = model_and_scaler
    X_sample = pd.DataFrame([{
        'Gender': 0, 'Married': 0, 'Dependents': 1, 'Education': 0,
        'Self_Employed': 1, 'ApplicantIncome': 2500, 'CoapplicantIncome': 0,
        'LoanAmount': 80, 'Loan_Amount_Term': 240, 'Credit_History': 0, 'Property_Area': 1
    }])
    X_scaled = scaler.transform(X_sample)
    prediction = model.predict(X_scaled)
    assert prediction[0] in [0, 1], "Prediction should be binary (0 or 1)."
