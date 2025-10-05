# tareas.py (Indicamos el nombre del archivo)

# ================================
# 0. IMPORTAR LIBRERIAS
# ================================

from typing import (
    TypedDict,
    List,
)  # Esta libreria nos permite crear tipos de datos (para hacer legible el codigo)
import json
import os
import sys

# ================================
# 1. VARIABLES GLOBALES
# ================================

# Cambiamos a ARCHIVO_POR_DEFECTO porque explica mejor la funcion del archivo
ARCHIVO_POR_DEFECTO = "tareas.json"

PRIORIDADES = ("alta", "media", "baja")


# ================================
# 1.1. TIPOS DE DATOS
# ================================
class Tarea(TypedDict):
    id: int
    nombre: str
    completada: bool
    prioridad: str  # Añadimos prioridad


# ================================
# 2. FUNCIONES
# ================================


# Vamos a escribir mejor la funcion para cargar tareas


def cargar_tareas(ruta: str) -> List[Tarea]:
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            datos = json.loads(contenido) if contenido else []
    except json.JSONDecodeError:
        return []

    # Backfill: garantiza campo prioridad
    for tarea in datos:
        if "prioridad" not in tarea or tarea["prioridad"] not in PRIORIDADES:
            tarea["prioridad"] = "media"
    return datos


# Esta función guarda las tareas en el archivo JSON
def guardar_tareas(ruta: str, tareas: List[Tarea]) -> None:
    """Guarda la lista de tareas en el archivo JSON con indentación legible."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)


def nuevo_id(tareas: List[Tarea]) -> int:
    """Genera un ID incremental robusto."""
    return 1 if not tareas else max(t["id"] for t in tareas) + 1


def agregar_tarea(
    ruta_archivo: str, nombre_tarea: str, prioridad: str = "media"
) -> dict:
    """Crea una tarea (por defecto prioridad='media'), la guarda y la devuelve."""
    if prioridad not in PRIORIDADES:
        prioridad = "media"

    lista_tareas = cargar_tareas(ruta_archivo)

    nueva_tarea = {
        "id": nuevo_id(lista_tareas),
        "nombre": nombre_tarea,
        "completada": False,
        "prioridad": prioridad,
    }

    lista_tareas.append(nueva_tarea)
    guardar_tareas(ruta_archivo, lista_tareas)
    return nueva_tarea


# Esta función lista las tareas
def listar_tareas(ruta_archivo: str, prioridad: str | None = None) -> list[dict]:
    """Devuelve la lista de tareas. Si se pasa prioridad, filtra por ella."""

    todas = cargar_tareas(ruta_archivo)

    if prioridad is None:
        return todas

    return [tarea for tarea in todas if tarea.get("prioridad") == prioridad]


# Esta función completa una tarea
def completar_tarea(ruta: str, id_tarea: int) -> bool:
    """Marca como completada la tarea con el ID indicado (si existe)."""
    tareas = cargar_tareas(ruta)
    for tarea in tareas:
        if tarea["id"] == id_tarea:
            tarea["completada"] = True
            guardar_tareas(ruta, tareas)
            return True
    return False  # no encontrada


def _normaliza_prioridad(prioridad: str) -> str:
    """Devuelve la prioridad normalizada o 'media' si es inválida."""
    prioridad_normalizada = (prioridad or "").lower()
    return prioridad_normalizada if prioridad_normalizada in PRIORIDADES else "media"


# Fíjate que ahora no imprimimos dentro de la lógica: devolvemos datos. Imprimir es cosa del CLI. Esto facilita los tests.


def uso():
    """Imprime el mensaje de uso."""

    print("Uso: python tareas.py <listar|agregar|completar> [args]")
    sys.exit(1)


# ================================
# 3. MAIN
# ================================

# Flujo principal

if __name__ == "__main__":
    if len(sys.argv) < 2:
        uso()

    comando = sys.argv[1]
    archivo = ARCHIVO_POR_DEFECTO

    if comando == "listar":
        for t in listar_tareas(archivo):
            estado = "✅" if t["completada"] else "❌"
            print(f"{t['id']}. {t['nombre']} {estado}")

    elif comando == "agregar":
        if len(sys.argv) < 3:
            print("Falta el nombre de la tarea")
            sys.exit(1)
        tarea = agregar_tarea(archivo, sys.argv[2])
        print(f"Agregada: {tarea['id']}. {tarea['nombre']}")

    elif comando == "completar":
        if len(sys.argv) < 3:
            print("Falta el ID de la tarea")
            sys.exit(1)
        ok = completar_tarea(archivo, int(sys.argv[2]))
        print("Completada ✅" if ok else "No encontrada ❌")
    else:
        print("Comando no reconocido")
        uso()
