# tests/conftest.py
"""
Configuración de pytest para tests unitarios.

Este archivo agrega el directorio padre al path para que
los imports funcionen correctamente:
    from api.models import TareaModel  ✅
"""
import sys
from pathlib import Path

# Agregar el directorio padre al PYTHONPATH
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
