from typing import List, Optional
from src.domain.interfaces import ItemRepository, UserRepository
from src.domain.schemas import SubscriptionResponse


class MemoryItemRepository(ItemRepository):
    """
    Implementación en memoria de la interfaz ItemRepository.
    """

    def __init__(self):
        # Base de datos en memoria local a esta instancia
        self._db: dict[str, dict] = {}

    def get_all(self) -> List[SubscriptionResponse]:
        return [SubscriptionResponse(**item) for item in self._db.values()]

    def get_by_id(self, item_id: str) -> Optional[SubscriptionResponse]:
        item_data = self._db.get(item_id)
        if item_data:
            return SubscriptionResponse(**item_data)
        return None

    def save(self, item_id: str, item_data: dict) -> SubscriptionResponse:
        self._db[item_id] = item_data
        return SubscriptionResponse(**item_data)

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
