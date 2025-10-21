# Student Test Score Prediction - Streamlit Web App

An interactive Streamlit web application for predicting student test scores based on hours studied using a trained linear regression model.

## Features

- **User-friendly web interface** built with Streamlit
- **Real-time predictions** based on user input
- **Pre-trained linear regression model** using scikit-learn
- **Feature scaling** with StandardScaler for accurate predictions
- **Lightweight deployment** with minimal dependencies
- **Interactive UI** with instant feedback

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Project Structure

```
ml_streamlit/
├── streamlit.py                 # Streamlit web application
├── linear_regression_model.pkl  # Trained ML model
├── scaler.pkl                   # StandardScaler for input normalization
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation & Setup

### 1. Install Dependencies

```bash
# Navigate to project directory
cd ml_streamlit

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Verify Model Files

Ensure the following files exist in the project directory:
- `linear_regression_model.pkl` - Trained model
- `scaler.pkl` - Feature scaler

## Usage

### Start the Streamlit App

```bash
streamlit run streamlit.py
```

The application will automatically open in your default web browser at:
- Local URL: [http://localhost:8501](http://localhost:8501)
- Network URL: Will be displayed in terminal (accessible from other devices on your network)

### Using the Application

1. **Launch** the Streamlit app using the command above
2. **Enter** the number of hours studied in the input field
3. **View** the predicted test score instantly
4. **Adjust** the input to see different predictions in real-time

### Example

```
Input: Hours studied = 6
Output: Predicted Test Score = 62.12
```

## Model Information

### Linear Regression Model

The application uses a simple linear regression model trained on student study hours and test scores data:

- **Input**: Hours studied (float)
- **Output**: Predicted test score (float)
- **Algorithm**: Linear Regression from scikit-learn
- **Preprocessing**: StandardScaler normalization

### Model Training

The model was trained separately (typically in a Jupyter notebook) and saved as pickle files:
- Training process includes data collection, preprocessing, model fitting, and evaluation
- Model and scaler are serialized using joblib
- Files are loaded at runtime by the Streamlit app

## Dependencies

See [requirements.txt](requirements.txt) for the complete list:

```
streamlit
scikit-learn
pandas
numpy
joblib
```

**Core Libraries:**
- **streamlit**: Web application framework for ML/data apps
- **scikit-learn**: Machine learning library (includes LinearRegression and StandardScaler)
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **joblib**: Model serialization and loading

## Application Code Structure

The `streamlit.py` file contains:

1. **Import statements**: Required libraries
2. **Model loading**: Loads trained model and scaler from pickle files
3. **UI components**: Streamlit widgets for user input
4. **Prediction logic**: Processes input, scales features, and generates predictions
5. **Output display**: Shows predicted score to user

## Customization

### Modify the UI

Edit `streamlit.py` to customize:
- Title and description
- Input widgets (sliders, number inputs, etc.)
- Output formatting
- Add visualizations (charts, graphs)
- Include data validation

### Example Customization

```python
import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Custom title and icon
st.set_page_config(page_title="Score Predictor", page_icon="📊")

# Load models
model = joblib.load('linear_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

# Custom header
st.title("📚 Student Test Score Predictor")
st.markdown("Predict your test score based on study hours")

# Use slider instead of number input
hours = st.slider("Hours Studied", min_value=0.0, max_value=24.0, value=5.0, step=0.5)

# Predict button
if st.button("Predict Score"):
    input_data = pd.DataFrame([[hours]], columns=['Hours_Studied'])
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)

    # Display result with formatting
    st.success(f"Predicted Test Score: {prediction[0]:.2f}")
    st.balloons()  # Celebration animation
```

## Deployment Options

### Option 1: Local Deployment
Run locally using `streamlit run streamlit.py`

### Option 2: Streamlit Cloud
Deploy for free on Streamlit Cloud:
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click

### Option 3: Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t ml-streamlit-app .
docker run -p 8501:8501 ml-streamlit-app
```

### Option 4: Cloud Platforms
Deploy to:
- Heroku
- AWS (EC2, ECS, Lambda)
- Google Cloud Platform (Cloud Run, App Engine)
- Azure (App Service, Container Instances)

## Advanced Features

### Add Visualizations

```python
import matplotlib.pyplot as plt

# Plot prediction vs study hours
fig, ax = plt.subplots()
hours_range = np.linspace(0, 24, 100)
predictions = model.predict(scaler.transform(hours_range.reshape(-1, 1)))
ax.plot(hours_range, predictions)
ax.scatter([hours], [prediction], color='red', s=100)
st.pyplot(fig)
```

### Add Data Upload

```python
uploaded_file = st.file_uploader("Upload CSV with hours studied")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    scaled = scaler.transform(df[['Hours_Studied']])
    predictions = model.predict(scaled)
    df['Predicted_Score'] = predictions
    st.dataframe(df)
```

### Add Model Metrics

```python
st.sidebar.title("Model Information")
st.sidebar.metric("Model Type", "Linear Regression")
st.sidebar.metric("R² Score", "0.85")
st.sidebar.metric("MSE", "15.2")
```

## Troubleshooting

### Issue: Streamlit command not found
**Solution**: Ensure streamlit is installed and virtual environment is activated
```bash
pip install streamlit
```

### Issue: Model file not found
**Solution**: Verify that `linear_regression_model.pkl` and `scaler.pkl` are in the same directory as `streamlit.py`

### Issue: Port already in use
**Solution**: Specify a different port
```bash
streamlit run streamlit.py --server.port 8502
```

### Issue: Browser doesn't open automatically
**Solution**: Manually navigate to the URL shown in the terminal (usually http://localhost:8501)

## Performance Tips

- **Caching**: Use `@st.cache_resource` to cache model loading
- **Optimize imports**: Only import necessary libraries
- **Minimize reloads**: Structure code to avoid unnecessary reruns

Example with caching:
```python
@st.cache_resource
def load_model():
    model = joblib.load('linear_regression_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_model()
```

## Next Steps

After mastering this basic app:
1. Add more features (e.g., attendance, previous scores)
2. Try different ML models (Ridge, Lasso, Random Forest)
3. Add data visualization and exploratory analysis
4. Implement model comparison and selection
5. Deploy to production with monitoring

## License

MIT License (or specify your license)

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Streamlit Cloud](https://share.streamlit.io)
