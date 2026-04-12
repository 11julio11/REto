# Día 17: Observabilidad (Los 3 Pilares)

En la ingeniería de software moderna, no basta con que el código "funcione". Necesitamos saber **por qué** falla cuando lo hace, **qué tan rápido** responde y **qué camino** sigue una petición a través de nuestro sistema. Estos son los tres pilares de la observabilidad.

## 1. Logs Estructurados (JSON)

El logging tradicional ("texto plano") es fácil de leer para humanos pero una pesadilla para las máquinas. En sistemas distribuidos, usamos **Logs Estructurados**.

- **Antes:** `INFO:src.main:Conexión exitosa a la DB`
- **Ahora (JSON):** 
  ```json
  {"timestamp": "2024-04-11T21:45:00", "severity": "INFO", "name": "src.main", "message": "Conexión exitosa a la DB", "trace_id": "550e..."}
  ```

Al usar JSON, herramientas como **Grafana Loki** o **Elasticsearch** pueden filtrar instantáneamente por severidad, servicio o ID de rastro sin necesidad de expresiones regulares complejas.

## 2. Métricas (Prometheus)

Las métricas son datos numéricos agregados que nos dan la salud general del sistema. En lugar de mirar un log individual, miramos tendencias.

Hemos implementado un endpoint en `/metrics` que expone:
- **Latencia:** Cuántos milisegundos tarda cada endpoint.
- **Rendimiento (Throughput):** Cuántas peticiones por segundo estamos procesando.
- **Errores:** Conteo de respuestas 4xx y 5xx.

Este formato es compatible con **Prometheus**, el estándar de la industria para recolectar métricas y generar alertas si la latencia sube demasiado.

## 3. Tracing y Correlación

El tracing permite seguir el "hilo" de una petición. En este proyecto, hemos implementado la **Correlación de Logs** mediante un `trace_id`.

1. Cuando llega una petición, el `TracingMiddleware` genera un UUID único.
2. Este ID se inyecta en cada línea de log generada durante esa ejecución.
3. El ID se devuelve al cliente en el header `X-Trace-Id`.

> [!IMPORTANT]  
> Si un usuario reporta un error y te da su `X-Trace-Id`, puedes buscar ese ID en tu sistema de logs y ver **exactamente** qué pasos dio el servidor y dónde falló, ignorando el ruido de los otros miles de usuarios.

## Resumen de la Implementación

- **Librerías:** `python-json-logger` y `prometheus-fastapi-instrumentator`.
- **Ubicación:** Centralizado en `src/config/observability.py`.
- **Uso:** Importado en `main.py` mediante `setup_logging()` y `setup_metrics(app)`.
