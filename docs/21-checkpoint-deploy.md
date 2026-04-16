# Día 21: Checkpoint — App Desplegada con Redis y Logs

Después de las implementaciones independientes de caché, resiliencia y observabilidad, este es el hito donde validamos que todas las piezas del rompecabezas encajan perfectamente en un entorno unificado orchestrado por `docker-compose.yml`.

## 1. El Estado del Sistema

Nuestra infraestructura ahora corre 4 componentes clave en armonía:

1. **`db` (Postgres 14)**: La fuente de verdad. Segura, con health checks y datos persistentes mediante volúmenes.
2. **`redis` (Alpine)**: Nuestra capa de caché en memoria ultra rápida.
3. **`app` (FastAPI)**: La lógica de negocio construida con Clean Architecture. Incluye nuestra pool de Workers, inyección de dependencias para fallback de BD y el patrón *Cache-Aside*.
4. **`web` (Nginx + React)**: Sirve la aplicación frontal estática pre-compilada y actúa como `Reverse Proxy` enrutando silenciosamente el tráfico `/api/` hacia el backend.

## 2. Validando la Observabilidad (Logs JSON)

En entornos serios de producción, nadie lee la terminal en crudo. Los logs se ingieren en sistemas centralizados (ELK, Datadog, Loki) que exigen un formato estructurado.

Para ver los logs en formato JSON puro que hemos implementado, corremos:
```bash
docker compose logs app --tail 20
```

**Lo que verás:**
```json
{"timestamp": "2026-04-16 00:25:10,123", "severity": "INFO", "message": "Cache Miss: item:test-1. Cargando de DB...", "trace_id": "abc-123-xyz"}
{"timestamp": "2026-04-16 00:25:11,456", "severity": "INFO", "message": "Cache Hit: item:test-1", "trace_id": "def-456-uvw"}
```

El `trace_id` es nuestra magia: nos permite hilar un error desde que entra al middleware HTTP, pasa por los repositorios y servicios, hasta que termina la solicitud.

## 3. Validando el Caché (Redis)

El patrón instalado (*Cache-Aside*) es uno de los más resilientes en la industria. 

**Flujo de Verificación Práctica:**

1. **Escritura inicial:** Crea o actualiza un dato. Esto actualiza la DB y **borra** la caché antigua (Invalidación).
```bash
curl -X POST http://localhost:8000/items/test-2 \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Producto X\", \"price\": 19.99}"
```

2. **Lectura Fria (Cache Miss):** Pide el dato. FastAPI revisa Redis, no lo encuentra, va a Postgres, agarra el dato e inmediatamente lo guarda en Redis con un Time-To-Live (TTL).
```bash
curl http://localhost:8000/items/test-2
```
*Si miras los logs verás `Cache Miss...`*

3. **Lectura Caliente (Cache Hit):** Vuelve a pedirlo.
```bash
curl http://localhost:8000/items/test-2
```
*Si miras los logs verás `Cache Hit`. Ya no tocamos la base de datos y la latencia bajó notablemente.*

## 4. Validando Resiliencia (Graceful Shutdown)

La prueba de fuego del Día 19 que podemos hacer ahora.

Si detenemos bruscamente el servicio principal:
```bash
docker compose stop app
```

El log final será:
```json
{"timestamp": "...", "severity": "INFO", "message": "Recibida señal de apagado. Iniciando Graceful Shutdown...", "trace_id": "n/a"}
{"timestamp": "...", "severity": "INFO", "message": "Cerrando pool de conexiones PostgreSQL...", "trace_id": "n/a"}
{"timestamp": "...", "severity": "INFO", "message": "Apagado finalizado con éxito. ¡Adiós!", "trace_id": "n/a"}
```

Esto certifica que no estamos corrompiendo en medio de peticiones largas. 

> [!TIP]
> **Misión del Día 21 Cumplida**. Hemos pasado de simples scripts a una plataforma robusta, observable, rápida e interconectada de nivel productivo, capaz de correr en una EC2 barata sin sudar una gota.
