from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List

from domain.schemas import ItemCreate, ItemResponse
from service.item_service import ItemService, ItemNotFoundError
from api.dependencies import get_item_service
from workers.queue import enqueue_job

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=List[ItemResponse])
def list_items(service: ItemService = Depends(get_item_service)):
    # La ruta no sabe de DBs, solo llama a list_items()
    return service.list_items()


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create_item(item)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: str, service: ItemService = Depends(get_item_service)):
    try:
        return service.get_item(item_id)
    except ItemNotFoundError as e:
        # Aquí mapeamos un Error de Dominio a un Error HTTP
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str, service: ItemService = Depends(get_item_service)):
    try:
        service.delete_item(item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{item_id}/process", status_code=status.HTTP_202_ACCEPTED)
async def process_item_async(item_id: str, service: ItemService = Depends(get_item_service)):
    """
    Ruta delegada (Día 9)
    Simula ordenar que se procese un Item en segundo plano por el Worker Pool.
    Retorna 202 Inmediatamente para no bloquear al usuario.
    """
    # 1. Checamos que el item exista de forma sincrona
    try:
        item = service.get_item(item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    # 2. Delegamos la tarea pesada al canal
    await enqueue_job(job_type="SEND_EMAIL_PROMO", payload={"id": item.id, "name": item.name})
    
    return {"message": "Procesamiento de item aceptado y enrutado a workers."}
