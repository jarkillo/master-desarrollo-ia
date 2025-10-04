# Clase 4 – Testing ampliado y primeros principios SOLID

### Escenario inicial

Ya tienes un CLI que:

- Agrega tareas.
- Lista tareas.
- Marca tareas como completadas.
- Tiene **tests unitarios básicos** (agregar, completar, listar).

Hasta aquí, bien.

Pero en el mundo real, la historia no se detiene. Te piden una **nueva feature**: *“necesitamos prioridades en las tareas (alta, media, baja) y poder filtrarlas”*.

Tu reacción natural como dev novato podría ser:

*“Bueno, meto un nuevo campo `prioridad` en el diccionario y apaño las funciones para que lo impriman”*.

### El problema

Si haces eso sin cuidado:

- Cambias la estructura de datos → **rompes funciones** sin darte cuenta.
- Los tests que escribiste antes quizás fallen, o peor: no fallen aunque el programa ya tenga inconsistencias.
- El archivo empieza a tener funciones que hacen demasiadas cosas (olor a spaghetti).

Aquí es donde se juntan dos ideas:

1. **Tests más fuertes** → te avisan de qué rompiste al tocar la estructura.
2. **Principio de responsabilidad única (SRP de SOLID)** → cada función o módulo debe tener un motivo único para cambiar.

---

👉 Primer mini-ejercicio:

Mira tu función `agregar_tarea` actual. Si ahora necesita guardar también `prioridad`, ¿qué cambiarías exactamente en esa función y en sus tests?

(Haz un apunte mental o anótalo en tu repo. No lo codifiques aún. Queremos ver dónde empieza a doler antes de sacar la “cura”).

¿Se te ha ocurrido esto?

En la clase:

```
# ================================
# 1.1. TIPOS DE DATOS
# ================================
class Tarea(TypedDict):
    id: int
    nombre: str
    completada: bool
    prioridad: str 
```

En agregar tarea

```sql
def agregar_tarea(ruta: str, nombre: str, prioridad: str) -> Tarea:
    """Crea una nueva tarea no completada y la persiste."""

    tareas = cargar_tareas(ruta)
    tarea: Tarea = {"id": nuevo_id(tareas), "nombre": nombre, "completada": False, "prioridad": prioridad}
    tareas.append(tarea)
    guardar_tareas(ruta, tareas)
    return tarea  # devolver la entidad ayuda en tests 
```

Exacto, ese es el movimiento natural: añadir un campo nuevo y extender la función.

Lo interesante es que al hacerlo… ya has creado **un punto de dolor**:

1. Todos los lugares donde se llama a `agregar_tarea` ahora **rompen**, porque piden solo `(ruta, nombre)` y tú exiges `(ruta, nombre, prioridad)`.
2. Tus **tests anteriores** tampoco compilan ni pasan, porque no saben qué es `prioridad`.
3. Si alguien se olvida de pasar la prioridad, se lía.

Y aquí entra la magia de lo que estamos aprendiendo hoy:

- **Los tests te sirven de alarma**: si tu cambio rompe algo, lo detectas antes de usar el programa.
- **SOLID te da brújula**: “cada función debería tener un único motivo para cambiar”. Tu función `agregar_tarea` está asumiendo varias responsabilidades (crear estructura, decidir ID, meter la prioridad, guardar en disco).

---

Lo que vamos a hacer ahora es **reforzar un test existente** para incluir la prioridad, antes incluso de tocar más funciones. Así practicamos cómo los tests te dan red de seguridad.

Por ejemplo, tu test de agregar podría ampliarse así:

```python
def test_agregar_tarea_con_prioridad(self):
    t = agregar_tarea(self.tmp, "Estudiar IA", "alta")
    tareas = cargar_tareas(self.tmp)
    self.assertEqual(len(tareas), 1)
    self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
    self.assertEqual(tareas[0]["prioridad"], "alta")
    self.assertFalse(tareas[0]["completada"])

```

Si corres este test ahora, ¿qué pasará?

- Si ya cambiaste la función como escribiste, pasará ✅.
- Si alguien sigue usando la versión vieja de `agregar_tarea`, fallará ❌.

¿Que sucedio? ¿Te ha ocurrido este error?

```sql
======================================================================
ERROR: test_completar_tarea (__main__.TestTareas.test_completar_tarea)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "e:\master-ia-manu\Modulo 1 – Fundamentos Dev y pensamiento\Clase 4 – Testing ampliado y primeros principios SOLID\cli-tareas\test_tareas.py", line 41, in test_completar_tarea
    tarea = agregar_tarea(self.tmp, "Repasar Git")
TypeError: agregar_tarea() missing 1 required positional argument: 'prioridad'

======================================================================
ERROR: test_listar_con_tareas (__main__.TestTareas.test_listar_con_tareas)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "e:\master-ia-manu\Modulo 1 – Fundamentos Dev y pensamiento\Clase 4 – Testing ampliado y primeros principios SOLID\cli-tareas\test_tareas.py", line 63, in test_listar_con_tareas
    agregar_tarea(self.tmp, "Estudiar IA")
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: agregar_tarea() missing 1 required positional argument: 'prioridad'

----------------------------------------------------------------------
Ran 5 tests in 0.009s

FAILED (errors=2)
```

Perfecto: tus tests han fallado **como deben**. Has cambiado la firma de `agregar_tarea` y los tests antiguos no pasan la nueva `prioridad`. Antes de ponernos finos con SOLID, vamos a **desbloquear la suite** sin romper a nadie.

## Paso 1 — Cambio no rompedor (retrocompatibilidad)

Haz que `agregar_tarea` acepte una prioridad **por defecto**. Así los tests antiguos (que no pasan prioridad) vuelven a funcionar y podemos migrarlos con calma.

```python
from typing import Literal

PRIORIDADES = ("alta", "media", "baja")

def _normaliza_prioridad(p: str) -> str:
    p = (p or "").lower()
    return p if p in PRIORIDADES else "media"

def agregar_tarea(ruta_archivo: str, nombre_tarea: str, prioridad: str = "media") -> dict:
    """Crea una tarea (por defecto prioridad='media'), la guarda y la devuelve."""
    if prioridad not in PRIORIDADES_VALIDAS:
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

```

Antes de cambiar nada, he colado un detallito que seguro que habras visto en los codigos que te ha dado la IA.

una variable llamada p.

Quizas, cuando lo escribe la IA o lo escribes tu, lo entiendes del tirón. Pero… ¿Qué ocurrirá dentro de 6 meses? ¿Y si le das este codigo a otro desarrollador?

Va a perder horas trazando el codigo para descubrir que querias decir con “p”

Esto es algo que la IA hace con muchisima frecuencia. Y si te dedicas a copiar y pegar, luego no entenderás nada de lo que está haciendo.

Un dev humano que lea `t["prioridad"]` o una variable llamada `t` se queda pensando: “¿t de qué? ¿trabajo? ¿task? ¿taza de café?”

Esto conecta directamente con **Clean Code** y con el primer principio de **SOLID (Single Responsibility Principle)**: cada parte del código debería contar su historia de forma clara y tener un único motivo para cambiar. Si encima usas nombres crípticos, la historia se convierte en jeroglífico.

la forma correcta sería:

```sql
PRIORIDADES = ("alta", "media", "baja")

def _normaliza_prioridad(prioridad: str) -> str:
    """Devuelve la prioridad normalizada o 'media' si es inválida."""
    prioridad_normalizada = (prioridad or "").lower()
    return prioridad_normalizada if prioridad_normalizada in PRIORIDADES else "media"
```

Siempre hay que preocuparse de dejar código legible.

## Paso 2 — Backfill suave al leer (por si hay JSON viejo)

Si ya tienes `tareas.json` (porque has ejecutado el programa) sin el campo, añadimos la prioridad al vuelo al cargar para que nada explote.

```python
def cargar_tareas(ruta_archivo: str) -> list[dict]:
    if not os.path.exists(ruta_archivo):
        return []

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as fichero:
            contenido = fichero.read().strip()
            lista_tareas = json.loads(contenido) if contenido else []
    except json.JSONDecodeError:
        return []

    # Aseguramos que cada tarea tenga 'prioridad'
    for tarea in lista_tareas:
        if "prioridad" not in tarea or tarea["prioridad"] not in PRIORIDADES_VALIDAS:
            tarea["prioridad"] = "media"

    return lista_tareas

```

Con esto, tus dos tests que llamaban `agregar_tarea(self.tmp, "…")` **dejan de petar** porque la prioridad tiene valor por defecto.

## Paso 3 — Añade 1 test nuevo (cubrir la nueva feature)

Ahora sí, sumamos una prueba mínima para la prioridad (sin reescribir todo tu suite):

```python
def test_agregar_tarea_prioridad_por_defecto(self):
    nueva = agregar_tarea(self.tmp, "Repasar SOLID")  # sin prioridad
    self.assertEqual(nueva["prioridad"], "media")

def test_agregar_tarea_con_prioridad_alta(self):
    nueva = agregar_tarea(self.tmp, "Estudiar IA", "alta")
    self.assertEqual(nueva["prioridad"], "alta")
```

## Mini check de diseño (SRP en miniatura)

- **Antes** `agregar_tarea` rompía llamadas antiguas → múltiples motivos de cambio a la vez.
- **Ahora** aislamos el cambio con un **valor por defecto** + **normalización** + **backfill en carga**. Una cosa a la vez; tests verdes; cabeza fría.

## Qué sigue

Cuando confirmes que **tu suite está en verde**, atacamos **filtrar por prioridad** en `listar_tareas` con el mismo estilo:

1. escribimos **un test** súper claro,
2. implementamos **lo mínimo** para pasarlo,
3. nombres largos y cero magia.

Dime cuando tengas los tests verdes y seguimos con el filtro.

## Antes de continuar

¿Te has dado cuenta de que hemos hecho una función que empieza por _? ¿Es magia?

En Python, cuando ves una función o variable con **guion bajo delante** (`_normaliza_prioridad`, `_variable`), significa:

- **Convención.**
    
    No cambia cómo funciona Python. Es simplemente una forma de decir: *“esto es interno, no lo llames desde fuera del módulo”*.
    
- Ejemplo en castellano:
    - `agregar_tarea()` sería la “puerta principal” del restaurante: la función que cualquier cliente puede usar.
    - `_normaliza_prioridad()` sería la “cocina interna”: existe para ayudar, pero no está pensada para que el cliente meta mano ahí.
- El guion bajo es un **aviso para humanos y para linters** (programas que revisan tu estilo de código):
    
    *“Esto es privado. Si lo usas fuera, bajo tu responsabilidad”*.
    

En tu caso, quizás **yo metí `_normaliza_prioridad()` demasiado pronto**, y te di un dolor de cabeza extra cuando todavía estás asentando cosas.

Vamos a dejarlo así para evitar complicarlo, simplemente debes entender que:

- Si empieza por _ , es una funcion interna (una funcion que ayuda a otra función que si puede ser llamada desde fuera.

¿Esto provoca que no puedas llamarla desde fuera?

NO, tan solo es una forma de escribirlo para que los humanos y programas automaticos lo entiendan. Escribir con buenas convenciones ayudará tambien a la IA a entender.

## ¿seguimos?

Hasta ahora en la clase hemos hecho:

- **Problema real**: “tu CLI empieza a crecer, el jefe pide prioridad en las tareas”.
- **Primer choque**: al añadir `prioridad` rompimos los tests → vimos cómo los tests son tu red de seguridad.
- **Solución didáctica**: añadimos `prioridad` con valor por defecto, explicamos la convención del `_` y dejamos el código **claro y legible**.

Vale, quiero dejar algo claro. Es posible que ahora mismo digas:

- No entiendo los codigos de los tests
- No entiendo muchas partes del codigo python que se esta escribiendo
- Me estoy aturullando de tanta información de golpe

Si esto es así, necesitas refrescar conceptos.

1. Esto es un master para desarrollar con IA, el objetivo no es que sepas todo el codigo de memoria, sino que lo entiendas al leerlo y que tengas los conceptos de la metodología que quieres seguir.
2. En Internet hay muchos cursos de Python básicos. Antes de continuar, te recomiendo que te los mires, aunque sea rapidamente, sin pararte a memorizar todo.
3. Si quieres aprender a hacer test con profundidad, hay muchos cursos de testing en programación.

MI objetivo ahora mismo es montar un esquema mental, que te indique como se debe de programar, crear proyectos y hacer aplicaciones escalables. No es tanto que seas un experto en testing o en python. Para eso ya hay muchos cursos gratuitos que cubren esos aspectos.

Po tanto, lo que quiero que ahora mismo tengas claro en tu cabeza es:

1. Un proyecto empieza con un repo de git, para permitirnos volver atras si nos cargamos el proyecto entero
2. Antes de realiza cualquier cambio en la aplicacion, hacemos una rama (branch) y ahí hacemos los cambios. Si todo está correcto, hacemos pull request para escribir los cambios en la rama principal (o en la rama dev, como veremos mas adelante)
3. Si queremos usar TDD (Y con IA es lo mejor), primero se hacen los test y luego se programan las funciones
4. Los test verifican casos de uso (historias de usuario), y comprueban que la salida devuelva lo que debe devolver.
5. Para modificar funciones, primero debemos modificar los test y luego modificar la funcion.
6. A la IA se le pide codigo con una estructura, contexto y en pasos pequeños:
    1. Rol
    2. Tarea
    3. Objetivo
7. Siempre dividimos el problema es funciones con una sola responsabilidad, y a la IA le iremos dando estas tareas.
8. La IA escribe abreviaturas, pidele que no lo haga y siempre haz codigo limpio y legible. Si tu no lo entiendes, está mal.
9. Antes de hacer PR los test deben pasar.
10. Los test deben cubrir todas las posibilidades que puedan ocurrirle a un usuario. (Esto antes para un programador era practicamente imposible, debido a los presupuestos, ahora con la IA es posible hacerlo, y es necesario.

Vale, ahora que tienes en la cabeza este esquema de trabajo, vamos a añadir una **nueva historia de usuario**: listar tareas filtradas por prioridad.

Lo atacamos con TDD: primero un test que exprese esa historia, luego el código mínimo para que pase.

### La historia continúa

Imagina que tu CLI de tareas ya lo usas en tu día a día. Has agregado varias tareas con distinta prioridad:

- Estudiar IA → prioridad alta
- Repasar Git → prioridad baja
- Llamar a tu madre → prioridad media

Hasta aquí todo bien.

Pero un día, con la lista llena de cosas, piensas:

*"Necesito ver solo lo que es **urgente**. No quiero que se me pierda entre todo lo demás."*

Ese es el **nuevo problema** que enfrentamos: **filtrar tareas por prioridad**.

Y es perfecto para practicar **TDD + SRP**: escribir primero el test, luego el código mínimo, y asegurarnos de que la función hace **una sola cosa clara**.

### Paso 1 — Escribir el test (el contrato)

Antes de tocar código, describimos la historia como prueba automatizada:

```python
def test_listar_solo_prioridad_alta(self):
    agregar_tarea(self.tmp, "Estudiar IA", "alta")
    agregar_tarea(self.tmp, "Repasar Git", "baja")
    agregar_tarea(self.tmp, "Llamar a mamá", "media")

    tareas_alta = listar_tareas(self.tmp, prioridad="alta")

    # Debe haber exactamente 1 tarea
    self.assertEqual(len(tareas_alta), 1)
    
    # Esa tarea debe ser la de "Estudiar IA"
    self.assertEqual(tareas_alta[0]["nombre"], "Estudiar IA")
    self.assertEqual(tareas_alta[0]["prioridad"], "alta")

```

Este test cuenta la historia: *“cuando filtro por prioridad alta, solo me devuelve esas tareas”*.

### Paso 2 — Implementar lo mínimo

Ahora sí, ampliamos `listar_tareas` para aceptar un filtro opcional:

```python
def listar_tareas(ruta_archivo: str, prioridad: str | None = None) -> list[dict]:
    """Devuelve la lista de tareas. Si se pasa prioridad, filtra por ella."""
    todas = cargar_tareas(ruta_archivo)

    if prioridad is None:
        return todas

    return [tarea for tarea in todas if tarea.get("prioridad") == prioridad]

```

- **Si no pasas prioridad** → devuelve todas (como hasta ahora).
- **Si pasas prioridad** → devuelve solo las que coincidan.

### Paso 3 — Relación con SRP (Single Responsibility Principle)

Fíjate qué hemos hecho aquí:

- `listar_tareas` tiene **una responsabilidad clara**: devolver tareas.
- Si además le pides filtrar, lo hace, pero sigue siendo **coherente con su propósito**.
- No imprime, no escribe en archivos, no cambia datos. Solo **lee y selecciona**.

Esto es SRP en miniatura: una función que tiene **un único motivo para cambiar** → si mañana cambia cómo se guardan las prioridades, tocarías aquí; pero si cambia cómo se imprimen en el CLI, eso va en otro lado.

### Pausa de respiración

¿Te das cuenta del patrón?

1. Empieza un **problema real** (quiero ver solo lo urgente).
2. Lo transformamos en un **test** (un contrato claro).
3. Escribimos el **código mínimo** para que pase.
4. Confirmamos que cada función mantiene una **única responsabilidad**.

Ya no estamos improvisando ni escribiendo jeroglíficos: estamos siguiendo una metodología que escala.

👉 Ejercicio de la clase:

- Crea rama `feature/cli-prioridades`.
- Añade el test de filtro + el cambio en `listar_tareas`.
- Corre todos los tests.
- Si todo está verde, haz PR.
- Documenta en `notes.md`: *“Añadí prioridad a tareas. Al principio se rompieron los tests. Los arreglé con valor por defecto y ahora también tengo filtrado por prioridad.”*

# ✅ Checklist de la Clase 4 – Testing ampliado + primer principio SOLID

### Conceptos que deben quedarte claros

- Los **tests** son tu red de seguridad: cuando cambiaste la función `agregar_tarea` para añadir `prioridad`, los tests fallaron y te avisaron del problema.
- Un cambio grande debe empezar por el **test**: escribes lo que quieres comprobar, luego ajustas el código para que lo cumpla.
- El guion bajo `_` delante de una función o variable es solo **una convención**: indica que es interna, pero no te impide usarla.
- **SRP (Single Responsibility Principle)** en miniatura: cada función debe tener un motivo único para cambiar.
    - `agregar_tarea` crea y guarda.
    - `listar_tareas` devuelve y filtra.
    - No mezclan impresión ni argumentos del CLI.

### Resultado tangible del PR

- Rama nueva: `feature/cli-prioridades`.
- `agregar_tarea` ahora admite un campo `prioridad` con valor por defecto `"media"`.
- `cargar_tareas` rellena el campo si el archivo viejo no lo tiene.
- `listar_tareas` acepta un argumento opcional `prioridad` para filtrar.
- Tests añadidos:
    - Agregar con prioridad por defecto.
    - Agregar con prioridad explícita.
    - Listar solo las tareas de una prioridad.
- Todos los tests deben estar en verde antes de hacer el PR.

### Meta-mensaje de la clase

No necesitas ser experto en Python o unittest. Lo importante es que interiorices la **metodología**:

1. Rama → test → código mínimo → PR.
2. Funciones pequeñas y con responsabilidad clara.
3. Convenciones que ayudan a humanos, IA y al “yo del futuro” a entender el código.

---

👉 Con esto, tu CLI ya empieza a parecerse a un mini-proyecto real: tiene nuevas features, tests que lo protegen y una base de diseño que evita que se convierta en spaghetti.