#!/bin/bash
# Script de validación completa antes de crear Pull Request
# Ejecuta todas las validaciones que se ejecutarían en CI

set -e

echo "🚀 Pre-PR Validation Script"
echo "================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

error() { echo -e "${RED}❌ $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Verificar que estamos en el root del repo
if [ ! -d ".git" ]; then
    error "Not in repository root directory"
    exit 1
fi

VALIDATION_FAILED=false

# 1. Git status
echo "📊 Git Status"
echo "--------------------------------"
git status -s
echo ""

# 2. Branch info
CURRENT_BRANCH=$(git branch --show-current)
info "Current branch: $CURRENT_BRANCH"
echo ""

# 3. Ruff linting
echo "📝 Running Ruff Linting"
echo "--------------------------------"
if command -v ruff &> /dev/null || python -m ruff --version &> /dev/null; then
    if python -m ruff check .; then
        success "Ruff linting passed"
    else
        error "Ruff linting failed"
        VALIDATION_FAILED=true
    fi
else
    warning "Ruff not installed. Install with: pip install ruff"
    VALIDATION_FAILED=true
fi
echo ""

# 4. Tests con coverage en todas las clases
echo "🧪 Running Tests with Coverage"
echo "--------------------------------"

CLASS_DIRS=(
    "Modulo 4 - Infraestructura y Cloud/Clase 2 - Tu API en un contenedor"
)

for class_dir in "${CLASS_DIRS[@]}"; do
    if [ -d "$class_dir/tests" ]; then
        echo ""
        info "Testing: $class_dir"

        cd "$class_dir"

        # Limpiar cachés
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true

        # Ejecutar tests
        if python -m pytest --cov=api --cov-report=term-missing --cov-fail-under=80; then
            success "Tests passed in $class_dir"
        else
            error "Tests failed in $class_dir"
            VALIDATION_FAILED=true
        fi

        cd - > /dev/null
    fi
done
echo ""

# 5. Bandit security audit
echo "🔒 Security Audit (Bandit)"
echo "--------------------------------"
if python -m bandit --version &> /dev/null; then
    for class_dir in "${CLASS_DIRS[@]}"; do
        if [ -d "$class_dir/api" ]; then
            info "Auditing: $class_dir"
            if python -m bandit -r "$class_dir/api/" -ll; then
                success "Security audit passed for $class_dir"
            else
                error "Security issues found in $class_dir"
                VALIDATION_FAILED=true
            fi
        fi
    done
else
    warning "Bandit not installed. Install with: pip install bandit"
fi
echo ""

# 6. Gitleaks (secret scanning)
echo "🔐 Secret Scanning (Gitleaks)"
echo "--------------------------------"
if command -v gitleaks &> /dev/null; then
    if gitleaks detect --no-git; then
        success "No secrets detected"
    else
        error "Secrets detected!"
        VALIDATION_FAILED=true
    fi
else
    warning "gitleaks not installed"
    warning "Install from: https://github.com/gitleaks/gitleaks#installing"
fi
echo ""

# 7. Environment validation (si existe)
echo "⚙️  Environment Validation"
echo "--------------------------------"
for class_dir in "${CLASS_DIRS[@]}"; do
    if [ -f "$class_dir/infra/check_env.py" ]; then
        info "Validating env for: $class_dir"
        if python "$class_dir/infra/check_env.py"; then
            success "Environment validation passed"
        else
            error "Environment validation failed"
            VALIDATION_FAILED=true
        fi
    fi
done
echo ""

# Resumen final
echo "================================"
if [ "$VALIDATION_FAILED" = true ]; then
    error "VALIDATION FAILED"
    echo ""
    echo "Fix the errors above before creating a PR"
    exit 1
else
    success "ALL VALIDATIONS PASSED! ✨"
    echo ""
    echo "You can safely create a Pull Request now"
    echo "Use: gh pr create"
    exit 0
fi
