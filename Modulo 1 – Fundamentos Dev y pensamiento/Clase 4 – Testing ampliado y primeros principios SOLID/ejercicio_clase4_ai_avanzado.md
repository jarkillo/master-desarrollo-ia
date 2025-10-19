# Ejercicio Clase 4: Coverage de Excelencia con IA (90%+)

## 🎯 Objetivo

Alcanzar **90%+ coverage** en tu CLI de tareas con prioridades, usando el workflow **RED → GREEN → REFACTOR** con asistencia del **Test Coverage Strategist agent**.

---

## 📋 Pre-requisitos

1. **Completaste Clase 3**: Tienes tests básicos con pytest y coverage 80%+
2. **Feature nueva**: Vas a añadir sistema de prioridades (alta/media/baja)
3. **pytest configurado**:
   ```bash
   pip install pytest pytest-cov
   ```

---

## 🔄 Workflow TDD con IA

### Contexto: La Nueva Feature

Tu jefe te dice: *"Necesitamos prioridades en las tareas: alta, media, baja. Y poder filtrarlas."*

En vez de lanzarte a codificar, vas a usar **TDD con IA**:
1. **RED**: Escribe tests que fallen (la feature no existe aún)
2. **GREEN**: Implementa lo mínimo para que pasen
3. **REFACTOR**: Limpia el código con IA

---

## Fase 1: RED (Tests que Fallan) - 20 min

### Paso 1.1: Define la feature (Manual)

**Pregúntate**:
- ¿Qué quiero lograr? → Añadir prioridad a tareas y filtrar
- ¿Qué cambia en el código? → `agregar_tarea` necesita parámetro `prioridad`
- ¿Qué casos debo testear?

**Anota tu lista inicial**:
```markdown
## Feature: Prioridades en tareas

### Casos a testear:
- [ ] Agregar tarea con prioridad "alta"
- [ ] Agregar tarea sin prioridad (default "media")
- [ ] Filtrar tareas por prioridad "alta"
- [ ] ¿Qué más...?
```

### Paso 1.2: Pedir casos de prueba a IA (Con IA)

**Prompt al Test Coverage Strategist**:

```
Rol: Test Coverage Strategist
Feature nueva: Sistema de prioridades en tareas (alta/media/baja)

Funcionalidad:
- agregar_tarea(ruta, nombre, prioridad="media") → añade campo prioridad
- listar_tareas(ruta, prioridad=None) → filtra por prioridad si se pasa

Objetivo: Lista completa de casos de prueba para esta feature (TDD).
Incluye: happy path, edge cases, validación, backward compatibility.
Categoriza por criticidad (Alta/Media/Baja).
```

**Resultado esperado de IA**:

```markdown
## Casos de Prueba - Sistema de Prioridades

### Criticidad ALTA:
1. Happy path: Agregar tarea con prioridad explícita "alta"
2. Default: Agregar sin prioridad usa "media"
3. Validación: Prioridad inválida ("super-urgente") usa "media"
4. Filtrado: Listar solo prioridad "alta" (filtra correctamente)
5. Sin filtro: Listar sin parámetro devuelve todas
6. Backward compatibility: Tareas antiguas sin prioridad reciben "media" al cargar

### Criticidad MEDIA:
7. Filtrado vacío: Filtrar prioridad que no existe devuelve []
8. Normalización: "ALTA" se convierte a "alta" (case-insensitive)
9. Persistencia: Prioridad se guarda correctamente en JSON

### Criticidad BAJA:
10. Todas las prioridades: Testear alta/media/baja (parametrización)
```

### Paso 1.3: Escribir tests que FALLEN (Manual)

**Importante**: Escribe TÚ MISMO los tests. La IA solo sugirió QUÉ testear.

```python
# test_tareas_pytest_prioridades.py
import pytest
from tareas import agregar_tarea, listar_tareas, cargar_tareas

# RED: Este test FALLARÁ porque agregar_tarea no acepta prioridad aún

def test_agregar_tarea_prioridad_alta(archivo_temporal):
    """Test: Agregar tarea con prioridad alta."""
    tarea = agregar_tarea(archivo_temporal, "Urgente", prioridad="alta")

    assert tarea["prioridad"] == "alta"
    # ❌ Fallará: TypeError agregar_tarea() got unexpected keyword 'prioridad'


def test_listar_solo_prioridad_alta(archivo_temporal):
    """Test: Filtrar por prioridad alta."""
    agregar_tarea(archivo_temporal, "Urgente", prioridad="alta")
    agregar_tarea(archivo_temporal, "Normal", prioridad="media")

    altas = listar_tareas(archivo_temporal, prioridad="alta")

    assert len(altas) == 1
    assert altas[0]["nombre"] == "Urgente"
    # ❌ Fallará: función no acepta parámetro prioridad


def test_agregar_tarea_prioridad_default(archivo_temporal):
    """Test: Sin prioridad debe usar 'media'."""
    tarea = agregar_tarea(archivo_temporal, "Normal")

    assert tarea["prioridad"] == "media"
    # ❌ Fallará: KeyError 'prioridad'
```

**Ejecuta los tests** (deben fallar ❌):
```bash
pytest test_tareas_pytest_prioridades.py -v
```

**Resultado esperado**:
```
FAILED test_agregar_tarea_prioridad_alta - TypeError: agregar_tarea() got unexpected keyword argument 'prioridad'
FAILED test_listar_solo_prioridad_alta - TypeError: agregar_tarea() got unexpected keyword argument 'prioridad'
FAILED test_agregar_tarea_prioridad_default - KeyError: 'prioridad'
```

**✅ Checkpoint RED**: Tienes tests que fallan porque la feature no existe.

---

## Fase 2: GREEN (Implementación Mínima) - 20 min

### Paso 2.1: Pedir implementación mínima a IA (Con IA)

**Prompt**:

```
Rol: Python developer
Contexto: Tengo tests que fallan porque necesito añadir prioridades a tareas.

Tests que deben pasar:
[pega los 3 tests de arriba]

Código actual de agregar_tarea y listar_tareas:
[pega las funciones]

Objetivo: Modifica las funciones para que pasen los tests.
Requisitos:
- agregar_tarea acepta parámetro opcional prioridad="media"
- listar_tareas acepta parámetro opcional prioridad=None
- Si prioridad inválida, usa "media"
- Código limpio con type hints
```

**La IA generará** algo como:

```python
PRIORIDADES_VALIDAS = ("alta", "media", "baja")

def agregar_tarea(ruta: str, nombre: str, prioridad: str = "media") -> dict:
    """Crea tarea con prioridad."""
    if prioridad not in PRIORIDADES_VALIDAS:
        prioridad = "media"

    tareas = cargar_tareas(ruta)
    nueva = {
        "id": nuevo_id(tareas),
        "nombre": nombre,
        "completada": False,
        "prioridad": prioridad
    }
    tareas.append(nueva)
    guardar_tareas(ruta, tareas)
    return nueva


def listar_tareas(ruta: str, prioridad: str | None = None) -> list[dict]:
    """Devuelve tareas, opcionalmente filtradas por prioridad."""
    todas = cargar_tareas(ruta)

    if prioridad is None:
        return todas

    return [t for t in todas if t.get("prioridad") == prioridad]
```

### Paso 2.2: Revisar código generado (Manual)

**TÚ DECIDES**:
- ✅ ¿Entiendes cada línea?
- ✅ ¿Sigue SRP? (una función = una cosa)
- ✅ ¿Es el mínimo necesario o añade complejidad extra?
- ✅ ¿Tiene type hints?

**Pregunta crítica**: Si no entiendes algo, pregunta a la IA:
```
Explica esta línea: return [t for t in todas if t.get("prioridad") == prioridad]
```

### Paso 2.3: Ejecutar tests (deben pasar ✅)

```bash
pytest test_tareas_pytest_prioridades.py -v
```

**Resultado esperado**:
```
test_agregar_tarea_prioridad_alta PASSED
test_listar_solo_prioridad_alta PASSED
test_agregar_tarea_prioridad_default PASSED
```

**✅ Checkpoint GREEN**: Tests pasan, feature implementada.

---

## Fase 3: REFACTOR (Limpieza con IA) - 15 min

### Paso 3.1: Pedir refactoring a Python Best Practices Coach

**Prompt**:

```
Rol: Python Best Practices Coach
Contexto: Acabo de implementar prioridades en tareas. Tests pasan ✅.

Código:
[pega agregar_tarea y listar_tareas]

Objetivo: Revisa y sugiere mejoras Pythonic (NO cambies funcionalidad).
- ¿Hay anti-patterns?
- ¿Puedo usar f-strings, comprehensions, etc.?
- ¿Están bien los type hints?
```

**La IA sugerirá** (ejemplo):

```markdown
## Mejoras Pythonic

### 1. Type hints más específicos
❌ Antes: `prioridad: str | None = None`
✅ Después: `prioridad: Literal["alta", "media", "baja"] | None = None`

### 2. Validación con función helper
❌ Antes: `if prioridad not in PRIORIDADES_VALIDAS:`
✅ Después: Extraer a `_normalizar_prioridad(prioridad)`

### 3. List comprehension OK ✅
Tu código `[t for t in todas if t.get("prioridad") == prioridad]` está bien.
```

### Paso 3.2: Aplicar mejoras (Manual)

```python
from typing import Literal

Prioridad = Literal["alta", "media", "baja"]

def _normalizar_prioridad(prioridad: str) -> Prioridad:
    """Normaliza prioridad o usa 'media' si inválida."""
    prioridad_lower = prioridad.lower()
    return prioridad_lower if prioridad_lower in ("alta", "media", "baja") else "media"


def agregar_tarea(ruta: str, nombre: str, prioridad: Prioridad = "media") -> dict:
    # Ahora con type hint específico y helper
    ...
```

### Paso 3.3: Ejecutar tests después de refactor

```bash
pytest test_tareas_pytest_prioridades.py -v
```

**Deben seguir pasando** ✅. Si fallan, revertir cambio.

**✅ Checkpoint REFACTOR**: Código limpio, tests pasan.

---

## Fase 4: COVERAGE 90%+ (El Objetivo Final) - 30 min

### Paso 4.1: Ejecutar coverage actual

```bash
pytest --cov=. --cov-report=term-missing
```

**Resultado ejemplo**:
```
Name          Stmts   Miss  Cover   Missing
-------------------------------------------
tareas.py        45      5    89%   23-25, 67, 89
test_...py       32      0   100%
-------------------------------------------
TOTAL            77      5    94%
```

Estás en **89%**. Necesitas llegar a **90%+**.

### Paso 4.2: Invocar Test Coverage Strategist para plan

**Prompt**:

```
Rol: Test Coverage Strategist
Contexto: Estoy en 89% coverage, quiero llegar a 90%+.

Código: tareas.py (completo)
Coverage report:
[pega output de pytest --cov]

Objetivo: Plan priorizado de tests para alcanzar 90%+ coverage.
Identifica líneas sin cubrir y qué tests necesito.
```

**IA responderá**:

```markdown
## Gaps de Coverage

### Líneas sin cubrir:
- **Línea 23-25**: Normalización case-insensitive ("ALTA" → "alta")
- **Línea 67**: Exception TareaNoEncontrada (si existe)
- **Línea 89**: Backfill de prioridad en tareas legacy

### Plan para 90%+:

**Test 1** (cubre líneas 23-25):
```python
def test_prioridad_case_insensitive(archivo_temporal):
    tarea = agregar_tarea(archivo_temporal, "Test", prioridad="ALTA")
    assert tarea["prioridad"] == "alta"
```

**Test 2** (cubre línea 89):
```python
def test_backfill_prioridad_legacy(archivo_temporal):
    # Simular tarea sin prioridad (formato antiguo)
    legacy = [{"id": 1, "nombre": "Antigua", "completada": False}]
    guardar_tareas(archivo_temporal, legacy)

    tareas = cargar_tareas(archivo_temporal)
    assert tareas[0]["prioridad"] == "media"
```

**Impacto**: +3 líneas cubiertas → **92% coverage** ✅
```

### Paso 4.3: Implementar tests del plan (Manual)

Escribe TÚ los tests sugeridos. Verifica que cubren las líneas indicadas.

### Paso 4.4: Parametrización para reducir duplicación (Con IA)

**Detecta duplicación**:

```python
def test_prioridad_alta(...): ...
def test_prioridad_media(...): ...
def test_prioridad_baja(...): ...
```

**Prompt**:
```
Refactoriza estos 3 tests usando pytest.mark.parametrize:
[pega los 3 tests]
```

**IA genera**:
```python
@pytest.mark.parametrize("prioridad", ["alta", "media", "baja"])
def test_prioridades_validas(archivo_temporal, prioridad):
    tarea = agregar_tarea(archivo_temporal, f"Tarea {prioridad}", prioridad=prioridad)
    assert tarea["prioridad"] == prioridad
```

**Beneficio**: 1 test en vez de 3, más mantenible.

### Paso 4.5: Validación final

```bash
pytest --cov=. --cov-report=html --cov-fail-under=90 -v
```

**Resultado esperado**:
```
======================== 12 passed in 0.52s ========================
Coverage: 92%
```

**✅ ÉXITO**: 90%+ coverage alcanzado.

Abre `htmlcov/index.html` para ver qué líneas están cubiertas.

---

## 📝 Entregables

Al final de este ejercicio, debes tener:

### 1. Archivos de código

- **test_tareas_pytest_prioridades.py** con 10+ tests:
  - Tests RED escritos manualmente
  - Tests GREEN validando implementación
  - Tests de coverage gaps
  - Parametrización aplicada

- **tareas.py** refactorizado:
  - Feature de prioridades implementada
  - Código Pythonic (type hints, helpers)
  - Tests pasando ✅

### 2. Documentación

**notes.md** con reflexiones:

```markdown
# Clase 4 - TDD con IA (90%+ Coverage)

## Workflow RED-GREEN-REFACTOR

### RED: Tests escritos
- test_agregar_tarea_prioridad_alta
- test_listar_solo_prioridad_alta
- test_agregar_tarea_prioridad_default

### GREEN: Implementación
- Código generado con ayuda de IA ✅
- Entendí cada línea (expliqué list comprehension) ✅

### REFACTOR: Mejoras aplicadas
- Type hints específicos (Literal["alta", "media", "baja"])
- Función helper _normalizar_prioridad
- Tests siguen pasando ✅

## Coverage Journey

- Inicio: 75% (Clase 3)
- Después de feature: 89%
- Después de gaps: 92% ✅

## Edge cases descubiertos con IA

### Casos que NO había pensado:
- Backfill de prioridad en tareas legacy ← CRÍTICO
- Case-insensitive ("ALTA" → "alta")
- Filtrado sin resultados devuelve []

### Tests escritos

| Test | Manual/IA | Criticidad |
|------|-----------|------------|
| test_agregar_prioridad_alta | Manual | Alta |
| test_listar_filtrado | Manual | Alta |
| test_backfill_legacy | Con ayuda IA | Alta |
| test_case_insensitive | IA sugirió | Media |

## Aprendizajes

1. **TDD funciona**: Tests primero → implementación → refactor
2. **IA como asistente**: Sugiere casos, NO copia código
3. **Parametrización**: Reduce duplicación (3 tests → 1)
4. **Coverage 90%+ es alcanzable** con estrategia
```

### 3. Validación técnica

```bash
# Todos los tests pasan
pytest test_tareas_pytest_prioridades.py -v

# Coverage 90%+
pytest --cov=. --cov-report=term-missing --cov-fail-under=90

# No hay issues de linting
ruff check tareas.py test_tareas_pytest_prioridades.py
```

---

## ✅ Criterios de Éxito

Has completado el ejercicio si:

- [ ] Escribiste tests RED que fallaron (TDD workflow)
- [ ] Implementaste código GREEN que los pasó
- [ ] Refactorizaste con Python Best Practices Coach
- [ ] Alcanzaste 90%+ coverage
- [ ] Usaste parametrización para reducir duplicación
- [ ] Documentaste el workflow en notes.md
- [ ] Entendiste CADA línea de código (no copiaste sin leer)

---

## 🚫 Antipatrones a Evitar

❌ **NO HAGAS ESTO**:
- Implementar código antes de escribir tests (saltar RED)
- Copiar toda la implementación de la IA sin entender
- Alcanzar 90% con tests inútiles (testing por testing)
- Usar IA para TODO (perder la oportunidad de aprender)

✅ **HAZ ESTO**:
- Seguir RED → GREEN → REFACTOR estrictamente
- Pedir a IA QUÉ testear, TÚ escribes el código
- Refactorizar con confianza (tests te protegen)
- Documentar qué aprendiste vs qué delegaste a IA

---

## 🎓 Siguientes Pasos

Cuando completes este ejercicio, estarás listo para:

- **Módulo 2**: Arquitectura limpia con FastAPI
- **TDD en proyectos reales**: Feature compleja dividida en ciclos RED-GREEN-REFACTOR
- **Coverage como estándar**: 90%+ en todo proyecto profesional

---

**Recuerda**: El objetivo NO es un número (90%), es **confianza en tu código**. Si tus tests son buenos, puedes refactorizar sin miedo. Eso es lo que hace a un desarrollador profesional.
