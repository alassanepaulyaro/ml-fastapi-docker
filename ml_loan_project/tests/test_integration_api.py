import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Loan Approval Prediction API" in response.text

def test_predict_post_approved():
    form_data = {
        "Gender": 1,
        "Married": 1,
        "Dependents": 0,
        "Education": 1,
        "Self_Employed": 0,
        "ApplicantIncome": 4000,
        "CoapplicantIncome": 1500,
        "LoanAmount": 100,
        "Loan_Amount_Term": 360,
        "Credit_History": 1,
        "Property_Area": 2
    }
    response = client.post("/predict", data=form_data)
    assert response.status_code == 200
    assert "Loan Status" in response.text

def test_predict_post_missing_field():
    form_data = {
        "Gender": 1,
        "Married": 1,
        # Missing Dependents
        "Education": 1,
        "Self_Employed": 0,
        "ApplicantIncome": 4000,
        "CoapplicantIncome": 1500,
        "LoanAmount": 100,
        "Loan_Amount_Term": 360,
        "Credit_History": 1,
        "Property_Area": 2
    }
    response = client.post("/predict", data=form_data)
    assert response.status_code == 200
    assert "Loan Status" in response.text and ("Approved" in response.text or "Not Approved" in response.text)
