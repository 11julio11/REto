from fastapi import Depends
from repository.memory_repository import db_instance
from domain.interfaces import ItemRepository
from service.item_service import ItemService


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
