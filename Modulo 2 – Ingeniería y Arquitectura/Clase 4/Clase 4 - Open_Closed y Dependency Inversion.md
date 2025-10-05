# Clase 4 – Open/Closed y Dependency Inversion: el código que no se asusta al cambio

Recuerda el hilo narrativo hasta aquí, porque seguimos construyendo sobre todo lo anterior:

- En la **Clase 1**, aprendiste el *ciclo de vida del software*: cómo planificar trabajo, backlog, sprints y entregas cortas.
- En la **Clase 2**, aplicaste **SRP** y **TDD** en tu primer endpoint real con FastAPI.
- En la **Clase 3**, diste el salto a **arquitectura limpia**, separando API, servicio y repositorio.
- Ahora toca subir el nivel: entender cómo esas piezas se comunican **sin romperse entre sí**, y cómo los siguientes principios de **SOLID** (OCP y DIP) te permiten *abrir tu arquitectura sin destruirla*.

### 1. Concepto

Todo buen sistema crece. La diferencia entre un proyecto sano y uno roto es **cómo absorbe el cambio**.

Imagina que tu API ya tiene un `ServicioTareas` que guarda en memoria. Un día te piden:

> “Queremos guardar las tareas en disco (JSON) y, más adelante, en base de datos.”
> 

Si en tu código hay `if repositorio == "json"` por todas partes, ya estás en problemas.

Eso rompe el **Principio Abierto/Cerrado (Open/Closed Principle)**: el código debería poder **extenderse sin modificarse**.

Y para lograrlo, necesitamos el siguiente principio: **Inversión de Dependencias (Dependency Inversion Principle, DIP)**.

En lugar de que el servicio *dependa* directamente de cómo guardas, dependerá de una **interfaz abstracta**, y luego podrás “inyectar” distintas implementaciones (memoria, JSON, SQL…).

---

### 2. Aplicación manual (sin IA)

Vamos a practicar este cambio paso a paso.

Tu clase `ServicioTareas` de la clase anterior podría verse así:

```python
# servicio_tareas.py
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

Esto funciona, pero está **cerrado al cambio**: solo puede usar listas en memoria.

Queremos que sea **abierto** a nuevas formas de guardar sin tener que reescribirlo.

---

### 3. Invertir la dependencia (DIP en acción)

Creamos una interfaz (o “contrato”) que cualquier repositorio deberá cumplir:

```python
# repositorio_base.py
from typing import Protocol, List
from api.servicio_tareas import Tarea

class RepositorioTareas(Protocol):
    def guardar(self, tarea: Tarea) -> None: ...
    def listar(self) -> List[Tarea]: ...

```

Ahora, en el servicio, en lugar de crear su lista interna, **recibe un repositorio**:

```python
# servicio_tareas.py
from typing import List
from api.repositorio_base import RepositorioTareas
from api.servicio_tareas import Tarea

class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas):
        self._repositorio = repositorio

    def crear(self, nombre: str) -> Tarea:
        tarea = Tarea(id=0, nombre=nombre)
        self._repositorio.guardar(tarea)
        return tarea

    def listar(self) -> List[Tarea]:
        return self._repositorio.listar()

```

Y el repositorio concreto (por ejemplo, el que guarda en memoria) implementa ese contrato:

```python
# repositorio_memoria.py
from typing import List
from api.servicio_tareas import Tarea

class RepositorioMemoria:
    def __init__(self):
        self._tareas: List[Tarea] = []
        self._contador = 0

    def guardar(self, tarea: Tarea) -> None:
        self._contador += 1
        tarea.id = self._contador
        self._tareas.append(tarea)

    def listar(self) -> List[Tarea]:
        return self._tareas

```

Ahora, tu API elige qué repositorio usar sin cambiar el servicio:

```python
# api.py
from fastapi import FastAPI
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria
from pydantic import BaseModel, Field

app = FastAPI()
repositorio = RepositorioMemoria()
servicio = ServicioTareas(repositorio)

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

¿Notas la magia?

Si mañana haces un `RepositorioJSON` o `RepositorioSQL`, el servicio no cambia una línea.

---

### 4. Aplicación con IA (para que aprendas a delegar con cabeza)

Prompt sugerido:

```
Rol: Arquitecto Python senior.
Contexto: Tengo un servicio de tareas en FastAPI con un repositorio en memoria.
Objetivo: Implementa un repositorio que guarde las tareas en un archivo JSON, aplicando Open/Closed y Dependency Inversion.

Restricciones:
- No modificar ServicioTareas.
- Implementa la clase RepositorioJSON con guardar() y listar().
- Explica las decisiones de diseño.

```

La IA te devolverá una implementación parecida a esta:

```python
# repositorio_json.py
import json, os
from typing import List
from api.servicio_tareas import Tarea

class RepositorioJSON:
    def __init__(self, ruta_archivo: str = "tareas.json"):
        self.ruta = ruta_archivo
        if not os.path.exists(self.ruta):
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump([], f)

    def guardar(self, tarea: Tarea) -> None:
        tareas = self.listar()
        tarea.id = max([t.id for t in tareas], default=0) + 1
        tareas.append(tarea)
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump([t.model_dump() for t in tareas], f, ensure_ascii=False, indent=2)

    def listar(self) -> List[Tarea]:
        with open(self.ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Tarea(**t) for t in data]

```

Y lo mejor: para cambiar de un repositorio a otro, solo cambias **una línea** en tu API:

```python
# repositorio = RepositorioMemoria()
repositorio = RepositorioJSON("data/tareas.json")

```

Tu servicio ni se inmuta.

Tus tests siguen verdes.

Tu arquitectura ahora **es extensible y robusta**.

---

### 5. Mini-proyecto de la clase

**Objetivo:** refactorizar tu API para que use el patrón de inyección de dependencias.

**Pasos:**

1. Crea rama `feature/arquitectura-dip`.
2. Crea `repositorio_base.py` (el contrato) y `repositorio_json.py`.
3. Modifica el `ServicioTareas` para depender del contrato, no de una lista interna.
4. Actualiza la API para inyectar el repositorio que quieras.
5. Añade tests de integración que prueben ambos repositorios.
6. En `notes.md`, explica qué significa “abrir sin romper”.

---

### Checklist de esta clase

- Entiendes **Open/Closed**: el código se puede extender sin modificar lo existente.
- Entiendes **Dependency Inversion**: el servicio depende de una abstracción, no de un detalle.
- Sabes usar **inyección de dependencias** en Python.
- Tienes una API funcional con repositorios intercambiables.
- Tus tests siguen pasando en verde.

---

La próxima clase subirá otro escalón: **interfaces múltiples y segregación**, donde verás cómo dividir responsabilidades más finas y preparar tu API para crecer hacia múltiples módulos (usuarios, proyectos, autenticación).

Pero hoy, quédate con la idea central: *el buen código no teme al cambio, lo anticipa.*