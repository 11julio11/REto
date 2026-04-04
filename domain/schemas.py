from pydantic import BaseModel
from typing import Optional


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
