# Dockerfile
# Multi-stage build optimizado para producción
#
# Ventajas de multi-stage:
# - Imagen final más pequeña (solo runtime, sin build tools)
# - Builds más rápidos (cachea layers)
# - Más seguro (menos superficie de ataque)
#
# Tamaño aproximado: ~150MB (vs 1GB+ sin multi-stage)

# ==============================================================================
# STAGE 1: Builder
# ==============================================================================
FROM python:3.12-slim as builder

# Metadata
LABEL maintainer="tu-email@example.com"
LABEL description="API de Tareas - Build stage"

# Instalar dependencias de sistema necesarias para compilar
# (psycopg2 necesita gcc, postgresql-dev, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /build

# Copiar solo requirements.txt primero (para cachear layer)
COPY requirements.txt .

# Instalar dependencias en un directorio temporal
# --no-cache-dir: No guardar cache de pip (reduce tamaño)
# --user: Instala en ~/.local (fácil de copiar al stage final)
RUN pip install --no-cache-dir --user -r requirements.txt

# ==============================================================================
# STAGE 2: Runtime (Imagen final)
# ==============================================================================
FROM python:3.12-slim

# Metadata
LABEL maintainer="tu-email@example.com"
LABEL description="API de Tareas - Production ready"
LABEL version="1.0.0"

# Instalar solo las dependencias runtime necesarias
# (psycopg2 necesita libpq en runtime, pero NO gcc)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario non-root (seguridad)
# NUNCA correr aplicaciones como root en producción
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Asegurarse de que los binarios en ~/.local/bin están en PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copiar código de la aplicación
COPY --chown=appuser:appuser api/ ./api/
COPY --chown=appuser:appuser requirements.txt .

# Cambiar a usuario non-root
USER appuser

# Exponer puerto (Railway y Render lo detectan automáticamente)
EXPOSE 8000

# Health check (Docker puede verificar si el container está sano)
# Cada 30s, después de 30s inicial, timeout 10s, 3 reintentos
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Variables de entorno por defecto (se pueden overridear)
ENV ENVIRONMENT=prod
ENV HOST=0.0.0.0
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Comando para iniciar la aplicación
# --host 0.0.0.0: Permite conexiones externas (necesario en cloud)
# --port $PORT: Railway y Render asignan el puerto dinámicamente
# --workers 2: Múltiples workers para concurrencia (ajustar según RAM)
# --timeout-keep-alive 120: Mantiene conexiones abiertas (útil para load balancers)
CMD uvicorn api.api:app \
    --host $HOST \
    --port $PORT \
    --workers 2 \
    --timeout-keep-alive 120 \
    --access-log
