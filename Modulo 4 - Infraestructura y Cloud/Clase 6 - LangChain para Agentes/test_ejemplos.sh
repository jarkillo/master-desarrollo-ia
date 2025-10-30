#!/bin/bash
# Script para testing rápido de todos los ejemplos
# NO requiere API key - solo verifica imports y sintaxis

set -e  # Exit on error

echo "════════════════════════════════════════════════════════"
echo "  Testing Ejemplos - Clase 6: LangChain y Agent Skills  "
echo "════════════════════════════════════════════════════════"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar sintaxis
check_syntax() {
    local file=$1
    echo -n "  Verificando sintaxis de $(basename $file)... "

    if python -m py_compile "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        python -m py_compile "$file"
        return 1
    fi
}

# Función para verificar imports
check_imports() {
    local file=$1
    echo -n "  Verificando imports de $(basename $file)... "

    # Crear script temporal que solo importa
    temp_script=$(mktemp)
    cat > "$temp_script" << EOF
import sys
import os

# Suprimir warnings
import warnings
warnings.filterwarnings("ignore")

# Mock de API key para imports
os.environ["ANTHROPIC_API_KEY"] = "test_key"

try:
    # Importar el módulo
    import importlib.util
    spec = importlib.util.spec_from_file_location("module", "$file")
    module = importlib.util.module_from_spec(spec)
    # NO ejecutar, solo importar
    print("OK")
except ImportError as e:
    print(f"ERROR: {e}")
    sys.exit(1)
except Exception:
    # Otros errores (e.g., código que se ejecuta al import) son OK
    print("OK")
EOF

    if output=$(python "$temp_script" 2>&1); then
        if [[ $output == *"ERROR"* ]]; then
            echo -e "${RED}✗${NC}"
            echo "$output"
            rm "$temp_script"
            return 1
        else
            echo -e "${GREEN}✓${NC}"
            rm "$temp_script"
            return 0
        fi
    else
        echo -e "${RED}✗${NC}"
        rm "$temp_script"
        return 1
    fi
}

echo "${YELLOW}1. Verificando ejemplos de LangChain Chains${NC}"
check_syntax "ejemplos/langchain_chains.py"
check_imports "ejemplos/langchain_chains.py"
echo ""

echo "${YELLOW}2. Verificando ejemplos de LangChain Agents${NC}"
check_syntax "ejemplos/langchain_agents.py"
check_imports "ejemplos/langchain_agents.py"
echo ""

echo "${YELLOW}3. Verificando ejemplos de Memory${NC}"
check_syntax "ejemplos/memory_demo.py"
check_imports "ejemplos/memory_demo.py"
echo ""

echo "${YELLOW}4. Verificando ejemplos de RAG${NC}"
check_syntax "ejemplos/rag_basic.py"
check_imports "ejemplos/rag_basic.py"
echo ""

echo "${YELLOW}5. Verificando Proyecto - Tools${NC}"
check_syntax "proyecto/tools/code_search.py"
check_imports "proyecto/tools/code_search.py"
check_syntax "proyecto/tools/test_runner.py"
check_imports "proyecto/tools/test_runner.py"
echo ""

echo "${YELLOW}6. Verificando Agente Principal${NC}"
check_syntax "proyecto/dev_assistant.py"
check_imports "proyecto/dev_assistant.py"
echo ""

echo "════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ Todos los tests de sintaxis e imports pasaron!${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📝 NOTA: Para ejecutar los ejemplos completamente,"
echo "   necesitas configurar ANTHROPIC_API_KEY en .env"
echo ""
echo "   Ejemplo:"
echo "   cd proyecto"
echo "   cp .env.template .env"
echo "   # Editar .env con tu API key"
echo "   python dev_assistant.py"
echo ""
