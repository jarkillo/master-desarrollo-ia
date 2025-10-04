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

## Paso 5.1. - Explicación del Test

Antes de ver`test_tareas.py` tenemos que explicarlo por si **nunca en tu vida has escrito un test**

y lo que tienes delante es como un ritual extraño.

Vamos a verlo como un experimento de laboratorio: probamos una función → vemos si hace lo que prometió.

### ¿Qué es un test?

Un **test** no es más que un mini-programa que llama a tus funciones y comprueba que el resultado sea correcto.

Es como si dijeras: *“oye función, te doy esto y tendrias que devolverme esto… al pasar el test comprobamos que el resultado sea correcto”*.

Seguramente alguno habreis visto test con pytest, esto lo veremos más adelante, de momento usaremos unittest que es mucho mas simple.

### El archivo `test_tareas.py`

Vamos a destripar el `test_tareas.py` línea a línea, como si estuviéramos juntos leyéndolo y entendiendo qué hace cada trocito. Así te quedas con la **plantilla mental** para cualquier test futuro.

### Paso 1 – Importamos cosas

```python
import os, tempfile, unittest
from tareas import guardar_tareas, cargar_tareas, agregar_tarea, completar_tarea, listar_tareas
```

- `unittest` → librería de Python para escribir tests (ya viene instalada).
- `tempfile` → nos deja crear un archivo temporal, así no tocamos tu `tareas.json` real.
- Importamos las funciones que vamos a probar (`agregar_tarea`, `completar_tarea`, etc.).

### Paso 2 – Creamos una “caja de pruebas”

```python
class TestTareas(unittest.TestCase):
```

Aquí juntamos todas las pruebas. Piensa que es como un cuaderno: cada método dentro es una comprobación.

### Paso 3 – Preparar y limpiar

```python
    def setUp(self):
        fd, self.tmp = tempfile.mkstemp(prefix="tareas_", suffix=".json")
        os.close(fd)
        guardar_tareas(self.tmp, [])

    def tearDown(self):
        os.remove(self.tmp)
```

- `setUp` → se ejecuta **antes de cada prueba**. Crea un archivo vacío.
- `tearDown` → se ejecuta **después de cada prueba**. Borra el archivo.
    
    Así cada prueba empieza desde cero, sin basura de pruebas anteriores.
    

### Paso 4 – Una prueba sencilla

```python
    def test_agregar_tarea(self):
        agregar_tarea(self.tmp, "Estudiar IA")
        tareas = cargar_tareas(self.tmp)
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
        self.assertFalse(tareas[0]["completada"])
```

Traducción a lenguaje humano:

1. Agrego una tarea llamada “Estudiar IA”.
2. Vuelvo a leer el archivo.
3. Compruebo tres cosas:
    - La lista tiene 1 tarea.
    - El nombre es el correcto.
    - La tarea no está completada.

### Paso 5 – Otra prueba

```python
    def test_completar_tarea(self):
        t = agregar_tarea(self.tmp, "Repasar Git")
        ok = completar_tarea(self.tmp, t["id"])
        self.assertTrue(ok)
        tareas = listar_tareas(self.tmp)
        self.assertTrue(tareas[0]["completada"])

```

Aquí lo que hacemos es:

1. Crear una tarea.
2. Llamar a `completar_tarea`.
3. Comprobar que la función nos dijo “sí, la completé” (`ok = True`).
4. Ver que efectivamente en la lista aparece como completada.

### Paso 6 – Caso raro

```python
    def test_completar_inexistente(self):
        guardar_tareas(self.tmp, [])
        ok = completar_tarea(self.tmp, 999)
        self.assertFalse(ok)
```

Aquí probamos qué pasa si intentas completar una tarea que **no existe**.

Esperamos que la función devuelva `False` (fallo controlado).

### Paso 7 – Lanzar los tests

```python
if __name__ == "__main__":
    unittest.main()
```

Esto hace que si ejecutas el archivo, todos los tests se corran automáticamente.

En la terminal:

```bash
python -m unittest -v
```

Verás algo como:

```
test_agregar_tarea ... ok
test_completar_tarea ... ok
test_completar_inexistente ... ok
```

Si algo falla, Python te dirá cuál test y por qué.

---

### Resumen mental

- **Cada test = una pequeña historia**: “si hago X, espero Y”.
- `assertEqual`, `assertTrue`, `assertFalse` son formas de decir *“comprueba que esto sea así”*.
- Usamos un **archivo temporal** para que no rompas tu app real al probar.

## Paso 8 — Comprobación de lista vacia

Vamos a escribir un **test para `listar_tareas`** en el caso de que la lista esté vacía y también cuando tenga varias tareas. Así te queda claro cómo comprobar listas. 

No lo copies, intenta hacerlo tu primero, y cuando estes muy atascado y ya no se te ocurra, miras la solución.

### Caso 1: lista vacía

```python
    def test_listar_vacio(self):
        # Arrancamos con el archivo vacío
        guardar_tareas(self.tmp, [])

        tareas = listar_tareas(self.tmp)

        # La lista debe estar vacía
        self.assertEqual(tareas, [])
```

Traducción:

- Guardo explícitamente una lista vacía en el archivo temporal.
- Llamo a `listar_tareas`.
- Compruebo que lo que devuelve es una lista vacía (`[]`).

### Caso 2: lista con varias tareas

```python
    def test_listar_con_tareas(self):
        # Agrego dos tareas
        agregar_tarea(self.tmp, "Estudiar IA")
        agregar_tarea(self.tmp, "Repasar Git")

        tareas = listar_tareas(self.tmp)

        # Debe haber 2 tareas
        self.assertEqual(len(tareas), 2)

        # Verificamos que los nombres están correctos
        self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
        self.assertEqual(tareas[1]["nombre"], "Repasar Git")

        # Ambas deben empezar como no completadas
        self.assertFalse(tareas[0]["completada"])
        self.assertFalse(tareas[1]["completada"])

```

Traducción:

- Meto dos tareas en el archivo temporal.
- Al listar, espero exactamente 2.
- Compruebo que los nombres coinciden y que ninguna está completada.

### Salida esperada

Al correr `python -m unittest -v`, ahora deberías ver también:

```
Ran 5 tests in 0.016s

OK
```

---

Esto ya te cubre los **4 escenarios básicos** de tu app:

1. Agregar una tarea.
2. Completar una tarea.
3. Completar algo que no existe.
4. Listar en vacío y con varias tareas.

Con eso tienes un **mini-escudo** que te avisa si al refactorizar rompes algo sin darte cuenta.

## Paso 9 — Check rápido de “Clean Code”

Haz esta mini-checklist en tu `tareas.py`:

- [ ]  ¿Los nombres cuentan la historia? (`agregar_tarea`, no `agregar` a secas).
- [ ]  ¿Cada función hace **una cosa**?
- [ ]  ¿La lógica no imprime ni lee argumentos?
- [ ]  ¿Los comentarios que quedan aportan contexto/decisión?
- [ ]  ¿Puedo testear sin tocar el mundo real?

---

## Mini-ejercicio (tu PR de la clase)

1. Crea rama `feature/cli-clean-tests`.
2. Aplica los pasos 1–8 a tu repo.
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

Con esto tienes una clase completa, paso a paso, **sin perder la parte didáctica**. El siguiente peldaño, cuando te sientas cómodo, es añadir **formato de salida** (ej. `--json` en el CLI) y un par de tests más (IDs, vacíos, JSON corrupto). 

## De momento para estas pruebas estamos usando ChatGPT 5 en auto. Puedes probar con diferentes IA para ver el resultado que da cada una.

Mi prompt:

```sql
Tengo esto:

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

Rol: Revisor Python.
Contexto: Tengo lógica de dominio en tareas.py que ya devuelve datos y no imprime. Quiero migrar la capa CLI a argparse sin cambiar firmas de funciones.

Entrega: un diff o archivo CLI con argparse, subcomandos (listar/agregar/completar) y opción global -f/--file para ruta JSON. Sin modificar la lógica ni los tests.
```

Respuesta GPT

```sql
Perfecto, Quillo. Mantengo tareas.py tal cual (sin tocar firmas ni lógica) y te doy un CLI separado con argparse: tareas_cli.py. Usa subcomandos listar | agregar | completar y una opción global -f/--file para la ruta del JSON.

tareas_cli.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI para el gestor de tareas usando argparse.
No modifica la lógica de dominio en tareas.py.
"""

import argparse
import sys

# Importa la lógica existente sin cambiar firmas
from tareas import (
    ARCHIVO_POR_DEFECTO,
    listar_tareas,
    agregar_tarea,
    completar_tarea,
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
        "-f", "--file",
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
```

Lo que ha devuelto la IA es un nuevo archivo tareas-cli.py

Deja **la lógica en `tareas.py`** y mueve **la interfaz de línea de comandos** a un archivo aparte, `tareas_cli.py`. Eso te permite testear la lógica sin pelearte con argumentos de terminal. Vamos a leerlo con gafas de aprendiz y a usarlo paso a paso.

## Qué es `tareas_cli.py` (en cristiano)

- **Tu “mando a distancia”**: recoge lo que escribes en la terminal, lo interpreta con `argparse` y llama a las funciones de `tareas.py`.
- **Subcomandos**: `listar`, `agregar`, `completar`.
- **Opción global `f/--file`**: eliges qué archivo JSON usar (por defecto, `tareas.json`).

Separar “mando” (CLI) de “motor” (lógica) es la base de un proyecto limpio: el motor se testea fácil; el mando se cambia sin tocar el motor.

## Cómo se usa (pruébalo ya)

Desde la carpeta del proyecto:

```bash
# 1) Listar (si no hay archivo o está vacío, no pasa nada)
python tareas_cli.py listar

# 2) Agregar tareas (nota: permite espacios en el nombre)
python tareas_cli.py agregar "Estudiar IA con Manu"
python tareas_cli.py agregar Repasar Git

# 3) Completar por ID (empiezan en 1, 2, 3…)
python tareas_cli.py completar 1

# 4) Usar otro archivo distinto
python tareas_cli.py -f tareas_demo.json agregar "Probar archivo alternativo"
python tareas_cli.py -f tareas_demo.json listar

```

Verás las marquitas ✅/❌ y mensajes como “Agregada: 1. Estudiar IA con Manu”.

## Lectura guiada (qué hace cada parte)

- `build_parser()` define el “diccionario de la terminal”:
    - `f/--file` → ruta del JSON (default: `ARCHIVO_POR_DEFECTO` de tu `tareas.py`).
    - Subcomandos:
        - `listar` → llama a `cmd_listar`.
        - `agregar nombre...` → `nargs="+"` permite nombres con espacios; luego los une en el comando.
        - `completar id` → recibe el id como texto y luego lo convierte a `int`.
- `cmd_*` son “adaptadores”: traducen argumentos → llaman a tu lógica → imprimen salida.
- `main()` parsea los argumentos y ejecuta la función del subcomando elegido; devuelve un **código de salida** (0 = ok, 1/2 = error). Esto es útil si algún día automatizas con scripts o CI.

---

## Dos mini-mejoras (para que aprendas afinando)

1. **Parsear el `id` como entero directamente en argparse**. Así evitas el `try/except` manual:

```python
p_completar.add_argument("id", type=int, help="ID numérico de la tarea a completar.")

```

y en `cmd_completar` ya recibes `args.id` como `int`.

1. **Mensaje amable si no hay tareas** (solo en el CLI; la lógica sigue devolviendo lista vacía):

```python
def cmd_listar(args):
    tareas = listar_tareas(args.file)
    if not tareas:
        print("No hay tareas aún. Usa 'agregar' para crear la primera.")
        return 0
    for t in tareas:
        estado = "✅" if t["completada"] else "❌"
        print(f"{t['id']}. {t['nombre']} {estado}")
    return 0

```

Estas mejoras no tocan tu “motor” y hacen la experiencia más clara.

---

## Cómo encaja con tus tests

- Tus tests unitarios siguen apuntando a **`tareas.py`** (motor). Perfecto.
- Si más adelante quieres probar el CLI, lo haces aparte, con **tests de integración** (por ejemplo, ejecutando `python tareas_cli.py ...` con `subprocess` y mirando la salida). De momento no hace falta: **primero consolida la lógica**, que ya estás testando bien. (No te marees con el subprocess, la idea es que te vayan sonando los conceptos)

## Qué subir al repo (y rama sugerida)

1. Crea rama: `feature/cli-argparse-separado`.
2. Añade `tareas_cli.py` tal como te lo dieron (o con las 2 mini-mejoras).
3. Mantén `tareas.py` y `test_tareas.py` **sin cambios funcionales**.
4. En el PR, explica: “Se separa CLI de la lógica. `tareas_cli.py` usa argparse; `tareas.py` queda testeable y estable”.

