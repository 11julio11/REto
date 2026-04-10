import asyncio
from typing import Any, Dict

# Esta es nuestra "Banda Transportadora" (Canal de Go adaptado a Python)
# Limitamos la cola a 10,000 tareas para prevenir saturación de RAM infinita
job_queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue(maxsize=10000)

async def enqueue_job(job_type: str, payload: dict):
    """
    Función que invocará la API para delegar trabajo a los trabajadores.
    """
    job = {"type": job_type, "payload": payload}
    await job_queue.put(job)
