import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def mock_model(monkeypatch):
    # Mock model with a .predict method
    mock_model = MagicMock()
    mock_model.predict.return_value = [1]  # Versicolor
    monkeypatch.setattr(main, "model", mock_model)
    yield mock_model

@pytest.fixture(autouse=True)
def mock_static_files(monkeypatch, tmp_path):
    import builtins
    # Prepare dummy HTML files
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<html>Home</html>")
    (static_dir / "predict.html").write_text("<html>Predict</html>")

    real_open = builtins.open  # Save original open before patching

    def fake_open(file, mode='r', *args, **kwargs):
        filename = str(file)
        if "index.html" in filename:
            return real_open(static_dir / "index.html", mode, encoding="utf-8")
        elif "predict.html" in filename:
            return real_open(static_dir / "predict.html", mode, encoding="utf-8")
        return real_open(file, mode, *args, **kwargs)
    monkeypatch.setattr("builtins.open", fake_open)

def test_home_success():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html>Home</html>" in response.text

def test_predict_get_success():
    response = client.get("/predict")
    assert response.status_code == 200
    assert "<html>Predict</html>" in response.text

def test_home_file_not_found(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    response = client.get("/")
    assert response.status_code == 500
    assert "Error loading the home page." in response.text

def test_predict_file_not_found(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    response = client.get("/predict")
    assert response.status_code == 500
    assert "Error loading the prediction page." in response.text

def test_post_predict_success(mock_model):
    payload = {
        "sepal_length": 5.8,
        "sepal_width": 2.7,
        "petal_length": 4.1,
        "petal_width": 1.0
    }
    response = client.post(
        "/predict",
        data=payload
    )
    assert response.status_code == 200
    # Should map 1 -> "Iris Versicolor"
    assert response.json() == {"prediction": "Iris Versicolor"}

def test_post_predict_model_error(monkeypatch, mock_model):
    # Force model.predict to raise an Exception
    mock_model.predict.side_effect = Exception("Model fail")
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", data=payload)
    assert response.status_code == 500
    assert response.json()["error"] == "Failed to make a prediction"

def test_post_predict_invalid_form():
    # Missing fields
    payload = {
        "sepal_length": 5.8,
        "sepal_width": 2.7,
        "petal_length": 4.1
        # petal_width missing
    }
    response = client.post("/predict", data=payload)
    assert response.status_code == 422
