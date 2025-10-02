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