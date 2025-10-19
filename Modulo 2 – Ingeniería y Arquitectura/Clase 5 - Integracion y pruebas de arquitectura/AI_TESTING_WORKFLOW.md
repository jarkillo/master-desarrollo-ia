# Workflow de IA: Test Coverage Strategist para APIs

## 🎯 Objetivo

Aprender a usar IA para **diseñar estrategias de testing inteligentes** que maximicen el valor de los tests minimizando el esfuerzo.

**Meta**: Al final, tendrás:
- ✅ Estrategia de testing basada en análisis de riesgos
- ✅ Tests parametrizados que validan múltiples implementaciones
- ✅ Mocking estratégico (solo donde aporta valor)
- ✅ >= 80% coverage con tests de alto valor

---

## 📋 Fase 1: Análisis de Arquitectura (Test Coverage Strategist)

### Paso 1.1: Mapear la arquitectura con IA

**Objetivo**: Entender QUÉ componentes tiene tu sistema y cómo interactúan.

**Prompt**:

```
Rol: Software Architect experto en análisis de sistemas

Contexto:
Tengo una API FastAPI con esta estructura de archivos:
[Listar estructura del proyecto]

Código de componentes principales:
[Pegar api.py, servicio_tareas.py, repositorio_base.py]

Objetivo:
Genera un mapa de arquitectura identificando:
1. Capas (API, Servicio, Repositorio)
2. Flujos de datos entre capas
3. Puntos de integración (dónde se comunican las capas)
4. Dependencias externas (archivos, APIs, BD)

Formato:
```
Capa API (api.py)
├── POST /tareas → ServicioTareas.crear()
└── GET /tareas → ServicioTareas.listar()

Capa Servicio (servicio_tareas.py)
├── crear(nombre) → RepositorioTareas.guardar()
└── listar() → RepositorioTareas.listar()

Capa Repositorio (repositorio_base.py + implementaciones)
├── RepositorioMemoria (en RAM)
└── RepositorioJSON (archivo JSON)
```

Lista los **puntos de riesgo** (lugares donde pueden aparecer bugs)
```

---

### Paso 1.2: Generar estrategia de testing con Test Coverage Strategist

**Prompt estructurado**:

```
Rol: Test Coverage Strategist experto en pytest y FastAPI

Contexto:
Arquitectura:
[Pegar mapa del paso 1.1]

Código actual:
[Pegar código completo]

Objetivo:
Genera una ESTRATEGIA DE TESTING completa priorizando tests de alto valor

Formato:

## 1. Tests Unitarios (por capa)
| Capa | Componente | Edge cases críticos | Valor (1-10) | Esfuerzo (1-10) |
|------|------------|---------------------|--------------|-----------------|

## 2. Tests de Integración
| Flujo completo | Capas | Edge cases | Mockear | Valor | Esfuerzo |
|----------------|-------|------------|---------|-------|----------|

## 3. Top 10 Edge Cases por Impacto
[Lista priorizada de bugs más probables]

## 4. Gaps de Cobertura Actuales
[Código sin tests, ramas sin cubrir]

## 5. Recomendación de Mocking
| Componente | Mockear | Testear Real | Justificación |
|------------|---------|--------------|---------------|

Restricciones:
- Prioriza por ROI (valor / esfuerzo)
- Identifica tests triviales que NO vale la pena escribir
- Recomienda qué testear primero (quick wins)
```

**Output esperado** (ejemplo):

```markdown
## 1. Tests Unitarios

| Capa | Componente | Edge cases | Valor | Esfuerzo |
|------|------------|------------|-------|----------|
| Servicio | crear() | Nombre vacío, IDs negativos | 9/10 | 2/10 |
| Repo | guardar() | IDs únicos, mutación de estado | 10/10 | 3/10 |
| API | POST /tareas | Content-Type incorrecto | 6/10 | 2/10 |

## 2. Tests de Integración

| Flujo | Capas | Edge cases | Mockear | Valor | Esfuerzo |
|-------|-------|------------|---------|-------|----------|
| POST → crear → guardar | API+Servicio+Repo | Caracteres especiales (', ", \) | Ninguno | 10/10 | 4/10 |
| GET con repo vacío | API+Servicio+Repo | Devuelve [] no 404 | Ninguno | 8/10 | 2/10 |

## 3. Top 10 Edge Cases por Impacto

1. **IDs duplicados** (Valor: 10, Impacto: CRÍTICO)
   - Qué: Dos tareas tienen el mismo ID
   - Por qué: Rompe invariante de unicidad, bugs de UPDATE/DELETE

2. **Nombres con SQL injection** (Valor: 9, Impacto: ALTO)
   - Qué: `nombre = "'; DROP TABLE tareas;--"`
   - Por qué: Si usas BD SQL sin parametrizar, vulnerabilidad crítica

3. **Archivo JSON corrupto** (Valor: 8, Impacto: MEDIO)
   - Qué: JSON inválido en disco
   - Por qué: App crashea al arrancar si no maneja excepción

[... 7 casos más]

## 4. Gaps de Cobertura

❌ **RepositorioJSON.listar()**: No maneja FileNotFoundError si alguien borra el archivo
❌ **API POST /tareas**: No valida longitud máxima (ataque DoS con nombre de 10MB)
❌ **ServicioTareas**: No tiene tests para múltiples tareas con mismo nombre (permitido o no?)

## 5. Recomendación de Mocking

| Componente | Mockear | Testear Real | Justificación |
|------------|---------|--------------|---------------|
| RepositorioMemoria | ❌ No | ✅ Sí | Es rápido (<1ms), testear real valida comportamiento |
| RepositorioJSON | ❌ No | ✅ Sí | Usar tmp_path, testear I/O real detecta bugs |
| API externa (Stripe) | ✅ Sí | ❌ No | Lenta, cara, no controlamos |
```

---

## 🔨 Fase 2: Implementación de Tests Parametrizados

### Paso 2.1: Generar fixture parametrizado

**Prompt**:

```
Rol: Pytest Expert

Contexto:
Tengo 2 repositorios que cumplen el mismo Protocol:
- RepositorioMemoria
- RepositorioJSON

Objetivo:
Genera fixture parametrizado que devuelva AMBOS repositorios

Requisitos:
- Usa @pytest.fixture(params=[...])
- Para JSON, usa tmp_path para archivos temporales
- Cleanup automático (archivos se borran después del test)
- Documentación clara de por qué usar fixture vs pytest.mark.parametrize

Formato:
```python
import pytest
from pathlib import Path
# ... código con explicación
```
```

**Output esperado**:

```python
import pytest
from pathlib import Path
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_json import RepositorioJSON


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    """Fixture parametrizado que devuelve cada repositorio.

    ¿Por qué fixture parametrizado y no pytest.mark.parametrize?

    1. **Flexibilidad**: Permite setup/teardown específico por tipo
    2. **Archivos temporales**: tmp_path solo disponible en fixtures
    3. **Escalabilidad**: Agregar nuevo repo = añadir 1 línea en params

    Args:
        request: Objeto pytest con parámetro actual
        tmp_path: Directorio temporal de pytest (se limpia automático)

    Yields:
        RepositorioMemoria o RepositorioJSON
    """
    if request.param == "memoria":
        yield RepositorioMemoria()

    elif request.param == "json":
        # Archivo temporal ÚNICO por test (evita colisiones paralelas)
        archivo = tmp_path / f"test_{request.node.name}.json"
        yield RepositorioJSON(str(archivo))
        # Cleanup automático: pytest borra tmp_path al terminar
```

---

### Paso 2.2: Generar tests para edge cases críticos

Usa la lista del Paso 1.2 para generar tests priorizados.

**Prompt para cada edge case**:

```
Rol: Pytest Developer

Contexto:
Edge case a testear: [Describir el edge case del Top 10]
Fixture disponible: repositorio (parametrizado, Memoria + JSON)

Objetivo:
Genera test parametrizado que valide este edge case

Requisitos:
- Nombre descriptivo (test_<componente>_<caso>_<resultado_esperado>)
- Docstring que explique QUÉ se testea y POR QUÉ es crítico
- Assertions fuertes (no solo `is not None`)
- Mensajes de error claros en assertions

Ejemplo:
```python
def test_guardar_asigna_ids_unicos_a_multiples_tareas(repositorio):
    \"\"\"Valida que no hay IDs duplicados al guardar múltiples tareas.

    Edge case crítico: IDs duplicados rompen DELETE y UPDATE.
    \"\"\"
    tareas = [Tarea(id=0, nombre=f"Tarea {i}") for i in range(5)]

    for tarea in tareas:
        repositorio.guardar(tarea)

    ids = [t.id for t in tareas]
    assert len(set(ids)) == 5, f"IDs duplicados: {ids}"
    assert all(id > 0 for id in ids), f"IDs inválidos: {ids}"
```
```

---

## ✅ Fase 3: Estrategia de Mocking

### Cuándo mockear (regla de oro)

**Mockear SÍ** cuando:
- ✅ Es **lento** (>100ms por test)
- ✅ Es **no determinista** (random, time, red)
- ✅ Es **caro** (llamadas a APIs de pago)
- ✅ Es **no controlable** (servicios externos, prod DB)

**Mockear NO** cuando:
- ❌ Es **rápido** (<10ms)
- ❌ Es **crítico** (core business logic)
- ❌ Es **fácil de testear real** (in-memory DB, temp files)

### Tabla de decisión

| Componente | Velocidad | Control | Mockear | Alternativa |
|------------|-----------|---------|---------|-------------|
| RepositorioMemoria | <1ms | Total | ❌ No | Testear real |
| RepositorioJSON (tmp_path) | ~10ms | Total | ❌ No | Testear real |
| RepositorioDB (SQLite :memory:) | ~50ms | Total | ❌ No | Testear real |
| API externa (Stripe) | ~500ms | Ninguno | ✅ Sí | `responses` library |
| Email service (SendGrid) | ~300ms | Ninguno | ✅ Sí | Mock SMTP |

---

### Paso 3.1: Validar estrategia de mocking con IA

**Prompt**:

```
Rol: Testing Architect

Revisa esta suite de tests y evalúa la estrategia de mocking:

Código:
[Pegar tests]

Checklist:
1. ¿Hay over-mocking? (componentes rápidos que deberían testearse reales)
2. ¿Hay under-mocking? (APIs externas testeadas reales que ralentizan CI)
3. ¿Los mocks son frágiles? (acoplados a detalles de implementación)
4. ¿Los tests con mocks siguen siendo valiosos? (o solo validan que se llama al mock)

Para cada problema, dame:
- Línea exacta del problema
- Por qué es un problema (consecuencia)
- Refactorización (código antes/después)
```

**Ejemplo de detección**:

```python
# ❌ OVER-MOCKING detectado
def test_servicio_llama_repo(mocker):
    mock_repo = mocker.Mock()
    servicio = ServicioTareas(mock_repo)

    servicio.crear("Test")

    mock_repo.guardar.assert_called_once()  # Solo valida llamada, no comportamiento

# IA te alertaría:
> **Problema**: Test solo valida que `guardar()` se llama, no que la tarea se guarda correctamente.
> Si `guardar()` tiene un bug que ignora la tarea, el test sigue pasando.
>
> **Refactorización**: Usa RepositorioMemoria real (es rápido)

# ✅ CORRECTO
def test_servicio_persiste_tarea_correctamente():
    repo = RepositorioMemoria()  # Real
    servicio = ServicioTareas(repo)

    tarea = servicio.crear("Test")

    tareas_guardadas = repo.listar()
    assert len(tareas_guardadas) == 1
    assert tareas_guardadas[0].nombre == "Test"
```

---

## 🧪 Fase 4: Validación de Calidad de Tests

### Paso 4.1: Evaluar calidad con Test Quality Reviewer

**Prompt**:

```
Rol: Test Quality Reviewer

Evalúa la calidad de estos tests:

Código:
[Pegar tests]

Criterios (1-10 cada uno):
1. **Assertions significativas**: ¿Validan comportamiento o solo existencia?
2. **Independencia**: ¿Pueden correr en cualquier orden?
3. **Nombres descriptivos**: ¿Explican QUÉ testean?
4. **Edge cases**: ¿Cubren casos límite?
5. **Fragilidad**: ¿Se rompen solo con bugs reales o con cualquier cambio interno?
6. **Velocidad**: ¿Corren en <1 segundo?
7. **Legibilidad**: ¿Un junior entiende qué falla leyendo el nombre del test?

Formato:
| Test | Criterio 1 | Criterio 2 | ... | Total | Problemas |
|------|------------|------------|-----|-------|-----------|

Recomendaciones de mejora para tests con score <7
```

---

### Red Flags Comunes

#### 1. Assertions débiles

```python
# ❌ MAL (score: 2/10)
def test_crear_tarea():
    tarea = servicio.crear("Test")
    assert tarea  # Solo valida que no es None

# ✅ BIEN (score: 9/10)
def test_crear_tarea_asigna_id_positivo_y_nombre_correcto():
    tarea = servicio.crear("Test")
    assert tarea.id > 0, f"ID debe ser positivo, fue {tarea.id}"
    assert tarea.nombre == "Test", "Nombre debe coincidir"
    assert tarea.completada is False, "Nueva tarea debe estar pendiente"
```

#### 2. Tests dependientes (orden importa)

```python
# ❌ MAL (score: 1/10) - Tests acoplados
def test_1_crear():
    servicio.crear("Tarea 1")

def test_2_listar():
    tareas = servicio.listar()
    assert len(tareas) == 1  # Falla si test_1 no corrió antes

# ✅ BIEN (score: 10/10) - Tests independientes
def test_crear_y_listar_devuelve_tarea_creada():
    servicio = ServicioTareas(RepositorioMemoria())  # Repo limpio
    servicio.crear("Tarea 1")

    tareas = servicio.listar()
    assert len(tareas) == 1
```

#### 3. Tests frágiles (acoplados a implementación)

```python
# ❌ MAL (score: 3/10) - Testea detalle interno
def test_contador_incrementa():
    repo = RepositorioMemoria()
    repo.guardar(Tarea(id=0, nombre="Test"))

    assert repo._contador == 1  # Acoplado a variable privada

# ✅ BIEN (score: 9/10) - Testea contrato público
def test_ids_son_secuenciales():
    repo = RepositorioMemoria()
    t1 = Tarea(id=0, nombre="Test1")
    t2 = Tarea(id=0, nombre="Test2")

    repo.guardar(t1)
    repo.guardar(t2)

    assert t2.id == t1.id + 1  # Testea comportamiento observable
```

---

## 📊 Fase 5: Medición de Coverage

### Paso 5.1: Ejecutar pytest con coverage

```bash
pytest --cov=api --cov-report=term-missing --cov-fail-under=80 -v
```

**Qué significa**:
- `--cov=api`: Medir coverage del directorio api/
- `--cov-report=term-missing`: Mostrar líneas NO cubiertas
- `--cov-fail-under=80`: Fallar si <80%
- `-v`: Verbose (ver cada test)

---

### Paso 5.2: Analizar gaps de cobertura con IA

**Prompt**:

```
Rol: Coverage Analyst

Contexto:
Aquí está el reporte de coverage de pytest:

[Pegar output de pytest --cov --cov-report=term-missing]

Objetivo:
Analiza los gaps y recomienda qué tests agregar

Formato:
## Líneas sin cubrir
| Archivo | Líneas | Componente | Criticidad (1-10) | Test sugerido |
|---------|--------|------------|-------------------|---------------|

## Ramas sin cubrir
[if/else, try/except que no se ejecutan]

## Recomendación
[Qué testear primero para llegar a 80%+ con mínimo esfuerzo]
```

---

## 🚨 Checklist Final

### Estrategia de Testing Completa

**Análisis previo**:
- [ ] Mapa de arquitectura generado (capas, flujos, riesgos)
- [ ] Top 10 edge cases priorizados por impacto
- [ ] Estrategia de mocking definida (qué mockear, qué no)

**Tests implementados**:
- [ ] Tests parametrizados para TODOS los repositorios
- [ ] Edge cases críticos cubiertos (IDs únicos, nombres especiales, repo vacío)
- [ ] Tests de integración end-to-end (API → Servicio → Repo)

**Calidad de tests**:
- [ ] Assertions significativas (no solo `is not None`)
- [ ] Tests independientes (orden no importa)
- [ ] Nombres descriptivos (explican QUÉ y CUÁNDO)
- [ ] Sin over-mocking (componentes rápidos testeados reales)

**Coverage y performance**:
- [ ] >= 80% line coverage
- [ ] 100% de métodos públicos testeados
- [ ] Todos los tests corren en <10 segundos total

---

## 💡 Tips para Usar IA Efectivamente

### 1. Prompts iterativos (no esperes perfección en primer intento)

```
# Iteración 1: Estrategia general
→ IA: "Analiza arquitectura y genera estrategia de testing"

# Iteración 2: Validar estrategia
→ IA: "Revisa esta estrategia, ¿hay over-testing o under-testing?"

# Iteración 3: Implementar
→ IA: "Genera tests para los 3 edge cases de mayor valor"

# Iteración 4: Validar calidad
→ IA: "Evalúa estos tests con criterios de calidad"
```

### 2. Pregunta "¿Por qué?" para aprender

```
"¿Por qué este test necesita mock del repositorio?"
"¿Por qué este edge case es más importante que este otro?"
"¿Por qué usar fixture parametrizado en vez de pytest.mark.parametrize?"
```

### 3. Valida con múltiples agentes

- **Python Best Practices Coach**: Sintaxis, fixtures, type hints
- **FastAPI Design Coach**: Tests de endpoints, status codes
- **Performance Optimizer**: Tests lentos (>1s)

Cada agente detecta problemas diferentes → cobertura completa.

---

**Resumen**: Tests inteligentes > tests en cantidad. IA te ayuda a priorizar los tests que realmente atrapan bugs. 🎯
