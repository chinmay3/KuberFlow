import os

import httpx
import redis
from fastapi import FastAPI


app = FastAPI(title="kuber-api")

APP_ENV = os.getenv("APP_ENV", "development")
FEATURE_ANALYTICS = os.getenv("FEATURE_ANALYTICS", "false").lower() == "true"
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Hello from the API")
WORKER_SERVICE_URL = os.getenv("WORKER_SERVICE_URL", "http://worker-service:8001")
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD or None,
    decode_responses=True,
)


@app.get("/healthz")
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readiness() -> dict[str, str]:
    redis_client.ping()
    return {"status": "ready"}


@app.get("/api/info")
async def info() -> dict:
    request_count = redis_client.incr("api:request_count")
    async with httpx.AsyncClient(timeout=5.0) as client:
        worker_response = await client.get(f"{WORKER_SERVICE_URL}/task-status")
        worker_response.raise_for_status()
        worker_payload = worker_response.json()

    return {
        "service": "api",
        "environment": APP_ENV,
        "feature_analytics": FEATURE_ANALYTICS,
        "welcome_message": WELCOME_MESSAGE,
        "request_count": request_count,
        "worker": worker_payload,
    }

