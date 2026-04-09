"""
Pool de conexiones usando psycopg3 (psycopg).
psycopg3 maneja correctamente el encoding en Windows Python 3.13,
a diferencia de psycopg2 que falla con locales en español.
"""
import psycopg                      # psycopg3
from psycopg.rows import dict_row
from core.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)


def get_connection() -> psycopg.Connection:
    """Abre una conexión nueva a PostgreSQL usando psycopg3."""
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    return conn


def release_connection(conn: psycopg.Connection):
    """Cierra la conexión después de usar."""
    try:
        conn.close()
    except Exception:
        pass


def close_pool():
    """Compatibilidad con el lifespan de main.py — no hace nada con conexiones simples."""
    logger.info("Conexiones PostgreSQL cerradas.")
