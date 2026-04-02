# 🏁 Día 7: Checkpoint — API Containerizada con Pipeline CI/CD

## Objetivo cumplido

> "API containerizada con un pipeline que valida tests antes de permitir el merge."

## Arquitectura del Pipeline

```
Push a main / Pull Request
         │
         ▼
┌─────────────────┐
│   1. LINT       │  flake8 — errores de sintaxis bloquean
│   (flake8)      │  warnings de estilo no bloquean
└────────┬────────┘
         │ ✅ Pasa
         ▼
┌─────────────────┐
│   2. TEST       │  pytest — 12 tests unitarios
│   (pytest)      │  CRUD completo + edge cases
└────────┬────────┘
         │ ✅ Pasa
         ▼
┌─────────────────┐
│   3. BUILD      │  docker build — imagen multi-stage
│   (Docker)      │  Solo buildea si tests pasan
└─────────────────┘
```

## Decisiones técnicas

### ¿Por qué FastAPI?
- Validación automática con Pydantic (no tienes que validar manualmente cada campo).
- Documentación automática en `/docs` (Swagger UI).
- Async-ready para cuando escalemos.
- Tipado fuerte = menos bugs.

### ¿Por qué Multi-stage Docker?
- Stage 1 (builder): instala dependencias con `pip`. Imagen pesada pero solo se usa para compilar.
- Stage 2 (runtime): Alpine base. Solo copia el virtualenv y el código. Resultado: ~40MB vs ~800MB.

### ¿Por qué secrets en Docker Compose?
- Las contraseñas NO están en variables de entorno visibles con `docker inspect`.
- Se montan como archivos en `/run/secrets/` dentro del contenedor.
- `db_password.txt` está en `.gitignore`, nunca llega al repo.

### ¿Por qué pipeline con dependencias (needs)?
- `lint` → `test` → `build`: cada paso **depende** del anterior.
- Si el linter encuentra un error de sintaxis, no se gastan recursos corriendo tests.
- Si un test falla, no se construye la imagen (no queremos deployar código roto).

## Estructura del proyecto

```
reto/
├── .github/workflows/ci.yml    ← Pipeline: lint → test → build
├── docs/
│   ├── dia1-cloud-iac.md       ← Notas: Qué es IaC y Terraform
│   ├── dia5-k8s-networking.md  ← Notas: Pods, Services, Ingress
│   └── dia7-checkpoint.md      ← Este archivo
├── tests/
│   └── test_main.py            ← 12 tests unitarios
├── .gitignore                  ← Seguridad: ignora secretos
├── README.md                   ← Cómo correr el proyecto
├── main.py                     ← API FastAPI (CRUD items)
├── requirements.txt            ← Dependencias pinned
├── dockerfile                  ← Multi-stage build
├── docker-compose.yml          ← App + PostgreSQL con secrets
└── db_password.txt             ← Secreto local (NO en git)
```

## Endpoints de la API

| Método | Ruta | Descripción | Status |
|--------|------|-------------|--------|
| GET | `/` | Health check | 200 |
| GET | `/items` | Listar items | 200 |
| POST | `/items` | Crear item | 201 |
| GET | `/items/{id}` | Obtener item | 200 / 404 |
| DELETE | `/items/{id}` | Eliminar item | 204 / 404 |

## Qué viene en Semana 2

- [ ] Migrar de "DB en memoria" a PostgreSQL real con migraciones.
- [ ] Agregar autenticación (JWT + Refresh Tokens).
- [ ] Clean Architecture con Dependency Injection.
- [ ] Frontend con React + TanStack Query.
