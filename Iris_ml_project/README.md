# FastAPI Iris Species Prediction

A production-ready FastAPI application for predicting Iris species using a trained scikit-learn model. Features a REST API, interactive HTML UI, Docker support, and comprehensive test coverage.

## Features

- **REST API** with `/predict` endpoint for programmatic access
- **Interactive web interface** with HTML forms
- **Pre-trained scikit-learn model** for iris species classification
- **Docker support** for containerized deployment
- **Comprehensive test suite** with pytest (unit and integration tests)
- **Robust error handling** and logging
- **Input validation** using Pydantic

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Project Structure

```
Iris_ml_project/
├── .gitignore                # Excludes models, CSV, venv, IDE, cache, etc.
├── Dockerfile                # Containerizes the application
├── IRIS.csv                  # (Git-ignored) Original dataset for training
├── main.py                   # FastAPI app (serves API and web)
├── ml_iris.ipynb             # (Git-ignored) Model training notebook
├── model.pkl                 # (Git-ignored) Trained sklearn model
├── requirements.txt          # Python dependencies
├── static/
│   ├── index.html            # Home page
│   └── predict.html          # Prediction form page
├── test_integration_main.py  # Integration tests (API + static serving)
├── test_main.py              # Unit and edge-case tests
└── README.md                 # This file
```

## Installation & Setup

### 1. Local Development Setup

```bash
# Clone the repository
cd Iris_ml_project

# Create and activate virtual environment (recommended)
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Locally

```bash
uvicorn main:app --reload
```

The application will be available at [http://localhost:8000](http://localhost:8000)

### 3. Run with Docker

```bash
# Build the Docker image
docker build -t iris-fastapi-app .

# Run the container
docker run -p 8000:8000 iris-fastapi-app
```

Access the application at [http://localhost:8000](http://localhost:8000)

## API Usage

### Home Endpoint

- **GET /** - Returns the home page (static HTML)

### Prediction Page

- **GET /predict** - Returns the prediction form (static HTML)

### Prediction API

- **POST /predict** - Predict Iris species from input features

**Form-data parameters:**
- `sepal_length` (float): Sepal length in cm
- `sepal_width` (float): Sepal width in cm
- `petal_length` (float): Petal length in cm
- `petal_width` (float): Petal width in cm

**Example using cURL:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -F sepal_length=5.1 \
  -F sepal_width=3.5 \
  -F petal_length=1.4 \
  -F petal_width=0.2
```

**Example Response:**

```json
{
  "prediction": "Iris Setosa"
}
```

## Testing

The project includes comprehensive test coverage:

- **test_main.py**: Unit tests and edge case validation
- **test_integration_main.py**: Integration tests for routes, static files, and predictions

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
# Unit tests only
pytest test_main.py

# Integration tests only
pytest test_integration_main.py
```

### Run Tests with Coverage

```bash
pytest --cov=main --cov-report=html
```

## Model & Data

- **model.pkl**: Pre-trained Random Forest classifier using the Iris dataset
- **IRIS.csv**: Original dataset used for training
- **ml_iris.ipynb**: Jupyter notebook containing model training pipeline

Note: Model files and datasets are excluded from Git as per `.gitignore` configuration.

## Docker Deployment

The application is fully containerized using Docker.

**Dockerfile highlights:**
- Base image: `python:3.10-slim`
- Installs all dependencies from `requirements.txt`
- Exposes port 8000
- Uses Uvicorn as the ASGI server

**Build and run:**

```bash
docker build -t iris-fastapi-app .
docker run -p 8000:8000 iris-fastapi-app
```

## Static Files

The `static/` directory contains HTML pages for the web interface:

- **index.html**: Welcome page with navigation
- **predict.html**: Interactive prediction form

Minimal example for `static/index.html`:

```html
<!DOCTYPE html>
<html>
<body>
  <h1>Welcome to the Iris Species Predictor!</h1>
  <p><a href="/predict">Make a Prediction</a></p>
</body>
</html>
```

## Dependencies

See [requirements.txt](requirements.txt) for the complete list:

- fastapi - Web framework
- uvicorn - ASGI server
- scikit-learn - Machine learning library
- pandas - Data manipulation
- numpy - Numerical computations
- joblib - Model serialization
- pydantic - Data validation
- python-multipart - Form data handling
- pytest - Testing framework
- pytest-mock - Mocking for tests
- httpx - HTTP client for testing

## Advanced Features

- **Logging**: All application events and errors are logged to console
- **Environment variables**: Uses `$PORT` for container compatibility
- **Extensibility**: Easily add new endpoints or retrain the model using `ml_iris.ipynb`
- **CORS support**: Can be enabled for cross-origin requests (configured in main.py)

## License

MIT License (or specify your license)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn Iris Dataset](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pytest Documentation](https://docs.pytest.org/)
