from abc import ABC, abstractmethod
from typing import List, Optional
from domain.schemas import ItemResponse


class ItemRepository(ABC):
    """
    Contrato (Interfaz) que cualquier repositorio de BD debe cumplir.
    En Go esto sería 'type ItemRepository interface { ... }'
    """

    @abstractmethod
    def get_all(self) -> List[ItemResponse]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: str) -> Optional[ItemResponse]:
        pass

    @abstractmethod
    def save(self, item_id: str, item_data: dict) -> ItemResponse:
        pass

    @abstractmethod
    def delete(self, item_id: str) -> bool:
        pass

class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[dict]:
        pass

    @abstractmethod
    def save(self, user_id: str, user_data: dict) -> dict:
        pass
