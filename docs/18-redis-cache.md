# Día 18: Escalabilidad - Caché con Redis

En sistemas de alta demanda, la base de datos relacional (PostgreSQL) suele ser el primer cuello de botella. El acceso a disco es lento comparado con el acceso a memoria RAM. Para solucionar esto, implementamos una capa de **Caché** usando **Redis**.

## 1. El problema: Datos calientes y lecturas repetitivas
Muchas veces, nuestra API consulta los mismos datos una y otra vez (por ejemplo, la lista de productos o un perfil de usuario). Consultar la DB principal para cada petición es ineficiente si los datos no han cambiado.

## 2. Solución: Estrategia "Cache Aside" (Lazy Loading)
Hemos implementado el patrón **Cache Aside**:

1. El servidor recibe una petición `GET`.
2. Busca en **Redis** (Memoria RAM):
   - **HIT:** Encuentra el dato y lo devuelve instantáneamente.
   - **MISS:** No está el dato. Consulta la **DB**, guarda el resultado en Redis con un **TTL** (Time To Live) y lo devuelve.

## 3. Patrón Decorador para Repositorios
Para mantener nuestra **Clean Architecture**, no hemos ensuciado el `PostgresItemRepository` con lógica de Redis. En su lugar, usamos un **Decorador**:

- `CachedItemRepository` envuelve al repositorio original.
- Para el resto de la aplicación, el objeto sigue siendo un `ItemRepository`.
- La lógica de "cuando usar Redis y cuando DB" queda encapsulada en esta capa intermedia.

## 4. Coherencia de Datos (Invalidación)
Un error común en caché es servir datos viejos. Para evitarlo:
- **Escrituras (POST/DELETE):** Cuando un item se guarda o borra en la DB, inmediatamente **borramos** la entrada correspondiente en Redis.
- Así, la siguiente lectura forzará un "Cache Miss" y traerá el dato fresco de la DB.

## Resumen de la Implementación

- **Infraestructura:** Redis corriendo en Docker (puerto 6379).
- **Librería:** `redis-py`.
- **Ubicación:** 
  - `src/config/redis.py`: Conexión y cliente.
  - `src/repository/cached_item_repository.py`: Lógica del decorador.
- **Inyección:** Configurado dinámicamente en `dependencies.py`.

> [!TIP]
> La caché es una espada de doble filo. Úsala solo para datos que se leen mucho más de lo que se escriben. Cachear datos que cambian cada segundo puede causar más problemas de los que resuelve.
