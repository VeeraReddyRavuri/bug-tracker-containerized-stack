from fastapi import FastAPI
from app.config import settings
from app.db import get_connection
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/db-url")
def get_db_url():
    return {
        "db_url": settings.DATABASE_URL
    }

@app.get("/db-check")
def db_check():
    conn = get_connection()
    if conn:
        conn.close()
        return {
            "db": "connected"
        }
    return {
        "db": "failed"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "db_host": settings.DB_HOST
    }