# tests_integrations/conftest.py
"""
Configuración para pytest de tests de integración.

Agrega el directorio padre al path para importar el módulo api.
"""
import sys
from pathlib import Path

# Añadir el directorio padre al path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
