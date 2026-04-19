# Día 24: Métricas de Producto y Tracking de Eventos

Una vez que configuramos la observabilidad técnica (latencia, uso de CPU, errores HTTP 500), el siguiente paso crítico en cualquier SaaS es la **Observabilidad de Producto**. Es aquí donde medimos qué hacen concretamente los usuarios para saber si nuestras funciones (o MVP) realmente están aportando valor y si nuestras estimaciones del framework RICE eran correctas.

## Event Tracking (Rastreo de Eventos)

Para entender el comportamiento y el ciclo de vida de los usuarios dentro de nuestra aplicación, debemos disparar "Eventos de Producto". Un evento bien estructurado generalmente contiene:

- **Nombre del Evento (Event Name):** Una cadena en mayúsculas que describe la acción, ej. `USER_SIGNED_UP`, `ITEM_CREATED`.
- **Atributos/Propiedades:** El contexto de la acción, ej. el `user_id`, qué `plan` eligió o el origen del registro.
- **Timestamp:** Cuándo ocurrió exactamente (nuestro logger JSON ya maneja esto de forma automática).

### Implementación Práctica en la API

Aprovechando que ya tenemos un sistema de logs estructurados en JSON, la forma más elegante y sencilla de emitir métricas de producto sin introducir librerías externas complejas es embeber estos eventos críticos en nuestros propios logs. 

Herramientas tipo Datadog, Splunk o el stack ELK pueden ingerir estos logs JSON y crear tableros automáticos basados en ciertas "llaves".

#### Ejemplo implementado en `auth_service.py`:

```python
import logging
logger = logging.getLogger(__name__)

# Dentro de la lógica de negocio cuando un registro es exitoso:
logger.info("New user successfully registered", extra={
    "metric_type": "product_event",
    "event_name": "USER_SIGNED_UP",
    "user_id": user_id,
    "username": user_create.username
})
```

Al utilizar un diferenciador como `"metric_type": "product_event"`, desde nuestro servidor de logs o nuestra herramienta de analíticas, podemos crear un filtro para extraer y graficar:
- Cuántos `USER_SIGNED_UP` tuvimos por hora/día.
- Tasas de conversión si combinamos esto con otros eventos en el frontend.
- Crecimiento mensual activo.

Esta separación intencional a nivel código nos da visibilidad de negocio en tiempo real.
