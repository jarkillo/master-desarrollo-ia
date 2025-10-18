#!/bin/bash
# Script para configurar Git hooks en el repositorio

echo "🔧 Setting up Git hooks..."
echo ""

# Verificar que estamos en el root del repo
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in repository root directory"
    exit 1
fi

# Configurar directorio de hooks personalizado
echo "📁 Configuring Git hooks directory..."
git config core.hooksPath .githooks

# Hacer el hook ejecutable (en sistemas Unix)
if [ -f ".githooks/pre-push" ]; then
    chmod +x .githooks/pre-push
    echo "✅ Made pre-push hook executable"
fi

echo ""
echo "✨ Git hooks configured successfully!"
echo ""
echo "Installed hooks:"
echo "  - pre-push: Runs linting and tests before push"
echo ""
echo "To bypass hooks (not recommended):"
echo "  git push --no-verify"
echo ""
echo "To run validation manually:"
echo "  bash scripts/pre-pr-check.sh"
echo ""
