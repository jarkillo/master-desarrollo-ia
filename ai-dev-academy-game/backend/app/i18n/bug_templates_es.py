"""Bug Hunt - Plantillas de bugs en Español."""

from typing import Dict, List, Any

# Traducciones de bug templates en Español
BUG_TEMPLATES_ES: Dict[str, Dict[str, Any]] = {
    "bug_001": {
        "title": "Error de Límite en Bucle",
        "description": "Encuentra el error off-by-one en esta iteración de lista",
        "bugs": [
            {
                "description": "El bucle empieza en 1 en lugar de 0, causando IndexError y saltando el primer elemento",
                "hint": "Las listas de Python usan índices desde 0"
            }
        ]
    },
    "bug_002": {
        "title": "Argumento Por Defecto Mutable",
        "description": "Trampa clásica de Python con valores por defecto mutables",
        "bugs": [
            {
                "description": "El argumento por defecto [] es compartido entre todas las llamadas",
                "hint": "Los argumentos por defecto se evalúan una vez al definir la función"
            }
        ]
    },
    "bug_003": {
        "title": "Validación de Entrada Faltante",
        "description": "Endpoint de API sin validación apropiada",
        "bugs": [
            {
                "description": "No hay validación para longitud de username o rango de edad",
                "hint": "Usa modelos Pydantic con validación Field()"
            },
            {
                "description": "Debería devolver 201 Created, no 200 OK",
                "hint": "Endpoints POST que crean recursos deberían devolver 201"
            }
        ]
    },
    "bug_004": {
        "title": "Vulnerabilidad de Inyección SQL",
        "description": "Vulnerabilidad de seguridad en consulta a base de datos",
        "bugs": [
            {
                "description": "La interpolación de strings en query SQL permite inyección SQL",
                "hint": "Usa queries parametrizadas con placeholders"
            }
        ]
    },
    "bug_005": {
        "title": "Credenciales Hardcodeadas",
        "description": "Problema de seguridad con secretos hardcodeados",
        "bugs": [
            {
                "description": "API key hardcodeada en el código fuente",
                "hint": "Usa variables de entorno para secretos"
            }
        ]
    },
    "bug_006": {
        "title": "Error de Conversión de Tipo",
        "description": "Falta conversión de tipo causando bug de comparación",
        "bugs": [
            {
                "description": "Comparando string con int sin conversión",
                "hint": "Los inputs de formularios son strings, necesitan conversión int()"
            }
        ]
    },
    "bug_007": {
        "title": "Manejo de Excepciones Faltante",
        "description": "División sin manejo de errores",
        "bugs": [
            {
                "description": "División por cero cuando la lista está vacía",
                "hint": "Verifica si la lista está vacía antes de dividir"
            }
        ]
    },
    "bug_008": {
        "title": "Sombreado de Variable",
        "description": "Variable de bucle sombrea el scope exterior",
        "bugs": [
            {
                "description": "La variable de bucle 'total' sombrea la variable acumuladora",
                "hint": "Usa nombres diferentes para el iterador del bucle"
            }
        ]
    },
    "bug_009": {
        "title": "Comparación Incorrecta",
        "description": "Asignación en lugar de comparación",
        "bugs": [
            {
                "description": "Usando operador de asignación = en lugar de comparación ==",
                "hint": "Esto es un error de sintaxis en Python (a diferencia de otros lenguajes)"
            }
        ]
    },
    "bug_010": {
        "title": "Error de Código de Estado FastAPI",
        "description": "Código de estado HTTP incorrecto para respuesta de error",
        "bugs": [
            {
                "description": "Debería devolver 404 Not Found, no 500 Internal Server Error",
                "hint": "500 es para errores del servidor, 404 es para recurso no encontrado"
            }
        ]
    },
}
