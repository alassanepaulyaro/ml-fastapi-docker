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
- **GET /** : Returns a welcome message.
- **GET /items/** : Lists example items.
- **POST /items/** : Creates an item (expects JSON `{ name, price }`).
- **PUT /items/{item_id}** : Updates an item by ID.
- **DELETE /items/{item_id}** : Deletes an item by ID.

### 2. `app_2.py`
- **GET /{name}** : Returns the name as a response parameter.
- **GET /** : Returns name, age, and height as query params.
- **POST /items** : Creates an item (expects JSON `{ name, price }`).

### 3. `main.py`
- **GET /** : Simple test endpoint, returns: `{"message": "Hello, Docker!"}`.

---

## 🐳 Dockerized Deployment

### 1. Build Docker Image

```sh
docker build -t fastapi-docker-app .
```

### 2. Run Docker Container

```sh
docker run -d -p 8000:8000 fastapi-docker-app
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
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Notes

- The project is designed for educational and demonstration purposes.
- You can swap the main file in the Dockerfile (default: `app.py` or as configured) to change the running API.

---
