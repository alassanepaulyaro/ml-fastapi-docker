import streamlit as st
import joblib
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the model and scaler with absolute paths
model = joblib.load(os.path.join(script_dir, "linear_regression_model.pkl"))
scaler = joblib.load(os.path.join(script_dir, "scaler.pkl"))

# Streamlit app
st.title("Student Test Score Predictor")

st.write("Enter the number of hours studied to predict the test score.")

# User input
hours = st.number_input("Hours studied:", min_value=0.0, step=1.0)

if st.button("Predict"):
    try:
        data = [[hours]]
        scaled_data = scaler.transform(data)
        prediction = model.predict(scaled_data)
        st.write(f"Predicted Test Score: {prediction[0]:.2f}")
    except Exception as e:
        st.error(f"Prediction error: {e}")