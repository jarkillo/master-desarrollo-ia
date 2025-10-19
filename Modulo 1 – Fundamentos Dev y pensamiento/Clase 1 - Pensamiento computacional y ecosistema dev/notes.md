# Notes - Clase 1: Prompts y Resultados

## 🎯 Objetivo de este documento

Este archivo registra la evolución del trabajo con IA durante la Clase 1, documentando:
- Prompts utilizados (buenos y malos)
- Resultados obtenidos
- Lecciones aprendidas sobre prompt engineering

---

## 📝 Prompt Initial (Genérico) - ANTES de aprender

Ejercicio

Tras darle a la IA el codigo explicado y pasarle el prompt correcto pero generico:

En este caso, hemos copiado directamente el codigo (era cortito) y le hemos puesto el prompt al final. El resultado es este:

```sql
# Mi prompt

import sys  # sys nos da acceso a los argumentos de la terminal

# Si el usuario no puso nada más después de "python tareas.py"
# Si hay menos de dos argumentos (El primero es el nombre del programa):
if len(sys.argv) < 2:
    print("Uso: python tareas.py <comando>")  # Imprimimos en pantalla el mensaje

# En caso contrario:
else:
    # Creamos la variable comando y metemos dentro el argumento.
    comando = sys.argv[1]  # el segundo argumento: listar, agregar, etc.

    # Ojo, es sys.argv[1] porque en python empezamos desde el 0, es decir,
    # el primer argumento sería el [0] = tareas.py
    # el segundo argumento sería el [1] = listar / agregar / completar

    # Si el comando es listar
    if comando == "listar":
        print("Aquí se mostrarían las tareas")  # Imprimimos el mensaje

    # Si es agregar
    elif comando == "agregar":
        print("Aquí se agregaría una tarea")  # Imprimimos el mensaje

    # si es completar
    elif comando == "completar":
        print("Aquí se completaría una tarea")  # Imprimimos el mensaje

    else:
        print("Comando no reconocido")  # Avisamos del error

Rol: Dev Python senior.
Tarea: Tengo un script CLI que recibe comandos agregar, listar y completar. Quiero que las tareas se guarden en un archivo JSON.
Formato: Dame el código base limpio y con comentarios.
```

### ChatGPT said:

Thought for 13s

Aquí tienes un **tareas.py** base, limpio y comentado, que persiste las tareas en un **JSON**. Soporta los comandos `agregar`, `listar` y `completar`, con ids autoincrementales y manejo de errores comunes.

```python
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
            print("Aviso: El archivo de tareas no es una lista. Se ignora.", file=sys.stderr)
            return []
    except json.JSONDecodeError:
        print("Aviso: El archivo de tareas está corrupto. Se ignorará y se regenerará.", file=sys.stderr)
        return []

def guardar_tareas(tareas: List[Dict[str, Any]], db_path: Path = DEFAULT_DB_PATH) -> None:
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
    return (max((t["id"] for t in tareas), default=0) + 1)

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
    grupo_filtro.add_argument("--hechas", action="store_true", help="Listar solo completadas")
    grupo_filtro.add_argument("--pendientes", action="store_true", help="Listar solo pendientes (por defecto)")
    p_listar.add_argument("--json", action="store_true", help="Salida en formato JSON en lugar de texto")

    # comando: completar
    p_completar = subparsers.add_parser("completar", help="Marca una tarea como completada")
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
            estado = "ya estaba completada" if tarea["hecha"] and tarea["completada_en"] else "completada"
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

```

---

## 🔄 Evolución de Prompts - DESPUÉS de aprender

### Comparación: Prompt Genérico vs Prompt Específico

#### ❌ Prompt Genérico (el que usamos al inicio)

```
Rol: Dev Python senior.
Tarea: Tengo un script CLI que recibe comandos agregar, listar y completar. Quiero que las tareas se guarden en un archivo JSON.
Formato: Dame el código base limpio y con comentarios.
```

**Problemas identificados**:
- ✅ Tiene rol (bueno)
- ⚠️ Tarea demasiado vaga ("que las tareas se guarden" no especifica estructura)
- ❌ No especifica versión de Python
- ❌ No indica si usar stdlib o permitir dependencias
- ❌ "Código base" es ambiguo (¿refactorizar el existente? ¿crear nuevo?)
- ❌ No especifica manejo de errores
- ✅ Pide comentarios (bueno)

**Resultado obtenido**: Código funcional pero con features que no pedimos (timestamps, argparse, validaciones extra)

---

#### ✅ Prompt Mejorado (aplicando lecciones de Clase 1)

```
Rol: Dev Python senior especializado en CLIs.

Tarea: Refactoriza este script CLI básico para añadir persistencia en JSON.

Requisitos funcionales:
- Mantener comandos actuales: listar, agregar, completar
- Persistir tareas en archivo tareas.json
- Cada tarea debe tener: id (autoincremental), texto, estado (completada: true/false)
- Al listar, mostrar formato: [x] 1. Texto tarea (si completada) o [ ] 1. Texto tarea (si pendiente)

Requisitos técnicos:
- Python 3.12
- Solo usar biblioteca estándar (stdlib, no dependencias externas)
- Mantener sys.argv para parsing (NO usar argparse todavía)
- Funciones separadas: cargar_tareas(), guardar_tareas(), agregar_tarea(), etc.
- Manejo de errores básico: si JSON corrupto, crear nuevo archivo

Output esperado:
- Un archivo tareas_json.py
- Máximo 150 líneas
- Docstrings en funciones principales
- Comentarios solo donde sea necesario

Código base actual:
[pegar el código de tareas.py]
```

**Mejoras aplicadas**:
- ✅ Especifica versión Python
- ✅ Constraint: solo stdlib (evita dependencias complejas)
- ✅ Indica estructura de datos exacta (id, texto, estado)
- ✅ Especifica formato de salida
- ✅ Mantiene simplicidad (sys.argv, no argparse)
- ✅ Límite de líneas (evita over-engineering)
- ✅ Incluye código base

**Resultado esperado**: Código más alineado con nuestras necesidades y nivel actual

---

## 📊 Lecciones Aprendidas

### 1. Especificidad reduce iteraciones

**Antes**: Prompt genérico → IA genera código → revisamos → 3-4 rondas de ajustes

**Después**: Prompt específico → IA genera código cercano al objetivo → 1 ronda de ajustes

**Tiempo ahorrado**: ~50%

---

### 2. Constraints claros evitan over-engineering

Sin constraint de "solo stdlib":
- IA usa `argparse`, `dataclasses`, `typing`, `pathlib`
- Código más complejo del necesario para este nivel

Con constraint "solo stdlib, sys.argv":
- IA mantiene simplicidad
- Código más acorde al nivel del estudiante

---

### 3. Formato de output importa

Sin especificar:
- IA decide estructura arbitraria
- Puede generar múltiples archivos
- Puede usar nombres de variables/funciones inconsistentes

Especificando "un archivo, máximo 150 líneas, docstrings en funciones":
- Código más compacto y mantenible
- Estilo consistente

---

### 4. El código base como contexto

**Sin código base**: IA genera desde cero, puede divergir completamente

**Con código base**: IA respeta estructura existente, solo añade lo necesario

---

## 🎯 Template de Prompt Mejorado (para futuros proyectos)

```
Rol: [Dev Python senior / Especialista en X]

Tarea: [Acción específica: refactorizar/crear/extender/corregir]

Requisitos funcionales:
- [Feature 1 con detalles]
- [Feature 2 con detalles]
- [Feature 3 con detalles]

Requisitos técnicos:
- Python [versión específica]
- [Solo stdlib / Permitir dependencias X, Y]
- [Framework/patrón específico]
- [Estructura: funciones/clases/módulos]
- [Manejo de errores: básico/completo]

Output esperado:
- [Número de archivos y nombres]
- [Máximo X líneas por archivo]
- [Estilo: docstrings/type hints/tests]

Constraints:
- [No usar X]
- [Mantener Y]
- [Evitar Z]

Código base (si aplica):
[pegar código]
```

---

## 📚 Recursos Adicionales

Para profundizar en prompt engineering:
- Módulo 0, Clase 5: Prompt Engineering Avanzado
- `cli-tareas/prompts_usados.md`: Más ejemplos de prompts buenos/malos

---

## 🧪 Experimento: Mismo Problema, Diferentes Prompts

**Prueba tú mismo** (ejercicio opcional):

1. **Prompt Vago**: "Crea una CLI de tareas"
2. **Prompt Mejorado**: "Crea una CLI en Python 3.12 con comandos listar/agregar, persistencia JSON, solo stdlib"
3. **Prompt Específico**: [Usa el template de arriba con todos los detalles]

Documenta las diferencias en los resultados y guárdalas aquí.

