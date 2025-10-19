# Workflow de IA: Generando Arquitectura Limpia con Repository Pattern

## 🎯 Objetivo

Aprender a usar IA para **diseñar, implementar y validar arquitectura limpia** aplicando:
- **Open/Closed Principle (OCP)**: Extensible sin modificación
- **Dependency Inversion Principle (DIP)**: Dependencias apuntan a abstracciones
- **Repository Pattern**: Separación de lógica de negocio y persistencia

**Meta**: Al final de este workflow, tendrás:
- ✅ Un `Protocol` bien diseñado que define el contrato de persistencia
- ✅ Múltiples implementaciones concretas (Memoria, JSON, SQLite)
- ✅ Arquitectura validada por agentes educacionales
- ✅ Tests de integración que demuestran intercambiabilidad

---

## 📋 Fase 1: Generación del Protocol (contrato de persistencia)

### Paso 1.1: Análisis de requisitos con IA

**Objetivo**: Identificar qué métodos debe tener el contrato del repositorio.

**Prompt**:

```
Rol: Product Manager experto en análisis de requisitos

Contexto:
- Tengo un ServicioTareas que gestiona tareas
- Cada tarea tiene: id (int), nombre (str), completada (bool)
- El servicio necesita: crear, listar, obtener por ID, completar, eliminar tareas

Objetivo:
Lista TODAS las operaciones de persistencia que un repositorio debe soportar

Formato:
| Operación | Descripción | Parámetros | Retorno |
|-----------|-------------|------------|---------|

Considera:
- CRUD completo (Create, Read, Update, Delete)
- Casos de error (tarea no encontrada)
- Operaciones de búsqueda
```

**Resultado esperado**:

| Operación | Descripción | Parámetros | Retorno |
|-----------|-------------|------------|---------|
| guardar | Persiste una tarea (nueva o existente) | tarea: Tarea | None |
| listar | Devuelve todas las tareas | - | List[Tarea] |
| obtener_por_id | Busca una tarea por ID | id: int | Optional[Tarea] |
| eliminar | Elimina una tarea por ID | id: int | bool (True si existía) |
| completar | Marca una tarea como completada | id: int | Optional[Tarea] |

---

### Paso 1.2: Generación del Protocol con IA

**Objetivo**: Crear el contrato formal usando `typing.Protocol`.

**Prompt estructurado**:

```
Rol: Arquitecto Python senior experto en SOLID y Clean Architecture

Contexto:
- Python 3.10+ (usa | para Optional)
- Tengo este análisis de operaciones: [pegar tabla anterior]
- Necesito aplicar Dependency Inversion Principle (DIP)

Objetivo:
Genera un Protocol llamado RepositorioTareas que defina el contrato que CUALQUIER repositorio debe cumplir

Requisitos:
- Usa typing.Protocol (PEP 544)
- Define métodos: guardar, listar, obtener_por_id, eliminar, completar
- Usa TYPE_CHECKING para evitar imports circulares
- Incluye docstrings que expliquen:
  * QUÉ hace cada método (contrato)
  * QUÉ debe devolver
  * QUÉ pasa en casos de error (None, False, etc.)
- NO implementes lógica, solo firma de métodos

Restricciones:
- Type hints completos (usa List, Optional correctamente)
- Docstrings en español
- NO uses ABC (usa Protocol)
- Forward references para Tarea (usa "Tarea" entre comillas)

Formato:
```python
# api/repositorio_base.py
# Código aquí con comentarios explicativos
```

Explica:
1. Por qué cada método es necesario
2. Por qué usamos Protocol en vez de ABC
3. Por qué TYPE_CHECKING evita imports circulares
```

**Resultado esperado**:

```python
# api/repositorio_base.py
from typing import Protocol, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # Solo para type hints (no se ejecuta en runtime)
    # Evita imports circulares si Tarea está en servicio_tareas.py
    from api.servicio_tareas import Tarea


class RepositorioTareas(Protocol):
    """Contrato que define cómo CUALQUIER repositorio debe comportarse.

    Este Protocol permite aplicar Dependency Inversion Principle (DIP):
    - El servicio depende de esta ABSTRACCIÓN
    - NO depende de implementaciones concretas (RepositorioMemoria, RepositorioJSON, etc.)
    - Permite cambiar de implementación sin modificar el servicio (Open/Closed)

    Cualquier clase que implemente estos métodos con estas firmas
    automáticamente cumple el contrato (structural subtyping).
    """

    def guardar(self, tarea: "Tarea") -> None:
        """Persiste una tarea (nueva o existente).

        - Si tarea.id == 0: asigna un ID único y la crea
        - Si tarea.id > 0: actualiza la tarea existente

        Args:
            tarea: Tarea a persistir

        Nota: NO devuelve nada. La tarea se modifica in-place (se le asigna id).
        """
        ...

    def listar(self) -> List["Tarea"]:
        """Devuelve todas las tareas persistidas.

        Returns:
            Lista de tareas (puede estar vacía)
        """
        ...

    def obtener_por_id(self, id: int) -> Optional["Tarea"]:
        """Busca una tarea por su ID.

        Args:
            id: ID de la tarea a buscar

        Returns:
            La tarea si existe, None si no se encuentra
        """
        ...

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea por su ID.

        Args:
            id: ID de la tarea a eliminar

        Returns:
            True si la tarea existía y fue eliminada
            False si la tarea no existía
        """
        ...

    def completar(self, id: int) -> Optional["Tarea"]:
        """Marca una tarea como completada.

        Args:
            id: ID de la tarea a completar

        Returns:
            La tarea actualizada si existía
            None si la tarea no fue encontrada
        """
        ...
```

---

### Paso 1.3: Validación del Protocol con Python Best Practices Coach

**Prompt de validación**:

```
Rol: Python Best Practices Coach

Contexto:
Acabo de generar este Protocol para aplicar DIP en mi arquitectura

Código:
[Pegar el Protocol completo]

Objetivo:
Valida que cumple best practices de Python y SOLID

Checklist:
1. ✅ ¿Usa typing.Protocol (no ABC)?
2. ✅ ¿Usa TYPE_CHECKING para evitar imports circulares?
3. ✅ ¿Todos los métodos tienen type hints completos?
4. ✅ ¿Los docstrings explican el CONTRATO (qué hace), no la implementación (cómo)?
5. ✅ ¿Los métodos solo tienen ... (no implementación)?
6. ✅ ¿Usa | para Optional (Python 3.10+)?
7. ✅ ¿Los métodos son cohesivos (todos sobre persistencia)?
8. ✅ ¿Cumple Single Responsibility? (solo persistencia, no lógica de negocio)

Para cada violación:
- Explica POR QUÉ es un problema
- Propón la corrección exacta
- Muestra un ejemplo antes/después
```

**Red flags que IA detectaría**:

```python
# ❌ ANTI-PATTERN 1: Usa ABC en vez de Protocol
from abc import ABC, abstractmethod
class RepositorioTareas(ABC):  # MAL: Viejo estilo, requiere herencia explícita
    @abstractmethod
    def guardar(self, tarea): ...

# ✅ CORRECTO: Usa Protocol (structural subtyping)
from typing import Protocol
class RepositorioTareas(Protocol):  # BIEN: Cualquier clase con estos métodos cumple
    def guardar(self, tarea: "Tarea") -> None: ...


# ❌ ANTI-PATTERN 2: No usa TYPE_CHECKING
from api.servicio_tareas import Tarea  # MAL: Import circular en runtime
class RepositorioTareas(Protocol): ...

# ✅ CORRECTO: TYPE_CHECKING
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # BIEN: Solo se ejecuta para type checkers (mypy)
    from api.servicio_tareas import Tarea


# ❌ ANTI-PATTERN 3: Protocol con implementación
class RepositorioTareas(Protocol):
    def listar(self):
        return []  # MAL: Los Protocols NO deben tener lógica

# ✅ CORRECTO: Solo firma
class RepositorioTareas(Protocol):
    def listar(self) -> List["Tarea"]: ...  # BIEN: Solo firma
```

---

## 🔨 Fase 2: Implementación de clases concretas

### Paso 2.1: Implementar RepositorioMemoria con IA

**Objetivo**: Crear la implementación más simple (almacenamiento en memoria).

**Prompt**:

```
Rol: Python Developer experto en patrones de diseño

Contexto:
Tengo este Protocol:
[Pegar RepositorioTareas completo]

Objetivo:
Implementa RepositorioMemoria que cumple el contrato usando almacenamiento en memoria (listas de Python)

Requisitos funcionales:
- Implementa TODOS los métodos del Protocol
- IDs autoincrementales (empieza en 1)
- guardar(): si id==0, asigna nuevo ID; si id>0, actualiza
- obtener_por_id(): devuelve None si no existe
- eliminar(): devuelve True si existía, False si no
- completar(): devuelve tarea actualizada o None

Requisitos técnicos:
- Usa type hints completos
- NO modifiques el Protocol
- NO agregues métodos públicos extras
- Thread-safe NO es necesario (es una demo educativa)
- Usa list comprehensions donde sea apropiado
- Docstrings en español

Restricciones:
- Solo usa built-ins de Python (List, no numpy)
- NO uses global, usa atributos de instancia

Formato:
```python
# api/repositorio_memoria.py
# Código con comentarios explicativos
```

Explica:
- Por qué usas _tareas (atributo privado)
- Cómo manejas IDs autoincrementales
- Por qué no modificas tareas existentes en listar()
```

**Resultado esperado** (simplificado):

```python
# api/repositorio_memoria.py
from typing import List, Optional
from api.servicio_tareas import Tarea


class RepositorioMemoria:
    """Implementación en memoria del repositorio de tareas.

    Usa una lista interna para almacenar tareas. Los datos se pierden
    al reiniciar la aplicación (no hay persistencia real).
    """

    def __init__(self):
        self._tareas: List[Tarea] = []
        self._contador: int = 0

    def guardar(self, tarea: Tarea) -> None:
        """Guarda una tarea en memoria (crea o actualiza)."""
        if tarea.id == 0:
            # Caso: tarea nueva, asignar ID
            self._contador += 1
            tarea.id = self._contador
            self._tareas.append(tarea)
        else:
            # Caso: actualizar tarea existente
            for i, t in enumerate(self._tareas):
                if t.id == tarea.id:
                    self._tareas[i] = tarea
                    return
            # Si llegamos aquí, no existía → la creamos
            self._tareas.append(tarea)

    def listar(self) -> List[Tarea]:
        """Devuelve todas las tareas almacenadas."""
        return self._tareas.copy()  # Copia defensiva

    def obtener_por_id(self, id: int) -> Optional[Tarea]:
        """Busca una tarea por ID."""
        for tarea in self._tareas:
            if tarea.id == id:
                return tarea
        return None

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea por ID."""
        for i, tarea in enumerate(self._tareas):
            if tarea.id == id:
                self._tareas.pop(i)
                return True
        return False

    def completar(self, id: int) -> Optional[Tarea]:
        """Marca una tarea como completada."""
        for tarea in self._tareas:
            if tarea.id == id:
                tarea.completada = True
                return tarea
        return None
```

---

### Paso 2.2: Implementar RepositorioJSON con IA

**Objetivo**: Crear implementación con persistencia real en archivo JSON.

**Prompt**:

```
Rol: Python Developer experto en persistencia y manejo de archivos

Contexto:
Tengo este Protocol:
[Pegar RepositorioTareas]

Objetivo:
Implementa RepositorioJSON que persiste tareas en un archivo JSON

Requisitos funcionales:
- Implementa TODOS los métodos del Protocol
- Crea el archivo si no existe (con lista vacía [])
- IDs autoincrementales basados en max(ids existentes) + 1
- Maneja encoding UTF-8 (tareas con tildes, emojis)
- Escribe JSON con indentación (legible)

Requisitos técnicos:
- Usa pathlib.Path (no os.path)
- Context managers (with) para archivos
- Maneja excepciones (archivo corrupto, permisos)
- Type hints completos
- Docstrings que expliquen manejo de errores

Restricciones:
- NO uses librerías externas (solo json, pathlib del stdlib)
- NO uses pickle (inseguro)
- Asume que el archivo puede estar corrupto (try/except)

Formato:
```python
# api/repositorio_json.py
# Código con manejo de errores robusto
```

Explica:
- Cómo manejas archivo corrupto
- Por qué lees+escribes en cada operación (no mantienes cache)
- Cómo calculas el próximo ID
```

**Resultado esperado** (simplificado):

```python
# api/repositorio_json.py
import json
from pathlib import Path
from typing import List, Optional
from api.servicio_tareas import Tarea


class RepositorioJSON:
    """Implementación de repositorio que persiste tareas en archivo JSON.

    Los datos se guardan en formato JSON legible (con indentación).
    Se lee y escribe el archivo completo en cada operación (simple pero ineficiente).
    """

    def __init__(self, ruta_archivo: str = "tareas.json"):
        self.ruta = Path(ruta_archivo)
        # Crear archivo vacío si no existe
        if not self.ruta.exists():
            self._escribir([])

    def _leer(self) -> List[Tarea]:
        """Lee todas las tareas del archivo JSON."""
        try:
            with self.ruta.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return [Tarea(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            # Archivo corrupto o no existe → devolver lista vacía
            return []

    def _escribir(self, tareas: List[Tarea]) -> None:
        """Escribe todas las tareas al archivo JSON."""
        with self.ruta.open("w", encoding="utf-8") as f:
            json.dump(
                [t.model_dump() for t in tareas],
                f,
                ensure_ascii=False,  # Permite tildes y emojis
                indent=2  # JSON legible
            )

    def guardar(self, tarea: Tarea) -> None:
        """Guarda una tarea en el archivo JSON."""
        tareas = self._leer()

        if tarea.id == 0:
            # Calcular próximo ID
            max_id = max([t.id for t in tareas], default=0)
            tarea.id = max_id + 1
            tareas.append(tarea)
        else:
            # Actualizar existente o agregar
            encontrada = False
            for i, t in enumerate(tareas):
                if t.id == tarea.id:
                    tareas[i] = tarea
                    encontrada = True
                    break
            if not encontrada:
                tareas.append(tarea)

        self._escribir(tareas)

    def listar(self) -> List[Tarea]:
        """Devuelve todas las tareas del archivo."""
        return self._leer()

    def obtener_por_id(self, id: int) -> Optional[Tarea]:
        """Busca una tarea por ID."""
        tareas = self._leer()
        for tarea in tareas:
            if tarea.id == id:
                return tarea
        return None

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea del archivo."""
        tareas = self._leer()
        for i, tarea in enumerate(tareas):
            if tarea.id == id:
                tareas.pop(i)
                self._escribir(tareas)
                return True
        return False

    def completar(self, id: int) -> Optional[Tarea]:
        """Marca una tarea como completada."""
        tareas = self._leer()
        for tarea in tareas:
            if tarea.id == id:
                tarea.completada = True
                self._escribir(tareas)
                return tarea
        return None
```

---

## ✅ Fase 3: Validación de arquitectura limpia

### Paso 3.1: Validar separación de capas con FastAPI Design Coach

**Objetivo**: Verificar que el servicio y la API cumplen Clean Architecture.

**Prompt**:

```
Rol: FastAPI Design Coach experto en Clean Architecture

Contexto:
Tengo estas 3 capas:
1. API (endpoints FastAPI)
2. Servicio (lógica de negocio)
3. Repositorio (abstracción + implementaciones)

Código:

--- api/api.py ---
[Pegar api.py completo]

--- api/servicio_tareas.py ---
[Pegar servicio_tareas.py completo]

--- api/repositorio_base.py ---
[Pegar Protocol]

Objetivo:
Valida que la arquitectura cumple Clean Architecture y SOLID

Checklist de validación:
1. ¿La API depende solo del Servicio? (NO debe importar repositorios)
2. ¿El Servicio depende solo del Protocol? (NO de RepositorioMemoria/JSON concretos)
3. ¿Las dependencias apuntan hacia adentro? (API → Servicio → Protocol)
4. ¿Hay inyección de dependencias? (api.py inyecta repositorio al servicio)
5. ¿El Servicio está cerrado a modificación? (OCP: no cambiar al agregar repositorios)
6. ¿Existen imports circulares?
7. ¿Hay lógica de negocio en la API? (debería estar en Servicio)
8. ¿Hay lógica de persistencia en el Servicio? (debería estar en Repositorio)

Para cada violación:
- Identifica la línea exacta
- Explica POR QUÉ es un problema (qué principio SOLID viola)
- Propón la refactorización paso a paso
- Muestra código antes/después

Formato de respuesta:
## ✅ Validaciones correctas
## ❌ Violaciones encontradas
## 🔧 Refactorizaciones recomendadas
```

**Ejemplo de violación que IA detectaría**:

```python
# ❌ VIOLACIÓN: API importa repositorio concreto
# Archivo: api/api.py
from api.repositorio_json import RepositorioJSON  # MAL

app = FastAPI()
servicio = ServicioTareas(RepositorioJSON("tareas.json"))  # Detalle en capa alta
```

**IA reportaría**:

> ❌ **Violación de Clean Architecture**
>
> **Archivo**: `api/api.py`, línea 3
>
> **Problema**: La API (capa externa) conoce detalles de implementación del repositorio (capa interna)
>
> **Principio violado**:
> - **Dependency Inversion Principle (DIP)**: La capa alta depende de un detalle concreto
> - **Clean Architecture**: Las dependencias deben apuntar hacia adentro, no hacia detalles
>
> **Consecuencias**:
> - Cambiar de RepositorioJSON a RepositorioSQL requiere modificar api.py (viola OCP)
> - La API está acoplada a cómo se persiste (debería ser agnóstica)
>
> **Refactorización correcta**:
>
> ```python
> # ✅ BIEN: Usa Dependency Injection
> # Archivo: api/dependencias.py (nueva capa)
> from api.repositorio_json import RepositorioJSON
> from api.servicio_tareas import ServicioTareas
>
> def obtener_servicio() -> ServicioTareas:
>     """Factory que crea el servicio con su repositorio.
>
>     Cambiar de repositorio solo requiere modificar ESTA función.
>     """
>     repo = RepositorioJSON("tareas.json")
>     return ServicioTareas(repo)
>
> # Archivo: api/api.py
> from fastapi import Depends
> from api.dependencias import obtener_servicio
>
> @app.post("/tareas")
> def crear_tarea(
>     cuerpo: CrearTareaRequest,
>     servicio: ServicioTareas = Depends(obtener_servicio)  # Inyección
> ):
>     tarea = servicio.crear(cuerpo.nombre)
>     return tarea.model_dump()
> ```
>
> **Beneficios**:
> - ✅ api.py ya NO importa RepositorioJSON
> - ✅ Cambiar de repositorio solo requiere editar `dependencias.py`
> - ✅ Tests pueden inyectar mocks fácilmente

---

### Paso 3.2: Validar intercambiabilidad de repositorios

**Objetivo**: Confirmar que cambiar de repositorio solo requiere 1 línea.

**Prompt de prueba**:

```
Dado este código:

--- api/dependencias.py ---
def obtener_servicio():
    repo = RepositorioMemoria()  # Línea 3
    return ServicioTareas(repo)

Tarea:
Cambia a RepositorioJSON SIN modificar:
- api.py
- servicio_tareas.py
- repositorio_base.py
- Ningún test

¿Cuántas líneas necesitas modificar?
```

**Respuesta esperada**:
> Solo 1 línea (línea 3 de `dependencias.py`):
> ```python
> repo = RepositorioJSON("tareas.json")  # Cambio mínimo
> ```
>
> Si necesitas modificar más de 1 línea, tu arquitectura NO cumple Open/Closed.

---

## 🧪 Fase 4: Tests de integración

### Paso 4.1: Generar tests de integración con IA

**Objetivo**: Crear tests que validen que TODOS los repositorios son intercambiables.

**Prompt**:

```
Rol: Test Engineer experto en pytest

Contexto:
Tengo 2 implementaciones del Protocol RepositorioTareas:
- RepositorioMemoria
- RepositorioJSON

Objetivo:
Genera tests de integración parametrizados que validen que AMBOS repositorios
son intercambiables (cumplen el contrato exactamente igual)

Requisitos:
- Usa pytest con @pytest.fixture parametrizado
- Cada test debe correr contra AMBOS repositorios
- Tests para: guardar, listar, obtener_por_id, eliminar, completar
- Tests de edge cases: ID no encontrado, lista vacía, etc.
- Limpieza entre tests (archivo JSON se borra)

Restricciones:
- NO uses mocks (son tests de integración reales)
- Usa pytest.mark.parametrize
- Type hints completos
- Docstrings que expliquen QUÉ se valida

Formato:
```python
# tests_integrations/test_repositorios.py
import pytest
# ... código
```

Explica:
- Por qué usar fixtures parametrizados
- Cómo garantizar aislamiento entre tests
```

**Resultado esperado** (simplificado):

```python
# tests_integrations/test_repositorios.py
import pytest
from pathlib import Path
from api.servicio_tareas import Tarea
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_json import RepositorioJSON


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    """Fixture parametrizado que devuelve cada repositorio."""
    if request.param == "memoria":
        return RepositorioMemoria()
    elif request.param == "json":
        archivo_test = tmp_path / "tareas_test.json"
        return RepositorioJSON(str(archivo_test))


def test_guardar_y_listar(repositorio):
    """Valida que guardar y listar funciona igual en todos los repositorios."""
    tarea = Tarea(id=0, nombre="Test", completada=False)

    repositorio.guardar(tarea)

    tareas = repositorio.listar()
    assert len(tareas) == 1
    assert tareas[0].nombre == "Test"
    assert tareas[0].id > 0  # ID fue asignado


def test_obtener_por_id_existente(repositorio):
    """Valida que obtener_por_id devuelve la tarea correcta."""
    tarea = Tarea(id=0, nombre="Buscar", completada=False)
    repositorio.guardar(tarea)

    encontrada = repositorio.obtener_por_id(tarea.id)

    assert encontrada is not None
    assert encontrada.nombre == "Buscar"


def test_obtener_por_id_no_existente(repositorio):
    """Valida que devuelve None si el ID no existe."""
    resultado = repositorio.obtener_por_id(999)
    assert resultado is None


def test_eliminar_existente(repositorio):
    """Valida que eliminar devuelve True si la tarea existía."""
    tarea = Tarea(id=0, nombre="Eliminar", completada=False)
    repositorio.guardar(tarea)

    eliminada = repositorio.eliminar(tarea.id)

    assert eliminada is True
    assert repositorio.obtener_por_id(tarea.id) is None


def test_eliminar_no_existente(repositorio):
    """Valida que eliminar devuelve False si no existe."""
    eliminada = repositorio.eliminar(999)
    assert eliminada is False
```

---

## 🚨 Red Flags y Checklist Final

### Red Flags en arquitectura generada por IA

🚨 **Señales de que la arquitectura NO cumple SOLID**:

1. **Servicio importa repositorio concreto**:
   ```python
   # ❌ MAL
   from api.repositorio_memoria import RepositorioMemoria
   class ServicioTareas:
       def __init__(self):
           self._repo = RepositorioMemoria()
   ```

2. **API tiene lógica de negocio**:
   ```python
   # ❌ MAL
   @app.post("/tareas")
   def crear_tarea(cuerpo):
       nueva = Tarea(id=get_next_id(), nombre=cuerpo.nombre)  # Lógica aquí
       repo.guardar(nueva)
   ```

3. **Servicio tiene lógica de persistencia**:
   ```python
   # ❌ MAL
   class ServicioTareas:
       def crear(self, nombre):
           with open("tareas.json") as f:  # Persistencia en servicio
               ...
   ```

4. **No puedes cambiar repositorio con 1 línea**:
   Si necesitas modificar más de 1 archivo para cambiar de RepositorioMemoria a RepositorioJSON,
   hay un problema de arquitectura.

5. **Protocol con implementación**:
   ```python
   # ❌ MAL
   class RepositorioTareas(Protocol):
       def listar(self):
           return []  # NO debe tener lógica
   ```

---

### Checklist de arquitectura limpia validada

**Antes de dar por terminada la implementación, verifica**:

#### Capa de abstracción
- [ ] Existe un Protocol que define el contrato
- [ ] El Protocol solo tiene firmas de métodos (no implementación)
- [ ] Usa `TYPE_CHECKING` para evitar imports circulares
- [ ] Docstrings explican el CONTRATO, no la implementación

#### Capa de servicio
- [ ] El servicio depende del Protocol, NO de clases concretas
- [ ] El servicio recibe el repositorio por inyección (constructor)
- [ ] NO hay lógica de persistencia en el servicio
- [ ] NO hay imports de RepositorioMemoria/JSON/SQL en servicio_tareas.py

#### Capa de API
- [ ] La API depende solo del servicio
- [ ] La API NO importa repositorios concretos
- [ ] Usa Dependency Injection (FastAPI Depends)
- [ ] NO hay lógica de negocio en los endpoints

#### Implementaciones concretas
- [ ] Cada repositorio implementa TODOS los métodos del Protocol
- [ ] Las firmas coinciden exactamente con el Protocol
- [ ] Manejo de errores robusto (archivos corruptos, IDs no encontrados)
- [ ] Type hints completos

#### Tests
- [ ] Tests de integración parametrizados (corren contra TODOS los repositorios)
- [ ] Tests validan que los repositorios son intercambiables
- [ ] Aislamiento entre tests (limpiar datos entre ejecuciones)
- [ ] Coverage mínimo 80%

#### Pregunta final de validación
**¿Puedes cambiar de RepositorioMemoria a RepositorioJSON modificando solo 1 línea de código?**

- ✅ **SÍ** → Arquitectura limpia validada
- ❌ **NO** → Revisar separación de capas y DIP

---

## 💡 Tips avanzados

### Tip 1: Detectar violaciones con herramientas

Usa `mypy` para detectar violaciones de type hints:

```bash
mypy api/ --strict
```

Si ves errores como:
```
api/servicio_tareas.py:10: error: Cannot assign to a type
```
→ Probablemente importaste un tipo concreto donde debería ser un Protocol

### Tip 2: Validar con IA periódicamente

Después de cada cambio, valida con este prompt rápido:

```
Revisa este código y lista SOLO las violaciones de SOLID:

[Pegar código modificado]

Formato de respuesta:
❌ [Archivo:línea] - [Principio violado] - [Breve explicación]
```

### Tip 3: Refactorización incremental

Si tu código actual viola SOLID:
1. Escribe tests que validen el comportamiento actual
2. Refactoriza SIN cambiar comportamiento (tests siguen verdes)
3. Valida con IA después de cada paso
4. Itera hasta que no haya violaciones

**No intentes refactorizar todo de golpe → hazlo incremental**

---

## 📚 Recursos adicionales

**Agentes educacionales recomendados**:
- `.claude/agents/educational/python-best-practices-coach.md` → Valida Protocols y type hints
- `.claude/agents/educational/fastapi-design-coach.md` → Valida separación API/Servicio
- `.claude/agents/educational/database-orm-specialist.md` → Útil para RepositorioDB futuro

**Documentación**:
- PEP 544 (Protocols): https://peps.python.org/pep-0544/
- Clean Architecture by Robert C. Martin
- SOLID principles en Python

**Próximos pasos**:
- Implementar `RepositorioSQLite` (ver `EJERCICIOS_REPOSITORY.md`)
- Añadir cache con Redis (decorator pattern)
- Implementar event sourcing sobre el Repository Pattern

---

**Resumen**: Si al final puedes cambiar de repositorio cambiando 1 línea, y tus tests siguen pasando,
has dominado Clean Architecture con IA. 🎯
