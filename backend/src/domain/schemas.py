from pydantic import BaseModel
from typing import Optional


class SubscriptionCreate(BaseModel):
    """Schema para crear una suscripción."""
    name: str
    description: Optional[str] = None
    cost: float
    billing_cycle: str  # monthly, yearly
    next_payment: str   # ISO format date


class SubscriptionResponse(BaseModel):
    """Schema de respuesta de una suscripción."""
    id: str
    name: str
    description: Optional[str] = None
    cost: float
    billing_cycle: str
    next_payment: str
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
