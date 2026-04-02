"""
API principal del Reto T-Shaped Engineer.

Día 7 Checkpoint: API containerizada con pipeline CI/CD.
Arquitectura simple pero profesional con FastAPI.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


# ──────────────────────────────────────────────
# Modelos (Pydantic)
# ──────────────────────────────────────────────

class ItemCreate(BaseModel):
    """Schema para crear un item."""
    name: str
    description: Optional[str] = None
    price: float


class ItemResponse(BaseModel):
    """Schema de respuesta de un item."""
    id: str
    name: str
    description: Optional[str] = None
    price: float
    created_at: str


# ──────────────────────────────────────────────
# "Base de datos" en memoria (se reemplaza en Semana 2)
# ──────────────────────────────────────────────

items_db: dict[str, dict] = {}


# ──────────────────────────────────────────────
# App FastAPI
# ──────────────────────────────────────────────

app = FastAPI(
    title="Reto API",
    description="API del Reto T-Shaped Engineer — Checkpoint Día 7",
    version="1.0.0",
)


# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────

@app.get("/", tags=["health"])
def health_check():
    """Health check — usado por Docker HEALTHCHECK y K8s probes."""
    return {
        "status": "healthy",
        "service": "reto-api",
        "version": "1.0.0",
    }


@app.get("/items", response_model=list[ItemResponse], tags=["items"])
def list_items():
    """Devuelve todos los items."""
    return list(items_db.values())


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
)
def create_item(item: ItemCreate):
    """Crea un nuevo item."""
    item_id = str(uuid.uuid4())
    new_item = {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "created_at": datetime.utcnow().isoformat(),
    }
    items_db[item_id] = new_item
    return new_item


@app.get("/items/{item_id}", response_model=ItemResponse, tags=["items"])
def get_item(item_id: str):
    """Obtiene un item por su ID."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item_id}' no encontrado",
        )
    return items_db[item_id]


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["items"],
)
def delete_item(item_id: str):
    """Elimina un item por su ID."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item_id}' no encontrado",
        )
    del items_db[item_id]


# ──────────────────────────────────────────────
# Entry point para desarrollo local
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)