# ML Linear Regression Example

This project demonstrates how to train, evaluate, and save a simple linear regression model using scikit-learn and Jupyter Notebook.

## Overview
- Predicts test scores from hours studied using linear regression.
- Covers: data loading, EDA, training, evaluation, saving/loading the model, and making new predictions.

## Workflow Summary

1. **Data Preparation**
    - Generates synthetic data for 'Hours_Studied' and 'Test_Score'.

2. **Exploratory Data Analysis**
    - Scatter plots, correlation analysis.

3. **Preprocessing**
    - Train-test split
    - Feature scaling with StandardScaler

4. **Model Training**
    - LinearRegression fit on scaled features

5. **Evaluation**
    - Mean Squared Error (MSE) and R² on test set

6. **Persistence**
    - Save model and scaler with joblib

7. **Inference**
    - Load model/scaler, predict for new data points

## How to Run

1. Clone or download this repository.
2. Open `train_ml_model.ipynb` in Jupyter Notebook or VSCode.
3. Run all cells sequentially.

## Key Files
- `train_ml_model.ipynb`: Main notebook with code and explanations
- `linear_regression_model.pkl`: Saved trained model
- `scaler.pkl`: Saved scaler for input normalization

## Requirements
- Python 3.8+
- numpy, pandas, matplotlib, scikit-learn, joblib, jupyter

## Example Command to Install Requirements
```bash
pip install numpy pandas matplotlib scikit-learn joblib notebook
```

## Example Prediction Code
```python
import joblib
import numpy as np
import pandas as pd

model = joblib.load('linear_regression_model.pkl')
scaler = joblib.load('scaler.pkl')
new_data = pd.DataFrame([[6]], columns=['Hours_Studied'])
new_data_scaled = scaler.transform(new_data)
predicted_score = model.predict(new_data_scaled)
print("Predicted Test Score for 6 hours of study:", predicted_score[0])
```

---
