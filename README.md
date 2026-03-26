# Kubernetes Microservices Demo

This project is a small microservices-style app built to demonstrate containerization and Kubernetes deployment patterns:

- Static frontend served by NGINX
- FastAPI backend API
- FastAPI worker service
- Redis for lightweight state
- Docker images for each service
- Kubernetes manifests with ConfigMaps, Secrets, Ingress, health probes, and rolling updates

## Architecture

- `frontend` calls `GET /api/info`
- `api` uses Kubernetes service discovery to call `worker-service`
- `api` stores a request counter in Redis
- `Ingress` routes:
  - `/` -> frontend
  - `/api` -> api

## Project Structure

- `frontend/` static UI + NGINX config
- `api/` FastAPI backend
- `worker/` FastAPI secondary service
- `k8s/base/` Kubernetes manifests
- `docker-compose.yml` local multi-container setup

## Run Locally With Docker Compose

```bash
docker compose up --build
```

Then open `http://localhost:8080`.

## Build Images Manually

```bash
docker build -t kuber-frontend:latest ./frontend
docker build -t kuber-api:latest ./api
docker build -t kuber-worker:latest ./worker
```

## Kubernetes Deploy

1. Build and push images to your registry.
2. Update image references in `k8s/base/*.yaml`.
3. Ensure an ingress controller is installed, for example NGINX Ingress.
4. Apply the manifests:

```bash
kubectl apply -f k8s/base
```

## Config-Driven Behavior

Config is provided through ConfigMaps and Secrets:

- `APP_ENV`
- `FEATURE_ANALYTICS`
- `WELCOME_MESSAGE`
- `WORKER_SERVICE_URL`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_PASSWORD`

Changing the ConfigMap changes application behavior without changing code. Restart the deployment or use a rollout to pick up the new config.

## Zero-Downtime Updates

The API, worker, and frontend deployments use rolling updates with:

- `maxUnavailable: 0`
- `maxSurge: 1`
- readiness and liveness probes

Example rollout:

```bash
kubectl set image deployment/api-deployment api=your-registry/kuber-api:v2
kubectl rollout status deployment/api-deployment
```

## Demo Points

- Service discovery via `http://worker-service:8001`
- ConfigMaps and Secrets
- Ingress routing
- Rolling updates
- Liveness and readiness probes
- Redis-backed shared state

