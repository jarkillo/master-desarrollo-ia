# tests/conftest.py
"""
Configuración de tests con pytest.

Agrega el directorio padre al path para imports.
"""
import sys
from pathlib import Path

# Agregar directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))
