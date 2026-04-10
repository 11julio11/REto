# Día 15: Deploy Cloud Tradicional (AWS EC2) y SSL/HTTPS

Hemos consolidado y orquestado nuestra aplicación completa (Frontend React/Vite + Backend FastAPI + Base de Datos Postgres) dentro de `docker-compose.yml`, donde **Nginx** sirve como la puerta de entrada oficial (puerto 80).

## 🚀 Despliegue en AWS EC2 (Paso a Paso)

### 1. Lanzar el Servidor en AWS
1. Ingresa a la consola de AWS y ve a **EC2 -> Launch Instance**.
2. Selecciona **Ubuntu 22.04 LTS**.
3. En la configuración de red (Security Groups), asegúrate de permitir:
   - **HTTP (Puerto 80)**
   - **HTTPS (Puerto 443)**
   - **SSH (Puerto 22)**
4. Conéctate a tu instancia vía SSH usando tu llave `.pem`.

### 2. Preparar el Servidor
Actualiza el servidor e instala Git y Docker:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

> **Nota:** Cierra sesión (`exit`) y vuelve a entrar por SSH para que los permisos de Docker apliquen sin usar `sudo`.

### 3. Clonar y Lanzar la Aplicación
1. Clona tu repositorio de GitHub:
   ```bash
   git clone https://github.com/TuUsuario/TuRepositorio.git
   cd TuRepositorio
   ```

2. Levanta toda la infraestructura. Nginx construirá el Frontend y FastAPI hará build del backend automáticamente:
   ```bash
   docker compose up -d --build
   ```

A partir de este momento, si entras a la IP pública de tu EC2 en tu navegador (ej. `http://54.123.45.67`), verás el Frontend funcionando y comunicándose sin errores de CORS con tu Backend.

---

## 🔒 Certificado SSL / HTTPS (Let's Encrypt)
Para habilitar HTTPS y quitar la advertencia de "Sitio no seguro", necesitas un **Dominio**.

### 1. Apuntar el Dominio
Ve a la configuración de DNS donde compraste tu dominio (ej. Namecheap, GoDaddy) y crea un **Récord A**:
- **Host**: `@` o `www`
- **Value**: `La IP pública de tu servidor EC2`

### 2. Configurar Nginx para SSL
Existen muchas formas de configurar SSL con Docker. La más nativa para este entorno es usando un contenedor de Certbot de tipo envolvente (como nginx-proxy u obtenerlo localmente).

La vía más manual y didáctica es instalar **Certbot** nativamente en el EC2 y alterar ligeramente la configuración de Nginx (que por ahora sirve en el puerto 80).

```bash
sudo apt install certbot python3-certbot-nginx -y
```

Dado que Nginx corre incrustado dentro de nuestro contenedor llamado `web`, la opción más profesional es **Certbot-en-Docker** o simplemente exponer temporalmente nuestro Nginx. 

**Recomendación Avanzada (Caddy):** Un servidor moderno como **Caddy** automatiza el SSL sin necesidad de Certbot. En futuros días podrías reemplazar el contenedor actual de Nginx por uno de Caddy, donde tu `Caddyfile` solo necesitará 2 líneas:

```caddyfile
tudominio.com {
    reverse_proxy /api/* app:8000
    root * /usr/share/caddy
    file_server
}
```
Caddy manejará las renovaciones de Let's Encrypt él mismo sin que muevas un dedo.
