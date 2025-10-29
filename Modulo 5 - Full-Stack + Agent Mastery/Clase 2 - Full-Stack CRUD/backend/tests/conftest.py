"""
Configuración de pytest para tests del backend.
"""
import sys
from pathlib import Path

# Agregar directorio padre al path para imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
