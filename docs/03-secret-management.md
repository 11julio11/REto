# 🔐 Día 3: Secret Management y Docker Compose

## El viejo error: usar el `.env` para todo

En tutoriales siempre verás cosas como:
```yaml
environment:
  - POSTGRES_PASSWORD=supersecreto123 
```
O simplemente mapeando un `env_file: .env` que acaba commiteado por accidente en GitHub.

¿El problema? Usar variables de entorno para todo lo sensible es un riesgo. Cualquier proceso dentro del contenedor puede leer estas variables. Cualquiera con acceso de lectura (con un simple `docker inspect mi-contenedor`) verá todas tus contraseñas en texto plano.

## Docker Secrets

*Docker Secrets* (y sus variantes en Swarm y K8s) permiten inyectar información de forma altamente segura. En lugar de exponer un string de entorno, Docker expone un **archivo de solo lectura temporalizado** dentro del contenedor montado generalmente en `/run/secrets/`.

### Configuración en `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:14
    environment:
      # Ya NO guardamos la contraseña directa, 
      # le decimos a postgres de qué archivo sacarla
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password 
    secrets:
      - db_password

secrets:
  db_password:
    # Esto apunta a un archivo local que debe estar 
    # listado en tu '.gitignore'
    file: ./db_password.txt
```

### ¿Cómo lo consume la aplicación?

El código de una aplicación profesional debe lidiar con la posible lectura mediante secretos. 

```python
# Ejemplo de cómo se leen:
def get_db_password():
    # 1. Intentamos leer desde secretos
    try:
        with open("/run/secrets/db_password", "r") as secret_file:
            return secret_file.read().strip()
    except IOError:
        pass
    
    # 2. Si no, leemos variable de entorno para fallback local
    return os.environ.get("DB_PASSWORD")
```

## Resiliencia y Healthchecks

Además de secretos, `docker-compose.yml` permite a los servicios "conversar" entre sí usando `depends_on`.
Es común que la API se inicie antes que la Base de Datos y termine crasheando (panicking en Go).

Para controlarlo no solo declaramos `depends_on: db`, sino `condition: service_healthy`:
Esto le dice a Docker: *"No corras mi API backend hasta que la Base de Datos Postgres no confirme que ya está lista y escuchando en el puerto 5432"*. Todo ello emparejado a las directivas `healthcheck` de las bases de datos.
