# ☸️ Día 5: Kubernetes Conceptual + Networking

## ¿Qué es Kubernetes (K8s)?

Un **orquestador de contenedores**. Si Docker es como un barco, K8s es el puerto que decide:
- Cuántos barcos (contenedores) necesitas.
- Dónde ponerlos.
- Qué hacer si uno se hunde (reiniciarlo).

## Conceptos clave

### Pod
- La unidad mínima de K8s. Un pod = 1 o más contenedores que comparten red.
- Tu API correría dentro de un pod.

```yaml
# Ejemplo mental de un Pod
apiVersion: v1
kind: Pod
metadata:
  name: reto-api
spec:
  containers:
    - name: api
      image: reto-api:latest
      ports:
        - containerPort: 8000
```

### Service
- Un **Service** da una dirección estable al pod. Los pods mueren y renacen, pero el Service mantiene la misma IP interna.
- Tipos: `ClusterIP` (interno), `NodePort` (expone un puerto), `LoadBalancer` (expone al mundo).

### Ingress
- El "portero" que recibe tráfico de Internet y lo manda al Service correcto.
- Maneja rutas: `/api` → Service A, `/admin` → Service B.

## Flujo de una petición HTTP en K8s

```
Internet → Load Balancer → Ingress → Service → Pod(s) → Container
```

```
[Usuario] 
    │
    ▼
[Load Balancer]  ← Distribye tráfico entre nodos
    │
    ▼
[Ingress]        ← Enruta por URL (api.miapp.com → Service API)
    │
    ▼
[Service]        ← IP estable que apunta a los pods
    │
    ├──▶ [Pod 1: API]  ← Réplica 1
    ├──▶ [Pod 2: API]  ← Réplica 2
    └──▶ [Pod 3: API]  ← Réplica 3
```

### Deployment
- Controla cuántas réplicas de tu pod corren. Si pides 3, K8s mantiene siempre 3.
- Si un pod muere, K8s crea otro automáticamente.

### Namespace
- Aísla recursos. Ejemplo: `dev`, `staging`, `production` pueden tener pods con el mismo nombre sin conflicto.

## ¿K8s vs Docker Compose?

| Aspecto | Docker Compose | Kubernetes |
|---------|---------------|------------|
| Dónde se usa | Desarrollo local, staging | Producción a escala |
| Escalado | Manual | Automático (HPA) |
| Recuperación | Restart policy básico | Self-healing completo |
| Complejidad | Baja | Alta |
| Cuándo usarlo | <1000 usuarios | >1000 usuarios o SLA exigente |

## ¿Necesito K8s para este proyecto?

**No todavía.** Para 100-1000 usuarios, Docker Compose o un PaaS (Railway, Fly.io) es suficiente. K8s es para cuando necesitas:
- Auto-escalado basado en tráfico.
- Zero-downtime deployments.
- Multi-región.

> **Regla del Día 20**: No sobreingenierees. Saber K8s conceptualmente te hace mejor ingeniero, pero usarlo sin necesidad te hace peor.

## Conexión con este proyecto

- Nuestro `docker-compose.yml` es como un "mini K8s" para desarrollo.
- El `HEALTHCHECK` del Dockerfile es el equivalente a los `livenessProbe`/`readinessProbe` de K8s.
- En Semana 3, si desplegamos en cloud, podríamos usar K8s o un servicio más simple.
