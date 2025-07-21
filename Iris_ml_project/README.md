# FastAPI Iris Species Prediction

## Overview

Production-ready FastAPI application to predict Iris species using a scikit-learn model, featuring a REST API, HTML form UI, Docker support, and full test coverage.

---

## Project Structure

```

├── .gitignore                # Excludes models, CSV, venv, IDE, cache, etc.
├── Dockerfile                # Containerizes the application
├── IRIS.csv                  # (Ignored by Git) Original dataset for training
├── main.py                   # FastAPI app (serves API and web)
├── ml\_iris.ipynb             # (Ignored by Git) Model training notebook
├── model.pkl                 # (Ignored by Git) Trained sklearn model
├── requirements.txt          # Python dependencies
├── static/
│   ├── index.html            # Home page (provide or customize as needed)
│   └── predict.html          # Prediction page (provide or customize as needed)
├── test\_integration\_main.py  # Integration tests (API + static serving)
├── test\_main.py              # Unit and edge-case tests

````

---

## Features

- **/ (GET):** Home page (static HTML)
- **/predict (GET):** Prediction form (static HTML)
- **/predict (POST):** Predict Iris species via form or API (returns JSON)
- **Robust logging and error handling**
- **Dockerized deployment**
- **Pytest-based integration/unit test suites**

---

## Quick Start

### 1. Build & Run Locally

```bash
# (Recommended) Use a virtual environment
python -m venv .venv
source .venv/bin/activate         # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
````

App available at [http://localhost:8000](http://localhost:8000)

### 2. Run with Docker

```bash
docker build -t iris-fastapi-app .
docker run -p 8000:8000 iris-fastapi-app
```

---

## API Usage

### Predict Endpoint

* **POST /predict**

  * Form-data:

    * `sepal_length` (float)
    * `sepal_width` (float)
    * `petal_length` (float)
    * `petal_width` (float)
  * **Example:**

    ```bash
    curl -X POST "http://localhost:8000/predict" \
      -F sepal_length=5.1 -F sepal_width=3.5 \
      -F petal_length=1.4 -F petal_width=0.2
    ```
  * **Response:**

    ```json
    {"prediction": "Iris Setosa"}
    ```

---

## Testing

Run all tests with:

```bash
pytest
```

* `test_main.py`: Unit tests and edge cases
* `test_integration_main.py`: Integration (routes + static + prediction)

---

## Model & Data

* **model.pkl**: Pretrained with `ml_iris.ipynb` using `IRIS.csv`.
* Both files are ignored by Git as per `.gitignore`.

---

## Docker

### Build

```dockerfile
# Dockerfile content (see actual file for details)
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Usage

```bash
docker build -t iris-fastapi-app .
docker run -p 8000:8000 iris-fastapi-app
```

---

## Static Files

* Place `index.html` and `predict.html` in `static/`.

  * Minimal example for `static/index.html`:

    ```html
    <html><body><h1>Welcome to the Iris Predictor!</h1></body></html>
    ```

---

## .gitignore Highlights

* Ignores: virtualenvs, `.pkl` models, datasets (`*.csv`), caches, notebooks, IDE/project files.

---

## Requirements

```
fastapi
joblib
numpy
pandas
pydantic
pytest
httpx
uvicorn
scikit-learn
python-multipart
pytest
pytest-mock
httpx
```

---

## Advanced

* Logging: All app events and errors are logged.
* Environment: Uses `$PORT` for container compatibility.
* Extendable: Add new endpoints, models, or retrain using `ml_iris.ipynb`.

---

## Authors

* \[Your Name / Org]

## License

* \[Specify License]

---

## References

* [FastAPI](https://fastapi.tiangolo.com/)
* [scikit-learn Iris Dataset](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html)
