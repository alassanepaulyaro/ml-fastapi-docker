from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# Load the saved model and scaler
model = joblib.load('best_model.pkl') 
scaler = joblib.load('scaler.pkl')   

# Initialize FastAPI app
app = FastAPI()

# Define the input data model
class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.get("/")
def home():
    # Home endpoint with welcome message
    return {
        "message": "Welcome to the Wine Quality Prediction API! Use the /predict endpoint to predict wine quality."
    }

# Define the prediction endpoint    
@app.post("/predict")
def predict(wine: WineFeatures):
    # Extract the features from the incoming request
    try:
        features = np.array([
            [
                wine.fixed_acidity,
                wine.volatile_acidity,
                wine.citric_acid,
                wine.residual_sugar,
                wine.chlorides,
                wine.free_sulfur_dioxide,
                wine.total_sulfur_dioxide,
                wine.density,
                wine.pH,
                wine.sulphates,
                wine.alcohol
            ]
        ])
        # Scale the input features using the saved scaler
        scaled_features = scaler.transform(features)

        # Make the prediction using the loaded model
        prediction = model.predict(scaled_features)

        # Return the prediction (wine quality)
        return {"predicted_quality": str(prediction[0])}
    except Exception as e:
        # Handle errors during prediction
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
