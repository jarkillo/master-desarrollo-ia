# ejemplos_vulnerables/a03_injection.py
"""
CÓDIGO VULNERABLE - A03: Injection

Este código fue generado por IA sin contexto de seguridad.
Demuestra vulnerabilidades típicas de inyección.

VULNERABILIDADES:
1. No usa Pydantic para validación (acepta dict)
2. Usa eval() para evaluación dinámica (code injection)
3. SQL injection en queries raw
4. Mass assignment (permite modificar cualquier campo)
"""

from fastapi import FastAPI, HTTPException
from typing import Dict, Any

app = FastAPI()

# Base de datos simulada
tareas_db = []


# VULNERABLE 1: Acepta dict sin validación
@app.post("/tareas")
def crear_tarea(datos: dict):
    """
    VULNERABILIDAD: No usa Pydantic, acepta cualquier dato.

    Escenario de ataque:
    POST /tareas {"nombre": "", "malicious_field": "value"}
    - Acepta nombre vacío ❌
    - Acepta campos no esperados ❌
    """
    # ❌ Sin validación de tipo/contenido
    tarea = {
        "id": len(tareas_db) + 1,
        **datos  # ❌ Acepta cualquier campo
    }
    tareas_db.append(tarea)
    return tarea


# VULNERABLE 2: Usa eval() - CODE INJECTION CRÍTICO
@app.post("/calcular")
def calcular_expresion(expresion: str):
    """
    VULNERABILIDAD CRÍTICA: Usa eval() con entrada del usuario.

    Escenario de ataque:
    POST /calcular {"expresion": "__import__('os').system('rm -rf /')"}
    - Ejecuta código arbitrario en el servidor ❌
    - Puede eliminar archivos, robar datos, ejecutar comandos ❌
    """
    try:
        # ❌ NUNCA USAR eval() con entrada de usuario
        resultado = eval(expresion)
        return {"resultado": resultado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# VULNERABLE 3: SQL Injection (si usas SQL raw)
@app.get("/tareas/buscar")
def buscar_tareas(nombre: str):
    """
    VULNERABILIDAD: SQL injection con f-strings.

    Escenario de ataque:
    GET /tareas/buscar?nombre=test'; DROP TABLE tareas; --
    - Elimina la tabla completa ❌

    NOTA: Este ejemplo es ilustrativo. En FastAPI normalmente usas ORM,
    pero si usas SQL raw, NUNCA uses f-strings para queries.
    """
    # ❌ SQL Injection - NUNCA hacer esto
    query = f"SELECT * FROM tareas WHERE nombre = '{nombre}'"

    # Si ejecutaras este query:
    # query = "SELECT * FROM tareas WHERE nombre = 'test'; DROP TABLE tareas; --'"
    # Resultado: Tabla eliminada ❌

    return {"query": query, "warning": "Este código es vulnerable a SQL injection"}


# VULNERABLE 4: Mass Assignment
@app.put("/tareas/{tarea_id}")
def actualizar_tarea(tarea_id: int, datos: Dict[str, Any]):
    """
    VULNERABILIDAD: Mass assignment - permite modificar cualquier campo.

    Escenario de ataque:
    PUT /tareas/1 {"nombre": "Test", "user_id": 999, "is_admin": true}
    - Cambia el dueño de la tarea ❌
    - Puede elevar privilegios ❌
    """
    tarea = next((t for t in tareas_db if t["id"] == tarea_id), None)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # ❌ Actualiza TODOS los campos sin validación
    for campo, valor in datos.items():
        tarea[campo] = valor  # ❌ Permite modificar user_id, permisos, etc.

    return tarea


# VULNERABLE 5: No valida límites en paginación
@app.get("/tareas")
def listar_tareas(limite: int = 10, offset: int = 0):
    """
    VULNERABILIDAD: No valida límites, permite DoS.

    Escenario de ataque:
    GET /tareas?limite=999999999
    - Consume toda la memoria del servidor ❌
    - Denial of Service (DoS) ❌
    """
    # ❌ No valida que limite esté en rango razonable (1-100)
    # ❌ No valida que offset sea >= 0
    return tareas_db[offset:offset + limite]


# ========================================
# CÓDIGO CORREGIDO (para comparación)
# ========================================

"""
CORRECCIÓN 1: Usar Pydantic para validación estricta

from pydantic import BaseModel, Field

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str = Field(None, max_length=500)

@app.post("/tareas")
def crear_tarea_seguro(datos: CrearTareaRequest):
    # ✅ Pydantic valida automáticamente
    # ✅ Rechaza nombres vacíos
    # ✅ Solo acepta campos definidos
    tarea = {
        "id": len(tareas_db) + 1,
        "nombre": datos.nombre,
        "descripcion": datos.descripcion
    }
    tareas_db.append(tarea)
    return tarea


CORRECCIÓN 2: NUNCA usar eval() - usar alternativas seguras

# ❌ NO HACER: eval(expresion)

# ✅ Para cálculos matemáticos, usar ast.literal_eval o bibliotecas especializadas
import ast

@app.post("/calcular")
def calcular_seguro(expresion: str):
    try:
        # ✅ ast.literal_eval solo acepta literales (números, strings, listas)
        # ✅ NO ejecuta código
        resultado = ast.literal_eval(expresion)
        return {"resultado": resultado}
    except (ValueError, SyntaxError):
        raise HTTPException(status_code=400, detail="Expresión inválida")


CORRECCIÓN 3: Usar ORM o prepared statements

from sqlalchemy import text

@app.get("/tareas/buscar")
def buscar_tareas_seguro(nombre: str):
    # ✅ Usar parámetros (prepared statements)
    query = text("SELECT * FROM tareas WHERE nombre = :nombre")
    result = db.execute(query, {"nombre": nombre})

    # O mejor aún, usar ORM:
    # ✅ tareas = db.query(Tarea).filter(Tarea.nombre == nombre).all()
    return result


CORRECCIÓN 4: Prevenir mass assignment con Pydantic

class ActualizarTareaRequest(BaseModel):
    nombre: str = Field(None, min_length=1, max_length=100)
    descripcion: str = Field(None, max_length=500)
    completada: bool = None
    # ✅ Solo campos permitidos - NO incluye user_id, is_admin, etc.

@app.put("/tareas/{tarea_id}")
def actualizar_tarea_seguro(tarea_id: int, datos: ActualizarTareaRequest):
    tarea = next((t for t in tareas_db if t["id"] == tarea_id), None)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # ✅ Solo actualizar campos permitidos
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        tarea[campo] = valor

    return tarea


CORRECCIÓN 5: Validar límites con Query

from fastapi import Query

@app.get("/tareas")
def listar_tareas_seguro(
    limite: int = Query(10, ge=1, le=100),  # ✅ Entre 1 y 100
    offset: int = Query(0, ge=0)  # ✅ >= 0
):
    return tareas_db[offset:offset + limite]
"""

# ========================================
# EJERCICIO
# ========================================

"""
1. Identifica las 5 vulnerabilidades de Injection en este código
2. Para cada vulnerabilidad, explica el riesgo y el ataque posible
3. Implementa las correcciones usando Pydantic, ast.literal_eval, y Query
4. Escribe tests que validen las mitigaciones:
   - test_pydantic_rechaza_nombre_vacio()
   - test_eval_no_ejecuta_codigo_malicioso()
   - test_paginacion_rechaza_limites_invalidos()
   - test_mass_assignment_no_permite_cambiar_user_id()
"""
