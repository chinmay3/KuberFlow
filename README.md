# KuberFlow

KuberFlow is a microservices-based web application built to demonstrate Docker, Kubernetes, and DevOps fundamentals through a practical project. It includes a static frontend served with NGINX, a FastAPI backend API, a second FastAPI worker service for internal service-to-service communication, and Redis for shared state. The project was built to show how multiple services can be containerized, connected, configured, and deployed with rolling updates, health checks, ingress routing, and configuration-driven behavior.

## What The Project Does

The frontend displays live application data by calling the backend API. The API reads environment-based configuration, stores and updates a request counter in Redis, and calls the worker service using internal service discovery. The worker responds with mock processing data so the app demonstrates communication across multiple services instead of only one backend.

## How I Built It

This project was built using:

- `HTML`, `CSS`, and `JavaScript` for the frontend
- `NGINX` to serve the frontend and proxy API requests
- `Python` and `FastAPI` for the API and worker services
- `Redis` for lightweight shared data storage
- `Docker` to containerize each service
- `Docker Compose` for local multi-container execution
- `Kubernetes` for orchestration
- `ConfigMaps` and `Secrets` for runtime configuration
- `Ingress` for routing external traffic
- `Liveness` and `readiness` probes for health monitoring
- `RollingUpdate` strategy for zero-downtime deployments
- `Render` blueprint config for quick hosted deployment

## Project Structure

- `frontend/` frontend assets, NGINX config template, and frontend Dockerfile
- `api/` FastAPI backend service
- `worker/` FastAPI worker service
- `k8s/base/` Kubernetes manifests
- `docker-compose.yml` local development setup
- `render.yaml` quick hosting blueprint

## How To Run Locally

### Run With Docker Compose

```bash
docker compose up --build
```

Open:

```text
http://localhost:8080
```

### Stop Local Containers

```bash
docker compose down
```

## How To Run On Kubernetes

### 1. Start Minikube

```bash
minikube start --driver=docker
minikube addons enable ingress
```

### 2. Build Images Inside Minikube

```bash
eval $(minikube docker-env)
docker build -t kuber-frontend:latest ./frontend
docker build -t kuber-api:latest ./api
docker build -t kuber-worker:latest ./worker
```

### 3. Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/base
```

### 4. Check Rollout Status

```bash
kubectl rollout status deployment/frontend-deployment
kubectl rollout status deployment/api-deployment
kubectl rollout status deployment/worker-deployment
kubectl get pods
```

### 5. Expose Ingress

Run this in a separate terminal:

```bash
minikube tunnel
```

Add this host entry once:

```bash
echo '127.0.0.1 kuber.local' | sudo tee -a /etc/hosts
```

Open:

```text
http://kuber.local
```

## Configuration Used

The application behavior is driven by runtime variables such as:

- `APP_ENV`
- `FEATURE_ANALYTICS`
- `WELCOME_MESSAGE`
- `WORKER_SERVICE_URL`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_PASSWORD`
- `REDIS_URL`

This makes it easy to change application behavior without modifying code.

## Quick Hosting

This repository includes `render.yaml` so the project can be hosted quickly using Render. The blueprint creates:

- a public frontend service
- a public API service
- a private worker service
- a managed key-value instance for Redis

To deploy:

1. Push the repository to GitHub.
2. In Render, create a new Blueprint.
3. Select this repository.
4. Let Render create the services from `render.yaml`.
5. Open the frontend service URL after the deployment completes.

## Key DevOps Concepts Demonstrated

- Multi-service application design
- Containerization with Docker
- Local orchestration with Docker Compose
- Kubernetes Deployments and Services
- Ingress-based routing
- Service discovery between services
- ConfigMaps and Secrets
- Health checks
- Rolling updates
- Zero-downtime deployment flow

