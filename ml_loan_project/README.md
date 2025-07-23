# Loan Approval Prediction API

A production-ready FastAPI application for loan approval prediction using a trained Random Forest model and a scaler.

---

## Features

* Predicts loan approval via a web interface and API.
* Input form for all required features (gender, marital status, income, etc.).
* Pre-trained scikit-learn model and scaler (**required in project root**).
* Docker-ready, deployable anywhere.
* **Unit and integration tests included**.

---

## Folder Structure

```
ml_loan_project/
├── main.py
├── requirements.txt
├── Dockerfile
├── LoanApprovalPrediction.csv
├── .gitignore
├── static/
│   ├── index.html
│   ├── predict.html
│   ├── style.css
│   └── styles.css
├── random_forest_model.pkl      
├── scaler.pkl                  
├── tests/
│   ├── __init__.py
│   ├── test_unit_model.py
│   └── test_integration_api.py
└── README.md
```

---

## Setup & Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Place model artifacts

* Add `random_forest_model.pkl` and `scaler.pkl` to the project root.

### 3. Run the application

```bash
uvicorn main:app --reload
```

The API is available at: `http://localhost:8000` or `http://127.0.0.1:8000`

### 4. Run tests

```bash
pytest tests/
```

---

## Docker Deployment

```bash
docker build -t loan-approval-api .
docker run -p 8000:8000 loan-approval-api
```

* Access the app at: `http://localhost:8000/` or `http://127.0.0.1:8000/`
* **Do NOT use `http://0.0.0.0:8000/` in your browser.**

---

## Endpoints

* `GET /` : Home page
* `GET/POST /predict` : Loan approval prediction form & result

---

## Test Coverage

* **Unit tests**: Validate model and scaler functionality with controlled input.
* **Integration tests**: Validate API endpoints, form submission, and prediction result.

---

## Project Notes

* **Model artifacts are not included** for security and size reasons.
* To re-train or update the model, use the provided notebook or your own pipeline, then save as `random_forest_model.pkl` and `scaler.pkl`.
* Static files are under `static/`.
* All code is Python 3.8+ and tested on FastAPI 0.110+.

---
