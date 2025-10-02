#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI simple de tareas con persistencia en un archivo JSON.

Comandos:
  - agregar <texto de la tarea>
  - listar [--todas] [--hechas] [--pendientes] [--json]
  - completar <id>

Uso rápido:
  python tareas.py agregar "Lavar los platos"
  python tareas.py listar --pendientes
  python tareas.py completar 3
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ruta por defecto del "repositorio" de tareas (junto al script)
DEFAULT_DB_PATH = Path(__file__).with_name("tareas.json")


# ---------- Utilidades de persistencia ----------


def _ahora_iso() -> str:
    """Devuelve fecha/hora actual en formato ISO 8601 (UTC naive)."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def cargar_tareas(db_path: Path = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """
    Carga la lista de tareas desde el JSON.
    Si el archivo no existe, devuelve una lista vacía.
    Si el JSON está corrupto, avisa y devuelve lista vacía (no revienta).
    """
    if not db_path.exists():
        return []
    try:
        with db_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Aseguramos que sea una lista
        if isinstance(data, list):
            return data
        else:
            print(
                "Aviso: El archivo de tareas no es una lista. Se ignora.",
                file=sys.stderr,
            )
            return []
    except json.JSONDecodeError:
        print(
            "Aviso: El archivo de tareas está corrupto. Se ignorará y se regenerará.",
            file=sys.stderr,
        )
        return []


def guardar_tareas(
    tareas: List[Dict[str, Any]], db_path: Path = DEFAULT_DB_PATH
) -> None:
    """
    Guarda la lista de tareas en el JSON con indentación.
    Se escribe de forma segura: primero a un archivo temporal y luego se renombra.
    """
    tmp_path = db_path.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp_path.replace(db_path)  # Operación atómica en la mayoría de FS


def siguiente_id(tareas: List[Dict[str, Any]]) -> int:
    """Calcula el siguiente id autoincremental (max + 1) sobre las tareas existentes."""
    return max((t["id"] for t in tareas), default=0) + 1


# ---------- Operaciones de dominio ----------


def op_agregar(texto: str, db_path: Path = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """
    Agrega una tarea nueva con 'texto' y la marca como pendiente.
    Devuelve la tarea creada.
    """
    tareas = cargar_tareas(db_path)
    nueva = {
        "id": siguiente_id(tareas),
        "texto": texto.strip(),
        "hecha": False,
        "creada_en": _ahora_iso(),
        "completada_en": None,
    }
    tareas.append(nueva)
    guardar_tareas(tareas, db_path)
    return nueva


def op_listar(
    db_path: Path = DEFAULT_DB_PATH,
    filtro: Optional[str] = None,  # "todas" | "hechas" | "pendientes" | None
) -> List[Dict[str, Any]]:
    """
    Lista tareas aplicando un filtro opcional:
      - None o "pendientes": solo pendientes (por defecto)
      - "todas": todas
      - "hechas": solo completadas
    Devuelve la lista filtrada ordenada por id asc.
    """
    tareas = sorted(cargar_tareas(db_path), key=lambda t: t["id"])
    if filtro in (None, "pendientes"):
        return [t for t in tareas if not t.get("hecha")]
    if filtro == "hechas":
        return [t for t in tareas if t.get("hecha")]
    if filtro == "todas":
        return tareas
    # Filtro desconocido → por seguridad, pendientes
    return [t for t in tareas if not t.get("hecha")]


def op_completar(task_id: int, db_path: Path = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """
    Marca como completada la tarea con id = task_id.
    Devuelve la tarea actualizada.
    Lanza ValueError si no existe.
    """
    tareas = cargar_tareas(db_path)
    for t in tareas:
        if t["id"] == task_id:
            if not t["hecha"]:
                t["hecha"] = True
                t["completada_en"] = _ahora_iso()
                guardar_tareas(tareas, db_path)
            return t
    raise ValueError(f"No existe una tarea con id {task_id}.")


# ---------- Formato de salida ----------


def imprimir_tareas_humano(tareas: List[Dict[str, Any]]) -> None:
    """
    Muestra las tareas de forma legible en consola:
      [ ] id  texto
      [x] id  texto
    """
    if not tareas:
        print("No hay tareas que mostrar.")
        return
    for t in tareas:
        check = "x" if t.get("hecha") else " "
        print(f"[{check}] {t['id']:>3}  {t.get('texto','')}")


# ---------- CLI / argparse ----------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI de tareas con backend JSON.",
        prog="tareas.py",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Ruta del archivo JSON de tareas (por defecto: {DEFAULT_DB_PATH.name})",
    )

    subparsers = parser.add_subparsers(dest="comando", required=True)

    # comando: agregar
    p_agregar = subparsers.add_parser("agregar", help="Agrega una nueva tarea")
    p_agregar.add_argument("texto", type=str, help="Texto/descripcion de la tarea")

    # comando: listar
    p_listar = subparsers.add_parser("listar", help="Lista tareas")
    grupo_filtro = p_listar.add_mutually_exclusive_group()
    grupo_filtro.add_argument("--todas", action="store_true", help="Listar todas")
    grupo_filtro.add_argument(
        "--hechas", action="store_true", help="Listar solo completadas"
    )
    grupo_filtro.add_argument(
        "--pendientes", action="store_true", help="Listar solo pendientes (por defecto)"
    )
    p_listar.add_argument(
        "--json", action="store_true", help="Salida en formato JSON en lugar de texto"
    )

    # comando: completar
    p_completar = subparsers.add_parser(
        "completar", help="Marca una tarea como completada"
    )
    p_completar.add_argument("id", type=int, help="ID de la tarea a completar")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    db_path: Path = args.db

    try:
        if args.comando == "agregar":
            tarea = op_agregar(args.texto, db_path)
            print(f"Tarea creada #{tarea['id']}: {tarea['texto']}")

        elif args.comando == "listar":
            if args.todas:
                filtro = "todas"
            elif args.hechas:
                filtro = "hechas"
            else:
                filtro = "pendientes"
            tareas = op_listar(db_path, filtro=filtro)
            if args.json:
                print(json.dumps(tareas, ensure_ascii=False, indent=2))
            else:
                imprimir_tareas_humano(tareas)

        elif args.comando == "completar":
            tarea = op_completar(args.id, db_path)
            estado = (
                "ya estaba completada"
                if tarea["hecha"] and tarea["completada_en"]
                else "completada"
            )
            # Nota: el mensaje refleja el resultado; si ya estaba, no cambia nada.
            print(f"Tarea #{tarea['id']} {estado}: {tarea['texto']}")

        else:
            parser.print_help()
            return 2

        return 0

    except ValueError as e:
        # Errores de dominio (por ejemplo, id inexistente)
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelado por el usuario.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
