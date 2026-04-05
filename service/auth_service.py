from typing import Optional
from jose import JWTError
from domain.interfaces import UserRepository
from domain.schemas import UserCreate, UserInDB
from core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, verify_token
import uuid

class AuthError(Exception):
    pass

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, user_create: UserCreate) -> dict:
        existing_user = self.repo.get_by_username(user_create.username)
        if existing_user:
            raise AuthError("Username already registered")
        
        hashed_password = get_password_hash(user_create.password)
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "username": user_create.username,
            "hashed_password": hashed_password
        }
        self.repo.save(user_id, user_data)
        
        return {"id": user_id, "username": user_create.username}

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        user_data = self.repo.get_by_username(username)
        if not user_data:
            return None
        if not verify_password(password, user_data["hashed_password"]):
            return None
        return user_data

    def create_tokens_for_user(self, user_id: str) -> dict:
        access_token = create_access_token(subject=user_id)
        refresh_token = create_refresh_token(subject=user_id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str) -> dict:
        try:
            payload = verify_token(refresh_token)
            if payload.get("type") != "refresh":
                raise AuthError("Invalid token type")
            
            user_id = payload.get("sub")
            if user_id is None:
                raise AuthError("Invalid token payload")
                
            new_access_token = create_access_token(subject=user_id)
            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }
        except JWTError:
            raise AuthError("Token verify failed")
