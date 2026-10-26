import logging
import os

from fastapi import FastAPI


APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Team Draw", version=APP_VERSION)


@app.get("/health")
def health():
    logger.info("Health check")
    return {"status": "ok"}


@app.get("/version")
def version():
    logger.info("Version requested")
    return {"version": APP_VERSION}
