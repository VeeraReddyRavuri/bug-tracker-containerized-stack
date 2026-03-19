import psycopg2
import logging
from app.config import settings

logger = logging.getLogger(__name__)

def get_connection():
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        return conn
    except Exception as e:
        logger.error(f"DB connection failed: {e}")
        return None