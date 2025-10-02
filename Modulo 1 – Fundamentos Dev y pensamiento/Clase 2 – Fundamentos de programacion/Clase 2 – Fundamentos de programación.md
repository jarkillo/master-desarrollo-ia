# Clase 2 – Fundamentos de programación: estructuras, funciones y persistencia mínima.

En esta clase haremos el siguiente ejercicio: 

Ampliar el CLI para que guarde las tareas en un archivo (`tareas.json`). Hacerlo primero a mano, luego dejar que la IA te lo refactorice con `argparse`.

### Concepto

En la clase anterior tenías un **esqueleto**: el programa recibía comandos desde la terminal y respondía con mensajes fijos. Eso es flujo básico de entrada/procesamiento/salida.

Ahora toca meterle **músculo**:

- **Estructuras de control**: condicionales (`if/elif/else`) y bucles (`for`, `while`).
- **Funciones**: dividir el código en piezas reutilizables, cada una con un propósito claro.
- **Persistencia**: hasta ahora las tareas “vivían en el aire”. Con un archivo (ej. JSON) podemos **guardar estado** entre ejecuciones.

La idea:

1. Si el usuario ejecuta `python tareas.py agregar "estudiar IA"`, la tarea se guarda en `tareas.json`.
2. Si ejecuta `listar`, el programa lee el archivo y muestra las tareas.
3. Si ejecuta `completar 1`, se actualiza el estado de esa tarea.

---

### Aplicación manual (sin IA)

Primero, piensa en pasos claros:

- Crear una función `cargar_tareas()` → abre `tareas.json` (si existe) y devuelve una lista de tareas.
- Crear una función `guardar_tareas(tareas)` → escribe la lista en el JSON.
- `agregar_tarea(nombre)` → añade un dict `{id, nombre, completada: False}`.
- `listar_tareas()` → recorre la lista y la imprime con un bucle.
- `completar_tarea(id)` → busca en la lista y marca `completada = True`.

Ejemplo base en Python (Explico todo en los comentarios, excepto lo que viene del paso anterior:

```python
# tareas.py (Indicamos el nombre del archivo)

# ================================
# 0. IMPORTAR LIBRERIAS
# ================================

import sys
import json  # json nos permite guardar y cargar datos en un archivo
import os  # os nos permite interactuar con el sistema operativo

# (Cuidado, esta librería puede ser peligrosa y a veces los antivirus la detectan como malware)

# ================================
# 1. VARIABLES GLOBALES
# ================================

# Creamos la variable FILE y le asignamos el nombre del archivo de tareas
NOMBRE_ARCHIVO = "tareas.json"

# ================================
# 2. FUNCIONES
# ================================

# Esta función carga las tareas desde el archivo JSON
def cargar_tareas():

    # Si el archivo FILE no existe
    if not os.path.exists(NOMBRE_ARCHIVO):
        # creamos una lista vacía
        return []

    # Si el archivo FILE existe lo abrimos en modo lectura
    with open(NOMBRE_ARCHIVO, "r") as archivo_json:

        # cargamos el contenido con la librería json y lo devolvemos
        return json.load(archivo_json)

# Esta función guarda las tareas en el archivo JSON
def guardar_tareas(tareas):

    # Si el archivo FILE existe lo abrimos en modo escritura
    with open(NOMBRE_ARCHIVO, "w") as archivo_json:

        # guardamos el contenido con la librería json y con indentación de 2 espacios
        json.dump(tareas, archivo_json, indent=2)

# Esta función agrega una tarea a la lista de tareas
def agregar_tarea(nombre):

    # cargamos las tareas usando la función cargar_tareas que hemos creado anteriormente y lo guardamos en la variable tareas
    tareas = cargar_tareas()

    # creamos una nueva tarea con el id = longitud de la lista de tareas + 1, nombre y completada = False
    nueva = {"id": len(tareas) + 1, "nombre": nombre, "completada": False}

    # con append añadimos la nueva tarea a la lista de tareas
    tareas.append(nueva)

    # guardamos las tareas usando la función guardar_tareas que hemos creado anteriormente
    guardar_tareas(tareas)

# Esta función lista las tareas
def listar_tareas():

    # cargamos las tareas usando la función cargar_tareas que hemos creado anteriormente y lo guardamos en la variable tareas
    tareas = cargar_tareas()

    # por cada tarea en la lista de tareas
    for tarea in tareas:

        # si la tarea está completada, el estado es ✅, si no, es ❌
        estado = "✅" if tarea["completada"] else "❌"

        # imprimimos el id, nombre y estado de la tarea
        print(f"{tarea['id']}. {tarea['nombre']} {estado}")

# Esta función completa una tarea
def completar_tarea(id_tarea):

    # cargamos las tareas usando la función cargar_tareas que hemos creado anteriormente y lo guardamos en la variable tareas
    tareas = cargar_tareas()

    # por cada tarea en la lista de tareas
    for tarea in tareas:

        # si la tarea tiene el id igual a id_tarea
        if tarea["id"] == id_tarea:

            # cambiamos el estado de la tarea a completada
            tarea["completada"] = True

    # guardamos las tareas usando la función guardar_tareas que hemos creado anteriormente
    guardar_tareas(tareas)

# ================================
# 3. MAIN
# ================================

# con el nombre main, si el archivo se ejecuta directamente, se ejecuta el siguiente código
if __name__ == "__main__":

    # si el usuario no puso nada más después de "python tareas.py"
    if len(sys.argv) < 2:

        # imprimimos el mensaje de uso
        print("Uso: python tareas.py <comando>")

        # salimos del programa con el código 1
        sys.exit(1)

    # creamos la variable comando y metemos dentro el argumento
    comando = sys.argv[1]

    # si el comando es listar
    if comando == "listar":

        # llamamos a la función listar_tareas
        listar_tareas()

    # si el comando es agregar
    elif comando == "agregar":

        # si el usuario no puso el nombre de la tarea
        if len(sys.argv) < 3:

            # imprimimos el mensaje de error
            print("Falta el nombre de la tarea")

        # si el usuario puso el nombre de la tarea
        else:

            # llamamos a la función agregar_tarea
            agregar_tarea(sys.argv[2])

    # si el comando es completar
    elif comando == "completar":

        # si el usuario no puso el ID de la tarea
        if len(sys.argv) < 3:

            # imprimimos el mensaje de error
            print("Falta el ID de la tarea")

        # si el usuario puso el ID de la tarea
        else:

            # llamamos a la función completar_tarea
            completar_tarea(int(sys.argv[2]))

    # si el comando no es listar, agregar o completar
    else:

        # imprimimos el mensaje de error
        print("Comando no reconocido")

```

Con esto ya tienes un CLI **mínimo pero funcional**.

---
### Aplicación con IA

Ahora que sabes cómo hacerlo a mano, puedes delegar en la IA para mejorarlo:

Prompt ejemplo:

```
Rol: Dev Python senior
Contexto: Tengo un CLI básico de tareas que usa sys.argv para listar, agregar y completar tareas guardadas en JSON.
Objetivo: Refactorízalo usando argparse para un parsing de comandos más limpio, y separa el código en funciones claras.
Formato: Dame el código con comentarios explicativos.

```

El resultado típico que dará la IA:

- Uso de `argparse` con subcomandos (`agregar`, `listar`, `completar`).
- Mejor validación de argumentos.
- Código más legible y modular.

---

### Ejercicio de la clase

1. Crea una rama `feature/cli-json`.
2. Implementa **a mano** la versión mínima con persistencia en JSON (como el ejemplo).
3. Haz commit y abre un PR con esa versión.
4. En otra rama (`feature/cli-argparse`), pide ayuda a la IA con el prompt que te di y sube la versión refactorizada.
5. Documenta en `Modulo1/cli-tareas/notes.md` la comparación:
    - qué entendiste del código manual,
    - qué mejoró la IA,
    - qué partes todavía no entiendes del refactor.

---

### Lo que buscamos con esta clase

- Practicar **estructuras de control y funciones** en Python.
- Entender cómo se hace **persistencia básica** en un archivo.
- Empezar a ver la diferencia entre tu estilo manual y el “código pro” que escupe la IA.

En la clase 3 daremos el salto a **Clean Code y testing inicial**: ahí veremos cómo refactorizar para legibilidad y cómo escribir los primeros tests automatizados.

---

## Mi prompt

```sql
Tengo esto:

# tareas.py (Indicamos el nombre del archivo)

# ================================
# 0. IMPORTAR LIBRERIAS
# ================================

import sys
import json  # json nos permite guardar y cargar datos en un archivo
import os  # os nos permite interactuar con el sistema operativo

# (Cuidado, esta librería puede ser peligrosa y a veces los antivirus la detectan como malware)

# ================================
# 1. VARIABLES GLOBALES
# ================================

# Creamos la variable FILE y le asignamos el nombre del archivo de tareas
NOMBRE_ARCHIVO = "tareas.json"

# ================================
# 2. FUNCIONES
# ================================

# Esta función carga las tareas desde el archivo JSON
def cargar_tareas():

    # Si el archivo FILE no existe
    if not os.path.exists(NOMBRE_ARCHIVO):
        # creamos una lista vacía
        return []

    # Si el archivo FILE existe lo abrimos en modo lectura
    with open(NOMBRE_ARCHIVO, "r") as archivo_json:

        # cargamos el contenido con la librería json y lo devolvemos
        return json.load(archivo_json)

# Esta función guarda las tareas en el archivo JSON
def guardar_tareas(tareas):

    # Si el archivo FILE existe lo abrimos en modo escritura
    with open(NOMBRE_ARCHIVO, "w") as archivo_json:

        # guardamos el contenido con la librería json y con indentación de 2 espacios
        json.dump(tareas, archivo_json, indent=2)

# Esta función agrega una tarea a la lista de tareas
def agregar_tarea(nombre):

    # cargamos las tareas usando la función cargar_tareas que hemos creado anteriormente y lo guardamos en la variable tareas
    tareas = cargar_tareas()

    # creamos una nueva tarea con el id = longitud de la lista de tareas + 1, nombre y completada = False
    nueva = {"id": len(tareas) + 1, "nombre": nombre, "completada": False}

    # con append añadimos la nueva tarea a la lista de tareas
    tareas.append(nueva)

    # guardamos las tareas usando la función guardar_tareas que hemos creado anteriormente
    guardar_tareas(tareas)

# Esta función lista las tareas
def listar_tareas():

    # cargamos las tareas usando la función cargar_tareas que hemos creado anteriormente y lo guardamos en la variable tareas
    tareas = cargar_tareas()

    # por cada tarea en la lista de tareas
    for tarea in tareas:

        # si la tarea está completada, el estado es ✅, si no, es ❌
        estado = "✅" if tarea["completada"] else "❌"

        # imprimimos el id, nombre y estado de la tarea
        print(f"{tarea['id']}. {tarea['nombre']} {estado}")

# Esta función completa una tarea
def completar_tarea(id_tarea):

    # cargamos las tareas usando la función cargar_tareas que hemos creado anteriormente y lo guardamos en la variable tareas
    tareas = cargar_tareas()

    # por cada tarea en la lista de tareas
    for tarea in tareas:

        # si la tarea tiene el id igual a id_tarea
        if tarea["id"] == id_tarea:

            # cambiamos el estado de la tarea a completada
            tarea["completada"] = True

    # guardamos las tareas usando la función guardar_tareas que hemos creado anteriormente
    guardar_tareas(tareas)

# ================================
# 3. MAIN
# ================================

# con el nombre main, si el archivo se ejecuta directamente, se ejecuta el siguiente código
if __name__ == "__main__":

    # si el usuario no puso nada más después de "python tareas.py"
    if len(sys.argv) < 2:

        # imprimimos el mensaje de uso
        print("Uso: python tareas.py <comando>")

        # salimos del programa con el código 1
        sys.exit(1)

    # creamos la variable comando y metemos dentro el argumento
    comando = sys.argv[1]

    # si el comando es listar
    if comando == "listar":

        # llamamos a la función listar_tareas
        listar_tareas()

    # si el comando es agregar
    elif comando == "agregar":

        # si el usuario no puso el nombre de la tarea
        if len(sys.argv) < 3:

            # imprimimos el mensaje de error
            print("Falta el nombre de la tarea")

        # si el usuario puso el nombre de la tarea
        else:

            # llamamos a la función agregar_tarea
            agregar_tarea(sys.argv[2])

    # si el comando es completar
    elif comando == "completar":

        # si el usuario no puso el ID de la tarea
        if len(sys.argv) < 3:

            # imprimimos el mensaje de error
            print("Falta el ID de la tarea")

        # si el usuario puso el ID de la tarea
        else:

            # llamamos a la función completar_tarea
            completar_tarea(int(sys.argv[2]))

    # si el comando no es listar, agregar o completar
    else:

        # imprimimos el mensaje de error
        print("Comando no reconocido")

Rol: Dev Python senior
Contexto: Tengo un CLI básico de tareas que usa sys.argv para listar, agregar y completar tareas guardadas en JSON.
Objetivo: Refactorízalo usando argparse para un parsing de comandos más limpio, y separa el código en funciones claras.
Formato: Dame el código con comentarios explicativos.
```

## Respuesta de ChatGPT 5.

```sql
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

import argparse      # argparse: parsing de argumentos moderno y robusto
import json          # json: guardar/cargar las tareas
import os            # os: comprobar existencia de archivo
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
    nueva: Tarea = {"id": generar_nuevo_id(tareas), "nombre": nombre, "completada": False}
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
        description="CLI simple para gestionar tareas en un archivo JSON."
    )

    # Opción global para cambiar la ruta del archivo de almacenamiento
    parser.add_argument(
        "-f", "--file",
        default=NOMBRE_ARCHIVO_POR_DEFECTO,
        help=f"Ruta del archivo JSON de tareas (por defecto: {NOMBRE_ARCHIVO_POR_DEFECTO})"
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
    sp_completar = subparsers.add_parser("completar", help="Marca una tarea como completada")
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

```

Si has hecho justo lo que pedíamos en la **Clase 2**: primero tu versión manual clara y comentada, y luego la versión “refactor pro” con `argparse`.

Vamos a diseccionar qué ha pasado aquí, porque esto es oro para aprender:

---

### Lo que hiciste a mano (tu versión con `sys.argv`)

- **Claridad pedagógica**: cada función está comentada, cada paso explicado, el flujo se entiende perfecto.
- **Estructura básica pero completa**: entrada → proceso → salida → persistencia en JSON.
- **Limitaciones**: parsing manual de argumentos (si el usuario mete algo raro, toca validarlo a pelo), IDs generados como `len(lista)+1` (que se rompe si borras alguna tarea en el futuro).

---

### Lo que hizo la IA (versión con `argparse`)

- **Parsing robusto**: ahora los comandos (`listar`, `agregar`, `completar`) son subcomandos oficiales, con validación automática de parámetros. Si te equivocas en la sintaxis, `argparse` muestra ayuda.
- **Opciones globales**: añade `-file/-f` para cambiar el JSON. Esto da flexibilidad de trabajar con varios archivos.
- **Robustez en IDs**: genera el ID como `max(id) + 1` → evita colisiones si en el futuro implementas `borrar`.
- **Manejo de errores**: controla JSON corrupto o vacío devolviendo lista vacía.
- **Capas separadas**:
    - Acceso a datos (I/O) → `cargar_tareas`, `guardar_tareas`.
    - Lógica de negocio → `agregar_tarea`, `listar_tareas`, `completar_tarea`.
    - CLI / interfaz → `construir_parser`, comandos adaptadores.
        
        Esto ya es arquitectura en miniatura.
        

---

### Qué significa esto para ti ahora

1. **Tu versión** es *perfecta para aprender*: la entiendes entera, sabes lo que hace cada línea.
2. **La versión IA** es *perfecta para crecer*: modularidad, buenas prácticas, escalabilidad.

Si hubieras empezado directamente con la segunda, te habrías perdido la comprensión del flujo básico. Ahora tienes ambas perspectivas y sabes qué aporta cada estilo.

---

### Próximo paso recomendado

- Deja en tu repo **dos ramas**:
    - `feature/cli-json` → tu versión manual.
    - `feature/cli-argparse` → la versión refactorizada por IA.
- Documenta en `notes.md` (con el esquema que te pasé) **qué entiendes y qué dudas te deja la versión IA**.
- En la **Clase 3** vamos a atacar justo esas dudas: refactorizar para **Clean Code** y meter **tests automáticos** (para que puedas verificar que ambas versiones se comportan igual).
Con esto ya tienes un CLI **mínimo pero funcional**.
