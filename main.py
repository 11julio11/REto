"""
API principal del Reto T-Shaped Engineer.

Día 8: Refactor a Clean Architecture + Dependency Injection.
El main solo arranca el servidor y conecta los routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routers import router as items_router
from workers.pool import WorkerPool
import logging

# Configurar logs básicos para ver el WorkerPool
logging.basicConfig(level=logging.INFO)

pool = WorkerPool(num_workers=3)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Arrancamos los trabajadores
    await pool.start()
    yield
    # Apagamos ordenadamente los trabajadores al morir el app
    await pool.stop()

# ──────────────────────────────────────────────
# App FastAPI
# ──────────────────────────────────────────────

app = FastAPI(
    title="Reto API Clean Architecture",
    description="API del Reto T-Shaped Engineer — Checkpoint Día 9 (Worker Pools)",
    version="3.0.0",
    lifespan=lifespan,
)

# Incluir Rutas
app.include_router(items_router)


@app.get("/", tags=["health"])
def health_check():
    """Health check — usado por Docker HEALTHCHECK y K8s probes."""
    return {
        "status": "healthy",
        "service": "reto-api",
        "version": "2.0.0",
        "arch": "clean-architecture"
    }


# ──────────────────────────────────────────────
# Entry point para desarrollo local
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
