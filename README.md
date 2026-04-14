# 🚀 Reto API — T-Shaped Engineer Challenge

API containerizada con CI/CD profesional. Checkpoint del Día 7.

## Stack

| Capa | Tecnología |
|------|-----------|
| API | Python 3.11 + FastAPI |
| DB | PostgreSQL 14 (Docker) |
| Container | Docker multi-stage (Alpine) |
| Orquestación | Docker Compose + Secrets |
| Caché | Redis (Día 18) |
| Observabilidad | JSON Logs + Prometheus (Día 17) |
| CI/CD | GitHub Actions (Lint → Test → Build) |
| Testing | pytest (12 tests unitarios) |

## Quick Start

### Requisitos
- Docker y Docker Compose instalados
- Python 3.11 (para desarrollo local)

### Correr con Docker Compose
```bash
# Levantar API + PostgreSQL
docker-compose up --build

# La API estará en http://localhost:8000
# Documentación Swagger en http://localhost:8000/docs
```

### Desarrollo local
```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Correr la API
python main.py

# Correr tests
pytest tests/ -v
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/items` | Listar todos los items |
| `POST` | `/items` | Crear un item |
| `GET` | `/items/{id}` | Obtener un item |
| `DELETE` | `/items/{id}` | Eliminar un item |

### Ejemplo: Crear un item
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "MacBook Pro", "price": 2499.99}'
```

## Pipeline CI/CD

```
Push/PR a main → Lint (flake8) → Tests (pytest) → Build (Docker)
```

Si cualquier paso falla, los siguientes NO se ejecutan.

## Estructura del proyecto

```
reto/
├── .github/workflows/ci.yml    ← Pipeline CI/CD
├── docs/                        ← Notas de aprendizaje (Second Brain)
├── tests/test_main.py           ← Tests unitarios
├── main.py                      ← API FastAPI
├── dockerfile                   ← Multi-stage build
├── docker-compose.yml           ← App + PostgreSQL
└── requirements.txt             ← Dependencias
```

## Documentación de aprendizaje

- [Día 1: Cloud & IaC](docs/01-cloud-iac.md)
- [Día 2: Docker Avanzado](docs/02-docker-avanzado.md)
- [Día 3: Secret Management](docs/03-secret-management.md)
- [Día 4: CI/CD Testing](docs/04-cicd-testing.md)
- [Día 5: K8s & Networking](docs/05-k8s-networking.md)
- [Día 6: Second Brain](docs/06-second-brain.md)
- [Día 7: Checkpoint](docs/07-checkpoint.md)
- [Día 8: Clean Architecture & DI](docs/08-clean-architecture.md)
- [Día 9: Worker Pools](docs/09-worker-pools.md)
- [Día 10: Seguridad](docs/10-seguridad.md)
- [Día 11: Migraciones](docs/11-migraciones.md)
- [Día 12: TanStack Query](docs/12-tanstack-query.md)
- [Día 13: Error Handling](docs/13-error-handling.md)
- [Día 14: Fullstack Integración](docs/14-fullstack-integracion.md)
- [Día 15: Deploy Pipeline](docs/15-deploy.md)
- [Día 16: DB Performance & Indexes](docs/16-db-indexes.md)
- [Día 17: Observabilidad](docs/17-observabilidad.md)
- [Día 18: Redis Cache](docs/18-redis-cache.md)
