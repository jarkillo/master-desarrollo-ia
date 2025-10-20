# Ejercicios Prácticos: Testing de APIs con IA (Test Coverage Strategist)

## 🎯 Objetivo

Dominar el uso de IA para **diseñar estrategias de testing inteligentes** que maximicen la detección de bugs minimizando el esfuerzo.

Al completar estos ejercicios, sabrás:
- ✅ Usar Test Coverage Strategist para identificar edge cases críticos
- ✅ Generar tests parametrizados con fixtures avanzados
- ✅ Decidir cuándo mockear y cuándo testear real
- ✅ Validar calidad de tests con agentes educacionales
- ✅ Alcanzar >=80% coverage con tests de alto valor

---

## Ejercicio 1: Generar Estrategia de Testing con IA

### 📋 Contexto

Tienes una API de tareas con 3 capas (API → Servicio → Repositorio). Necesitas una estrategia de testing completa que priorice los tests de mayor valor.

**Requisitos**:
- Identificar edge cases críticos (top 10)
- Priorizar por ROI (valor / esfuerzo)
- Recomendar qué testear primero (quick wins)
- Detectar gaps de cobertura en código actual

---

### 🤖 Paso 1: Análisis de arquitectura

**Tu tarea**: Diseña el prompt para que IA analice la arquitectura y genere un mapa de riesgos.

**Plantilla sugerida**:

```
Rol: [¿Qué tipo de experto necesitas?]

Contexto:
[Describe la arquitectura: capas, componentes, dependencias]

Código actual:
[Pegar código de api.py, servicio_tareas.py, repositorio_base.py]

Objetivo:
[Qué análisis quieres: mapa de riesgos, puntos de integración, dependencias externas]

Formato de respuesta:
```
Capa API
├── Endpoints
├── Validaciones
└── Puntos de riesgo

Capa Servicio
├── Lógica de negocio
└── Puntos de riesgo

Capa Repositorio
├── Implementaciones
└── Puntos de riesgo
```

Lista los **top 5 puntos de riesgo** (lugares más propensos a bugs)
```

**Criterios de éxito**:
- [ ] Prompt identifica las 3 capas correctamente
- [ ] Lista al menos 5 puntos de riesgo priorizados
- [ ] Explica POR QUÉ cada punto es riesgoso
- [ ] Recomienda tipos de tests para cada riesgo

---

### 🤖 Paso 2: Generar estrategia de testing con Test Coverage Strategist

**Prompt sugerido**:

```
Rol: Test Coverage Strategist experto en pytest y FastAPI

Contexto:
Arquitectura:
[Pegar el mapa del Paso 1]

Código actual:
[Pegar código completo]

Objetivo:
Genera una ESTRATEGIA DE TESTING completa priorizando tests de alto valor

Formato:

## 1. Tests Unitarios (por capa)
| Componente | Edge cases críticos | Valor (1-10) | Esfuerzo (1-10) | ROI |
|------------|---------------------|--------------|-----------------|-----|

## 2. Tests de Integración
| Flujo completo | Edge cases | Mockear | Valor | Esfuerzo | ROI |
|----------------|------------|---------|-------|----------|-----|

## 3. Top 10 Edge Cases por Impacto
[Lista priorizada]

## 4. Gaps de Cobertura Actuales
[Código sin tests]

## 5. Recomendación: ¿Qué testear primero?
[Quick wins: alto valor, bajo esfuerzo]

Restricciones:
- Prioriza por ROI (valor / esfuerzo)
- Identifica tests triviales que NO vale la pena escribir
- Recomienda orden de implementación
```

**Criterios de éxito**:
- [ ] Lista al menos 10 edge cases priorizados
- [ ] Calcula ROI para cada test
- [ ] Identifica al menos 3 "quick wins" (ROI >5)
- [ ] Detecta gaps de cobertura existentes

---

### 💾 Entregable

**Documento a crear**: `ESTRATEGIA_TESTING.md`

**Contenido mínimo**:

```markdown
# Estrategia de Testing - API de Tareas

## 1. Mapa de Arquitectura y Riesgos
[Diagrama de capas con puntos de riesgo marcados]

## 2. Top 10 Edge Cases Priorizados
| # | Edge Case | Impacto | Probabilidad | Esfuerzo | ROI | Test sugerido |
|---|-----------|---------|--------------|----------|-----|---------------|
| 1 | IDs duplicados | CRÍTICO | MEDIA | BAJO | 10/10 | test_guardar_asigna_ids_unicos |
| 2 | Archivo JSON corrupto | ALTO | ALTA | MEDIO | 8/10 | test_listar_maneja_json_invalido |
| ... |

## 3. Plan de Implementación
### Fase 1: Quick Wins (Semana 1)
- [ ] test_ids_unicos (ROI: 10)
- [ ] test_json_corrupto (ROI: 8)
- [ ] test_repo_vacio (ROI: 7)

### Fase 2: Tests de Integración (Semana 2)
[... tests end-to-end]

### Fase 3: Edge Cases Avanzados (Semana 3)
[... casos raros pero importantes]

## 4. Gaps de Cobertura Detectados
❌ RepositorioJSON.listar() no maneja FileNotFoundError
❌ API no valida Content-Type
❌ ServicioTareas no valida longitud máxima de nombre

## 5. Decisiones de Mocking
| Componente | ¿Mockear? | Justificación |
|------------|-----------|---------------|
| RepositorioMemoria | ❌ No | Rápido (<1ms), testear real |
| RepositorioJSON | ❌ No | Usar tmp_path, testear I/O |
| API externa | ✅ Sí | Lenta, cara, no controlamos |
```

---

## Ejercicio 2: Implementar Tests Parametrizados con Edge Cases

### 📋 Contexto

Has identificado 3 edge cases críticos:
1. **IDs duplicados**: Dos tareas no pueden tener el mismo ID
2. **Copia defensiva**: listar() no debe exponer referencias mutables
3. **Nombres con caracteres especiales**: ", ', \, <, > no deben romper la app

**Tu tarea**: Implementa tests parametrizados que validen estos edge cases en AMBOS repositorios (Memoria y JSON).

---

### 🤖 Paso 1: Generar fixture parametrizado

**Prompt**:

```
Rol: Pytest Expert

Contexto:
Tengo 2 repositorios: RepositorioMemoria y RepositorioJSON
Ambos cumplen el Protocol: guardar(), listar()

Objetivo:
Genera fixture parametrizado que devuelva AMBOS repositorios

Requisitos:
- Usa @pytest.fixture(params=["memoria", "json"])
- Para JSON, usa tmp_path para archivos temporales
- Cleanup automático (archivos se borran después)
- Documentación de por qué usar fixture vs pytest.mark.parametrize

Formato:
```python
import pytest
from pathlib import Path
# ... código con docstrings completos
```

Explica:
- Ventajas de fixture parametrizado
- Cómo funciona tmp_path
- Por qué cada test corre 2 veces
```

---

### 🤖 Paso 2: Implementar tests para cada edge case

Para cada uno de los 3 edge cases, genera un test.

**Ejemplo de prompt para Edge Case #1** (IDs únicos):

```
Rol: Pytest Developer

Contexto:
Edge case: IDs duplicados rompen la arquitectura
Fixture disponible: repositorio (parametrizado, Memoria + JSON)
Modelo: Tarea(id, nombre, completada)

Objetivo:
Genera test que valide que NO hay IDs duplicados al guardar múltiples tareas

Requisitos:
- Nombre descriptivo: test_guardar_asigna_ids_unicos_a_multiples_tareas
- Docstring que explique POR QUÉ este edge case es crítico
- Guarda al menos 5 tareas con id=0
- Assertions fuertes:
  * Todos los IDs son únicos (usa set())
  * Todos los IDs son positivos
  * Los IDs son secuenciales
- Mensajes de error claros en assertions

Formato:
```python
def test_guardar_asigna_ids_unicos_a_multiples_tareas(repositorio):
    \"\"\"[Docstring explicativo]\"\"\"
    # ... código
```
```

**Repite para Edge Case #2** (copia defensiva) y **Edge Case #3** (caracteres especiales).

---

### 💾 Entregable

**Archivo a crear**: `tests_integrations/test_edge_cases_parametrizados.py` (~150 líneas)

**Contenido mínimo**:

```python
import pytest
from pathlib import Path
from api.servicio_tareas import Tarea
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_json import RepositorioJSON


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    """Fixture parametrizado con docstring completo."""
    # ... implementación


def test_guardar_asigna_ids_unicos_a_multiples_tareas(repositorio):
    """Valida que no hay IDs duplicados (edge case crítico)."""
    # ... implementación con assertions fuertes


def test_listar_devuelve_copia_defensiva(repositorio):
    """Valida que modificar lista devuelta NO afecta repo interno."""
    # ... implementación


def test_guardar_con_nombre_caracteres_especiales(repositorio):
    """Valida que caracteres especiales no rompen persistencia."""
    # ... implementación con nombre = "\", ', <, >, &"
```

**Validación**:
```bash
pytest tests_integrations/test_edge_cases_parametrizados.py -v
```

**Resultado esperado**: 6 tests pasando (3 edge cases × 2 repos)

---

## Ejercicio 3: Validar Calidad de Tests con IA

### 📋 Contexto

Has escrito una suite de tests, pero no estás seguro si son de alta calidad. Necesitas que IA evalúe la calidad y sugiera mejoras.

---

### 🤖 Paso 1: Evaluar tests con Test Quality Reviewer

**Prompt**:

```
Rol: Test Quality Reviewer

Evalúa la calidad de estos tests usando 7 criterios:

Código de tests:
[Pegar tests completos]

Criterios (puntúa 1-10 cada uno):
1. **Assertions significativas**: ¿Validan comportamiento o solo existencia?
2. **Independencia**: ¿Pueden correr en cualquier orden?
3. **Nombres descriptivos**: ¿Explican QUÉ testean?
4. **Edge cases**: ¿Cubren casos límite?
5. **Fragilidad**: ¿Se rompen solo con bugs reales?
6. **Velocidad**: ¿Corren en <1 segundo?
7. **Legibilidad**: ¿Un junior entiende qué falla?

Formato:
| Test | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Total | Problemas detectados |
|------|----|----|----|----|----|----|----| ------|----------------------|

Para tests con score <7/10:
- Lista problemas específicos
- Propón correcciones (código antes/después)
```

---

### 🤖 Paso 2: Corregir tests según recomendaciones de IA

Toma los tests con score <7 y refactorízalos según las recomendaciones.

**Ejemplo**:

```python
# ❌ ANTES (score: 4/10)
def test_crear():
    tarea = servicio.crear("Test")
    assert tarea  # Assertion débil

# ✅ DESPUÉS (score: 9/10)
def test_crear_tarea_asigna_id_positivo_y_estado_inicial():
    """Valida que nuevas tareas tienen ID válido y estado pendiente."""
    tarea = servicio.crear("Test")

    assert tarea.id > 0, f"ID debe ser positivo, fue {tarea.id}"
    assert tarea.nombre == "Test", "Nombre debe coincidir con input"
    assert tarea.completada is False, "Nueva tarea debe estar pendiente"
```

---

### 💾 Entregable

**Documento a crear**: `REPORTE_CALIDAD_TESTS.md`

**Contenido**:

```markdown
# Reporte de Calidad de Tests

## Evaluación Inicial

| Test | Assertions | Independencia | Nombres | Edge Cases | Fragilidad | Velocidad | Legibilidad | Total |
|------|------------|---------------|---------|------------|------------|-----------|-------------|-------|
| test_crear | 2 | 10 | 5 | 3 | 8 | 10 | 6 | 6.3/10 |
| test_listar | 3 | 10 | 7 | 5 | 9 | 10 | 8 | 7.4/10 |
| ... |

## Problemas Detectados

### Test #1: test_crear (6.3/10)
**Problemas**:
1. Assertion débil (`assert tarea`) - Solo valida que no es None
2. Nombre poco descriptivo - No dice QUÉ valida
3. No cubre edge cases (nombre vacío, IDs negativos)

**Correcciones aplicadas**:
[Código antes/después]

### Test #2: ...
[... más tests]

## Resultado Post-Corrección

| Test | Total Antes | Total Después | Mejora |
|------|-------------|---------------|--------|
| test_crear | 6.3 | 9.2 | +2.9 |
| ... |

**Promedio general**: 7.8/10 → 9.1/10 (+1.3)
```

---

## 🏆 Criterios de Éxito General

Para considerar los 3 ejercicios completos:

### Ejercicio 1 (Estrategia de Testing)
- [ ] Identificaste al menos 10 edge cases críticos
- [ ] Priorizaste por ROI (valor / esfuerzo)
- [ ] Tienes un plan de implementación por fases
- [ ] Detectaste gaps de cobertura en código actual

### Ejercicio 2 (Tests Parametrizados)
- [ ] Tests corren contra AMBOS repositorios (6 tests = 3 × 2 repos)
- [ ] Cada test valida un edge case crítico diferente
- [ ] Usa fixture parametrizado con tmp_path
- [ ] Todos los tests pasan en <1 segundo

### Ejercicio 3 (Calidad de Tests)
- [ ] Evaluaste al menos 5 tests con los 7 criterios
- [ ] Identificaste al menos 3 problemas de calidad
- [ ] Refactorizaste tests con score <7
- [ ] Promedio general >= 8/10 después de correcciones

---

## 📚 Recursos Adicionales

**Agentes educacionales recomendados**:
- `.claude/agents/educational/python-best-practices-coach.md` → Valida sintaxis, fixtures
- `.claude/agents/educational/fastapi-design-coach.md` → Revisa tests de endpoints
- `.claude/agents/educational/performance-optimizer.md` → Detecta tests lentos

**Documentación**:
- pytest fixtures: https://docs.pytest.org/en/stable/fixture.html
- pytest parametrize: https://docs.pytest.org/en/stable/parametrize.html
- Coverage.py: https://coverage.readthedocs.io/

**Librerías útiles**:
- `pytest-cov`: Coverage con pytest
- `pytest-xdist`: Tests en paralelo
- `pytest-mock`: Mocking simplificado

---

## 💡 Tips para Usar IA Efectivamente

### Prompts iterativos (refina hasta obtener calidad)

```
# Iteración 1: Estrategia general
"Genera estrategia de testing para mi API"

# Iteración 2: Refinar
"La estrategia menciona 'mockear repositorio'. ¿Por qué? Es rápido (<1ms)"

# Iteración 3: Corregir
"Genera la estrategia SIN mockear repositorios rápidos"

# Iteración 4: Validar
"Evalúa esta estrategia con criterios de ROI y detecta over-testing"
```

### Pregunta "¿Por qué?" para aprender

```
"¿Por qué este edge case es más crítico que este otro?"
"¿Por qué usar fixture parametrizado en vez de pytest.mark.parametrize?"
"¿Por qué este test tiene score bajo en 'Assertions'?"
```

### Valida con múltiples agentes

- **Test Coverage Strategist**: Qué testear
- **Python Best Practices Coach**: Cómo testear
- **Test Quality Reviewer**: Qué mejorar

---

**¡Éxito con los ejercicios! Recuerda: tests inteligentes > tests en cantidad. 🎯**
