# FastAPI Docker Examples & Azure Deployment

A collection of minimal FastAPI application examples with Docker integration and comprehensive Azure Container Apps deployment guides. Perfect for learning FastAPI, Docker containerization, and cloud deployment workflows.

## Features

- **Multiple FastAPI examples** demonstrating different patterns and endpoints
- **Docker support** with optimized Dockerfile
- **Azure Container Apps deployment** with manual and CI/CD options
- **GitHub Actions workflow** for automated deployment
- **Production-ready configuration** with best practices

## Prerequisites

- Python 3.8+
- Docker Desktop (for containerization)
- Azure CLI (for Azure deployment)
- Azure subscription (for cloud deployment)
- GitHub account (for CI/CD)

## Project Structure

```
fastapi_project/
├── app.py              # Full CRUD API example
├── app_2.py            # Query parameters example
├── main.py             # Minimal "Hello Docker" example
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
└── README.md           # This file
```

## FastAPI Applications Overview

### 1. app.py - Full CRUD Example

A complete REST API with CRUD operations:

- **GET /** - Welcome message
- **GET /items/** - List all items
- **POST /items/** - Create new item (expects JSON `{ "name": "...", "price": ... }`)
- **PUT /items/{item_id}** - Update item by ID
- **DELETE /items/{item_id}** - Delete item by ID

### 2. app_2.py - Query Parameters Example

Demonstrates path and query parameters:

- **GET /{name}** - Returns name as path parameter
- **GET /** - Returns query parameters (name, age, height)
- **POST /items** - Create item (expects JSON `{ "name": "...", "price": ... }`)

### 3. main.py - Minimal Example

Simple Docker test endpoint:

- **GET /** - Returns `{"message": "Hello, Docker!"}`

## Installation & Setup

### 1. Local Development

```bash
# Navigate to project directory
cd fastapi_project

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

### 2. Run Locally

Run any of the example apps:

```bash
# Run app.py
uvicorn app:app --reload

# OR run app_2.py
uvicorn app_2:app --reload

# OR run main.py
uvicorn main:app --reload
```

Access the API at:
- Application: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Docker Deployment

### Build Docker Image

```bash
docker build -t fastapimlproject .
```

### Run Docker Container

```bash
docker run -d -p 8000:8000 fastapimlproject
```

Access the application at [http://localhost:8000](http://localhost:8000)

### Stop Container

```bash
# List running containers
docker ps

# Stop container
docker stop <container_id>
```

## Azure Container Apps Deployment

### Option 1: Manual Deployment (Azure CLI)

#### Step 1: Build and Push to Azure Container Registry (ACR)

```bash
# Build your Docker image
docker build -t testscore-predictor .

# Tag the image for ACR
docker tag testscore-predictor fastapimlproject.azurecr.io/testscore-predictor:v1

# Login to Azure Container Registry
az acr login --name fastapimlproject

# Push the image to ACR
docker push fastapimlproject.azurecr.io/testscore-predictor:v1
```

#### Step 2: Create Container App Environment

```bash
az containerapp env create \
  --name fastapi-env \
  --resource-group myResourceGroup \
  --location eastus
```

#### Step 3: Deploy Container App

```bash
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

#### Step 4: Get Application URL

```bash
az containerapp show \
  --name testscore-predictor-app \
  --resource-group myResourceGroup \
  --query properties.configuration.ingress.fqdn
```

### Option 2: CI/CD with GitHub Actions

Automate deployment using GitHub Actions workflow.

#### Prerequisites for CI/CD

Set up the following GitHub Secrets in your repository:

- `AZURE_CREDENTIALS` - Azure Service Principal JSON
- `REGISTRY_USERNAME` - ACR username
- `REGISTRY_PASSWORD` - ACR password
- `REGISTRY_LOGIN_SERVER` - ACR login server (e.g., fastapimlproject.azurecr.io)

#### Create Azure Service Principal

```bash
az ad sp create-for-rbac \
  --name "github-actions-fastapi" \
  --sdk-auth \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>
```

Copy the entire JSON output and save it as the `AZURE_CREDENTIALS` secret.

#### GitHub Actions Workflow

Create `.github/workflows/deploy-to-azure-containerapp.yml`:

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
              --image $ACR_LOGIN_SERVER/$IMAGE_NAME:latest || \
            az containerapp create \
              --name $CONTAINER_APP_NAME \
              --resource-group $RESOURCE_GROUP \
              --environment $CONTAINER_APP_ENV \
              --image $ACR_LOGIN_SERVER/$IMAGE_NAME:latest \
              --registry-server $ACR_LOGIN_SERVER \
              --cpu 1 --memory 1.0Gi \
              --ingress external \
              --target-port 8000
```

## Dependencies

See [requirements.txt](requirements.txt):

```
fastapi
uvicorn
```

## Azure Deployment Summary

1. **Build & tag Docker image**
2. **Push to Azure Container Registry (ACR)**
3. **Create Azure Container App environment**
4. **Deploy container app** from ACR image
5. **Access via external URL** provided by Azure

## Best Practices

- Use virtual environments for local development
- Store secrets in GitHub Secrets (never commit credentials)
- Use ACR for private container images
- Enable health checks in production
- Monitor logs using Azure Portal or CLI
- Scale resources based on traffic needs

## Troubleshooting

### Docker Issues

```bash
# View container logs
docker logs <container_id>

# Check running containers
docker ps -a

# Remove stopped containers
docker container prune
```

### Azure Issues

```bash
# View container app logs
az containerapp logs show \
  --name testscore-predictor-app \
  --resource-group myResourceGroup

# Check container app status
az containerapp show \
  --name testscore-predictor-app \
  --resource-group myResourceGroup
```

## License

MIT License (or specify your license)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Azure Container Apps Documentation](https://docs.microsoft.com/azure/container-apps/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)
