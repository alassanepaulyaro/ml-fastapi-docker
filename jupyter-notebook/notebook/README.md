# Linear Regression Model Training - Jupyter Notebook

A comprehensive Jupyter notebook demonstrating the complete machine learning workflow for training a linear regression model to predict student test scores based on study hours.

## Overview

This project provides an end-to-end example of:
- Data preparation and exploratory data analysis
- Feature engineering and preprocessing
- Model training with linear regression
- Model evaluation and validation
- Model persistence for deployment
- Making predictions with saved models

## Features

- **Synthetic data generation** for reproducible examples
- **Exploratory Data Analysis (EDA)** with visualizations
- **Feature scaling** using StandardScaler
- **Train-test split** for proper model validation
- **Model evaluation** with MSE and R² metrics
- **Model serialization** with joblib
- **Inference examples** for production use

## Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab
- pip (Python package manager)

## Project Structure

```
jupyter-notebook/notebook/
├── train_ml_model.ipynb         # Main training notebook
├── linear_regression_model.pkl  # Saved trained model
├── scaler.pkl                   # Saved StandardScaler
└── README.md                    # This file
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install numpy pandas matplotlib scikit-learn joblib jupyter
```

Or if you have a requirements file:

```bash
pip install -r requirements.txt
```

### 2. Launch Jupyter Notebook

```bash
# From the notebook directory
jupyter notebook
```

Or using JupyterLab:

```bash
jupyter lab
```

### 3. Open the Notebook

Navigate to `train_ml_model.ipynb` in the Jupyter interface and open it.

## Workflow Summary

The notebook follows this structured workflow:

### 1. Data Preparation
- Generates synthetic dataset with Hours_Studied and Test_Score
- Creates a pandas DataFrame for easy manipulation
- Displays data statistics and structure

### 2. Exploratory Data Analysis (EDA)
- Scatter plots to visualize relationships
- Correlation analysis between features
- Statistical summaries

### 3. Data Preprocessing
- Splits data into training and test sets (typically 80/20)
- Applies StandardScaler for feature normalization
- Prepares data for model training

### 4. Model Training
- Initializes LinearRegression model
- Fits the model on scaled training data
- Captures learned coefficients and intercept

### 5. Model Evaluation
- Calculates Mean Squared Error (MSE) on test set
- Computes R² score for model performance
- Visualizes predictions vs actual values

### 6. Model Persistence
- Saves trained model using joblib (`linear_regression_model.pkl`)
- Saves scaler using joblib (`scaler.pkl`)
- Ensures reproducibility for deployment

### 7. Inference/Prediction
- Loads saved model and scaler
- Demonstrates predictions on new data
- Shows how to deploy in production

## Usage

### Running the Complete Notebook

1. Open `train_ml_model.ipynb` in Jupyter
2. Run all cells sequentially (Cell > Run All)
3. Review outputs, visualizations, and metrics
4. Model artifacts will be saved in the same directory

### Making Predictions with Trained Model

After running the notebook, use the saved model:

```python
import joblib
import numpy as np
import pandas as pd

# Load the saved model and scaler
model = joblib.load('linear_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

# Prepare new data
new_data = pd.DataFrame([[6]], columns=['Hours_Studied'])

# Scale the input
new_data_scaled = scaler.transform(new_data)

# Make prediction
predicted_score = model.predict(new_data_scaled)

print(f"Predicted Test Score for 6 hours of study: {predicted_score[0]:.2f}")
```

**Example output:**
```
Predicted Test Score for 6 hours of study: 62.15
```

## Key Files Explained

### train_ml_model.ipynb
The main Jupyter notebook containing:
- All code cells with detailed comments
- Markdown cells with explanations
- Visualizations and output results
- Complete workflow from data to deployment

### linear_regression_model.pkl
Serialized trained linear regression model using joblib:
- Contains learned weights (coefficients)
- Contains intercept term
- Ready for production inference

### scaler.pkl
Serialized StandardScaler object:
- Contains mean and standard deviation from training data
- Essential for consistent feature scaling
- Must be applied to all new data before prediction

## Model Performance Metrics

The notebook calculates:

- **Mean Squared Error (MSE)**: Average squared difference between predictions and actual values
- **R² Score**: Proportion of variance explained by the model (0 to 1, higher is better)

Typical results:
```
MSE: ~15.2 (varies with synthetic data)
R²: ~0.85 (indicates good model fit)
```

## Customization

You can modify the notebook to:
- Use your own dataset (replace synthetic data generation)
- Add more features for multivariate regression
- Try different regression algorithms (Ridge, Lasso, etc.)
- Implement cross-validation
- Add feature engineering steps
- Export to different formats (ONNX, TensorFlow, etc.)

## Dependencies

Core libraries used:
- **numpy**: Numerical computations
- **pandas**: Data manipulation and analysis
- **matplotlib**: Data visualization
- **scikit-learn**: Machine learning algorithms and tools
- **joblib**: Model serialization and deserialization
- **jupyter**: Interactive notebook environment

## Best Practices Demonstrated

- Clear separation of training and testing data
- Feature scaling for better model performance
- Model persistence for deployment
- Comprehensive evaluation metrics
- Code documentation with comments
- Reproducible workflow

## Troubleshooting

### Issue: Kernel crashes or restarts
**Solution**: Reduce data size or increase available memory

### Issue: Import errors
**Solution**: Ensure all dependencies are installed
```bash
pip install --upgrade numpy pandas matplotlib scikit-learn joblib
```

### Issue: Model file not found
**Solution**: Run all cells in the notebook to generate model files

## Next Steps

After completing this notebook:
1. Deploy the model using FastAPI (see `ml_project` folder)
2. Create a web interface with Streamlit (see `ml_streamlit` folder)
3. Containerize with Docker for production deployment
4. Set up CI/CD pipelines for automated retraining

## License

MIT License (or specify your license)

## References

- [scikit-learn Linear Regression Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Jupyter Documentation](https://jupyter.org/documentation)
- [joblib Documentation](https://joblib.readthedocs.io/)
