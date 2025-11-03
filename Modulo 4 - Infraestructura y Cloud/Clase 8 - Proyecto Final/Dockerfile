# =================================
# Stage 1: Builder
# =================================
FROM python:3.12-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# =================================
# Stage 2: Runtime
# =================================
FROM python:3.12-slim

WORKDIR /app

# Instalar solo las librerías de runtime necesarias
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas desde el builder
COPY --from=builder /root/.local /root/.local

# Asegurar que los scripts en .local están en PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar el código de la aplicación
COPY ./api ./api
COPY ./alembic ./alembic
COPY alembic.ini .

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando por defecto
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
