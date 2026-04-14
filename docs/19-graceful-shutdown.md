# Día 19: Resiliencia - Graceful Shutdown

En un entorno de microservicios o contenedores (como Docker o Kubernetes), las instancias de nuestra aplicación pueden ser detenidas y reiniciadas en cualquier momento (por despliegues, auto-escalado o fallos). El **Graceful Shutdown** es la técnica que asegura que cuando esto ocurra, no dejemos tareas a medias ni rompamos transacciones.

## 1. El ciclo de vida: SIGTERM vs SIGKILL

Cuando ordenamos detener un contenedor:
1. El orquestador envía una señal **SIGTERM** (Signal Terminate). Es una "petición amable" para que la app cierre.
2. La app debe interceptar esto, dejar de aceptar tráfico y limpiar recursos.
3. Si después de un tiempo (ej. 30 segundos) la app sigue viva, el orquestador envía un **SIGKILL**. Esto mata el proceso al instante (muerte súbita), lo cual puede corromper datos o dejar tareas pesadas incompletas.

## 2. Implementación en FastAPI (Lifespan)

Hemos utilizado el evento `lifespan` de FastAPI, que actúa como un gestor de contexto global:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # FASE DE ARRANQUE: Abrir conexiones, workers, etc.
    yield
    # FASE DE APAGADO: Ocurre al recibir SIGTERM
    # Aquí cerramos todo en orden inverso.
```

## 3. Workers y Procesamiento de Fondo

El desafío principal son los **Background Workers**. Si un worker está procesando una tarea de 5 segundos y el servidor se apaga al segundo 2, la tarea se pierde.

Nuestra solución:
1. Al recibir el apagado, llamamos a `pool.stop()`.
2. Usamos `await job_queue.join()`: Esto bloquea el hilo de apagado hasta que todas las tareas encoladas hayan sido marcadas como finalizadas (`task_done()`).
3. Añadimos un **Timeout**: Si las tareas tardan demasiado (más de 30s), forzamos el cierre para no bloquear el despliegue del nuevo contenedor.

## 4. Diferencia con Go (Canales y Contexts)

En **Go**, el Graceful Shutdown se maneja de forma muy similar pero explícita:
- Se usa un canal (`chan os.Signal`) para escuchar señales del SO.
- Se pasa un `context.WithTimeout` a las funciones de limpieza.
- El servidor HTTP tiene un método `.Shutdown(ctx)` que hace exactamente lo que hemos configurado aquí.

> [!IMPORTANT]
> Un buen Graceful Shutdown es la diferencia entre un sistema que pierde datos aleatoriamente durante los deploys y uno que es 100% estable.
