import json
import logging
import sys
import os
from unittest.mock import MagicMock

# Añadir path para encontrar src
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from src.domain.schemas import ItemResponse
from src.repository.cached_item_repository import CachedItemRepository
from src.config.redis import redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_cache_logic():
    # 1. Mock del repositorio real (Postgres)
    mock_repo = MagicMock()
    mock_item = ItemResponse(
        id="test-123", 
        name="Cache Test", 
        description="Testing Redis", 
        price=10.0, 
        created_at="2024-01-01"
    )
    mock_repo.get_by_id.return_value = mock_item
    mock_repo.get_all.return_value = [mock_item]

    # 2. Instanciar decorador
    cached_repo = CachedItemRepository(mock_repo)

    print("\n--- Verificando Lógica de Caché ---")
    
    # Limpiar posibles restos
    redis_client.delete("item:test-123")
    redis_client.delete("items:all")

    # TEST 1: Cache Miss
    print("\n[Test 1] Primer get_by_id (debería ir a DB)")
    item1 = cached_repo.get_by_id("test-123")
    assert mock_repo.get_by_id.call_count == 1
    print(f"Resultado: {item1.name} (Cargado de DB)")

    # TEST 2: Cache Hit
    print("\n[Test 2] Segundo get_by_id (debería ir a Caché)")
    item2 = cached_repo.get_by_id("test-123")
    # El call count de mock_repo NO debería aumentar
    assert mock_repo.get_by_id.call_count == 1
    print(f"Resultado: {item2.name} (¡Cache Hit!)")

    # TEST 3: Invalación
    print("\n[Test 3] Guardar item (debería invalidar caché)")
    cached_repo.save("test-123", mock_item.model_dump())
    
    print("\n[Test 4] Tercer get_by_id post-save (debería ir a DB otra vez)")
    cached_repo.get_by_id("test-123")
    assert mock_repo.get_by_id.call_count == 2
    print("Resultado: Caché invalidada correctamente.")

if __name__ == "__main__":
    if not redis_client.client:
        print("ERROR: Redis no disponible. Asegúrate de que Redis esté corriendo (docker-compose up redis).")
        sys.exit(1)
    test_cache_logic()
