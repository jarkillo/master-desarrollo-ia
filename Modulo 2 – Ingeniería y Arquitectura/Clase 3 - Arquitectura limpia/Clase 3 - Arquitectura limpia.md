# 🎬 Clase 3 – Arquitectura limpia: del caos al orden
*(Módulo 2)*

Estamos en la **Clase 3 del Módulo 2**, así que debes venir ya con esta mochila en la cabeza:

- En la **Clase 1** entendiste cómo se organiza un proyecto real (backlog, sprints, entregas cortas).
- En la **Clase 2** viste **SOLID en acción** con el primer endpoint en FastAPI y aprendiste a usar **TDD** como brújula: escribir el test antes que el código.

Ahora toca **cerrar el círculo**: que tu código empiece a parecer el de un equipo profesional, modular, testeable y con responsabilidades claras, sin volverte loco con la complejidad.

## 1. El problema: el monstruo crece

Tu API funciona.

Recibe peticiones, crea tareas y las devuelve en JSON.

Todo vive en un único archivo (`api.py`).

El código no está mal… pero empieza a **oler**.

Tu jefe llega una mañana y dice:

> “Oye, necesitamos que las tareas se guarden en disco.
> 
> 
> Y luego, queremos poder listarlas filtradas por prioridad.
> 
> Y… ah, que cada usuario tenga las suyas.”
> 

Te ríes nervioso.

Abres `api.py`, miras tus 60 líneas y piensas:

*"¿Dónde meto todo esto sin romper nada?"*

Ese momento de pánico es el **inicio de la arquitectura**.

No nace del capricho, sino del **dolor real de mantener un proyecto que crece**.

---

## 2. El caos explicado

Hoy la función `crear_tarea` hace de todo:

- Valida la entrada.
- Decide el ID.
- Crea la estructura.
- La guarda (por ahora, en memoria).
- Y encima devuelve la respuesta HTTP.

Cinco responsabilidades en un solo sitio.

¿Te suena? Es como si el cocinero del restaurante tuviera que atender mesas, fregar platos y hacer la contabilidad.

Eso viola el primer principio SOLID: **Single Responsibility Principle**.

Y además te impide escalar: no puedes testear la lógica sin levantar FastAPI.

---

## 3. El descubrimiento: dividir para conquistar

Tu primer paso como arquitecto es **aislar los mundos**.

Separar lo que cambia a distinto ritmo.

1. La **API** (FastAPI, HTTP) → cambia cuando cambian las rutas o los contratos.
2. La **lógica de negocio** (crear, listar, completar) → cambia cuando cambian las reglas.
3. La **persistencia** (cómo y dónde guardas) → cambia cuando decides usar JSON, SQL o una nube.

Tres ritmos, tres mundos.

Si los dejas mezclados, cualquier cambio los arrastra a todos.

---

## 4. La primera cirugía

Vamos a abrir el código y hacer una pequeña cirugía sin dolor.

Crea tu estructura:

```
Modulo2/
 ├─ api/
 │   ├─ __init__.py
 │   ├─ api.py
 │   ├─ servicio_tareas.py
 │   └─ repositorio_memoria.py
 └─ tests/
     └─ test_tareas.py

```

Imagina tu código como un taller mecánico:

- La **API** es el mostrador donde el cliente deja el coche.
- El **servicio** es el mecánico que arregla.
- El **repositorio** es el almacén donde se guardan las piezas.

### Paso 1 – La capa de negocio`servicio_tareas.py` (el “mecánico”)

**Problema a resolver:** mezclar validación, reglas y almacenamiento en la capa API acaba en spaghetti.

**Solución:** mover la lógica a un **servicio** con un **modelo** claro.

- `class Tarea(BaseModel)`: usamos **Pydantic** para definir la “forma” de una tarea.
    - Campos: `id`, `nombre`, `completada`.
    - Beneficio: entrada/salida **tipada y validada**; cuando devuelves `Tarea`, FastAPI sabe convertirla a JSON sin dolores.
- `class ServicioTareas`: encapsula las **reglas de negocio** (crear, listar…).
    - `_tareas: list[Tarea]` y `_contador`: estado **en memoria**. Es perfecto para empezar y testear sin BD.
    - `crear(nombre)`: incrementa el contador, construye una `Tarea` válida y la guarda.
        - Regla oculta que ya aplicas: **una función = una acción**. No imprime, no habla HTTP, no sabe de FastAPI.
    - `listar()`: devuelve la lista tal cual, como datos (no como texto). Eso lo hace fácil de testear.

> Idea fuerza: aquí vive el “qué” del negocio (crear y listar tareas), no el “cómo HTTP” ni el “dónde se guardan” los datos. Eso es SRP en miniatura.
> 

```python
from pydantic import BaseModel
from typing import List

class Tarea(BaseModel):
    id: int
    nombre: str
    completada: bool = False

class ServicioTareas:
    def __init__(self):
        self._tareas: List[Tarea] = []
        self._contador = 0

    def crear(self, nombre: str) -> Tarea:
        self._contador += 1
        tarea = Tarea(id=self._contador, nombre=nombre)
        self._tareas.append(tarea)
        return tarea

    def listar(self) -> List[Tarea]:
        return self._tareas

```

### Paso 2 – La capa de API `api.py` (el “mostrador”)

**Problema a resolver:** la API no debe decidir reglas ni persistencia; solo **recibir peticiones** y **delegar**.

**Solución:** un controlador finito que orquesta.

- `app = FastAPI()`: creas la app que escucha peticiones.
- `servicio = ServicioTareas()`: inyectas la **dependencia** (por ahora a mano). Más adelante cambiaremos esto a **inyección configurable** para elegir memoria/JSON/BD sin tocar endpoints.
- `class CrearTareaRequest(BaseModel)`: contrato de **entrada**.
    - `min_length=1` evita nombre vacío → si no se cumple, FastAPI responde **422** automáticamente.
- `@app.post("/tareas", status_code=201)`: **contrato HTTP** del endpoint.
    - Dentro: `servicio.crear(...)` hace el trabajo.
    - `.model_dump()`: convierte la `Tarea` (objeto Pydantic) a **dict** listo para JSON (en Pydantic v2 es `model_dump`; antes era `.dict()`).
- `@app.get("/tareas")`: devuelve una lista de tareas.
    - `[t.model_dump() for t in servicio.listar()]`: la API solo **traduce** datos a JSON.

> Idea fuerza: la API no sabe cómo se generan IDs ni dónde se guardan; solo sabe hablar HTTP. El día que cambiemos a fichero o base de datos, este archivo casi no se toca.
> 

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from api.servicio_tareas import ServicioTareas

app = FastAPI()
servicio = ServicioTareas()

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)

@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()

@app.get("/tareas")
def listar_tareas():
    return [t.model_dump() for t in servicio.listar()]

```

Ejecuta tus tests.

Todo sigue verde.

No cambiaste el comportamiento, solo **limpiaste el mapa**.

---

## Por qué esta separación te salva (y a tus tests también)

- **Tests estables:** tus tests HTTP de la clase 2 siguen pasando porque **el contrato no cambió** (201/422 y el JSON esperado).
- **Refactors seguros:** si mañana mueves el almacenamiento a JSON, tocarás el servicio/repositorio, **no los endpoints ni los tests de contrato**.
- **Escalado mental:** cada capa cuenta **una historia**: API (habla), Servicio (decide), Repositorio (guarda). Menos carga cognitiva.

## 5. La metáfora del taller

## Qué viene después (mini–mapa mental)

- Añadir un **Repositorio**: una clase que guarde/cargue tareas (primero JSON).
    - El **Servicio** dependerá de una **interfaz** de repositorio (Dependency Inversion).
    - Cambiar de “memoria” a “JSON” o “PostgreSQL” será solo cambiar **la implementación inyectada**, no el servicio ni la API.

## Pequeñas trampas típicas (y cómo evitarlas)

- **Estado en memoria**: se pierde al reiniciar y no es concurrente; bien para aprender y testear, no para producción.
- **Devolver imprimibles**: nunca `print` en el servicio; **devuelve datos**. La API imprime/serializa.
- **Pydantic v1 vs v2**: en v2 usa `model_dump()`. Mantén esto igual en todas las capas.

¿Ves la magia?

Cada parte tiene su función. Si mañana cambias de almacén (pasas de guardar en memoria a usar una base de datos), el mostrador y el mecánico ni se enteran.

Eso es **arquitectura limpia**: las dependencias fluyen hacia dentro, nunca hacia fuera.

---

## 6. Aplicación con IA: el aprendiz disciplinado

Ahora, deja que la IA te ayude. Pero esta vez no como mago, sino como **aprendiz**.

Prompt:

```
Rol: Arquitecto Python.
Contexto: Tengo una API FastAPI con servicio_tareas.py que maneja las tareas en memoria.
Objetivo: Implementar un repositorio que guarde las tareas en archivo JSON,
y modificar el servicio para poder alternar entre repositorio en memoria o en disco sin cambiar la API.

Restricciones:
- Usa SOLID (Dependency Inversion).
- No rompas los tests existentes.
Formato: Código explicado con clases y dependencias claras.
```

La IA te devolverá probablemente dos piezas nuevas:

- `repositorio_json.py`
- una versión del `ServicioTareas` que recibe un repositorio en su constructor.

Tu tarea no es copiar el código, sino **leer y entender cómo fluye la dependencia**: la API depende del servicio, el servicio depende del repositorio… pero **cada uno habla con una interfaz**, no con una implementación concreta.

Ahí empieza la verdadera ingeniería.

---

## 7. El aprendizaje emocional

Hasta ahora programabas “para que funcione”.

Ahora programas “para que crezca sin romperse”.

Y eso cambia tu relación con la IA: ya no le pides milagros, le pides **modularidad**.

Cuando una IA entiende tu arquitectura, empieza a comportarse como un equipo de juniors que habla tu idioma.

---

## 🎯 Ejercicio práctico

1. Crea una rama `feature/arquitectura-limpia`.
2. Mueve tu lógica de negocio al `ServicioTareas`.
3. Implementa el endpoint `GET /tareas`.
4. Corre los tests anteriores.
5. Documenta en `Modulo2/api/notes.md`:
    - Qué partes separaste y por qué.
    - Qué beneficios notas al hacerlo.
    

---

## ✅ Checklist de la clase

- [ ]  Comprendes qué significa **separación de capas**.
- [ ]  Sabes explicar qué hace cada una (API, servicio, repositorio).
- [ ]  Los tests de `/tareas` siguen verdes.
- [ ]  Has escrito en `notes.md` una mini reflexión sobre lo aprendido.
- [ ]  Has probado a pedir a la IA una refactorización usando SOLID.

---

La próxima clase será el siguiente escalón lógico:

**Open/Closed y Dependency Inversion**, donde aprenderás cómo inyectar dependencias (repositorios, adaptadores, bases de datos) sin tocar el código principal.

Allí ya verás cómo el mismo código puede funcionar con memoria, con JSON o con PostgreSQL… sin que cambien tus tests.

Esa es la recompensa de construir con cabeza, no con prisa.