# Día 20: Optimización de Costos — Aprende a Decir "No"

La habilidad más cara de un ingeniero no es saber usar Kubernetes. Es saber **cuándo NO usarlo**.

## 1. La Pregunta del Millón

> ¿Vale la pena un cluster de K8s para 100 usuarios?

**No.** Y aquí están los números para demostrarlo.

## 2. Análisis de Costos: Tu App (100 usuarios)

Nuestra app actual tiene 4 servicios: **Nginx + FastAPI + PostgreSQL + Redis**.

### Opción A: Kubernetes (EKS en AWS)

| Recurso                  | Costo Mensual (USD) |
|--------------------------|--------------------:|
| EKS Control Plane        |              $73.00 |
| 2× t3.medium (nodos)    |              $60.80 |
| ALB (Load Balancer)      |              $22.00 |
| EBS (almacenamiento)     |              $10.00 |
| NAT Gateway              |              $32.00 |
| **Total estimado**       |         **~$198/mes** |

Y eso **sin contar** las horas de tu tiempo configurando manifiestos YAML, Helm charts, service meshes, RBAC, monitoreo del cluster, actualizaciones de nodos...

### Opción B: Docker Compose en EC2

| Recurso               | Costo Mensual (USD) |
|------------------------|--------------------:|
| 1× t3.small (2GB RAM) |              $15.18 |
| EBS 20GB               |               $2.00 |
| IP Elástica            |               $3.65 |
| **Total estimado**     |          **~$21/mes** |

Exactamente lo que ya tenemos configurado con nuestro `docker-compose.yml`.

### Opción C: PaaS (Railway / Render / Fly.io)

| Recurso               | Costo Mensual (USD) |
|------------------------|--------------------:|
| App server (256MB-1GB) |           $5–$15.00 |
| PostgreSQL managed     |           $7–$20.00 |
| Redis add-on           |            $0–$5.00 |
| **Total estimado**     |        **~$15–$40/mes** |

Zero configuración de infraestructura. Deploy con `git push`.

### Resumen Visual

```
Costo mensual para 100 usuarios:

K8s (EKS)       ████████████████████████████████████████  ~$198
EC2 + Compose   ████                                      ~$21
PaaS            ███                                       ~$15-40

Complejidad operacional:

K8s (EKS)       ████████████████████████████████████████  Muy alta
EC2 + Compose   ████████████                              Media
PaaS            ████                                      Mínima
```

## 3. El Costo Oculto: Tu Tiempo

El recurso más caro no está en la factura de AWS. **Eres tú.**

| Tarea                              | EC2+Compose | K8s       |
|------------------------------------|:-----------:|:---------:|
| Setup inicial                      | 2 horas     | 2-3 días  |
| Deploy de un cambio                | 5 minutos   | 30+ min   |
| Debugging de un error de red       | Simple      | Pesadilla |
| Actualización del cluster          | N/A         | Un rito   |
| Documentación que necesitas leer   | Docker docs | Un libro  |

Si tu hora vale $20 USD y gastas 20 horas extra al mes manteniendo K8s, eso son **$400 adicionales** que no aparecen en la factura de AWS pero sí salen de tu productividad.

## 4. El Framework de Decisión: ¿Cuándo SÍ usar K8s?

```
                        ¿Tu app tiene más de 10,000 usuarios activos?
                                    │
                        ┌───── NO ──┴── SÍ ─────┐
                        │                        │
                        ▼                        ▼
                ¿Tienes un equipo            ¿Necesitas auto-escalado
                de DevOps/SRE?               y multi-región?
                        │                        │
                 ┌─ NO ─┴─ SÍ ─┐          ┌─ NO ─┴─ SÍ ─┐
                 │              │          │              │
                 ▼              ▼          ▼              ▼
            Docker Compose  Evalúa K8s  Docker Compose  ✅ K8s
            o PaaS          como opción  + Load Balancer
```

### Señales de que necesitas K8s:
- ✅ Más de 10,000 usuarios concurrentes
- ✅ Tienes un equipo de plataforma/DevOps dedicado
- ✅ Necesitas desplegar en múltiples regiones
- ✅ Tienes SLAs de 99.99% contractuales
- ✅ Manejas más de 10 microservicios

### Señales de que NO necesitas K8s:
- ❌ Menos de 1,000 usuarios
- ❌ Eres un equipo de 1-5 personas
- ❌ Es un monolito o pocos servicios (como nuestro proyecto)
- ❌ No tienes presupuesto para un SRE
- ❌ "Pero suena cool en el CV"

## 5. La Escala Correcta Para Nuestro Proyecto

Basado en lo que hemos construido en 19 días:

```
Día 1-14:   Código      → Clean Architecture, Workers, Auth, Migraciones
Día 15:     Deploy      → EC2 + Docker Compose ✅  (esto es suficiente)
Día 16-19:  Resiliencia → Observabilidad, Caché, Graceful Shutdown
Día 20:     Reflexión   → Saber que K8s existe, pero NO sobreingenierear
```

Nuestro stack actual (Docker Compose) ya tiene:
- **Health checks** (`HEALTHCHECK` en Docker, `livenessProbe` equivalente)
- **Restart automático** (`restart: unless-stopped`)
- **Logs estructurados** (JSON para Loki/ELK)
- **Métricas** (Prometheus-ready)
- **Graceful Shutdown** (SIGTERM handling)
- **Caché distribuida** (Redis)

Esto cubre el 95% de lo que K8s te da... para una fracción del costo.

## 6. ¿Cuándo Escalar? El Plan de Crecimiento

| Etapa           | Usuarios   | Infra Recomendada         | Costo/mes  |
|-----------------|:----------:|---------------------------|:----------:|
| MVP / Sideproject | 1-100    | PaaS (Railway, Fly.io)    | $15-40     |
| Startup temprana | 100-1,000 | EC2 + Docker Compose      | $20-50     |
| Crecimiento     | 1K-10K    | EC2 más grande + LB       | $50-200    |
| Escala real     | 10K+      | K8s (EKS/GKE) o ECS      | $200+      |

La clave: **escala cuando el dolor lo justifique**, no antes.

## 7. Conexión con Nuestro Proyecto

Lo que aprendimos de K8s (Día 5) no fue en vano. Los conceptos se aplican directamente:

| Concepto K8s         | Equivalente en nuestro proyecto           |
|----------------------|-------------------------------------------|
| Pod                  | Un contenedor en Docker Compose           |
| Service              | Red interna de Compose (DNS por nombre)   |
| Deployment replicas  | `docker compose up --scale app=3`         |
| livenessProbe        | `HEALTHCHECK` en Dockerfile               |
| ConfigMap / Secrets  | `secrets:` en Compose + archivos          |
| Ingress              | Nginx como reverse proxy                  |
| HPA (auto-escalado)  | ❌ No tenemos (y no lo necesitamos aún)   |

> [!IMPORTANT]
> La sobreingeniería mata más proyectos que la falta de escalabilidad. Empieza simple, mide, y escala solo cuando los datos lo exijan. Nuestro Docker Compose + EC2 a ~$21/mes es la decisión correcta para esta etapa.
