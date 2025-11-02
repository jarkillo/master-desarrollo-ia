#!/usr/bin/env python3

"""
CLI para el gestor de tareas usando argparse.
No modifica la lógica de dominio en tareas.py.
"""

import argparse
import sys

# Importa la lógica existente sin cambiar firmas
from tareas import (
    ARCHIVO_POR_DEFECTO,
    agregar_tarea,
    completar_tarea,
    listar_tareas,
)


def cmd_listar(args: argparse.Namespace) -> int:
    tareas = listar_tareas(args.file)
    for t in tareas:
        estado = "✅" if t["completada"] else "❌"
        print(f"{t['id']}. {t['nombre']} {estado}")
    return 0


def cmd_agregar(args: argparse.Namespace) -> int:
    # Permitimos nombres con espacios: se recoge como lista y se une
    nombre = " ".join(args.nombre) if isinstance(args.nombre, list) else args.nombre
    tarea = agregar_tarea(args.file, nombre)
    print(f"Agregada: {tarea['id']}. {tarea['nombre']}")
    return 0


def cmd_completar(args: argparse.Namespace) -> int:
    try:
        id_tarea = int(args.id)
    except ValueError:
        print("El ID debe ser un número entero.", file=sys.stderr)
        return 2

    ok = completar_tarea(args.file, id_tarea)
    print("Completada ✅" if ok else "No encontrada ❌")
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tareas",
        description="CLI de tareas con subcomandos (listar, agregar, completar).",
    )

    # Opción global de archivo
    parser.add_argument(
        "-f",
        "--file",
        default=ARCHIVO_POR_DEFECTO,
        help=f"Ruta del archivo JSON (por defecto: {ARCHIVO_POR_DEFECTO})",
    )

    subparsers = parser.add_subparsers(
        title="subcomandos",
        dest="subcomando",
        metavar="{listar,agregar,completar}",
        required=True,  # exige un subcomando
    )

    # listar
    p_listar = subparsers.add_parser(
        "listar",
        help="Lista todas las tareas.",
        description="Lista todas las tareas.",
    )
    p_listar.set_defaults(func=cmd_listar)

    # agregar
    p_agregar = subparsers.add_parser(
        "agregar",
        help="Agrega una nueva tarea.",
        description="Agrega una nueva tarea.",
    )
    # Captura nombre con espacios: uno o más tokens
    p_agregar.add_argument(
        "nombre",
        nargs="+",
        help="Nombre de la tarea (se permiten espacios).",
    )
    p_agregar.set_defaults(func=cmd_agregar)

    # completar
    p_completar = subparsers.add_parser(
        "completar",
        help="Marca como completada una tarea por ID.",
        description="Marca como completada una tarea por ID.",
    )
    p_completar.add_argument(
        "id",
        help="ID numérico de la tarea a completar.",
    )
    p_completar.set_defaults(func=cmd_completar)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
