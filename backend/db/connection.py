import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv
from pathlib import Path
import time

if os.getenv("DOCKER"):
    dotenv_path = Path(__file__).parent.parent.parent / ".env.docker"
else:
    dotenv_path = Path(__file__).parent.parent.parent / ".env.local"
load_dotenv(dotenv_path)

def wait_for_postgres(host, port, user, password, db, timeout=30):
    """Wait until Postgres is ready to accept connections"""
    start = time.time()
    while True:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=db,
                user=user,
                password=password,
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            if time.time() - start > timeout:
                raise Exception(f"Postgres not ready after {timeout} seconds")
            time.sleep(1)

@contextmanager
def get_connection():
    wait_for_postgres(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
    )

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    try:
        yield conn
    finally:
        conn.close()