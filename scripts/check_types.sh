#!/bin/bash
# Script para verificar type hints con mypy

set -e

echo "🔍 Verificando type hints con mypy..."
echo ""

# Activar venv
source .venv/bin/activate

# Directorios a verificar
DIRS=(
    "Modulo 2 – Ingeniería y Arquitectura/Clase 6 - Integracion continua y control de calidad/api/"
    "Modulo 3 – Calidad y Seguridad/Clase 4 - Seguridad avanzada y autenticación con JWT/api/"
    "Modulo 4 - Infraestructura y Cloud/Clase 3 - Base de Datos con SQLAlchemy/api/"
)

echo "Verificando directorios:"
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    fi
done
echo ""

# Ejecutar mypy
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Verificando: $dir"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        mypy "$dir" || echo "⚠️  Errores encontrados en $dir"
        echo ""
    fi
done

echo "✅ Verificación completada"
