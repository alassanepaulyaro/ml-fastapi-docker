import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_model_and_scaler():
    mock_model = MagicMock()
    mock_model.predict.return_value = [7]
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = [[0.1]*11]
    with patch("main.joblib.load", side_effect=[mock_model, mock_scaler]):
        # reload model/scaler after patching
        import importlib
        import main as main_module
        importlib.reload(main_module)
        yield mock_model, mock_scaler

def test_home():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()
    assert "Wine Quality" in resp.json()["message"]

def test_predict_success(mock_model_and_scaler):
    payload = {
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.70,
        "citric_acid": 0.00,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11.0,
        "total_sulfur_dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    assert "predicted_quality" in resp.json()
    assert resp.json()["predicted_quality"] == "7"

@pytest.mark.parametrize("missing_field", [
    "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
    "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
    "pH", "sulphates", "alcohol"
])
def test_predict_missing_field(missing_field):
    payload = {
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.70,
        "citric_acid": 0.00,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11.0,
        "total_sulfur_dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4
    }
    del payload[missing_field]
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 422

def test_predict_invalid_type():
    payload = {
        "fixed_acidity": "not_a_float",  # Invalid
        "volatile_acidity": 0.70,
        "citric_acid": 0.00,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11.0,
        "total_sulfur_dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 422

def test_predict_model_exception(mock_model_and_scaler):
    model, scaler = mock_model_and_scaler
    model.predict.side_effect = Exception("Prediction error")
    payload = {
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.70,
        "citric_acid": 0.00,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11.0,
        "total_sulfur_dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4
    }
    with patch("main.model", model), patch("main.scaler", scaler):
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 500
        assert "Error during prediction" in resp.json()["detail"]
