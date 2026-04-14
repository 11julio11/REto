import asyncio
import logging
from src.workers.queue import job_queue

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
            
            # Simulamos un procesamiento de tarea pesada (Demora de 5 seg para test de shutdown)
            await asyncio.sleep(5)

            
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
        logger.info("Iniciando apagado elegante del Worker Pool...")
        
        # 1. Esperamos a que la cola se vacíe (timeout de 30s)
        try:
            pending_tasks = job_queue.qsize()
            if pending_tasks > 0:
                logger.info(f"Detectadas {pending_tasks} tareas pendientes. Esperando procesamiento...")
                # job_queue.join() espera a que todas las tareas tengan su correspondiente task_done()
                await asyncio.wait_for(job_queue.join(), timeout=30.0)
                logger.info("Todas las tareas pendientes han sido procesadas.")
        except asyncio.TimeoutError:
            logger.warning("Timeout de 30s agotado. Forzando apagado de workers (algunas tareas podrían perderse).")
        
        # 2. Cancelamos los workers (que ahora estarán bloqueados en job_queue.get())
        for w in self.workers:
            w.cancel()
        
        await asyncio.gather(*self.workers, return_exceptions=True)
        logger.info("WorkerPool apagado exitosamente.")

