# FastAPI Docker App Example

This repository demonstrates several simple FastAPI applications with Docker integration. The project contains multiple FastAPI app examples (`app.py`, `app_2.py`, `main.py`) and a Dockerfile for containerized deployment.

---

## 📦 Project Structure

```
.
├── app.py
├── app_2.py
├── main.py
├── requirements.txt
├── Dockerfile
```

---

## 🚀 FastAPI App Endpoints Overview

### 1. `app.py`

* **GET /** : Returns a welcome message.
* **GET /items/** : Lists example items.
* **POST /items/** : Creates an item (expects JSON `{ name, price }`).
* **PUT /items/{item\_id}** : Updates an item by ID.
* **DELETE /items/{item\_id}** : Deletes an item by ID.

### 2. `app_2.py`

* **GET /{name}** : Returns the name as a response parameter.
* **GET /** : Returns name, age, and height as query params.
* **POST /items** : Creates an item (expects JSON `{ name, price }`).

### 3. `main.py`

* **GET /** : Simple test endpoint, returns: `{"message": "Hello, Docker!"}`.

---

## 🐳 Dockerized Deployment

### 1. Build Docker Image

```sh
docker build -t fastapimlproject .
```

### 2. Run Docker Container

```sh
docker run -d -p 8000:8000 fastapimlproject
```

---

## 📄 requirements.txt

```
fastapi
uvicorn
```

---

## 🛠️ How to Use

1. **Install Dependencies Locally**

   ```sh
   pip install -r requirements.txt
   ```

2. **Run Any App Example Locally**

   ```sh
   uvicorn app:app --reload
   ```

   Or replace `app` by `app_2` or `main` as needed.

3. **Access the API**

   * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Deploy to Azure Container Apps

### 1. Build and Push Docker Image to Azure Container Registry (ACR)

```sh
# Build your Docker image locally
docker build -t testscore-predictor .

# Tag the image for ACR
docker tag testscore-predictor fastapimlproject.azurecr.io/testscore-predictor:v1

# Login to your Azure Container Registry
az acr login --name fastapimlproject

# Push the image to ACR
docker push fastapimlproject.azurecr.io/testscore-predictor:v1
```

---

### 2. Deploy Image to Azure Container App

#### a. Create Azure Container App Environment (if needed):

```sh
az containerapp env create \
  --name fastapi-env \
  --resource-group myResourceGroup \
  --location eastus
```

#### b. Deploy the Container App:

```sh
az containerapp create \
  --name testscore-predictor-app \
  --resource-group myResourceGroup \
  --environment fastapi-env \
  --image fastapimlproject.azurecr.io/testscore-predictor:v1 \
  --target-port 8000 \
  --ingress 'external' \
  --registry-server fastapimlproject.azurecr.io \
  --registry-username <ACR_USERNAME> \
  --registry-password <ACR_PASSWORD>
```

* To get ACR credentials:

  ```sh
  az acr credential show --name fastapimlproject
  ```

---

#### c. Retrieve Application URL

```sh
az containerapp show \
  --name testscore-predictor-app \
  --resource-group myResourceGroup \
  --query properties.configuration.ingress.fqdn
```

---

## Summary of Azure Deployment Flow

1. **Build & tag Docker image**
2. **Push to ACR**
3. **Create Azure Container App environment**
4. \*\*Deploy the image using \*\*\`\`
5. **Retrieve the external URL for your FastAPI app**

---
