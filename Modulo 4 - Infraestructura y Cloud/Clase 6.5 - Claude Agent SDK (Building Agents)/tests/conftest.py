"""
Configuración de pytest para tests de Clase 6.5

Añade el directorio padre al path para permitir imports
"""

import sys
from pathlib import Path

# Añadir directorio padre al path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
