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

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str

class UserInDB(UserResponse):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
