# 🔄 Día 9: Concurrencia Limitada (Worker Pools)

## ¿Qué es la Concurrencia y el Patrón Worker Pool?
En el desarrollo backend, cuando tienes una tarea pesada (ej: enviar correos, generar reportes pesados, procesar imágenes), si lo haces de forma síncrona, el usuario que hizo la petición se quedará esperando la respuesta, causando frustración o "Timeouts" críticos.

La solución inexperta es arrojar las tareas a procesos de fondo de manera ilimitada (tirar Goroutines en `Go` o Tareas Asíncronas en `Python`). El problema de correrlas sin control es que un pico de alto tráfico sofocará los recursos del hardware de tu servidor (CPU/RAM).

El **Worker Pool** (Piscina de Trabajadores) entra a dictar un límite sano. Instancias un número de recolectores (Workers), digamos `5`. Todos esos trabajadores consumen eventos provenientes de una Cola (`Queue` / `Channel`). 
Si llegan 100,000 eventos, los 5 trabajadores no morirán trabajando simultáneamente con todos, procesarán a su propio ritmo de 5 en 5, limitando y garantizando que el servidor permanezca estabilizado.

## ¿Cómo aplica en nuestro Stack?
Originalmente el reto dicta practicarlo en **Go** (donde los `goroutines` y `channels` son herramientas de primera clase), en **Python** logramos réplicas cuasi-idénticas usando `asyncio`:

1. `asyncio.Queue`: Será nuestra banda transportadora.
2. `asyncio.create_task()`: Serán los trabajadores corriendo concurrentemente dentro del Event-Loop (Bucle de Eventos).
3. **Eventos de FastAPI (`lifespan`)**: Arrancaremos nuestra "fábrica de trabajadores" justamente cuando el servidor inicie y la apagaremos gracefully cuando el servidor se desconecte.
