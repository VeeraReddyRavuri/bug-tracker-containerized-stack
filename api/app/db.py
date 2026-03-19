import psycopg2
from app.config import settings

def get_connection():
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        return conn
    except Exception as e:
        print(f"DB connection failed: {e}")
        return None