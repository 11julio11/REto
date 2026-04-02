# 🐳 Día 2: Docker Avanzado y Multi-stage Builds

## El problema con Docker tradicional

Cuando construyes una imagen de Docker copiando tu código base e instalando dependencias (por ejemplo, con `pip install` o `go build`), terminas con todo el entorno de desarrollo dentro de la imagen. 
Esto incluye compiladores, cabeceras, librerías que solo se usaron para crear un ejecutable, etc.

Una imagen de Python o Go puede pesar fácilmente **800 MB a 1 GB+**.
Esto genera:
- Tiempos muertos largos al descargar/subir (pull/push) imágenes.
- Mayor superficie de ataque (si un hacker entra al contenedor, encuentra herramientas listas para usar).
- Altas facturas en servicios Cloud.

## La Solución: Multi-stage Builds

Un *Multi-stage build* usa varias sentencias `FROM` en un solo archivo `dockerfile`. 
El truco es que cada instrucción `FROM` inicia un nuevo entorno (stage) y descarta el anterior, pero te permite **copiar** artefactos específicos (como un archivo compilado o dependencias de entorno virtual) de un *stage* previo.

### En la práctica (Python)

```dockerfile
# STAGE 1: Builder (Pesado: ~400MB+)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Se instala todo en un 'venv'
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . .

# STAGE 2: Runtime (Ligero: ~40-50MB) 
# Alpine es un Linux en miniatura
FROM python:3.11-alpine
WORKDIR /app
# Solo copiamos el entorno ya construido y el código necesario
COPY --from=builder /venv /venv
COPY --from=builder /app /app

ENV PATH="/venv/bin:$PATH"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Beneficios reales
1. **Seguridad**: Una imagen Alpine no tiene utilidades que los hackers adoran (curl, wget, gcc).
2. **Eficiencia**: Deployar una imagen de 50MB toma 3 segundos, una de 800MB toma minutos.
3. **Cache de Docker**: Al estructurar primero el copiado de `requirements.txt`/`go.mod` y luego correr dependencias, si cambias solo `main.py`, Docker usará caché y no volverá a descargar todos los paquetes.

## Conclusión

El objetivo no es que "funcione en mi máquina," sino que despliegue como en empresas top. Una imagen "gorda" grita "junior", una imagen destilada y optimizada demuestra conocimiento senior.
