# Clase 3 – Clean Code y testing inicial

Perfecto. Ya tenemos claras la **Clase 1 (pensamiento computacional + CLI mínimo)** y la **Clase 2 (fundamentos de programación + persistencia JSON + argparse)**.

La **Clase 3** de este Módulo 1, según el plan del máster, toca entrar en dos piezas clave:

- **Clean Code**: cómo escribir código legible, mantenible y fácil de refactorizar. Aquí veremos principios básicos (nombres claros, funciones cortas, separar responsabilidades, evitar duplicación).
- **Testing inicial**: empezar con tests unitarios muy simples, para verificar que nuestro CLI funciona igual después de los refactors.

El objetivo es que tu app de tareas pase de “funciona” a “se entiende y se puede comprobar automáticamente”.

---

### Esquema de la Clase 3

**Concepto**

- Qué significa Clean Code y por qué es más importante que “hacerlo funcionar”.
- Primeros pasos con testing: usar `unittest` en Python para probar funciones como `agregar_tarea`, `listar_tareas` o `completar_tarea`.

**Aplicación manual**

- Refactorizar el código del CLI (ya sea tu versión manual o la de `argparse`).
- Crear un archivo `test_tareas.py` con un par de pruebas unitarias que verifiquen:
    - Que al agregar se incrementa la lista de tareas.
    - Que al completar, el estado de la tarea cambia a `True`.

**Aplicación con IA**

- Prompt para pedirle a la IA que te ayude a aplicar Clean Code (por ejemplo: “refactoriza mis funciones para que no tengan efectos secundarios ocultos”).
- Prompt para que genere tests unitarios adicionales y explique qué cubren.

Empecemos:

---

### Clase 3 – Clean Code y Testing inicial

Hasta ahora tu app de tareas **funciona**, pero todavía tiene ese “olor” a código de principiante: comentarios que explican lo obvio, funciones con responsabilidades mezcladas, y nada que garantice que el programa siga funcionando después de un cambio.

Lo que toca hoy es **pasar de “funciona” a “se puede mantener”**.

### 1. Clean Code en pequeñito

No vamos a estudiar un libro entero de Robert C. Martin, pero sí algunos principios básicos que te sirven ya:

- **Nombres claros**: variables y funciones que se expliquen solas. `cargar_tareas` se entiende, `ct()` no.
- **Funciones cortas**: que hagan **una sola cosa**. Si tu función hace dos o tres cosas, sepárala.
- **Eliminar comentarios innecesarios**: si el código se explica solo, no hace falta comentar “abrimos el archivo en modo lectura”. El comentario debe aportar contexto, no repetir lo obvio.
- **Evitar duplicación**: si tienes el mismo bloque de código en dos sitios, conviértelo en función.
- **Separar capas**:
    - lógica de negocio (agregar, completar),
    - acceso a datos (leer/escribir JSON),
    - interfaz (CLI).
        
        Esa separación la IA ya la hizo en la versión con `argparse`, pero tú debes entenderla.
        

La idea es que cualquier dev (incluido tu “yo del futuro”) pueda leer tu código y entenderlo sin un máster en jeroglíficos.

### 2. Introducción al testing

Testing no es magia. En Python, lo mínimo se hace con `unittest`.

Un **test unitario** es solo una función que comprueba que otra función hace lo que esperamos.

Ejemplo sencillo:

```python
import unittest
from tareas import agregar_tarea, cargar_tareas, guardar_tareas

class TestTareas(unittest.TestCase):

    def setUp(self):
        # Preparamos un archivo temporal vacío antes de cada test
        self.archivo = "test_tareas.json"
        guardar_tareas(self.archivo, [])

    def test_agregar_tarea(self):
        agregar_tarea(self.archivo, "Estudiar IA")
        tareas = cargar_tareas(self.archivo)
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
        self.assertFalse(tareas[0]["completada"])

if __name__ == "__main__":
    unittest.main()
```

Con esto, cuando corras:

```bash
python -m unittest test_tareas.py
```

Ves si tu función hace lo correcto.

---

### 3. El ciclo “Refactor con seguridad”

- **Primero** escribes o ajustas un test.
- **Luego** haces un cambio en el código para limpiarlo.
- **Después** corres los tests.
- Si todo sigue verde ✅, sabes que el refactor no rompió nada.

Esto es la semilla de **TDD (Test Driven Development)**, pero de momento con que uses tests para **validar tus refactors** es suficiente.

---

### 4. Ejercicio de esta clase

1. Crea una rama `feature/cli-clean-tests`.
2. Refactoriza tu código aplicando: nombres claros, menos comentarios obvios, funciones cortas y capas separadas.
3. Escribe un `test_tareas.py` con al menos 2 tests unitarios: uno para `agregar_tarea`, otro para `completar_tarea`.
4. Ejecuta los tests. Comprueba que todo sigue funcionando.
5. Documenta en tu `notes.md` qué cambios hiciste y cómo los tests te dieron confianza para limpiar código sin miedo.

---

Lo que buscamos aquí no es que seas un fanático de “Clean Code”, sino que empieces a **oler cuándo tu código puede mejorar** y uses los tests como tu red de seguridad.

---

Aqui dejo el [tareas.py](http://tareas.py) refactorizado, con capas separadas, argparse, los tests, y todo explicado:

## Meta-objetivo de hoy

1. Mantener el comportamiento. 2) Hacer el código más legible. 3) Prepararlo para testear sin miedo.
    
    Estrategia: pequeños cambios → ejecutar → comprobar.
    

## Paso 0 — Pequeño “cambio de mentalidad”

- Comentarios que repiten lo obvio (tipo “abrimos archivo en lectura”) **se van**. (ya los explicamos en la clase anterior)
- Comentarios que explican una **decisión** o **convención** **se quedan**.
- Nombres y estructura deben contar la historia: funciones cortas y con **una sola responsabilidad**.

## Paso 1 — Extraer constantes y tipar un poco

La idea: nombres claros + una mínima pista de tipos (para lector humano y tu editor/IA).

```sql
# tareas.py

from typing import TypedDict, List
import json, os, sys

ARCHIVO_POR_DEFECTO = "tareas.json"

class Tarea(TypedDict):
    id: int
    nombre: str
    completada: bool

```

**Por qué**: `ARCHIVO_POR_DEFECTO` deja claro el contrato del programa. `Tarea` te da estructura mental (y autocompletado).

Si nunca has visto una clase, seguro que te acaba de explotar la cabeza, no te preocupes, vamos a explicarlo:

### Qué es eso de `class Tarea(TypedDict)`

- En Python, una **clase** (`class`) normalmente sirve para definir **objetos** (con atributos y métodos).

- Ejemplo típico:

```python
class Perro:
    def __init__(self, nombre):
        self.nombre = nombre

    def ladrar(self):
        print("Guau!")

```

Pero aquí **no hemos creado un objeto** nuevo. Lo que usamos es algo más ligero: **TypedDict**.

### Qué es `TypedDict`

- `TypedDict` viene del módulo `typing`.
- Sirve solo para **documentar** qué claves y tipos tiene un diccionario.
- No cambia cómo corre tu programa; es una **pista para humanos y para el editor/IA**.

Ejemplo:

```python
from typing import TypedDict

class Tarea(TypedDict):
    id: int
    nombre: str
    completada: bool
```

Esto equivale a decir: “una tarea es un diccionario con tres claves (`id`, `nombre`, `completada`) y esos tipos de datos”.

En tiempo de ejecución sigue siendo un `dict` normal:

```python
t: Tarea = {"id": 1, "nombre": "Estudiar IA", "completada": False}
print(t["nombre"])  # funciona igual que un dict

```

### ¿Por qué te lo metí ahí?

Porque en **Clean Code** es útil que cualquiera que lea tu función vea enseguida qué estructura manejas.

Ejemplo:

```python
def agregar_tarea(ruta: str, nombre: str) -> Tarea:
    ...
```

Ese `-> Tarea` le dice al lector: “esto devuelve un diccionario con esas tres claves”.

### ¿Qué hacer tú ahora?

- Si todavía no quieres liarte con clases ni `TypedDict`, puedes **borrarlo** y quedarte solo con `dict`.
- Ejemplo versión sin `class`:

```python
def agregar_tarea(ruta: str, nombre: str) -> dict:
    ...

```

El programa funciona igual.

Cuando te sientas cómodo, puedes añadir `TypedDict` como un **truco de legibilidad**.

## Paso 2 — Capa de acceso a datos limpia (I/O)

Quitamos comentarios redundantes y hacemos funciones cortas. Mantengo un comentario contextual donde aporta.

```python
def cargar_tareas(ruta: str) -> List[Tarea]:
    """Devuelve la lista de tareas. Si no hay archivo o está vacío/corrupto, lista vacía."""
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else []
    except json.JSONDecodeError:
        # Decisión: no romper por JSON corrupto; devolvemos vacío para que el CLI siga siendo usable.
        return []

def guardar_tareas(ruta: str, tareas: List[Tarea]) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

```

## Paso 3 — Lógica de dominio pequeña y directa

- **Una función = una acción**.
- IDs robustos con `max(id)+1` (por si en el futuro borras).

```python
def nuevo_id(tareas: List[Tarea]) -> int:
    return 1 if not tareas else max(t["id"] for t in tareas) + 1

def agregar_tarea(ruta: str, nombre: str) -> Tarea:
    tareas = cargar_tareas(ruta)
    tarea: Tarea = {"id": nuevo_id(tareas), "nombre": nombre, "completada": False}
    tareas.append(tarea)
    guardar_tareas(ruta, tareas)
    return tarea  # devolver la entidad ayuda en tests

def listar_tareas(ruta: str) -> List[Tarea]:
    return cargar_tareas(ruta)

def completar_tarea(ruta: str, id_tarea: int) -> bool:
    tareas = cargar_tareas(ruta)
    for t in tareas:
        if t["id"] == id_tarea:
            t["completada"] = True
            guardar_tareas(ruta, tareas)
            return True
    return False  # no encontrada

```

Fíjate que ahora **no imprimimos** dentro de la lógica: devolvemos datos. Imprimir es cosa del CLI. Esto facilita los **tests**.

## Paso 4 — Interfaz mínima (CLI) con `sys.argv` (todavía)

Seguimos con tu estilo de la clase anterior, solo **usamos las funciones nuevas**. Esto mantiene tu aprendizaje y te prepara para `argparse` sin romper nada.

```python
def uso():
    print("Uso: python tareas.py <listar|agregar|completar> [args]")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        uso()

    comando = sys.argv[1]
    archivo = ARCHIVO_POR_DEFECTO  # podrías añadir más tarde -f <ruta>

    if comando == "listar":
        for t in listar_tareas(archivo):
            estado = "✅" if t["completada"] else "❌"
            print(f"{t['id']}. {t['nombre']} {estado}")

    elif comando == "agregar":
        if len(sys.argv) < 3:
            print("Falta el nombre de la tarea"); sys.exit(1)
        tarea = agregar_tarea(archivo, sys.argv[2])
        print(f"Agregada: {tarea['id']}. {tarea['nombre']}")

    elif comando == "completar":
        if len(sys.argv) < 3:
            print("Falta el ID de la tarea"); sys.exit(1)
        ok = completar_tarea(archivo, int(sys.argv[2]))
        print("Completada ✅" if ok else "No encontrada ❌")

    else:
        print("Comando no reconocido"); uso()

```

**Qué cambió vs tu versión**

- La lógica ya **no imprime** ni lee `sys.argv` → **separación de capas** real.
- Las funciones **devuelven datos** (útil para tests y para futuras UIs).
- Los comentarios se reducen a **decisiones** y **contratos**.

## Paso 5 — Tests iniciales (sin magia)

Creamos `test_tareas.py`. Usamos un **archivo temporal** para no tocar tu `tareas.json`.

```python
# test_tareas.py
import os, tempfile, unittest
from tareas import guardar_tareas, cargar_tareas, agregar_tarea, completar_tarea, listar_tareas

class TestTareas(unittest.TestCase):
    def setUp(self):
        fd, self.tmp = tempfile.mkstemp(prefix="tareas_", suffix=".json")
        os.close(fd)          # cerramos el descriptor; usaremos la ruta
        guardar_tareas(self.tmp, [])  # empezamos limpio

    def tearDown(self):
        os.remove(self.tmp)

    def test_agregar_tarea(self):
        agregar_tarea(self.tmp, "Estudiar IA")
        tareas = cargar_tareas(self.tmp)
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
        self.assertFalse(tareas[0]["completada"])

    def test_completar_tarea(self):
        t = agregar_tarea(self.tmp, "Repasar Git")
        ok = completar_tarea(self.tmp, t["id"])
        self.assertTrue(ok)
        tareas = listar_tareas(self.tmp)
        self.assertTrue(tareas[0]["completada"])

    def test_completar_inexistente(self):
        guardar_tareas(self.tmp, [])
        ok = completar_tarea(self.tmp, 999)
        self.assertFalse(ok)

if __name__ == "__main__":
    unittest.main()

```

Ejecutas:

```bash
python -m unittest -v

```

**Qué aprendes aquí**

- `setUp/tearDown`: cada test empieza/termina limpio.
- Las funciones devuelven valores útiles → tests simples y claros.
- Nada de mocks exóticos todavía: **archivito temporal y a correr**.

## Paso 6 — Check rápido de “Clean Code”

Haz esta mini-checklist en tu `tareas.py`:

- [ ]  ¿Los nombres cuentan la historia? (`agregar_tarea`, no `agregar` a secas).
- [ ]  ¿Cada función hace **una cosa**?
- [ ]  ¿La lógica no imprime ni lee argumentos?
- [ ]  ¿Los comentarios que quedan aportan contexto/decisión?
- [ ]  ¿Puedo testear sin tocar el mundo real? (sí, paso ruta de archivo).

---

## Mini-ejercicio (tu PR de la clase)

1. Crea rama `feature/cli-clean-tests`.
2. Aplica los pasos 1–4 a tu repo.
3. Añade `test_tareas.py` y ejecuta `python -m unittest -v`.
4. Abre PR. En la descripción pega:
    - Qué cambiaste (separación de capas, nombres, return de datos).
    - Qué tests añadiste y por qué.

---

## “Aplicación con IA” (pero guiada por ti)

Cuando lo tengas verde, pide a la IA un segundo PR **solo** para migrar el CLI a `argparse` sin tocar la lógica:

```
Rol: Revisor Python.
Contexto: Tengo lógica de dominio en tareas.py que ya devuelve datos y no imprime. Quiero migrar la capa CLI a argparse sin cambiar firmas de funciones.
Entrega: un diff o archivo CLI con argparse, subcomandos (listar/agregar/completar) y opción global -f/--file para ruta JSON. Sin modificar la lógica ni los tests.

```

Así aprendes tú, y la IA **se limita** a la capa de interfaz.

Con esto tienes una clase completa, paso a paso, **sin perder la parte didáctica**. El siguiente peldaño, cuando te sientas cómodo, es añadir **formato de salida** (ej. `--json` en el CLI) y un par de tests más (IDs, vacíos, JSON corrupto). ¿Te monto luego una propuesta de esos dos incrementos para tu siguiente PR?