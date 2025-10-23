# api/dependencias.py
"""
Inyección de dependencias para FastAPI.

Centraliza la creación de instancias de servicios y repositorios.
"""
from api.repositorio_usuarios import RepositorioUsuarios
from api.servicio_usuarios import ServicioUsuarios

# Instancia global del repositorio (en memoria)
_repositorio_usuarios = RepositorioUsuarios()


def obtener_servicio_usuarios() -> ServicioUsuarios:
    """Dependency para inyectar el servicio de usuarios."""
    return ServicioUsuarios(_repositorio_usuarios)
