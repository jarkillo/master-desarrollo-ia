#!/bin/bash
# Script de Rollback Automático
#
# PROPÓSITO:
# Hacer rollback a la última versión estable cuando algo falla en producción.
#
# USO:
#   ./scripts/rollback.sh
#
# PREREQUISITOS:
# 1. Railway CLI instalado (npm i -g @railway/cli)
# 2. RAILWAY_TOKEN configurado como variable de entorno
# 3. Repository usa tags semánticos (v1.0.0, v1.1.0, etc.)
# 4. API tiene endpoint /health
#
# EJEMPLO:
#   export RAILWAY_TOKEN="tu_token_de_railway"
#   ./scripts/rollback.sh

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# ============================================================================
# CONFIGURACIÓN (PERSONALIZA ESTOS VALORES)
# ============================================================================

# URL de health check (REEMPLAZAR con tu URL de Railway)
HEALTH_URL="${HEALTH_URL:-https://tu-api.railway.app/health}"

# Máximo de reintentos para health check
MAX_RETRIES=5

# Tiempo de espera entre reintentos (segundos)
RETRY_DELAY=10

# Tiempo de espera después de deploy (para que app arranque)
DEPLOY_WAIT=30

# ============================================================================
# FUNCIONES
# ============================================================================

# Función para imprimir mensajes con color
log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

log_warning() {
    echo -e "\033[0;33m[WARNING]\033[0m $1"
}

# Función para verificar prerrequisitos
check_prerequisites() {
    log_info "Verificando prerrequisitos..."

    # Verificar Railway CLI instalado
    if ! command -v railway &> /dev/null; then
        log_error "Railway CLI no está instalado."
        log_info "Instalar con: npm i -g @railway/cli"
        exit 1
    fi

    # Verificar RAILWAY_TOKEN configurado
    if [ -z "${RAILWAY_TOKEN:-}" ]; then
        log_error "RAILWAY_TOKEN no está configurado."
        log_info "Exportar con: export RAILWAY_TOKEN=\"tu_token\""
        exit 1
    fi

    # Verificar que estamos en un repositorio Git
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "No estás en un repositorio Git."
        exit 1
    fi

    log_success "Prerrequisitos OK"
}

# Función para encontrar última versión estable
find_last_stable_version() {
    log_info "Buscando última versión estable..."

    # Obtener tag actual (si existe)
    CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

    # Obtener todos los tags con formato v*.*.* , ordenados
    ALL_TAGS=$(git tag -l "v*.*.*" | sort -V)

    if [ -z "$ALL_TAGS" ]; then
        log_error "No se encontraron tags de versiones en el repositorio."
        log_info "Los tags deben seguir formato semántico: v1.0.0, v1.1.0, etc."
        exit 1
    fi

    # Si no hay tag actual, usar el último tag
    if [ -z "$CURRENT_TAG" ]; then
        LAST_STABLE=$(echo "$ALL_TAGS" | tail -n 1)
        log_warning "No hay tag actual, usando última versión: $LAST_STABLE"
    else
        # Obtener penúltima versión (excluir la actual)
        LAST_STABLE=$(echo "$ALL_TAGS" | grep -v "^$CURRENT_TAG$" | tail -n 1)

        if [ -z "$LAST_STABLE" ]; then
            log_error "No se encontró versión anterior a $CURRENT_TAG"
            log_info "No hay a dónde hacer rollback."
            exit 1
        fi

        log_info "Versión actual: $CURRENT_TAG"
    fi

    log_success "Versión de rollback: $LAST_STABLE"
    echo "$LAST_STABLE"
}

# Función para hacer checkout de versión
checkout_version() {
    local version=$1

    log_info "Haciendo checkout de $version..."

    # Guardar cambios no commiteados (si hay)
    if ! git diff-index --quiet HEAD --; then
        log_warning "Hay cambios sin commitear. Guardando stash..."
        git stash push -m "Rollback stash $(date +%Y-%m-%d_%H:%M:%S)"
    fi

    # Checkout del tag
    if git checkout "$version" 2>&1; then
        log_success "Checkout exitoso a $version"
        return 0
    else
        log_error "Fallo el checkout de $version"
        return 1
    fi
}

# Función para deployar a Railway
deploy_to_railway() {
    log_info "Iniciando deploy a Railway..."

    # Deploy con Railway CLI
    # --detach: No esperar a que termine (lo verificamos con health check)
    if railway up --detach; then
        log_success "Deploy iniciado en Railway"
        return 0
    else
        log_error "Fallo el deploy a Railway"
        return 1
    fi
}

# Función para health check con retries
health_check() {
    local url=$1
    local max_retries=$2
    local retry_delay=$3
    local retry_count=0

    log_info "Esperando ${DEPLOY_WAIT}s para que app arranque..."
    sleep "$DEPLOY_WAIT"

    log_info "Verificando health check: $url"

    while [ $retry_count -lt $max_retries ]; do
        retry_count=$((retry_count + 1))
        log_info "Intento $retry_count de $max_retries..."

        # Hacer request a health check
        # -f: Fallar en HTTP errors
        # -s: Silent (no mostrar progress bar)
        # --max-time 5: Timeout de 5 segundos
        if curl -f -s --max-time 5 "$url" > /dev/null 2>&1; then
            log_success "Health check OK! App está respondiendo."
            return 0
        fi

        if [ $retry_count -lt $max_retries ]; then
            log_warning "Health check falló. Reintentando en ${retry_delay}s..."
            sleep "$retry_delay"
        fi
    done

    log_error "Health check falló después de $max_retries intentos"
    return 1
}

# Función para notificar resultado
notify_result() {
    local success=$1
    local version=$2

    # Si hay webhook de Slack configurado, notificar
    if [ -n "${SLACK_WEBHOOK:-}" ]; then
        if [ "$success" = true ]; then
            curl -X POST "$SLACK_WEBHOOK" \
                -H 'Content-Type: application/json' \
                -d "{
                    \"text\": \"✅ Rollback exitoso a \`$version\`\",
                    \"blocks\": [{
                        \"type\": \"section\",
                        \"text\": {
                            \"type\": \"mrkdwn\",
                            \"text\": \"*Rollback Completado*\n• Versión: \`$version\`\n• Estado: ✅ Healthy\n• Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)\"
                        }
                    }]
                }" 2>/dev/null || true
        else
            curl -X POST "$SLACK_WEBHOOK" \
                -H 'Content-Type: application/json' \
                -d "{
                    \"text\": \"❌ Rollback falló\",
                    \"blocks\": [{
                        \"type\": \"section\",
                        \"text\": {
                            \"type\": \"mrkdwn\",
                            \"text\": \"*Rollback Falló*\n• Versión objetivo: \`$version\`\n• Estado: ❌ Health check no pasó\n• Acción requerida: Investigación manual\"
                        }
                    }]
                }" 2>/dev/null || true
        fi
    fi
}

# ============================================================================
# MAIN SCRIPT
# ============================================================================

main() {
    echo "============================================"
    echo "🔄 SCRIPT DE ROLLBACK AUTOMÁTICO"
    echo "============================================"
    echo ""

    # 1. Verificar prerrequisitos
    check_prerequisites

    # 2. Encontrar última versión estable
    LAST_STABLE=$(find_last_stable_version)

    # 3. Confirmación (opcional, comentar para rollback automático)
    echo ""
    read -p "¿Confirmas rollback a $LAST_STABLE? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Rollback cancelado por el usuario."
        exit 0
    fi

    # 4. Checkout de versión
    if ! checkout_version "$LAST_STABLE"; then
        log_error "Fallo al hacer checkout. Abortando rollback."
        exit 1
    fi

    # 5. Deploy a Railway
    if ! deploy_to_railway; then
        log_error "Fallo al deployar. Abortando rollback."
        exit 1
    fi

    # 6. Health check
    if health_check "$HEALTH_URL" "$MAX_RETRIES" "$RETRY_DELAY"; then
        log_success "✅ ROLLBACK EXITOSO!"
        log_info "App corriendo en versión: $LAST_STABLE"
        log_info "Health check: OK"
        notify_result true "$LAST_STABLE"
        exit 0
    else
        log_error "❌ ROLLBACK FALLÓ!"
        log_error "Health check no pasó después de $MAX_RETRIES intentos."
        log_warning "Requiere investigación manual."
        notify_result false "$LAST_STABLE"
        exit 1
    fi
}

# Ejecutar main
main

# ============================================================================
# EJEMPLO DE USO
# ============================================================================
#
# 1. Configurar variables de entorno:
#    export RAILWAY_TOKEN="tu_railway_token"
#    export HEALTH_URL="https://tu-api.railway.app/health"
#    export SLACK_WEBHOOK="https://hooks.slack.com/..." (opcional)
#
# 2. Ejecutar script:
#    ./scripts/rollback.sh
#
# 3. Confirmar rollback cuando se pida
#
# ============================================================================
# PARA ROLLBACK AUTOMÁTICO (SIN CONFIRMACIÓN)
# ============================================================================
#
# Comentar líneas 163-169 (la sección de confirmación)
# Útil para automatizar rollback en workflows de CI/CD
#
# ============================================================================
