# Flask Comments API

A small Python 3.12 Flask REST API demo that stores comments in SQLite with SQLAlchemy.

## Project Structure

```text
app/
  __init__.py
  database.py
  models.py
  routes.py
run.py
requirements.txt
README.md
Dockerfile
.dockerignore
docker-compose.yml
k8s/
  namespace.yaml
  configmap.yaml
  persistent-volume-claim.yaml
  deployment.yaml
  service.yaml
helm/
  flask-comments-api/
    Chart.yaml
    values.yaml
    templates/
      namespace.yaml
      configmap.yaml
      persistent-volume-claim.yaml
      deployment.yaml
      service.yaml
```

## Configuration

The SQLite database path is read from the `DB_PATH` environment variable.

If `DB_PATH` is not set, the app uses `comments.db` in the project root. Database tables are created automatically when the app starts.

## Create a Virtual Environment on Windows

From the project root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts, allow them for your current user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run Locally

Using the default database path:

```powershell
python run.py
```

Using a custom database path:

```powershell
$env:DB_PATH = "C:\temp\comments.db"
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## Run with Docker

Build the image:

```powershell
docker build -t flask-comments-api .
```

Run the container with the image default database path:

```powershell
docker run --rm -p 5000:5000 flask-comments-api
```

Run the container with an explicit SQLite database path:

```powershell
docker run --rm `
  -p 5000:5000 `
  -e DB_PATH=/data/comments.db `
  flask-comments-api
```

To keep the SQLite database after the container stops, mount a local folder:

```powershell
mkdir data
docker run --rm `
  -p 5000:5000 `
  -e DB_PATH=/data/comments.db `
  -v ${PWD}\data:/data `
  flask-comments-api
```

## Run with Docker Compose

Start the API:

```powershell
docker compose up --build
```

Run it in the background:

```powershell
docker compose up --build -d
```

Stop and remove the container and network:

```powershell
docker compose down
```

Stop and also remove the named SQLite data volume:

```powershell
docker compose down -v
```

## Run with Kubernetes

Build the image expected by the manifests:

```powershell
docker build -t flask-comments-api:1.0 .
```

Apply the manifests:

```powershell
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/persistent-volume-claim.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Or apply the whole directory:

```powershell
kubectl apply -f k8s/
```

Check the resources:

```powershell
kubectl get all -n flask-demo
kubectl get pvc -n flask-demo
```

Test the NodePort service:

```powershell
curl.exe http://localhost:30080/health
curl.exe http://localhost:30080/comments
```

Create a comment through Kubernetes:

```powershell
curl.exe -X POST http://localhost:30080/comments `
  -H "Content-Type: application/json" `
  -d "{\"author\":\"Ada\",\"content\":\"Hello from Kubernetes\"}"
```

Remove the Kubernetes resources:

```powershell
kubectl delete -f k8s/
```

## Run with Helm

Render the manifests locally:

```powershell
helm template flask-comments-api .\helm\flask-comments-api
```

Install the chart:

```powershell
helm install flask-comments-api .\helm\flask-comments-api
```

Upgrade the release after changing chart values or templates:

```powershell
helm upgrade flask-comments-api .\helm\flask-comments-api
```

Test with port forwarding:

```powershell
kubectl port-forward -n flask-demo service/flask-comments-api 5000:5000
```

In another terminal:

```powershell
curl.exe http://127.0.0.1:5000/health
curl.exe http://127.0.0.1:5000/comments
```

Uninstall the release:

```powershell
helm uninstall flask-comments-api
```

## Endpoints

### Health Check

```powershell
curl.exe http://127.0.0.1:5000/health
```

Response:

```json
{"status":"ok"}
```

### Get Comments

PowerShell:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:5000/comments
```

curl:

```powershell
curl.exe http://127.0.0.1:5000/comments
```

### Create a Comment

PowerShell:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:5000/comments `
  -ContentType "application/json" `
  -Body '{"author":"Ada","content":"Hello from Flask"}'
```

curl:

```powershell
curl.exe -X POST http://127.0.0.1:5000/comments `
  -H "Content-Type: application/json" `
  -d "{\"author\":\"Ada\",\"content\":\"Hello from Flask\"}"
```

Invalid requests return `400 Bad Request` when `author` or `content` is missing or blank.
