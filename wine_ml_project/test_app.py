import pytest
import app

@pytest.fixture
def mock_streamlit(mocker):
    # Patch all Streamlit methods used
    mocker.patch("app.st.title")
    mocker.patch("app.st.write")
    mocker.patch("app.st.success")
    mocker.patch("app.st.error")
    mocker.patch("app.st.sidebar")
    mocker.patch("app.st.number_input", return_value=1.0)
    mocker.patch("app.st.button", return_value=True)
    mocker.patch("app.st.sidebar.radio", return_value="Home")

def test_home_page_success(mocker, mock_streamlit):
    # Mock backend response for GET /
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Welcome to the API!"}
    mocker.patch("app.requests.get", return_value=mock_response)

    app.home_page()
    app.st.success.assert_called_with("Welcome to the API!")

def test_home_page_backend_error(mocker, mock_streamlit):
    # Backend returns error status
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("app.requests.get", return_value=mock_response)
    app.home_page()
    app.st.error.assert_called_with("Failed to fetch data from the backend.")

def test_home_page_exception(mocker, mock_streamlit):
    mocker.patch("app.requests.get", side_effect=Exception("Network Down"))
    app.home_page()
    app.st.error.assert_called()
    assert "Error:" in app.st.error.call_args[0][0]

def test_prediction_page_success(mocker, mock_streamlit):
    # Patch sidebar to navigate to prediction page
    app.st.sidebar.radio.return_value = "Predict Wine Quality"
    # Patch button to True
    app.st.button.return_value = True
    # Patch number_input to return a specific value
    app.st.number_input.return_value = 1.0

    # Mock backend prediction response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"predicted_quality": "7"}
    mocker.patch("app.requests.post", return_value=mock_response)

    app.prediction_page()
    app.st.success.assert_called_with("Predicted Wine Quality: 7")

def test_prediction_page_backend_error(mocker, mock_streamlit):
    app.st.sidebar.radio.return_value = "Predict Wine Quality"
    app.st.button.return_value = True
    app.st.number_input.return_value = 1.0
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch("app.requests.post", return_value=mock_response)

    app.prediction_page()
    app.st.error.assert_called_with("Failed to get prediction from the backend.")

def test_prediction_page_exception(mocker, mock_streamlit):
    app.st.sidebar.radio.return_value = "Predict Wine Quality"
    app.st.button.return_value = True
    app.st.number_input.return_value = 1.0
    mocker.patch("app.requests.post", side_effect=Exception("Timeout"))
    app.prediction_page()
    app.st.error.assert_called()
    assert "Error:" in app.st.error.call_args[0][0]
