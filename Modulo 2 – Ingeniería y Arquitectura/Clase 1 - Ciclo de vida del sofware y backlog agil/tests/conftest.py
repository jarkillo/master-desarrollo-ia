# tests/conftest.py
"""
Configuración de pytest para los tests de la API.

Este archivo configura sys.path para que pytest pueda importar
el módulo 'api' correctamente.
"""

import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al path de Python
raiz_proyecto = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(raiz_proyecto))
