from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List

from src.domain.schemas import SubscriptionCreate, SubscriptionResponse
from src.service.item_service import ItemService, ItemNotFoundError
from src.api.dependencies import get_item_service, get_current_user
from src.workers.queue import enqueue_job

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("", response_model=List[SubscriptionResponse])
def list_subscriptions(
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    # La ruta no sabe de DBs, solo llama a list_items()
    return service.list_items()


@router.post("", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(
    subscription: SubscriptionCreate,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    return service.create_item(subscription)


@router.get("/{item_id}", response_model=SubscriptionResponse)
def get_subscription(
    item_id: str,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        return service.get_item(item_id)
    except ItemNotFoundError as e:
        # Aquí mapeamos un Error de Dominio a un Error HTTP
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: str,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        service.delete_item(item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{item_id}/process", status_code=status.HTTP_202_ACCEPTED)
async def process_item_async(
    item_id: str,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
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
