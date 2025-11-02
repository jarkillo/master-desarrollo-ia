"""
Configuración de pytest para tests async
"""

import sys
from pathlib import Path

# Agregar directorio padre al path para imports
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))
