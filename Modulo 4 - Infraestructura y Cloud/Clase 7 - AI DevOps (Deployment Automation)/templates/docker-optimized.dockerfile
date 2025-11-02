# Dockerfile Optimizado para CI/CD
#
# Este Dockerfile aplica mejores prácticas:
# ✅ Multi-stage build (imagen pequeña)
# ✅ Layer caching efectivo (builds rápidos)
# ✅ Non-root user (seguridad)
# ✅ Health check incluido
# ✅ Optimizado para Railway/Fly.io
#
# RESULTADO ESPERADO:
# - Build time: <2 minutos (con cache)
# - Image size: ~100-150MB (vs 400MB+ sin optimizar)

# ============================================================================
# STAGE 1: BUILDER
# Instala dependencias en un ambiente temporal
# ============================================================================
FROM python:3.12-slim AS builder

# Etiquetas para metadata
LABEL maintainer="tu@email.com"
LABEL description="API de Tareas con FastAPI"

# Directorio de trabajo
WORKDIR /app

# CRÍTICO: Copiar requirements.txt PRIMERO (antes que el código)
# Razón: Si requirements.txt no cambia, Docker reutiliza cache
# y no reinstala dependencias (ahorra ~80% del tiempo de build)
COPY requirements.txt .

# Instalar dependencias en directorio de usuario
# --user: Instala en ~/.local (no requiere root)
# --no-cache-dir: No guarda cache de pip (ahorra ~50MB)
# --no-warn-script-location: Silencia warnings innecesarios
#
# ⚠️ SEGURIDAD: Si requirements.txt contiene URLs con tokens privados:
# git+https://${TOKEN}@github.com/private/repo.git
#
# El token puede aparecer en logs del build. Para evitarlo:
# Opción 1: Usar BuildKit secrets (ver ejemplo al final del archivo)
# Opción 2: Usar .netrc file con credentials
# Opción 3: Redirigir stderr para ocultar URLs: 2>&1 | grep -v "http"
RUN pip install --user --no-cache-dir --no-warn-script-location \
    -r requirements.txt

# ============================================================================
# STAGE 2: PRODUCTION
# Imagen final con solo lo necesario para correr la app
# ============================================================================
FROM python:3.12-slim

# Instalar curl para health check
# --no-install-recommends: No instala paquetes sugeridos (ahorra ~30MB)
# rm -rf /var/lib/apt/lists/*: Limpia cache de apt (ahorra ~10MB)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario no-root (seguridad)
# -m: Crear home directory
# -u 1000: User ID (estándar para primer usuario)
RUN useradd -m -u 1000 appuser

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde builder (solo lo necesario)
# Esto evita tener compiladores, headers, etc. en imagen final
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código de la aplicación
# --chown: El usuario appuser debe ser dueño de los archivos
COPY --chown=appuser:appuser . .

# Añadir .local/bin al PATH (donde están los ejecutables de pip)
ENV PATH=/home/appuser/.local/bin:$PATH

# Cambiar a usuario no-root (no correr como root NUNCA)
USER appuser

# Puerto que expone la aplicación
EXPOSE 8000

# Health check (Railway/Docker usa esto para verificar que app está OK)
# --interval=30s: Verificar cada 30 segundos
# --timeout=10s: Esperar máximo 10 segundos por respuesta (tolerante a carga)
# --start-period=30s: Esperar 30s antes del primer check (app necesita tiempo para arrancar, migraciones, etc.)
# --retries=3: Marcar como unhealthy después de 3 fallos consecutivos
#
# NOTA: start-period de 30s previene restart loops cuando app tarda en arrancar
# (migraciones de DB, warm-up de conexiones, etc.)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Comando para iniciar la aplicación
# --host 0.0.0.0: Escuchar en todas las interfaces (necesario para Docker)
# --port 8000: Puerto (debe coincidir con EXPOSE)
# --workers 1: Un worker por defecto (Railway/Fly escalan horizontalmente)
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]

# ============================================================================
# OPCIONAL: Configuración para producción
# ============================================================================
# Si necesitas múltiples workers o configuración específica,
# descomenta y ajusta:

# Production-ready con Gunicorn + Uvicorn workers
# CMD ["gunicorn", "api.api:app", \
#      "--workers", "4", \
#      "--worker-class", "uvicorn.workers.UvicornWorker", \
#      "--bind", "0.0.0.0:8000", \
#      "--access-logfile", "-", \
#      "--error-logfile", "-"]

# ============================================================================
# CÓMO USAR ESTE DOCKERFILE
# ============================================================================
#
# BUILD:
#   docker build -t api-tareas .
#
# RUN LOCAL:
#   docker run -p 8000:8000 api-tareas
#
# TEST HEALTH CHECK:
#   docker ps  # Verificar que status es "healthy" (tarda ~35 segundos)
#
# ============================================================================
# TROUBLESHOOTING
# ============================================================================
#
# PROBLEMA: Build tarda mucho
# SOLUCIÓN: Verifica que requirements.txt esté antes de COPY del código
#
# PROBLEMA: Imagen muy grande (>300MB)
# SOLUCIÓN: Verifica que estés usando python:3.12-slim (no python:3.12)
#
# PROBLEMA: Health check falla
# SOLUCIÓN: Asegúrate de tener endpoint /health en tu API
#
# PROBLEMA: Permiso denegado al escribir archivos
# SOLUCIÓN: Verifica que appuser tenga permisos (--chown en COPY)
#
# ============================================================================
# OPTIMIZACIONES APLICADAS
# ============================================================================
#
# ✅ Multi-stage build: Imagen final no incluye compiladores
# ✅ Layer caching: requirements.txt copiado antes que código
# ✅ Slim base image: python:3.12-slim (~150MB vs python:3.12 ~900MB)
# ✅ --no-cache-dir: No guarda cache de pip (~50MB ahorrados)
# ✅ No root user: Seguridad (usuario appuser)
# ✅ Health check: Railway/Docker detecta crashes automáticamente (30s start-period)
# ✅ Cleanup apt: rm -rf /var/lib/apt/lists/* (~10MB ahorrados)
#
# RESULTADO:
# - Build time: ~1.5 min (con cache: ~15 segundos!)
# - Image size: ~120MB (vs ~450MB sin optimizar)
# - Security: ✅ Non-root user
# - Reliability: ✅ Health checks (tolerante a startup lento)
#
# ============================================================================
# EJEMPLO AVANZADO: BuildKit Secrets para Dependencias Privadas
# ============================================================================
#
# Si requirements.txt contiene dependencias privadas con tokens,
# usa BuildKit secrets para evitar leaks en logs:
#
# # syntax=docker/dockerfile:1.4
# FROM python:3.12-slim AS builder
# WORKDIR /app
# COPY requirements.txt .
#
# # Usar secret mount (no queda en imagen ni en logs)
# RUN --mount=type=secret,id=github_token \
#     export GITHUB_TOKEN=$(cat /run/secrets/github_token) && \
#     pip install --user --no-cache-dir -r requirements.txt
#
# Luego en GitHub Actions:
#
# - name: Build Docker image with secrets
#   uses: docker/build-push-action@v5
#   with:
#     context: .
#     secrets: |
#       github_token=${{ secrets.GH_TOKEN }}
#
# O en CLI local:
#
# docker buildx build --secret id=github_token,src=~/.secrets/github_token .
#
# ============================================================================
