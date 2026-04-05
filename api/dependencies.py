from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from repository.memory_repository import db_instance, user_db_instance
from domain.interfaces import ItemRepository, UserRepository
from service.item_service import ItemService
from service.auth_service import AuthService
from core.security import verify_token


def get_item_repository() -> ItemRepository:
    """
    Retorna la implementación específica de DB que usemos.
    Aquí es donde cambiaríamos a PostgresItemRepository(db_client) en la Semana 2.
    """
    return db_instance


def get_item_service(repo: ItemRepository = Depends(get_item_repository)) -> ItemService:
    """
    Inyector de dependencias para el framework de FastAPI.
    Construye nuestro servicio de negocio inyectándole el repositorio.
    """
    return ItemService(repo=repo)


def get_user_repository() -> UserRepository:
    return user_db_instance


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
