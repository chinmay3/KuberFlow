import os
from datetime import datetime, timezone

from fastapi import FastAPI


app = FastAPI(title="kuber-worker")

APP_ENV = os.getenv("APP_ENV", "development")
WORKER_NAME = os.getenv("WORKER_NAME", "analytics-worker")


@app.get("/healthz")
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/task-status")
def task_status() -> dict[str, str]:
    return {
        "worker_name": WORKER_NAME,
        "environment": APP_ENV,
        "last_seen": datetime.now(timezone.utc).isoformat(),
        "mode": "mock-processing",
    }

