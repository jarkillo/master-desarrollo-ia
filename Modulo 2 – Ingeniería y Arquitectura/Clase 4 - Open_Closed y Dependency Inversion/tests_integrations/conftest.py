"""Configuración de pytest para tests de integración.

Este archivo se ejecuta antes de los tests y configura el path
para que Python encuentre el módulo 'api'.
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
directorio_raiz = Path(__file__).parent.parent
sys.path.insert(0, str(directorio_raiz))
