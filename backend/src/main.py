"""
API principal del Reto T-Shaped Engineer.

Día 14: App Fullstack — Auth real + Migraciones de DB funcionando.
(Reorganizado en carpeta src)
"""

from contextlib import asynccontextmanager
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import router as items_router
from src.api.auth_router import router as auth_router
from src.workers.pool import WorkerPool
from src.config.observability import setup_logging, setup_metrics, TracingMiddleware

# 1. Configurar logs estructurados (JSON) ANTES de cualquier otra cosa
setup_logging()
logger = logging.getLogger(__name__)

pool = WorkerPool(num_workers=3)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Orquestación del ciclo de vida de la aplicación."""
    # --- FASE DE ARRANQUE ---
    if os.environ.get("DATABASE_URL"):
        try:
            from scripts.migrate import run_migrations
            run_migrations()
        except Exception as e:
            logger.warning(f"Migraciones no pudieron correr: {e}")

    await pool.start()
    
    yield
    
    # --- FASE DE APAGADO (Graceful Shutdown) ---
    logger.info("Recibida señal de apagado. Iniciando Graceful Shutdown...")
    
    # 1. Detener procesamiento de trabajadores (esperar a que terminen tareas pendientes)
    await pool.stop()
    
    # 2. Cerrar conexiones a bases de datos y caché
    try:
        from src.db.connection import close_pool
        from src.config.redis import redis_client
        
        logger.info("Cerrando pool de conexiones PostgreSQL...")
        close_pool()
        
        if redis_client.client:
            logger.info("Cerrando conexiones Redis...")
            redis_client.client.close()
            
    except Exception as e:
        logger.error(f"Error durante el cierre de conexiones: {e}")

    logger.info("Apagado finalizado con éxito. ¡Adiós!")


# ──────────────────────────────────────────────
# App FastAPI
# ──────────────────────────────────────────────

app = FastAPI(
    title="Reto API Clean Architecture",
    description="API del Reto T-Shaped Engineer — Checkpoint Día 9 (Worker Pools)",
    version="3.0.0",
    lifespan=lifespan,
)

# Middlewares (El orden importa: Tracing -> CORS)
app.add_middleware(TracingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Configurar Métricas (expone /metrics)
setup_metrics(app)

# Incluir Rutas
app.include_router(auth_router)
app.include_router(items_router)


@app.get("/", tags=["health"])
def health_check():
    """Health check — usado por Docker HEALTHCHECK y K8s probes."""
    return {
        "status": "healthy",
        "service": "reto-api",
        "version": "2.0.0",
        "arch": "clean-architecture",
        "location": "src/main.py"
    }


# ──────────────────────────────────────────────
# Entry point para desarrollo local
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    # Actualizado para correr el módulo src.main si se invoca con PYTHONPATH
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
