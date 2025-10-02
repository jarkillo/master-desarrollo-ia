# tareas.py
# ===========================================
# CLI de tareas con argparse y JSON
# ===========================================
# Rol: Dev Python senior — código didáctico, simple y extensible.
#
# Comandos:
#   - listar
#   - agregar "texto de la tarea"
#   - completar <id>
# Opción global:
#   - --file / -f para indicar la ruta del JSON (por defecto: tareas.json)

import argparse  # argparse: parsing de argumentos moderno y robusto
import json  # json: guardar/cargar las tareas
import os  # os: comprobar existencia de archivo
from typing import List, Dict, Any


# ================================
# 1. Constantes y tipos
# ================================
NOMBRE_ARCHIVO_POR_DEFECTO = "tareas.json"
Tarea = Dict[str, Any]  # Estructura: {"id": int, "nombre": str, "completada": bool}


# ================================
# 2. Capa de acceso a datos (I/O)
# ================================
def cargar_tareas(ruta_archivo: str) -> List[Tarea]:
    """Carga y devuelve la lista de tareas desde un archivo JSON.
    Si el archivo no existe o está vacío, devuelve una lista vacía.
    """
    if not os.path.exists(ruta_archivo):
        return []
    # Manejo de archivo corrupto o vacío: devolvemos lista vacía con fallback seguro
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else []
    except json.JSONDecodeError:
        # Si el JSON está corrupto, no explotamos: devolvemos lista vacía
        # (En un CLI real, podrías loguearlo o ofrecer un comando de "reparación")
        return []


def guardar_tareas(ruta_archivo: str, tareas: List[Tarea]) -> None:
    """Guarda la lista de tareas en el archivo JSON con indentación legible."""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)


# ================================
# 3. Lógica de negocio (operaciones)
# ================================
def generar_nuevo_id(tareas: List[Tarea]) -> int:
    """Genera un ID incremental robusto.
    - Usa (max(id) + 1) para evitar colisiones si algún día implementas 'borrar'.
    """
    if not tareas:
        return 1
    return max(t["id"] for t in tareas) + 1


def agregar_tarea(ruta_archivo: str, nombre: str) -> None:
    """Crea una nueva tarea no completada y la persiste."""
    tareas = cargar_tareas(ruta_archivo)
    nueva: Tarea = {
        "id": generar_nuevo_id(tareas),
        "nombre": nombre,
        "completada": False,
    }
    tareas.append(nueva)
    guardar_tareas(ruta_archivo, tareas)


def listar_tareas(ruta_archivo: str) -> None:
    """Imprime por stdout el listado de tareas con su estado."""
    tareas = cargar_tareas(ruta_archivo)
    if not tareas:
        print("No hay tareas aún. Usa 'agregar' para crear la primera.")
        return
    for t in tareas:
        estado = "✅" if t.get("completada") else "❌"
        print(f"{t.get('id')}. {t.get('nombre')} {estado}")


def completar_tarea(ruta_archivo: str, id_tarea: int) -> None:
    """Marca como completada la tarea con el ID indicado (si existe)."""
    tareas = cargar_tareas(ruta_archivo)
    encontrada = False
    for t in tareas:
        if t.get("id") == id_tarea:
            t["completada"] = True
            encontrada = True
            break

    if not encontrada:
        print(f"No se encontró la tarea con ID {id_tarea}.")
        return

    guardar_tareas(ruta_archivo, tareas)


# ================================
# 4. Capa de interfaz (CLI / argparse)
# ================================
def construir_parser() -> argparse.ArgumentParser:
    """Define el parser principal y los subparsers para cada comando."""
    parser = argparse.ArgumentParser(
        prog="tareas.py",
        description="CLI simple para gestionar tareas en un archivo JSON.",
    )

    # Opción global para cambiar la ruta del archivo de almacenamiento
    parser.add_argument(
        "-f",
        "--file",
        default=NOMBRE_ARCHIVO_POR_DEFECTO,
        help=f"Ruta del archivo JSON de tareas (por defecto: {NOMBRE_ARCHIVO_POR_DEFECTO})",
    )

    # Subcomandos
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando: listar
    sp_listar = subparsers.add_parser("listar", help="Lista todas las tareas")
    sp_listar.set_defaults(func=cmd_listar)

    # Subcomando: agregar
    sp_agregar = subparsers.add_parser("agregar", help="Agrega una nueva tarea")
    sp_agregar.add_argument("nombre", help="Texto de la tarea a agregar")
    sp_agregar.set_defaults(func=cmd_agregar)

    # Subcomando: completar
    sp_completar = subparsers.add_parser(
        "completar", help="Marca una tarea como completada"
    )
    sp_completar.add_argument("id", type=int, help="ID de la tarea a completar")
    sp_completar.set_defaults(func=cmd_completar)

    return parser


# ================================
# 5. Adaptadores entre argparse y lógica
# ================================
def cmd_listar(args: argparse.Namespace) -> None:
    """Adaptador del subcomando 'listar'."""
    listar_tareas(args.file)


def cmd_agregar(args: argparse.Namespace) -> None:
    """Adaptador del subcomando 'agregar'."""
    agregar_tarea(args.file, args.nombre)


def cmd_completar(args: argparse.Namespace) -> None:
    """Adaptador del subcomando 'completar'."""
    completar_tarea(args.file, args.id)


# ================================
# 6. Punto de entrada
# ================================
def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()
    # Ejecutamos la función asociada al subcomando elegido
    args.func(args)


if __name__ == "__main__":
    main()
