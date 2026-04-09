"""
Runner de migraciones usando psycopg3.
psycopg3 maneja correctamente el encoding en Windows Python 3.13.
"""
import time
import socket
import logging
import psycopg                      # psycopg3 — reemplaza a psycopg2
from pathlib import Path
from core.config import DATABASE_URL

logger = logging.getLogger(__name__)

MAX_RETRIES = 30
RETRY_DELAY = 3
DB_HOST = "127.0.0.1"
DB_PORT = 5432


def _port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def _connect():
    for attempt in range(1, MAX_RETRIES + 1):
        if not _port_open(DB_HOST, DB_PORT):
            logger.warning(f"⏳ Puerto {DB_PORT} cerrado (intento {attempt}/{MAX_RETRIES}). Reintentando en {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
            continue
        try:
            conn = psycopg.connect(DATABASE_URL)
            logger.info("✅ Conexión a PostgreSQL establecida (psycopg3).")
            return conn
        except psycopg.OperationalError as e:
            if attempt < MAX_RETRIES:
                logger.warning(f"⏳ Auth falló (intento {attempt}/{MAX_RETRIES}): {e}. Reintentando...")
                time.sleep(RETRY_DELAY)
            else:
                raise

    raise ConnectionError(f"No se pudo conectar a {DB_HOST}:{DB_PORT} tras {MAX_RETRIES} intentos.")


def run_migrations():
    """Aplica los archivos SQL de migrations/ en orden."""
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS _migrations (
                    id VARCHAR(255) PRIMARY KEY,
                    applied_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            conn.commit()

        migrations_dir = Path("migrations")
        applied = 0
        for sql_file in sorted(migrations_dir.glob("*.sql")):
            migration_id = sql_file.stem
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM _migrations WHERE id = %s", (migration_id,))
                if cur.fetchone():
                    logger.info(f"  ⏭  {migration_id} ya aplicado.")
                    continue
                logger.info(f"  ▶  Aplicando {migration_id}...")
                sql = sql_file.read_text(encoding="utf-8")
                cur.execute(sql)
                cur.execute("INSERT INTO _migrations (id) VALUES (%s)", (migration_id,))
                conn.commit()
                applied += 1

        if applied:
            logger.info(f"✅ {applied} migración(es) aplicada(s).")
        else:
            logger.info("✅ BD al día, sin migraciones pendientes.")
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_migrations()
