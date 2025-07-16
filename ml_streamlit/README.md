
# ML Model Deployment with Streamlit Server

This project demonstrates how to deploy a trained linear regression model for predicting student test scores based on hours studied, using a simple Streamlit web application.

## Features

- User-friendly web interface for prediction
- Real-time test score prediction based on user input (hours studied)
- Uses trained scikit-learn linear regression model and scaler

## Project Structure

```
.
├── linear_regression_model.pkl   # Trained ML model
├── scaler.pkl                   # Scaler used for input normalization
├── streamlit.py                 # Streamlit web application
├── requirements.txt             # Dependencies
├── README.md                    # Project documentation
```

## How to Run

1. **Install requirements:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Start the Streamlit app:**

    ```bash
    streamlit run streamlit.py
    ```

3. **Open the web interface:**
    - Visit the provided local URL in your browser (usually http://localhost:8501).

## Usage

- Enter the number of hours studied in the input box.
- Click **Predict** to see the predicted test score.

## Example

```
Hours studied: 6
→ Predicted Test Score: (e.g., 62.12)
```

## Files

- `streamlit.py` — Streamlit app code for user interaction and prediction
- `linear_regression_model.pkl` — Serialized trained linear regression model
- `scaler.pkl` — Serialized input scaler used during training
- `requirements.txt` — List of required Python packages

---
