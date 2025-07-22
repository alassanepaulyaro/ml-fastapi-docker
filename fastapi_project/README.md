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

### 1. Manual Deployment (Azure CLI)

#### Build and Push Docker Image to Azure Container Registry (ACR)

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

#### Deploy Image to Azure Container App

```sh
# Create Azure Container App Environment (if needed)
az containerapp env create \
  --name fastapi-env \
  --resource-group myResourceGroup \
  --location eastus

# Deploy the Container App
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

# Get the public URL of the app
az containerapp show \
  --name testscore-predictor-app \
  --resource-group myResourceGroup \
  --query properties.configuration.ingress.fqdn
```

---

### 2. CI/CD Deployment with GitHub Actions

You can automate the build, push, and deployment of your FastAPI project to Azure Container Apps using GitHub Actions.

#### Prerequisites

* Azure Container Registry (ACR) is created and accessible.
* Azure Container App environment exists (see steps above).
* The following **GitHub secrets** must be set:

  * `AZURE_CREDENTIALS`: Azure Service Principal JSON (see below)
  * `REGISTRY_USERNAME`: ACR username
  * `REGISTRY_PASSWORD`: ACR password
  * `REGISTRY_LOGIN_SERVER`: ACR login server (e.g. fastapimlproject.azurecr.io)

#### Example GitHub Actions Workflow

Create a file `.github/workflows/deploy-to-azure-containerapp.yml` in your repository:

```yaml
name: Build & Deploy to Azure Container Apps

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  ACR_NAME: fastapimlproject
  ACR_LOGIN_SERVER: ${{ secrets.REGISTRY_LOGIN_SERVER }}
  IMAGE_NAME: testscore-predictor
  RESOURCE_GROUP: myResourceGroup
  CONTAINER_APP_ENV: fastapi-env
  CONTAINER_APP_NAME: testscore-predictor-app
  AZURE_REGION: eastus

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Docker Login to ACR
        uses: azure/docker-login@v2
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build Docker image
        run: |
          docker build -t $ACR_LOGIN_SERVER/$IMAGE_NAME:${{ github.sha }} .
          docker tag $ACR_LOGIN_SERVER/$IMAGE_NAME:${{ github.sha }} $ACR_LOGIN_SERVER/$IMAGE_NAME:latest

      - name: Push image to ACR
        run: |
          docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:${{ github.sha }}
          docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:latest

      - name: Deploy to Azure Container App
        uses: azure/CLI@v2
        with:
          inlineScript: |
            az containerapp update \
              --name $CONTAINER_APP_NAME \
              --resource-group $RESOURCE_GROUP \
              --image $ACR_LOGIN_SERVER/$IMAGE_NAME:latest \
              --environment $CONTAINER_APP_ENV \
              --registry-server $ACR_LOGIN_SERVER \
              --registry-username ${{ secrets.REGISTRY_USERNAME }} \
              --registry-password ${{ secrets.REGISTRY_PASSWORD }} \
              --cpu 1 --memory 1.0Gi \
              --ingress external \
              --target-port 8000 || \
            az containerapp create \
              --name $CONTAINER_APP_NAME \
              --resource-group $RESOURCE_GROUP \
              --environment $CONTAINER_APP_ENV \
              --image $ACR_LOGIN_SERVER/$IMAGE_NAME:latest \
              --registry-server $ACR_LOGIN_SERVER \
              --registry-username ${{ secrets.REGISTRY_USERNAME }} \
              --registry-password ${{ secrets.REGISTRY_PASSWORD }} \
              --cpu 1 --memory 1.0Gi \
              --ingress external \
              --target-port 8000
```

#### Azure Service Principal JSON Example

To create and retrieve the JSON for `AZURE_CREDENTIALS`:

```sh
az ad sp create-for-rbac --name "github-actions-fastapi" --sdk-auth
```

Copy the entire output and save as the secret `AZURE_CREDENTIALS` in your repo settings.

---

## Summary of Azure Deployment Flow

1. **Build & tag Docker image**
2. **Push to ACR**
3. **Create Azure Container App environment**
4. \*\*Deploy the image using \*\*\`\`
5. **Retrieve the external URL for your FastAPI app**

---
