import os
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from src.domain.interfaces import ItemRepository, UserRepository
from src.service.item_service import ItemService
from src.service.auth_service import AuthService
from src.config.security import verify_token

logger = logging.getLogger(__name__)

# ── Detectar si PostgreSQL está disponible ────────────────────────────────
# Si DATABASE_URL está configurada, usamos Postgres. Si no, fallback a Memoria.
_use_postgres = bool(os.environ.get("DATABASE_URL"))

def _get_repos():
    """Retorna los repositorios correctos según el entorno."""
    if _use_postgres:
        try:
            from src.repository.postgres_item_repository import PostgresItemRepository
            from src.repository.postgres_user_repository import PostgresUserRepository
            return PostgresItemRepository(), PostgresUserRepository()
        except Exception as e:
            logger.warning(f"PostgreSQL no disponible, usando memoria: {e}")

    from src.repository.memory_repository import db_instance, user_db_instance
    return db_instance, user_db_instance

_item_repo, _user_repo = _get_repos()


def get_item_repository() -> ItemRepository:
    """Retorna la implementación de repositorio activa (Postgres o Memoria)."""
    return _item_repo


def get_item_service(repo: ItemRepository = Depends(get_item_repository)) -> ItemService:
    return ItemService(repo=repo)


def get_user_repository() -> UserRepository:
    return _user_repo


def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo=repo)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Podríamos buscar el usuario en la BD para más seguridad, pero para simplificar
    # validaremos solo la decodificación exitosa del ID
    return {"id": user_id}
