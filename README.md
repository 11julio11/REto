# ⚡ REto: Subscription Manager (Día 30)

¡Bienvenido al resultado final del **Reto T-Shaped Engineer**! Este proyecto ha evolucionado de una simple lista de items a un **Gestor de Suscripciones** profesional, optimizado para el usuario y con una infraestructura robusta.

## 🚀 Características Finales

-   **UX Senior (Día 25)**: Flujo de registro con **Auto-Login** inmediato. Menos clics para el usuario.
-   **Diseño Premium**: Interfaz moderna con temática **Indigo/Slate**, sombras suaves y responsive design.
-   **Dashboard de Métricas (Día 27)**: Cálculo automático de gasto mensual estimado y control de suscripciones activas.
-   **IA Copilot Avanzado (Día 26)**: Cobertura de tests del 70% enfocada en casos de borde (edge cases) y seguridad.
-   **Arquitectura Limpia (Clean Architecture)**: Separación clara entre Dominio, Servicios y Repositorios.

## 🏗️ Arquitectura Técnica

El sistema utiliza un enfoque de **Capas** para permitir la escalabilidad y el intercambio de componentes (ej: cambiar la base de datos en memoria por PostgreSQL sin tocar la lógica de negocio).

```mermaid
graph TD
    subgraph Frontend (React + Vite)
        UI[Componentes UI] --> TanStack[TanStack Query]
        TanStack --> Axios[Axios API Client]
    end

    subgraph Backend (FastAPI)
        Axios --> Router[API Routers]
        Router --> Service[Subscription Service]
        Service --> Domain[Domain Schemas]
        Service --> Repository[Repository Interface]
        Repository --> MemoryDB[(Memory DB / Postgres)]
    end

    subgraph Infrastructura
        Service --> Redis[(Redis Cache)]
        Service --> Workers[Background Workers]
    end
```

## 🛠️ Decisiones Técnicas Clave

1.  **FastAPI + Pydantic**: Para una validación de datos ultrarrápida y documentación automática (Swagger).
2.  **TanStack Query**: Manejo de estado asíncrono y caché en el frontend para una experiencia fluida.
3.  **Inyección de Dependencias**: Facilita el testing y desacopla la infraestructura del negocio.
4.  **Repositorio Cacheado**: Implementación de un patrón *Decorator* sobre el repositorio para integrar Redis de forma transparente.

## 🧪 Pruebas y Robustez

Se ha implementado una estrategia de testing que cubre:
-   Autenticación (Login, Registro, Refresh).
-   Casos de borde en CRUD de suscripciones (IDs inválidos, campos faltantes).
-   Seguridad de rutas protegidas.

---
*Este proyecto es el cierre del reto de 30 días para forjar un perfil T-Shaped Engineer.*
