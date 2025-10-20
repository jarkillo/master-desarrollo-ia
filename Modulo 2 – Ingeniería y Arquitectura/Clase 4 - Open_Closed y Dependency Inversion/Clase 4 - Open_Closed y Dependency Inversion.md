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
# api/servicio_tareas.py
from typing import List
from pydantic import BaseModel
from api.repositorio_base import RepositorioTareas

class Tarea(BaseModel):
    id: int
    nombre: str
    completada: bool = False

class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas):
        self._repo = repositorio

    def crear(self, nombre: str) -> Tarea:
        nueva = Tarea(id=0, nombre=nombre)  # el repo asigna ID real
        self._repo.guardar(nueva)
        return nueva

    def listar(self) -> List[Tarea]:
        return self._repo.listar()

```

Esto funciona, pero está **cerrado al cambio**: solo puede usar listas en memoria.

Queremos que sea **abierto** a nuevas formas de guardar sin tener que reescribirlo.

---

### 3. Invertir la dependencia (DIP en acción)

Creamos una interfaz (o “contrato”) que cualquier repositorio deberá cumplir:

```python
# api/repositorio_base.py
from typing import Protocol, List, TYPE_CHECKING

if TYPE_CHECKING:
    # Solo para tipos (no se ejecuta en runtime, evita el ciclo)
    from api.servicio_tareas import Tarea

class RepositorioTareas(Protocol):
    def guardar(self, tarea: "Tarea") -> None: ...
    def listar(self) -> List["Tarea"]: ...

```

Ahora, en el servicio, en lugar de crear su lista interna, **recibe un repositorio**:

```python
# api/servicio_tareas.py
from typing import List
from pydantic import BaseModel
from api.repositorio_base import RepositorioTareas

class Tarea(BaseModel):
    id: int
    nombre: str
    completada: bool = False

class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas):
        self._repo = repositorio

    def crear(self, nombre: str) -> Tarea:
        nueva = Tarea(id=0, nombre=nombre)  # el repo asigna ID real
        self._repo.guardar(nueva)
        return nueva

    def listar(self) -> List[Tarea]:
        return self._repo.listar()

```

Y el repositorio concreto (por ejemplo, el que guarda en memoria) implementa ese contrato:

```python
# api/repositorio_memoria.py
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
# api/api.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria

app = FastAPI()
servicio = ServicioTareas(RepositorioMemoria())

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)

@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()

@app.get("/tareas")
def listar_tareas():
    return [tarea.model_dump() for tarea in servicio.listar()]

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

### 6. Workflow IA: generando arquitectura limpia con asistencia inteligente

Hasta ahora has visto cómo aplicar OCP y DIP manualmente. Ahora vamos a subir el nivel: **usar IA para generar y validar arquitectura limpia**.

La diferencia entre un junior que copia código de IA y un senior que la domina es simple:

- **Junior**: "IA, dame un repositorio" → copia/pega sin entender
- **Senior**: "IA, genera un Protocol para X, valida la separación de capas, identifica violaciones de DIP"

Vamos a aprender a ser seniors.

---

#### 6.1. Por qué IA es poderosa para arquitectura limpia

**Ventajas**:
1. **Genera contratos (Protocols) rápidamente** - Define interfaces consistentes
2. **Identifica violaciones de SOLID** - Detecta dependencias concretas donde deberían ser abstractas
3. **Propone refactorizaciones** - Sugiere cómo separar capas sin romper tests
4. **Valida diseño** - Revisa si tu arquitectura cumple Clean Architecture

**Riesgos si no la usas con criterio**:
- ❌ Genera código que "funciona pero no escala" (sin interfaces)
- ❌ Mezcla capas (API llama directamente a base de datos)
- ❌ Crea dependencias circulares
- ❌ Ignora inyección de dependencias

Por eso necesitas **agentes especializados** que validen arquitectura.

---

#### 6.2. Paso 1: Generar un Protocol con IA

**Escenario**: Quieres crear un `RepositorioTareas` que pueda tener implementaciones en memoria, JSON y SQL.

**Prompt estructurado**:

```
Rol: Arquitecto Python senior experto en SOLID y Clean Architecture

Contexto:
- Tengo un ServicioTareas que gestiona tareas (crear, listar, completar, eliminar)
- Cada tarea tiene: id (int), nombre (str), completada (bool)
- Necesito aplicar Dependency Inversion Principle

Objetivo:
Genera un Protocol llamado RepositorioTareas que defina el contrato que CUALQUIER repositorio debe cumplir

Requisitos:
- Usa typing.Protocol
- Define métodos: guardar, listar, obtener_por_id, eliminar
- Usa TYPE_CHECKING para evitar imports circulares
- Incluye docstrings que expliquen el contrato
- NO implementes lógica, solo la interfaz

Restricciones:
- Python 3.10+
- Type hints completos
- PEP 544 (Protocols)

Formato:
```python
# Código aquí
```

Explica por qué cada método es necesario
```

**Resultado esperado de IA**:

```python
# api/repositorio_base.py
from typing import Protocol, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from api.servicio_tareas import Tarea

class RepositorioTareas(Protocol):
    """Contrato que define cómo CUALQUIER repositorio debe comportarse.

    Este Protocol permite aplicar Dependency Inversion: el servicio
    depende de esta abstracción, NO de implementaciones concretas.
    """

    def guardar(self, tarea: "Tarea") -> None:
        """Persiste una tarea (nueva o existente).

        Si la tarea tiene id=0, se le debe asignar un id único.
        Si ya tiene id, se actualiza.
        """
        ...

    def listar(self) -> List["Tarea"]:
        """Devuelve todas las tareas persistidas."""
        ...

    def obtener_por_id(self, id: int) -> Optional["Tarea"]:
        """Busca una tarea por ID. Devuelve None si no existe."""
        ...

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea. Devuelve True si existía, False si no."""
        ...
```

**Validación con IA**:

```
Rol: Clean Architecture Enforcer

Revisa el Protocol anterior y valida:
1. ¿Cumple con Dependency Inversion? (Es una abstracción, no un detalle)
2. ¿Los métodos son cohesivos? (Todos relacionados con persistencia)
3. ¿Hay dependencias concretas? (Solo debería usar tipos abstractos)
4. ¿Los docstrings explican el CONTRATO, no la implementación?

Lista cualquier violación de SOLID
```

---

#### 6.3. Paso 2: Implementar clases concretas con IA

Ahora que tienes el contrato, puedes generar implementaciones concretas.

**Prompt para RepositorioMemoria**:

```
Rol: Python Developer experto en patrones de diseño

Contexto:
Tengo este Protocol: [pegar el Protocol anterior]

Objetivo:
Implementa RepositorioMemoria que cumple el contrato usando almacenamiento en memoria (listas)

Requisitos:
- Implementa TODOS los métodos del Protocol
- Genera IDs autoincrementales
- Gestiona correctamente el caso de tarea no encontrada
- Thread-safe NO es necesario (es una demo)

Restricciones:
- NO modifiques el Protocol
- NO agregues métodos públicos extras
- Usa type hints completos

Formato:
Código + breve explicación de decisiones de diseño
```

**Prompt para RepositorioJSON**:

```
Rol: Python Developer experto en persistencia

Contexto:
Tengo este Protocol: [pegar el Protocol]

Objetivo:
Implementa RepositorioJSON que persiste tareas en un archivo JSON

Requisitos:
- Implementa TODOS los métodos del Protocol
- Crea el archivo si no existe
- Maneja encoding UTF-8
- Gestiona errores de I/O con try/except
- IDs autoincrementales basados en el máximo ID existente

Restricciones:
- NO uses librerías externas (solo json, pathlib)
- Escribe JSON con indentación (indent=2)
- Maneja el caso de archivo corrupto

Formato:
Código + explicación de manejo de errores
```

**Resultado esperado** (ver sección 4 del markdown para RepositorioJSON completo)

---

#### 6.4. Paso 3: Validar separación de capas con IA

Una vez implementados los repositorios, valida que tu arquitectura cumple Clean Architecture:

**Prompt para validación**:

```
Rol: Clean Architecture Enforcer

Contexto:
Tengo estas capas:
1. API (api.py) - Endpoints FastAPI
2. Servicio (servicio_tareas.py) - Lógica de negocio
3. Repositorio (repositorio_base.py + implementaciones)

Código:
[Pegar api.py]
[Pegar servicio_tareas.py]

Objetivo:
Valida que la separación de capas cumple Clean Architecture

Checklist:
1. ¿La API depende solo del Servicio? (NO debe conocer el repositorio concreto)
2. ¿El Servicio depende solo del Protocol? (NO de implementaciones concretas)
3. ¿Las dependencias apuntan hacia adentro? (API → Servicio → Abstracción)
4. ¿Hay inyección de dependencias explícita?
5. ¿Existen dependencias circulares?

Para cada violación:
- Explica POR QUÉ es un problema
- Propón la refactorización correcta
```

**Ejemplo de violación que IA detectaría**:

```python
# ❌ INCORRECTO (violación de DIP)
from api.repositorio_memoria import RepositorioMemoria

class ServicioTareas:
    def __init__(self):
        self._repo = RepositorioMemoria()  # Depende de un detalle concreto
```

**IA te alertaría**:
> "Violación de Dependency Inversion Principle (DIP):
> - ServicioTareas depende directamente de RepositorioMemoria (clase concreta)
> - Esto hace imposible cambiar de repositorio sin modificar ServicioTareas
> - Refactorización: Inyecta el repositorio como parámetro con type hint del Protocol"

```python
# ✅ CORRECTO (cumple DIP)
from api.repositorio_base import RepositorioTareas

class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas):  # Depende de abstracción
        self._repo = repositorio
```

---

#### 6.5. Red flags en código generado por IA

🚨 **Señales de que la IA te dio arquitectura débil**:

1. **No usa Protocol, usa herencia (ABC)**:
   ```python
   # ❌ Viejo estilo (pre-Python 3.8)
   from abc import ABC, abstractmethod
   class RepositorioTareas(ABC):
       @abstractmethod
       def guardar(self, tarea): ...
   ```
   → Pídele que use `typing.Protocol` (PEP 544, más flexible)

2. **Imports circulares sin TYPE_CHECKING**:
   ```python
   # ❌ Importa directamente (puede causar ciclos)
   from api.servicio_tareas import Tarea
   ```
   → Debe usar `if TYPE_CHECKING:` para tipos

3. **Servicio crea su propio repositorio**:
   ```python
   # ❌ No hay inyección de dependencias
   class ServicioTareas:
       def __init__(self):
           self._repo = RepositorioMemoria()
   ```
   → El repositorio debe venir del exterior (inyección)

4. **API conoce detalles de persistencia**:
   ```python
   # ❌ La API no debería saber CÓMO se persiste
   @app.post("/tareas")
   def crear_tarea(cuerpo):
       repo = RepositorioJSON("tareas.json")  # Detalle de implementación
       servicio = ServicioTareas(repo)
       ...
   ```
   → Usa **Dependency Injection** (ver Clase 5)

5. **Protocol con implementación**:
   ```python
   # ❌ Un Protocol NO debe tener lógica
   class RepositorioTareas(Protocol):
       def listar(self):
           return []  # MAL: los Protocols solo definen firma
   ```
   → Solo `...` en los métodos

---

#### 6.6. Checklist de validación con IA

Antes de dar por buena la arquitectura generada por IA, valida:

**Checklist de arquitectura limpia**:
- [ ] Existe un Protocol que define el contrato (abstracción)
- [ ] El servicio depende del Protocol, NO de clases concretas
- [ ] Las implementaciones concretas NO se importan en el servicio
- [ ] La API inyecta el repositorio al servicio (no lo crea internamente)
- [ ] No hay imports circulares (usa `TYPE_CHECKING`)
- [ ] Cada capa solo conoce la capa inmediatamente inferior
- [ ] Los tests pueden usar cualquier implementación (memoria, JSON, mock)

**Pregunta clave**: ¿Puedes cambiar de RepositorioMemoria a RepositorioJSON cambiando UNA sola línea en api.py?

Si la respuesta es **NO**, hay un problema de arquitectura.

---

#### 6.7. Agentes educacionales recomendados

Para esta clase, usa estos agentes (ver `.claude/agents/educational/`):

1. **Python Best Practices Coach**: Valida Protocols, TYPE_CHECKING, type hints
2. **FastAPI Design Coach**: Revisa separación API ↔ Servicio
3. **Database ORM Specialist**: Útil cuando implementes RepositorioDB (próximas clases)

**Workflow recomendado**:
1. Genera Protocol con IA → Valida con Python Best Practices Coach
2. Implementa repositorios concretos → Valida separación de capas
3. Revisa API → Valida con FastAPI Design Coach (inyección de dependencias)

**Ver documento completo**: `AI_REPOSITORY_WORKFLOW.md` (workflow detallado paso a paso)

---

#### 6.8. Ejercicio práctico con IA

**Desafío**: Implementa un `RepositorioSQLite` usando IA

**Paso 1**: Diseña el prompt para generar la clase (usa el patrón de la sección 6.3)

**Paso 2**: Pide a IA que valide:
- ¿Cumple el Protocol?
- ¿Maneja errores de BD correctamente?
- ¿Usa context managers para conexiones?

**Paso 3**: Escribe tests de integración que validen que RepositorioMemoria, RepositorioJSON y RepositorioSQLite son **intercambiables**

**Ver ejercicios completos**: `EJERCICIOS_REPOSITORY.md`

---

### Checklist de esta clase

- Entiendes **Open/Closed**: el código se puede extender sin modificar lo existente.
- Entiendes **Dependency Inversion**: el servicio depende de una abstracción, no de un detalle.
- Sabes usar **inyección de dependencias** en Python.
- Tienes una API funcional con repositorios intercambiables.
- Tus tests siguen pasando en verde.
- **[NUEVO]** Sabes usar IA para generar Protocols y validar arquitectura limpia
- **[NUEVO]** Identificas red flags en código generado por IA
- **[NUEVO]** Usas agentes educacionales para revisar separación de capas

---

La próxima clase subirá otro escalón: **interfaces múltiples y segregación**, donde verás cómo dividir responsabilidades más finas y preparar tu API para crecer hacia múltiples módulos (usuarios, proyectos, autenticación).

Pero hoy, quédate con la idea central: *el buen código no teme al cambio, lo anticipa. Y la IA bien usada acelera la arquitectura limpia, no la destruye.*