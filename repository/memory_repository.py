from typing import List, Optional
from domain.interfaces import ItemRepository, UserRepository
from domain.schemas import ItemResponse


class MemoryItemRepository(ItemRepository):
    """
    Implementación en memoria de la interfaz ItemRepository.
    En la Semana 2, crearemos un PostgresItemRepository(ItemRepository)
    y lo inyectaremos en lugar de este, sin cambiar nada en el servicio!
    """

    def __init__(self):
        # Base de datos en memoria local a esta instancia
        self._db: dict[str, dict] = {}

    def get_all(self) -> List[ItemResponse]:
        return [ItemResponse(**item) for item in self._db.values()]

    def get_by_id(self, item_id: str) -> Optional[ItemResponse]:
        item_data = self._db.get(item_id)
        if item_data:
            return ItemResponse(**item_data)
        return None

    def save(self, item_id: str, item_data: dict) -> ItemResponse:
        self._db[item_id] = item_data
        return ItemResponse(**item_data)

    def delete(self, item_id: str) -> bool:
        if item_id in self._db:
            del self._db[item_id]
            return True
        return False


# Instancia global como simulador de DB, solo por ser en memoria
db_instance = MemoryItemRepository()


class MemoryUserRepository(UserRepository):
    def __init__(self):
        # Base de datos en memoria local para usuarios
        # struct: {"user_id": {"id": "...", "username": "...", "hashed_password": "..."}}
        self._db: dict[str, dict] = {}

    def get_by_username(self, username: str) -> Optional[dict]:
        for user_data in self._db.values():
            if user_data.get("username") == username:
                return user_data
        return None

    def save(self, user_id: str, user_data: dict) -> dict:
        self._db[user_id] = user_data
        return user_data

user_db_instance = MemoryUserRepository()
