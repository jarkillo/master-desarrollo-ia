"""
Configuración de pytest para tests de tools.

Añade el directorio padre a sys.path para poder importar el módulo api.
"""

import sys
from pathlib import Path

# Añadir directorio padre a sys.path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
