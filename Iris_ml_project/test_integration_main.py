import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def setup_model_and_files(monkeypatch, tmp_path):
    import builtins
    # Patch model: always return class 2 (Iris Virginica)
    mock_model = MagicMock()
    mock_model.predict.return_value = [2]
    monkeypatch.setattr(main, "model", mock_model)

    # Patch open() for static files
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<html>Welcome</html>")
    (static_dir / "predict.html").write_text("<html>Predict</html>")

    real_open = builtins.open  # Save the original open

    def fake_open(file, mode='r', *args, **kwargs):
        filename = str(file)
        if "index.html" in filename:
            return real_open(static_dir / "index.html", mode, encoding="utf-8")
        elif "predict.html" in filename:
            return real_open(static_dir / "predict.html", mode, encoding="utf-8")
        # Fallback to original open for all other files (important for Python/pytest internals)
        return real_open(file, mode, *args, **kwargs)
    monkeypatch.setattr("builtins.open", fake_open)
    yield

def test_home_integration():
    r = client.get("/")
    assert r.status_code == 200
    assert "<html>Welcome</html>" in r.text

def test_predict_get_integration():
    r = client.get("/predict")
    assert r.status_code == 200
    assert "<html>Predict</html>" in r.text

def test_predict_species_integration():
    data = {
        "sepal_length": 6.1,
        "sepal_width": 2.8,
        "petal_length": 4.7,
        "petal_width": 1.2
    }
    r = client.post("/predict", data=data)
    assert r.status_code == 200
    # Should match species_mapping[2]
    assert r.json() == {"prediction": "Iris Virginica"}

def test_predict_species_integration_invalid(monkeypatch):
    # Force error in model
    monkeypatch.setattr(main.model, "predict", lambda x: (_ for _ in ()).throw(Exception("Boom")))
    data = {
        "sepal_length": 6.1,
        "sepal_width": 2.8,
        "petal_length": 4.7,
        "petal_width": 1.2
    }
    r = client.post("/predict", data=data)
    assert r.status_code == 500
    assert r.json()["error"] == "Failed to make a prediction"

def test_predict_missing_form_field():
    # Should return 422 due to missing field
    data = {
        "sepal_length": 6.1,
        "sepal_width": 2.8,
        "petal_length": 4.7
        # missing petal_width
    }
    r = client.post("/predict", data=data)
    assert r.status_code == 422
