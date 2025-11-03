"""
❌ EJEMPLOS DE TOOLS MAL DISEÑADOS

Este módulo contiene ejemplos de antipatrones en diseño de tools.
NO usar estos patrones en producción. Son ejemplos educativos.
"""

from typing import Any


def get_data(id: str) -> dict[str, Any]:
    """Get data."""  # ❌ Description demasiado vaga
    # ❌ Problemas:
    # 1. Nombre ambiguo (¿qué datos?)
    # 2. Description no dice qué hace
    # 3. Usa UUID (difícil de recordar para agentes)
    # 4. No documenta el schema de respuesta
    return {"data": "some data"}


def list_contacts() -> list[dict]:
    """Returns all contacts in the system."""
    # ❌ Problemas:
    # 1. Retorna TODOS los contactos (puede ser 5000+)
    # 2. Desperdicia tokens del agente
    # 3. Dificulta encontrar información relevante
    # 4. No hay paginación ni filtros
    fake_contacts = [{"id": i, "name": f"Contact {i}"} for i in range(5000)]
    return fake_contacts


def run_command(cmd: str) -> str:
    """Runs a shell command."""
    # ❌ PELIGRO DE SEGURIDAD:
    # 1. Permite ejecución arbitraria de comandos
    # 2. No valida inputs
    # 3. Puede ser usado para injection attacks
    # 4. No hay whitelist de comandos seguros
    import subprocess

    # ¡NUNCA hacer esto!
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def api_call(endpoint: str, data: dict) -> dict:
    """Calls an API."""
    # ❌ Problemas:
    # 1. Demasiado genérico (¿qué API? ¿qué hace?)
    # 2. No documenta qué endpoints son válidos
    # 3. No valida la estructura de data
    # 4. No maneja errores de HTTP
    # 5. Error messages crípticos
    import requests

    try:
        response = requests.post(endpoint, json=data)
        return response.json()
    except Exception:
        return {"error": "Failed"}  # ❌ Mensaje no accionable


def search(query: str) -> list:
    """Searches."""
    # ❌ Problemas:
    # 1. No dice dónde busca (¿archivos? ¿DB? ¿API?)
    # 2. No documenta formato de resultados
    # 3. No tiene límite de resultados
    # 4. Sin validación de query
    # 5. Type hints vagos (list de qué?)
    return []


def update(id: str, data: dict) -> bool:
    """Updates something."""
    # ❌ Problemas:
    # 1. ¿Actualiza qué? (usuarios, tareas, productos?)
    # 2. Schema de data no documentado
    # 3. Retorna bool (no informa qué se actualizó)
    # 4. No valida que el ID existe
    # 5. No maneja errores de validación
    return True


def get_config() -> dict:
    """Returns config."""
    # ❌ PELIGRO DE SEGURIDAD:
    # 1. Expone TODOS los secrets
    # 2. No filtra variables sensibles (API keys, passwords)
    # 3. Puede exponer información confidencial
    import os

    return dict(os.environ)  # ¡Expone API_KEY, SECRET, etc.!


def process_file(file: str) -> dict:
    """Processes a file."""
    # ❌ Problemas de seguridad:
    # 1. No valida path (path traversal possible)
    # 2. No verifica que el archivo existe
    # 3. No limita el tamaño del archivo
    # 4. Puede leer archivos fuera del proyecto
    with open(file) as f:  # ¡Peligro!
        content = f.read()
    return {"content": content}


def calc(expression: str) -> float:
    """Calculates expression."""
    # ❌ PELIGRO DE SEGURIDAD CRÍTICO:
    # 1. eval() permite ejecución arbitraria de código
    # 2. Puede ser usado para comprometer el sistema
    # 3. ¡NUNCA usar eval() con inputs de usuario/agente!
    return eval(expression)  # ¡PELIGRO!


def db_query(query: str) -> list[dict]:
    """Executes a database query."""
    # ❌ PELIGRO: SQL Injection
    # 1. Concatenación de strings en query SQL
    # 2. No usa prepared statements
    # 3. Permite queries arbitrarias (DELETE, DROP, etc.)
    import sqlite3

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # ¡SQL Injection posible!
    cursor.execute(f"SELECT * FROM users WHERE name = '{query}'")
    return cursor.fetchall()


# Resumen de antipatrones:
ANTIPATRONES = """
1. Nombres ambiguos (get_data, search, update)
2. Descriptions vagas o ausentes
3. No validación de inputs
4. Exposición de secrets/información sensible
5. Retornar TODOS los datos (sin paginación)
6. Mensajes de error crípticos
7. Type hints vagos o ausentes
8. Operaciones inseguras (eval, shell=True, SQL injection)
9. No documentar schemas de input/output
10. Falta de rate limiting
"""
