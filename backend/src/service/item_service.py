import uuid
from datetime import datetime, timezone
from typing import List

from src.domain.interfaces import ItemRepository
from src.domain.schemas import SubscriptionCreate, SubscriptionResponse

class ItemServiceError(Exception):
    """Excepción base para lógica de negocio de items."""
    pass


class ItemNotFoundError(ItemServiceError):
    """Excepción cuando un item no se encuentra."""
    pass


class ItemService:
    """Contiene toda la lógica de negocio de las Suscripciones."""

    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def list_items(self) -> List[SubscriptionResponse]:
        return self.repo.get_all()

    def create_item(self, subscription: SubscriptionCreate) -> SubscriptionResponse:
        # Logica de negocio: asignar IDs y timestamps
        item_id = str(uuid.uuid4())
        new_subscription_dict = {
            "id": item_id,
            "name": subscription.name,
            "description": subscription.description,
            "cost": subscription.cost,
            "billing_cycle": subscription.billing_cycle,
            "next_payment": subscription.next_payment,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        # Delegar guardar en infraestructura
        return self.repo.save(item_id, new_subscription_dict)

    def get_item(self, item_id: str) -> SubscriptionResponse:
        item = self.repo.get_by_id(item_id)
        if not item:
            # Error de negocio, no de base de datos
            raise ItemNotFoundError(f"Item '{item_id}' no encontrado")
        return item

    def delete_item(self, item_id: str) -> None:
        if not self.repo.delete(item_id):
            raise ItemNotFoundError(f"Item '{item_id}' no encontrado")
