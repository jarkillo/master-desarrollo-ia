# tareas.py (Indicamos el nombre del archivo)

# ================================
# 0. IMPORTAR LIBRERIAS
# ================================

from typing import (
    TypedDict,
    List,
)  # Esta libreria nos permite crear tipos de datos (para hacer legible el codigo)
import json, os, sys

# ================================
# 1. VARIABLES GLOBALES
# ================================

# Cambiamos a ARCHIVO_POR_DEFECTO porque explica mejor la funcion del archivo
ARCHIVO_POR_DEFECTO = "tareas.json"


# ================================
# 1.1. TIPOS DE DATOS
# ================================
class Tarea(TypedDict):
    id: int
    nombre: str
    completada: bool


# ================================
# 2. FUNCIONES
# ================================


# Vamos a escribir mejor la funcion para cargar tareas


def cargar_tareas(ruta: str) -> List[Tarea]:
    """Devuelve la lista de tareas. Si no hay archivo o está vacío/corrupto, lista vacía."""

    # Si el archivo no existe, devolvemos una lista vacía
    if not os.path.exists(ruta):
        return []

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else []

    except json.JSONDecodeError:
        # Decisión: no romper por JSON corrupto; devolvemos vacío para que el CLI siga siendo usable.
        return []


# Esta función guarda las tareas en el archivo JSON
def guardar_tareas(ruta: str, tareas: List[Tarea]) -> None:
    """Guarda la lista de tareas en el archivo JSON con indentación legible."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)


def nuevo_id(tareas: List[Tarea]) -> int:
    """Genera un ID incremental robusto."""
    return 1 if not tareas else max(t["id"] for t in tareas) + 1


def agregar_tarea(ruta: str, nombre: str) -> Tarea:
    """Crea una nueva tarea no completada y la persiste."""
    tareas = cargar_tareas(ruta)
    tarea: Tarea = {"id": nuevo_id(tareas), "nombre": nombre, "completada": False}
    tareas.append(tarea)
    guardar_tareas(ruta, tareas)
    return tarea  # devolver la entidad ayuda en tests


# Esta función lista las tareas
def listar_tareas(ruta: str) -> List[Tarea]:
    """Imprime el listado de tareas con su estado."""
    return cargar_tareas(ruta)


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
