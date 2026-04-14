import json
import logging
from typing import List, Optional
from src.domain.interfaces import ItemRepository
from src.domain.schemas import ItemResponse
from src.config.redis import redis_client

logger = logging.getLogger(__name__)

class CachedItemRepository(ItemRepository):
    """
    Decorador para ItemRepository que añade una capa de caché con Redis.
    Sigue el patrón 'Proxy' o 'Decorator' para no modificar la lógica de DB.
    """
    
    def __init__(self, real_repo: ItemRepository):
        self.real_repo = real_repo
        self.cache_key_all = "items:all"
        self.cache_prefix_item = "item:"

    def get_all(self) -> List[ItemResponse]:
        # 1. Intentar leer de caché
        cached_data = redis_client.get(self.cache_key_all)
        if cached_data:
            logger.info("Cache Hit: list_items")
            try:
                items_raw = json.loads(cached_data)
                return [ItemResponse(**item) for item in items_raw]
            except Exception as e:
                logger.error(f"Error parseando caché: {e}. Reintentando con DB.")

        # 2. Si no está en caché o falló, ir a la DB real
        logger.info("Cache Miss: list_items. Cargando de DB...")
        items = self.real_repo.get_all()
        
        # 3. Guardar en caché (serializar a JSON usando model_dump de Pydantic v2)
        try:
            items_json = json.dumps([item.model_dump() for item in items])
            redis_client.set(self.cache_key_all, items_json, ex=300) # TTL 5 min
        except Exception as e:
            logger.error(f"Error guardando en caché: {e}")
        
        return items

    def get_by_id(self, item_id: str) -> Optional[ItemResponse]:
        key = f"{self.cache_prefix_item}{item_id}"
        cached_data = redis_client.get(key)
        
        if cached_data:
            logger.info(f"Cache Hit: {key}")
            try:
                return ItemResponse(**json.loads(cached_data))
            except Exception:
                pass
        
        logger.info(f"Cache Miss: {key}. Cargando de DB...")
        item = self.real_repo.get_by_id(item_id)
        
        if item:
            try:
                redis_client.set(key, json.dumps(item.model_dump()), ex=600) # TTL 10 min
            except Exception as e:
                logger.error(f"Error guardando item en caché: {e}")
            
        return item

    def save(self, item_id: str, item_data: dict) -> ItemResponse:
        # 1. Persistencia en DB
        item = self.real_repo.save(item_id, item_data)
        
        # 2. INVALIDACIÓN: Borrar caché para asegurar consistencia (Cache Aside)
        logger.info(f"Invalidando caché tras guardado: {item_id}")
        redis_client.delete(self.cache_key_all)
        redis_client.delete(f"{self.cache_prefix_item}{item_id}")
        
        return item

    def delete(self, item_id: str) -> bool:
        # 1. Borrar en DB
        success = self.real_repo.delete(item_id)
        
        # 2. Si se borró con éxito, invalidar caché
        if success:
            logger.info(f"Invalidando caché tras borrado: {item_id}")
            redis_client.delete(self.cache_key_all)
            redis_client.delete(f"{self.cache_prefix_item}{item_id}")
            
        return success
