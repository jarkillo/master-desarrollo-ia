# 🎬 Clase 5 - **Integración y pruebas de arquitectura**.

Entramos en **la Clase 5 del Módulo 2**, justo donde todo empieza a sentirse como un proyecto “de verdad”.

Para situarnos:

- En la **Clase 1**, aprendiste cómo planificar el trabajo (backlog, historias, sprints).
- En la **Clase 2**, aplicaste **TDD y SRP** en tu primer endpoint con FastAPI.
- En la **Clase 3**, separaste **API / servicio / repositorio** y diste forma a tu primera arquitectura limpia.
- En la **Clase 4**, aplicaste **Open/Closed y Dependency Inversion**: tu servicio ya no depende de detalles, sino de contratos.

Ahora llega **la Clase 5 – Integración y pruebas de arquitectura**.

El objetivo: **ver si toda esta estructura realmente se comporta como esperábamos**.

Aquí empieza el oficio de **ingeniero**, no solo programador.

Antes de empezar a meter más contigo, PARATE UN SEGUNDO

Ahora mismo deberias tener un mapa mental de que hace cada archivo del proyecto, cada linea. Esto no significa que seas capaz de escribirla en un papel en blanco. Esto significa que si lees el codigo entiendes lo que esta ocurriendo.

Si esto no es así, no avances mas porque se te va a empezar a hacer bola (si no se te ha hecho ya)

Abre tu IA de confianza (Ej. ChatGPT 5) y pasale el codigo que hicimos en la clase 1 y que te lo explique linea a linea. Preguntale todas las dudas que tengas y no avances hasta tenerlo claro.

Lo mismo con las clases 2, 3, 4. El objetivo es que antes de continuar entiendas todo y tengas el mapa mental. (*Tomate esto como una tutoria con el profesor, solo que este no se frustra al explicarte las cosas 1000 veces*)

Ahora si. Continuamos

## 🎯 Concepto

Hasta ahora escribías tests de comportamiento (que el endpoint devuelva 201, que las tareas se guarden…).

Pero ¿qué pasa si alguien cambia una parte interna —por ejemplo, sustituye el repositorio en memoria por uno JSON— y la API sigue respondiendo igual?

Esa es la prueba de fuego de la **arquitectura limpia**:

> “Cambiar dentro sin romper fuera.”
> 

Hoy aprenderás a escribir **tests de integración** que crucen capas:

API → Servicio → Repositorio.

Así comprobamos que los contratos entre capas están bien definidos y que tu sistema es **coherente y extensible**.

---

## 🧠 Historia para entenderlo

Imagina que eres el jefe técnico y tienes dos devs:

- Ana ha implementado `RepositorioMemoria`.
- Luis crea `RepositorioJSON`.

Ambos prometen que sus clases cumplen el mismo contrato (`guardar()` y `listar()`), pero ¿cómo lo verificas sin abrir el código?

Con un **test de integración**, que trate ambos repositorios como cajas negras.

Si ambos pasan los mismos tests, tu arquitectura está viva y saludable.

---

Pero antes, vamos a crear **`RepositorioJSON`**

Vamos a hacerlo juntos, sin prisas y sin romper nada.

### 1) ¿Qué necesitamos que haga?

Igual que `RepositorioMemoria`, debe cumplir el **contrato** (`guardar`, `listar`). Solo que, en vez de una lista en RAM, **lee/escribe un archivo `.json`**.

### 2) Crea el archivo

Ruta sugerida: `api/repositorio_json.py`

```python
# api/repositorio_json.py
from __future__ import annotations
import json, os
from typing import List
from api.servicio_tareas import Tarea  # usamos el mismo modelo Pydantic

class RepositorioJSON:
    """Repositorio que persiste tareas en un archivo JSON sencillo."""

    def __init__(self, ruta_archivo: str = "tareas.json"):
        self._ruta = ruta_archivo
        # si no existe, lo creamos vacío
        if not os.path.exists(self._ruta):
            with open(self._ruta, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def listar(self) -> List[Tarea]:
        with open(self._ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            datos = json.loads(contenido) if contenido else []
        # devolvemos objetos Tarea (Pydantic), no dicts
        return [Tarea(**d) for d in datos]

    def guardar(self, tarea: Tarea) -> None:
        # leemos lo existente
        tareas = self.listar()
        # generamos ID robusto (max + 1)
        nuevo_id = (max((t.id for t in tareas), default=0) + 1)
        tarea.id = nuevo_id
        tareas.append(tarea)
        # guardamos todo
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump([t.model_dump() for t in tareas], f, ensure_ascii=False, indent=2)

```

Puntos clave, en cristiano:

- Si el archivo **no existe**, lo creamos con `[]`.
- `listar()` **lee el JSON** y convierte cada item a `Tarea`.
- `guardar()` **calcula el siguiente id** (`max + 1`), asigna y **reescribe** el archivo completo (simple y suficiente ahora).

### 3) Usarlo en la API

En `api/api.py`, donde eliges repositorio:

```python
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_json import RepositorioJSON

# repositorio = RepositorioMemoria()
repositorio = RepositorioJSON("data/tareas.json")  # por ejemplo, dentro de /data
servicio = ServicioTareas(repositorio)
```

No cambias nada más. Esa es la gracia de DIP: **una línea y listo**.

Simplemente cambiamos el repo que le damos al servicio y BOOM, ya lo tenemos funcionando en JSON sin escribir nada mas. Y los test pasando en verde.

### 5) Eliminar estado compartido

Vamos a modificar el test crear_tarea por:

```python
from fastapi.testclient import TestClient
from api import api as api_mod  # accedemos al módulo, no solo al app
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria

def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    # 1. Resetear el servicio a uno limpio
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    # 2. Crear el cliente justo después
    cliente = TestClient(api_mod.app)

    respuesta_con_nombre = cliente.post("/tareas", json={"nombre": "Estudiar SOLID"})
    assert respuesta_con_nombre.status_code == 201
    cuerpo = respuesta_con_nombre.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Estudiar SOLID"
    assert cuerpo["completada"] is False

def test_crear_tarea_con_nombre_vacio_devuelve_422():
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    cliente = TestClient(api_mod.app)

    respuesta_con_nombre_vacio = cliente.post("/tareas", json={"nombre": ""})
    assert respuesta_con_nombre_vacio.status_code == 422

```

## 🧠 Traducción para humanos

- Ya **no hay `cliente_http` global** que se quede con el repo sucio.
- Cada test **crea un cliente después de inyectar un repo limpio**.
- El `id` siempre arranca en 1. La API es predecible.

### 5) Test rápido de integración (para dormir tranquilo)

Crea (o añade) un test muy pequeño que pruebe memoria y json igual:

```python
# tests/test_crear_tarea_json.py
import tempfile, os
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_json import RepositorioJSON

def test_crear_tarea_con_repositorio_json_temporal():
    # Crear archivo temporal vacío
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()

    try:
        # Inyectar el servicio con RepositorioJSON usando el archivo temporal
        api_mod.servicio = ServicioTareas(RepositorioJSON(tmp.name))

        # Lanzar cliente HTTP contra la API
        cliente = TestClient(api_mod.app)
        r = cliente.post("/tareas", json={"nombre": "Aprender tests con IA"})

        # Verificar respuesta
        assert r.status_code == 201
        tarea = r.json()
        assert tarea["id"] == 1
        assert tarea["nombre"] == "Aprender tests con IA"
        assert tarea["completada"] is False

    finally:
        # Borrar archivo después del test
        os.remove(tmp.name)

```

Si esto pasa en verde, estás listo: **misma historia, distinto almacén**.

Fijate bien en una cosa, porque es un error muy tipico:

- Ahora estamos creando un archivo temporal para el test y eliminandolo al terminar. Hay que tener cuidado de no escribir el json real en los test, y la IA mete mucho la gamba en esto.

---

## 🤖 Aplicación con IA

Prompt ejemplo:

```
Rol: QA Engineer Python.

Contexto: Tengo una API con ServicioTareas y varios repositorios (memoria, JSON).
Objetivo: Genera tests de integración que verifiquen que todas las implementaciones del repositorio cumplen el mismo contrato.

Formato: Código pytest limpio y explicaciones breves.

Restricciones: No modificar el código de producción.
```

La IA puede proponerte una **prueba parametrizada** con `pytest.mark.parametrize`, o incluso generar fixtures automáticas.

Pero el punto es que tú entiendas *qué está comprobando*: consistencia de comportamiento entre implementaciones.

Es importante que compruebes el flujo que está siguiendo la IA, te irás dando cuenta de los típicos errores que comete y estarás preparado para evitarlos.

---

## 🧩 Ejercicio práctico

1. Rama: `feature/test-integracion-repositorios`.
2. Añade los tests genéricos como el ejemplo.
3. Corre toda la suite (`pytest -v`).
4. Documenta en `notes.md`:
    - Qué descubriste sobre tu arquitectura.
    - Qué rompería si cambiaras el contrato del repositorio.
    - Qué significa “extensible pero estable” en tu código.

---

## 🤖 Workflow IA avanzado: Test Coverage Strategist

Hasta ahora has escrito tests manualmente. Ahora vamos a subir el nivel: **usar IA como estratega de cobertura de tests**.

La diferencia entre un junior que usa IA y un senior:

- **Junior**: "IA, genera tests para mi código" → copia/pega sin saber qué se está testeando
- **Senior**: "IA, analiza mi arquitectura y lista los edge cases críticos que DEBO testear. Genera solo tests de alto valor"

Vamos a ser seniors.

---

### 6.1. Por qué IA es poderosa para testing

**Ventajas**:
1. **Identifica edge cases que no viste** - Inputs raros, estados inconsistentes
2. **Genera fixtures parametrizados** - Reduce duplicación de tests
3. **Propone estrategia de mocking** - Qué mockear y qué no
4. **Detecta gaps de cobertura** - Métodos sin tests, ramas sin cubrir
5. **Valida calidad de tests** - Tests frágiles, over-mocking, assertions débiles

**Riesgos si no la usas con criterio**:
- ❌ Tests que solo validan "happy path" (caso exitoso)
- ❌ Over-mocking (mockeas TODO, no testeas integración real)
- ❌ Tests frágiles (cambia 1 línea de código, rompen 50 tests)
- ❌ Cobertura alta pero sin valor (100% coverage, 0% de bugs atrapados)

Por eso necesitas **Test Coverage Strategist** + validación con agentes.

---

### 6.2. Fase 1: Análisis de arquitectura con IA (Test Coverage Strategist)

**Escenario**: Tienes una API con 3 capas (API → Servicio → Repositorio). ¿Qué tests necesitas REALMENTE?

**Prompt estructurado**:

```
Rol: Test Coverage Strategist experto en pytest y FastAPI

Contexto:
Tengo esta arquitectura:
- API (api.py): Endpoints POST /tareas, GET /tareas
- Servicio (servicio_tareas.py): Lógica de negocio (crear, listar)
- Repositorio (Protocol con 2 implementaciones: RepositorioMemoria, RepositorioJSON)

Código actual:
[Pegar api.py, servicio_tareas.py, repositorio_base.py]

Objetivo:
Analiza la arquitectura y genera una ESTRATEGIA DE TESTING completa

Formato de respuesta:
## 1. Tests Unitarios (capa por capa)
| Componente | Qué testear | Por qué es crítico | Qué NO testear |
|------------|-------------|---------------------|----------------|

## 2. Tests de Integración
| Flujo | Capas involucradas | Edge cases | Mocks necesarios |
|-------|-------------------|------------|------------------|

## 3. Edge Cases Críticos
[Lista de 10+ edge cases que DEBES cubrir]

## 4. Gaps de Cobertura Detectados
[Código sin tests, ramas no cubiertas]

Restricciones:
- NO generes código todavía, solo la estrategia
- Prioriza tests de alto valor (bugs reales, no triviales)
- Identifica qué mockear y qué testear end-to-end
```

**Resultado esperado** (parcial):

```markdown
## 1. Tests Unitarios

| Componente | Qué testear | Por qué es crítico | Qué NO testear |
|------------|-------------|---------------------|----------------|
| ServicioTareas.crear() | IDs autoincrementales, nombre vacío (validación Pydantic) | Es el core de la lógica de negocio | La persistencia (eso es responsabilidad del repo) |
| RepositorioMemoria | IDs únicos, listar devuelve copias (no refs mutables) | Bugs comunes: IDs duplicados, mutación de estado | La API (separation of concerns) |

## 2. Tests de Integración

| Flujo | Capas involucradas | Edge cases | Mocks necesarios |
|-------|-------------------|------------|------------------|
| POST /tareas → guardar | API + Servicio + Repo | Nombre con 1000 caracteres, emojis, caracteres especiales (", ', \) | **NINGUNO** (end-to-end real) |
| GET /tareas con repo vacío | API + Servicio + Repo | Lista vacía debe devolver 200 (no 404) | Ninguno |

## 3. Edge Cases Críticos

1. **IDs autoincrementales con repositorios vacíos**: ¿Qué pasa si listar() devuelve []?
2. **Nombres con caracteres especiales**: ", ', \, <, >, SQL injection attempts
3. **Repositorio JSON corrupto**: Archivo existe pero JSON inválido
4. **Archivo JSON con permisos de solo lectura**: ¿Falla guardar()?
5. **Múltiples tareas con mismo ID**: ¿Cómo reacciona el servicio?
6. **Tarea con id=None vs id=0**: ¿Se comportan igual?
7. **Cambiar de RepositorioMemoria a RepositorioJSON en runtime**: ¿Los IDs se mantienen consistentes?
8. **POST /tareas sin body**: ¿Devuelve 422 o 500?
9. **GET /tareas cuando hay 1000+ tareas**: ¿Hay timeout? ¿Pagination?
10. **Crear tarea, eliminar archivo JSON manualmente, listar**: ¿Devuelve [] o error?

## 4. Gaps de Cobertura Detectados

❌ **RepositorioJSON.listar()**: No tiene tests para archivo corrupto
❌ **ServicioTareas.crear()**: No valida longitud máxima de nombre
❌ **API**: No hay test para Content-Type incorrecto (text/plain en vez de JSON)
```

**Cómo usar este análisis**:
1. Prioriza edge cases por impacto (IDs duplicados > nombre largo)
2. Genera tests SOLO para los casos de alto valor
3. Valida con agente que no estés over-testing

---

### 6.3. Fase 2: Generar tests parametrizados con IA

**Objetivo**: Crear tests que corran contra MÚLTIPLES repositorios (Memoria, JSON).

**Prompt**:

```
Rol: Pytest Expert

Contexto:
Tengo 2 implementaciones del repositorio: RepositorioMemoria, RepositorioJSON
Ambos cumplen el mismo Protocol: guardar(), listar()

Objetivo:
Genera tests parametrizados con @pytest.fixture(params=...) que validen
que AMBOS repositorios son intercambiables

Requisitos:
- Usa pytest.fixture parametrizado (no pytest.mark.parametrize)
- Cada test debe correr 2 veces (una por repositorio)
- Manejo de cleanup (borrar archivos JSON temporales)
- Type hints completos
- Docstrings que expliquen QUÉ se valida y POR QUÉ

Tests a generar:
1. test_guardar_asigna_ids_unicos
2. test_listar_devuelve_copia_defensiva (no modifica repo interno)
3. test_guardar_con_nombre_caracteres_especiales
4. test_listar_repositorio_vacio_devuelve_lista_vacia

Restricciones:
- NO uses mocks (son tests de integración reales)
- Usa tmp_path de pytest para archivos temporales
- Cada test debe ser independiente (no estado compartido)

Formato:
```python
# tests_integrations/test_repositorios_parametrizados.py
import pytest
# ... código
```

Explica:
- Por qué usar fixture parametrizado vs pytest.mark.parametrize
- Cómo garantizar aislamiento entre tests
```

**Resultado esperado** (simplificado):

```python
# tests_integrations/test_repositorios_parametrizados.py
import pytest
from pathlib import Path
from api.servicio_tareas import Tarea
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_json import RepositorioJSON


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    """Fixture parametrizado que crea cada tipo de repositorio.

    Ventajas de fixture parametrizado vs pytest.mark.parametrize:
    - Permite setup/teardown específico por implementación
    - Más flexible para manejar archivos temporales
    - Fácil agregar nuevos repositorios (solo añadir a params)
    """
    if request.param == "memoria":
        return RepositorioMemoria()
    elif request.param == "json":
        # Archivo temporal único por test (evita colisiones)
        archivo_test = tmp_path / f"tareas_{request.node.name}.json"
        return RepositorioJSON(str(archivo_test))


def test_guardar_asigna_ids_unicos(repositorio):
    """Valida que cada tarea recibe un ID único e incremental.

    Edge case crítico: IDs duplicados rompen la arquitectura.
    """
    tarea1 = Tarea(id=0, nombre="Primera", completada=False)
    tarea2 = Tarea(id=0, nombre="Segunda", completada=False)

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)

    assert tarea1.id != tarea2.id, "IDs duplicados detectados"
    assert tarea1.id > 0 and tarea2.id > 0, "IDs deben ser positivos"


def test_listar_devuelve_copia_defensiva(repositorio):
    """Valida que listar() no expone referencias mutables internas.

    Bug común: modificar lista devuelta afecta el repo interno.
    """
    tarea = Tarea(id=0, nombre="Original", completada=False)
    repositorio.guardar(tarea)

    lista1 = repositorio.listar()
    lista1[0].nombre = "MODIFICADO"  # Intentar mutar

    lista2 = repositorio.listar()
    assert lista2[0].nombre == "Original", "El repo interno fue mutado (falla copia defensiva)"
```

---

### 6.4. Fase 3: Mocking estratégico con IA

**Cuándo mockear vs testear real**:

| Escenario | Mockear | Testear Real |
|-----------|---------|--------------|
| API llama Servicio llama Repo | ❌ No (test de integración) | ✅ Sí (end-to-end) |
| Llamadas a APIs externas (Stripe, AWS) | ✅ Sí (lento, caro) | ❌ No (en tests unitarios) |
| Base de datos en producción | ✅ Sí (no tocar prod) | ❌ No |
| Repositorio con BD SQLite en memoria | ❌ No (fast enough) | ✅ Sí (integración) |

**Prompt para validar estrategia de mocking**:

```
Rol: Testing Architect

Revisa estos tests y valida la estrategia de mocking:

Código de tests:
[Pegar tests]

Checklist:
1. ¿Hay over-mocking? (mockear cosas que deberían testearse reales)
2. ¿Hay under-mocking? (testear APIs externas reales en CI)
3. ¿Los mocks son frágiles? (acoplados a implementación interna)
4. ¿Los tests siguen siendo valiosos con mocks? (o solo validan el mock)

Para cada problema:
- Explica POR QUÉ es un problema
- Propón la corrección (más mocking / menos mocking)
- Muestra código antes/después
```

**Ejemplo de violación que IA detectaría**:

```python
# ❌ OVER-MOCKING: Mock innecesario
def test_crear_tarea_llama_repositorio(mocker):
    mock_repo = mocker.Mock()  # Mock del repositorio
    servicio = ServicioTareas(mock_repo)

    servicio.crear("Test")

    mock_repo.guardar.assert_called_once()  # Solo valida que se llama, no QUÉ hace

# ✅ MEJOR: Test de integración real
def test_crear_tarea_persiste_correctamente():
    repo = RepositorioMemoria()  # Repo real (es rápido)
    servicio = ServicioTareas(repo)

    tarea = servicio.crear("Test")

    tareas = repo.listar()
    assert len(tareas) == 1
    assert tareas[0].nombre == "Test"  # Valida comportamiento real
```

**IA te alertaría**:
> ❌ **Over-mocking detectado**
>
> **Problema**: Test solo valida que `guardar()` se llama, NO valida que la tarea se persiste correctamente.
> Si cambias la implementación de `guardar()` para que NO haga nada, el test sigue pasando.
>
> **Solución**: Usa repositorio real (RepositorioMemoria es rápido, no necesita mock)

---

### 6.5. Fase 4: Validar calidad de tests con agentes

**Prompt de validación**:

```
Rol: Test Quality Reviewer

Revisa estos tests y evalúa su calidad:

Código:
[Pegar tests]

Checklist de calidad:
1. **Assertions significativas**: ¿Validan comportamiento o solo existencia?
2. **Independencia**: ¿Cada test puede correr solo sin orden?
3. **Nombres descriptivos**: ¿El nombre explica QUÉ se testea y el caso?
4. **Edge cases**: ¿Cubre casos límite o solo happy path?
5. **Fragilidad**: ¿Se rompen con cambios internos o solo con bugs reales?
6. **Velocidad**: ¿Corren en <1 segundo?
7. **Legibilidad**: ¿Otro dev entiende qué falla al leer el test?

Evalúa cada test con una puntuación de 1-10 y justifica.
Lista problemas específicos con correcciones.
```

**Red flags comunes**:

```python
# ❌ RED FLAG 1: Assertion débil
def test_crear_tarea():
    tarea = servicio.crear("Test")
    assert tarea is not None  # MAL: Solo valida que devuelve algo

# ✅ CORRECTO: Assertion fuerte
def test_crear_tarea_asigna_id_y_estado_inicial():
    tarea = servicio.crear("Test")
    assert tarea.id > 0, "ID debe ser positivo"
    assert tarea.nombre == "Test", "Nombre debe coincidir"
    assert tarea.completada is False, "Nueva tarea debe estar incompleta"


# ❌ RED FLAG 2: Tests dependientes (orden importa)
def test_1_crear_tarea():
    servicio.crear("Tarea 1")

def test_2_listar_devuelve_una():
    tareas = servicio.listar()
    assert len(tareas) == 1  # MAL: Depende de test_1

# ✅ CORRECTO: Tests independientes
def test_listar_despues_de_crear():
    servicio = ServicioTareas(RepositorioMemoria())  # Repo limpio
    servicio.crear("Tarea 1")

    tareas = servicio.listar()
    assert len(tareas) == 1  # BIEN: Autocontenido


# ❌ RED FLAG 3: Test frágil (acoplado a implementación)
def test_crear_incrementa_contador_interno():
    repo = RepositorioMemoria()
    repo.guardar(Tarea(id=0, nombre="Test", completada=False))

    assert repo._contador == 1  # MAL: Testea detalle de implementación

# ✅ CORRECTO: Test de comportamiento
def test_guardar_asigna_ids_incrementales():
    repo = RepositorioMemoria()
    tarea1 = Tarea(id=0, nombre="Test1", completada=False)
    tarea2 = Tarea(id=0, nombre="Test2", completada=False)

    repo.guardar(tarea1)
    repo.guardar(tarea2)

    assert tarea2.id == tarea1.id + 1  # BIEN: Testea contrato público
```

---

### 6.6. Checklist de cobertura estratégica con IA

**Antes de dar por terminados los tests, valida**:

**Tests unitarios** (capa por capa):
- [ ] ServicioTareas tiene tests para cada método público
- [ ] Edge cases de validación (nombre vacío, IDs negativos)
- [ ] Errores de negocio (tarea no encontrada)

**Tests de integración** (flujo completo):
- [ ] Cada endpoint tiene test end-to-end (API → Servicio → Repo)
- [ ] Tests parametrizados para TODOS los repositorios
- [ ] Archivos temporales se limpian después de cada test

**Edge cases críticos**:
- [ ] Repositorio vacío (primera tarea tiene id=1)
- [ ] Nombres con caracteres especiales (", ', \, <, >)
- [ ] Archivo JSON corrupto (listar devuelve [])
- [ ] IDs autoincrementales son únicos

**Calidad de tests**:
- [ ] Assertions significativas (no solo `is not None`)
- [ ] Tests independientes (sin orden requerido)
- [ ] Nombres descriptivos (test_crear_tarea_asigna_id_positivo)
- [ ] Sin over-mocking (usar repos reales cuando sea rápido)

**Coverage mínimo**:
- [ ] 80%+ de line coverage (`pytest --cov`)
- [ ] 100% de métodos públicos testeados
- [ ] 0 ramas críticas sin cubrir

---

### 6.7. Agentes educacionales recomendados

Para esta clase, usa estos agentes:

1. **Python Best Practices Coach**: Valida sintaxis de tests, fixtures, parametrización
2. **FastAPI Design Coach**: Revisa tests de endpoints (status codes, JSON, validación)
3. **Performance Optimizer**: Detecta tests lentos (>1 segundo)

**Workflow recomendado**:
1. Genera estrategia de testing con Test Coverage Strategist
2. Implementa tests parametrizados
3. Valida con Python Best Practices Coach
4. Revisa mocking con Testing Architect
5. Evalúa calidad de tests con Test Quality Reviewer

**Ver documento completo**: `AI_TESTING_WORKFLOW.md` (workflow detallado paso a paso)

---

### 6.8. Ejercicio práctico con IA

**Desafío**: Genera tests de integración completos para la API de tareas

**Paso 1**: Usa Test Coverage Strategist para analizar gaps de cobertura

**Paso 2**: Genera 10+ tests parametrizados que cubran:
- Happy path (crear, listar)
- Edge cases (nombres especiales, repo vacío)
- Error cases (nombre vacío → 422)

**Paso 3**: Valida con agentes que:
- No hay over-mocking
- Assertions son fuertes
- Tests son independientes
- Coverage >= 80%

**Ver ejercicios completos**: `EJERCICIOS_TESTING.md`

---

## ✅ Checklist final

- [ ]  Entiendes la diferencia entre test unitario e integración.
- [ ]  Has comprobado que distintos repositorios se comportan igual.
- [ ]  Tu arquitectura puede cambiar internamente sin romper los contratos.
- [ ]  Has documentado la reflexión en `notes.md`.
- [ ]  **[NUEVO]** Usas Test Coverage Strategist para identificar edge cases críticos
- [ ]  **[NUEVO]** Generas tests parametrizados con fixtures
- [ ]  **[NUEVO]** Validas estrategia de mocking (cuándo mockear vs testear real)
- [ ]  **[NUEVO]** Tienes >= 80% coverage con tests de alto valor

---

En la próxima clase daremos un paso más: añadiremos **repositorios externos y adaptadores (JSON/DB)** y hablaremos de cómo preparar tu proyecto para **tests de aceptación y CI/CD**.

Y recuerda: **cobertura alta sin valor es peor que cobertura baja con tests inteligentes**. La IA te ayuda a priorizar los tests que realmente atrapan bugs. 🎯