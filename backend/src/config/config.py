"""
Módulo de configuración central.
Lee variables de entorno con fallback para desarrollo local.
"""
import os


def get_database_url() -> str:
    """
    Construye o retorna la DATABASE_URL.
    - En Docker, viene como variable de entorno completa.
    - En local (sin Docker), construye desde partes o usa el default.
    """
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    # URL por defecto con el puerto 5433 para conectarse a Docker y evitar conflictos con un PostgreSQL local de Windows.
    return "postgresql://myuser:superseguro123@localhost:5433/mydb"


DATABASE_URL = get_database_url()
