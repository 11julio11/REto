import os
import logging
import redis

logger = logging.getLogger(__name__)

# Configuración desde variables de entorno
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_URL = os.environ.get("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

class RedisClient:
    """Cliente wrapper para Redis con manejo de errores básico."""
    
    def __init__(self):
        try:
            self.client = redis.from_url(REDIS_URL, decode_responses=True)
            # Verificar conexión
            self.client.ping()
            logger.info(f"Conectado a Redis en {REDIS_URL}")
        except Exception as e:
            logger.warning(f"No se pudo conectar a Redis: {e}. El sistema funcionará sin caché.")
            self.client = None

    def get(self, key: str):
        if self.client:
            try:
                return self.client.get(key)
            except Exception as e:
                logger.error(f"Error al leer de Redis: {e}")
        return None

    def set(self, key: str, value: str, ex: int = 3600):
        """Guarda un valor con tiempo de expiración (default 1h)."""
        if self.client:
            try:
                self.client.set(key, value, ex=ex)
            except Exception as e:
                logger.error(f"Error al escribir en Redis: {e}")

    def delete(self, key: str):
        if self.client:
            try:
                self.client.delete(key)
            except Exception as e:
                logger.error(f"Error al borrar de Redis: {e}")

# Instancia única (Singleton-ish) facilitada por el import
redis_client = RedisClient()
