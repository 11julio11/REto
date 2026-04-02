# ────────────────────────────────────────────────────
# Multi-Stage Build — Día 2: Docker Avanzado
# Stage 1 (builder): instala dependencias pesadas
# Stage 2 (runtime): imagen mínima con Alpine (~40MB)
# ────────────────────────────────────────────────────

# Stage 1: build
FROM python:3.11-slim AS builder
WORKDIR /app

# Copiamos primero requirements para aprovechar la cache de Docker
COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Stage 2: runtime (imagen final ligera)
FROM python:3.11-alpine
WORKDIR /app

# Copiamos el entorno virtual y el código desde el builder
COPY --from=builder /venv /venv
COPY --from=builder /app /app

# Ajustamos el PATH para usar el virtualenv
ENV PATH="/venv/bin:$PATH"

# Puerto de la API
EXPOSE 8000

# Healthcheck: verifica que la API responde
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Ejecutar con Uvicorn (servidor ASGI profesional)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]