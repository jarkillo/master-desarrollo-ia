# ejemplos_vulnerables/a01_broken_access_control.py
"""
CÓDIGO VULNERABLE - A01: Broken Access Control

Este código fue generado por IA sin contexto de seguridad.
Demuestra vulnerabilidades típicas de control de acceso.

VULNERABILIDADES:
1. No valida ownership de recursos
2. Cualquier usuario autenticado puede acceder/modificar tareas de otros
3. No retorna 403 cuando corresponde (usa 404 para todo)
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Base de datos simulada
tareas_db = {}
tarea_id_counter = 1


class Tarea(BaseModel):
    id: int
    nombre: str
    user_id: int
    completada: bool = False


class CrearTareaRequest(BaseModel):
    nombre: str


def obtener_usuario_actual() -> int:
    """Simula autenticación - retorna user_id"""
    return 1  # En producción vendría del token/API Key


# VULNERABLE: No valida ownership
@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int, usuario_actual: int = Depends(obtener_usuario_actual)):
    """
    VULNERABILIDAD: Cualquier usuario autenticado puede ver tareas de otros.

    Escenario de ataque:
    - Usuario 1 crea tarea (id=5, user_id=1)
    - Usuario 2 (user_id=2) hace GET /tareas/5
    - Usuario 2 puede ver la tarea de Usuario 1 ❌
    """
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # ❌ NO VALIDA si tarea.user_id == usuario_actual
    return tareas_db[tarea_id]


# VULNERABLE: No valida ownership antes de modificar
@app.put("/tareas/{tarea_id}")
def actualizar_tarea(
    tarea_id: int,
    datos: CrearTareaRequest,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """
    VULNERABILIDAD: Cualquier usuario puede modificar tareas de otros.

    Escenario de ataque:
    - Usuario 1 crea tarea "Reunión confidencial" (id=10)
    - Usuario 2 hace PUT /tareas/10 {"nombre": "Tarea modificada por atacante"}
    - La tarea de Usuario 1 fue modificada por Usuario 2 ❌
    """
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # ❌ NO VALIDA ownership - permite modificar cualquier tarea
    tareas_db[tarea_id].nombre = datos.nombre
    return tareas_db[tarea_id]


# VULNERABLE: No valida ownership antes de eliminar
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, usuario_actual: int = Depends(obtener_usuario_actual)):
    """
    VULNERABILIDAD CRÍTICA: Cualquier usuario puede eliminar tareas de otros.

    Escenario de ataque:
    - Usuario 1 crea tarea importante (id=20)
    - Usuario 2 hace DELETE /tareas/20
    - La tarea de Usuario 1 fue eliminada por Usuario 2 ❌
    """
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # ❌ NO VALIDA ownership - permite eliminar cualquier tarea
    del tareas_db[tarea_id]
    return {"message": "Tarea eliminada"}


# VULNERABLE: Expone todas las tareas de todos los usuarios
@app.get("/tareas", response_model=List[Tarea])
def listar_tareas(usuario_actual: int = Depends(obtener_usuario_actual)):
    """
    VULNERABILIDAD: Retorna tareas de todos los usuarios.

    Escenario de ataque:
    - Usuario 1 crea tareas con información confidencial
    - Usuario 2 hace GET /tareas
    - Usuario 2 puede ver tareas de Usuario 1 ❌
    """
    # ❌ NO FILTRA por user_id - retorna todo
    return list(tareas_db.values())


# ========================================
# CÓDIGO CORREGIDO (para comparación)
# ========================================

"""
CORRECCIÓN: Validar ownership en TODOS los endpoints

@app.get("/tareas/{tarea_id}")
def obtener_tarea_seguro(tarea_id: int, usuario_actual: int = Depends(obtener_usuario_actual)):
    tarea = tareas_db.get(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # ✅ VALIDAR OWNERSHIP
    if tarea.user_id != usuario_actual:
        # ✅ RETORNAR 403 (no 404) para no exponer existencia de recurso
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return tarea


@app.get("/tareas", response_model=List[Tarea])
def listar_tareas_seguro(usuario_actual: int = Depends(obtener_usuario_actual)):
    # ✅ FILTRAR solo tareas del usuario autenticado
    return [t for t in tareas_db.values() if t.user_id == usuario_actual]
"""

# ========================================
# EJERCICIO
# ========================================

"""
1. Identifica las 3 vulnerabilidades de Broken Access Control en este código
2. Para cada vulnerabilidad, explica el riesgo y el escenario de ataque
3. Implementa las correcciones aplicando validación de ownership
4. Escribe tests que validen que la corrección funciona:
   - test_usuario_no_puede_ver_tarea_ajena()
   - test_usuario_no_puede_modificar_tarea_ajena()
   - test_usuario_no_puede_eliminar_tarea_ajena()
   - test_listar_solo_retorna_tareas_propias()
"""
