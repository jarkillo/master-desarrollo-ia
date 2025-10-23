# tests_integrations/conftest.py
"""
Configuración de pytest para tests de integración.

Agrega el directorio padre al path para imports correctos.
"""
import sys
from pathlib import Path

# Agregar el directorio padre al PYTHONPATH
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
