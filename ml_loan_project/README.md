# Loan Approval Prediction API

A production-ready FastAPI application for predicting loan approval using a trained Random Forest classifier. Features a web interface, REST API, comprehensive test coverage, and Docker support.

## Features

- **Machine Learning**: Random Forest classifier for binary loan approval prediction
- **Web Interface**: User-friendly HTML form for loan applications
- **REST API**: Programmatic access via POST endpoint
- **Pre-trained Model**: Includes trained Random Forest model and StandardScaler
- **Docker Ready**: Containerized for easy deployment
- **Test Coverage**: Unit and integration tests with pytest
- **Input Validation**: Robust form and API validation
- **Error Handling**: Comprehensive logging and error messages

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Project Structure

```
ml_loan_project/
├── main.py                      # FastAPI application
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── LoanApprovalPrediction.csv   # Dataset for training
├── .gitignore                   # Git ignore rules
├── static/
│   ├── index.html               # Home page
│   ├── predict.html             # Prediction form
│   ├── style.css                # Stylesheet
│   └── styles.css               # Additional styles
├── random_forest_model.pkl      # Trained Random Forest model
├── scaler.pkl                   # StandardScaler for feature scaling
├── tests/
│   ├── __init__.py
│   ├── test_unit_model.py       # Unit tests for model
│   └── test_integration_api.py  # API integration tests
└── README.md                    # This file
```

## Installation & Setup

### 1. Local Development Setup

```bash
# Navigate to project directory
cd ml_loan_project

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Place Model Artifacts

Ensure the following files are in the project root:
- `random_forest_model.pkl` - Trained Random Forest classifier
- `scaler.pkl` - StandardScaler for input normalization

### 3. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at:
- [http://localhost:8000](http://localhost:8000)
- [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 4. Run with Docker

```bash
# Build the Docker image
docker build -t loan-approval-api .

# Run the container
docker run -p 8000:8000 loan-approval-api
```

Access the application at [http://localhost:8000](http://localhost:8000)

**Note**: Use `http://localhost:8000` in your browser, NOT `http://0.0.0.0:8000`

## API Endpoints

### Home Page
- **GET /** - Returns the home page (static HTML)

### Prediction Interface
- **GET /predict** - Returns the loan prediction form (HTML)
- **POST /predict** - Submit loan application and get prediction

## Loan Prediction API

### POST /predict

Submit loan application details to get approval prediction.

**Form Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `gender` | string | Gender (Male/Female) |
| `married` | string | Marital status (Yes/No) |
| `dependents` | string | Number of dependents (0/1/2/3+) |
| `education` | string | Education level (Graduate/Not Graduate) |
| `self_employed` | string | Self-employment status (Yes/No) |
| `applicant_income` | float | Applicant's income |
| `coapplicant_income` | float | Co-applicant's income |
| `loan_amount` | float | Requested loan amount |
| `loan_amount_term` | float | Loan term in months |
| `credit_history` | float | Credit history (0.0 or 1.0) |
| `property_area` | string | Property location (Urban/Semiurban/Rural) |

**Example using cURL:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "gender=Male" \
  -F "married=Yes" \
  -F "dependents=1" \
  -F "education=Graduate" \
  -F "self_employed=No" \
  -F "applicant_income=5000" \
  -F "coapplicant_income=2000" \
  -F "loan_amount=150" \
  -F "loan_amount_term=360" \
  -F "credit_history=1.0" \
  -F "property_area=Urban"
```

**Example Response:**

```json
{
  "prediction": "Approved"
}
```

or

```json
{
  "prediction": "Rejected"
}
```

## Testing

The project includes comprehensive test coverage for both unit and integration testing.

### Test Files

- **tests/test_unit_model.py**: Validates model and scaler functionality with controlled inputs
- **tests/test_integration_api.py**: Validates API endpoints, form submission, and prediction results

### Run All Tests

```bash
pytest tests/
```

### Run Specific Tests

```bash
# Unit tests only
pytest tests/test_unit_model.py

# Integration tests only
pytest tests/test_integration_api.py
```

### Run Tests with Coverage

```bash
pytest --cov=main --cov-report=html tests/
```

### Run Tests Verbose

```bash
pytest -v tests/
```

## Model Information

### Random Forest Classifier

The model is trained to predict loan approval based on:
- Demographic information (gender, marital status, dependents)
- Financial data (income, loan amount, credit history)
- Property location
- Education and employment status

### Feature Engineering

Input features are preprocessed using:
- **One-hot encoding** for categorical variables
- **StandardScaler** for numerical normalization
- **Missing value handling** with appropriate defaults

### Model Performance

Typical metrics (depends on training data):
- Accuracy: ~80%
- Precision: ~75-85%
- Recall: ~70-80%

## Docker Deployment

The application is fully containerized for production deployment.

### Dockerfile Highlights

- Base image: `python:3.10-slim`
- Installs all dependencies from `requirements.txt`
- Copies model artifacts and static files
- Exposes port 8000
- Uses Uvicorn as ASGI server

### Build and Run

```bash
# Build
docker build -t loan-approval-api .

# Run
docker run -p 8000:8000 loan-approval-api

# Run in detached mode
docker run -d -p 8000:8000 loan-approval-api

# Stop container
docker stop <container_id>
```

## Static Files

The `static/` directory contains:
- **index.html**: Welcome page with navigation
- **predict.html**: Interactive loan application form
- **style.css** and **styles.css**: Styling for web interface

## Dependencies

See [requirements.txt](requirements.txt) for the complete list:

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **joblib**: Model serialization
- **pydantic**: Data validation
- **python-multipart**: Form data handling
- **pytest**: Testing framework

## Project Notes

### Model Artifacts

Model files (`random_forest_model.pkl` and `scaler.pkl`) are typically not included in Git repositories for security and size reasons.

To retrain or update the model:
1. Use the provided dataset `LoanApprovalPrediction.csv`
2. Train using your preferred notebook or script
3. Save the model and scaler using joblib
4. Place the `.pkl` files in the project root

### Security Considerations

- Never commit model artifacts with sensitive data
- Use environment variables for sensitive configuration
- Implement rate limiting for production APIs
- Add authentication for production deployments

## Advanced Features

- **Logging**: All requests and errors are logged to console
- **Error handling**: Comprehensive exception handling with user-friendly messages
- **CORS support**: Can be configured for cross-origin requests
- **Environment variables**: Support for configurable ports and paths
- **Hot reload**: Development mode with `--reload` flag

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License (or specify your license)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn Random Forest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)
