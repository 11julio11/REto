# Día 14: Proyecto Fullstack con Auth Real y Migraciones Funcionando

Este es el checkpoint de la segunda semana. Aqui conectamos todo lo aprendido en una sola aplicación que funciona de forma real, la cual ninguna parte usa datos simulados:

```
Frontend React (Vite)             ←→    Backend FastAPI
     TanStack Query                          JWT Auth
     Toasts globales                         Workers Pool
     Login / Register              ←→    PostgreSQL (real)
                                           Migraciones Yoyo
```

## Flujo Completo de una Petición

1. **Usuario abre el frontend** → ve `Login.jsx`
2. **Se registra** → `POST /auth/register` → `AuthService.register_user()` → hashes bcrypt guarado en **PostgreSQL** (`users` table)
3. **Hace login** → `POST /auth/login` → devuelve **JWT** firmado con HMAC-SHA256
4. **TanStack Query fetchea los items** → `GET /items` con `Authorization: Bearer <token>` → `get_current_user()` verifica el JWT → `PostgresItemRepository.get_all()` hace `SELECT` en **PostgreSQL** (`items` table)
5. **Crea un item** → `POST /items` → INSERT en PostgreSQL → `invalidateQueries(['items'])` → **refetch automático con nuevo dato**

## Arquitectura de capas

```
Frontend
└── src/
    ├── context/ToastContext.jsx   ← Errores globales
    ├── services/api.js            ← Axios + interceptor JWT
    └── components/
        ├── Login.jsx              ← Registro + Login
        └── ItemsList.jsx          ← useQuery + useMutation

Backend
├── api/
│   ├── auth_router.py             ← /auth/login, /auth/register
│   └── routers.py                 ← /items (protegido con JWT)
├── service/
│   ├── auth_service.py            ← Lógica de negocio de auth
│   └── item_service.py            ← Lógica de negocio de items
├── repository/
│   ├── postgres_item_repository.py ← SQL real para items
│   └── postgres_user_repository.py ← SQL real para users
├── db/
│   └── connection.py              ← Pool de conexiones psycopg2
├── core/
│   ├── security.py                ← JWT + Bcrypt
│   └── config.py                  ← DATABASE_URL desde entorno
├── migrations/
│   └── 0001_init_schema.sql       ← CREATE TABLE users, items
└── scripts/
    └── migrate.py                 ← Ejecuta migraciones programáticamente
```

## Auto-detección de entorno

El sistema detecta automáticamente si tiene Base de Datos disponible:
- **Con `DATABASE_URL`** → Usa `PostgresItemRepository` + `PostgresUserRepository`
- **Sin `DATABASE_URL`** → Fallback a `MemoryItemRepository` + `MemoryUserRepository`

Esto funciona en el lifespan de FastAPI:
```python
if os.environ.get("DATABASE_URL"):
    run_migrations()  # Crea tablas si no existen
```

## Cómo ejecutar localmente (con Docker)

```bash
# 1. Levantar la base de datos
docker compose up -d db

# 2. Aplicar migraciones
python -m scripts.migrate

# 3. Arrancar el backend
DATABASE_URL=postgresql://myuser:superseguro123@localhost:5432/mydb uvicorn main:app --reload

# 4. En otra terminal, el frontend
cd frontend && npm run dev
```
