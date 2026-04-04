import asyncio
import logging
from workers.queue import job_queue

logger = logging.getLogger("worker_pool")

async def worker(worker_id: int):
    """
    El 'Cartero' (Goroutine) que vive por siempre tomando paquetes de la cola.
    """
    logger.info(f"Worker {worker_id} inicializado y esperando trabajos...")
    
    while True:
        try:
            # Esperamos infinitamente hasta que un item entre a la cola
            job = await job_queue.get()
            
            logger.info(f"Worker {worker_id} procesando: {job['type']}")
            
            # Simulamos un procesamiento de tarea pesada de IA o envío de Correo (Demora de 1 seg)
            await asyncio.sleep(1)
            
            logger.info(f"Worker {worker_id} completó exitosamente la tarea de la data: {job['payload']}")
            
            # Notificamos a la cola que la tarea concluyó de forma segura
            job_queue.task_done()
            
        except asyncio.CancelledError:
            # Capturamos la señal de apagado del servidor principal
            logger.info(f"Worker {worker_id} terminando proceso (Graceful Shutdown).")
            break
        except Exception as e:
            logger.error(f"Worker {worker_id} reventó trabajando: {e}")


class WorkerPool:
    def __init__(self, num_workers: int = 3):
        self.num_workers = num_workers
        self.workers = []

    async def start(self):
        """Dispara las N tareas dentro del Event Loop de FastAPI"""
        for i in range(1, self.num_workers + 1):
            task = asyncio.create_task(worker(i))
            self.workers.append(task)
        logger.info(f"WorkerPool escaló {self.num_workers} workers.")

    async def stop(self):
        """Lógica de apagado elegante. Espera a que terminen o cancela."""
        logger.info("Solicitando shutdown del Worker Pool...")
        
        # Opcional: Podrías esperar a que vacíen la cola `await job_queue.join()`
        
        for w in self.workers:
            w.cancel() # Enviamos la CancelledError
        
        await asyncio.gather(*self.workers, return_exceptions=True)
        logger.info("WorkerPool apagado gloriosamente.")
