# Workflow de Validaciones con Pydantic + IA - Clase 3

## 🎯 Objetivo

Dominar el workflow de validación de datos robusta usando Pydantic y IA como asistente para:
1. Identificar edge cases peligrosos
2. Generar validadores custom
3. Testear exhaustivamente validaciones
4. Documentar contratos de datos

---

## 🛡️ ¿Por Qué Validación es Crítica?

### El Problema

```python
# ❌ API sin validación
@app.post("/tareas")
def crear_tarea(data: dict):
    tarea = Tarea(**data)  # Asume que data es válido
    # ¿Qué pasa si data = {"nombre": "", "prioridad": -999}?
    # BOOM: Datos basura en BD, lógica rota
```

### La Solución: Pydantic como Guardián

```python
# ✅ API con validación en frontera
class TareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    prioridad: int = Field(default=3, ge=1, le=5)

@app.post("/tareas")
def crear_tarea(data: TareaRequest):
    # Si llega aquí, data es 100% válido
    tarea = Tarea(**data.model_dump())
```

**Beneficios**:
- ✅ Falla temprano (en el endpoint, no en BD)
- ✅ Mensajes de error claros (422 con detalles)
- ✅ Documentación automática (OpenAPI/Swagger)
- ✅ Type safety (IDE autocomplete)

---

## 📋 Workflow Paso a Paso

### Paso 1: Identificar Edge Cases con IA

**Objetivo**: Descubrir todos los datos inválidos que pueden romper el sistema.

**Prompt para IA**:
```
Rol: QA Engineer especializado en edge cases
Contexto: API REST de tareas con modelo Tarea
Campos actuales:
- nombre: string (nombre de la tarea)
- prioridad: int (1 urgente a 5 baja)
- fecha_limite: date opcional
- etiquetas: lista de strings
Objetivo: Identifica 15 edge cases peligrosos que debo validar
Formato: Tabla markdown con columnas:
| Campo | Input Inválido | Por Qué es Peligroso | Validación Sugerida |
```

**Output esperado de IA**:

| Campo | Input Inválido | Por Qué es Peligroso | Validación Sugerida |
|-------|---------------|----------------------|---------------------|
| nombre | `""` (vacío) | Tareas sin identificador, imposible buscar | `min_length=1` |
| nombre | `" "` (solo espacios) | Parece válido pero es basura | `@field_validator`: strip + check |
| nombre | `"A"*1000` | Rompe UI, overflow en BD | `max_length=100` |
| nombre | `"<script>alert()</script>"` | XSS attack | Sanitizar caracteres `<>` |
| prioridad | `0` o `6` | Fuera de rango, lógica rota | `ge=1, le=5` |
| prioridad | `-999` | Overflow negativo | `ge=1` |
| prioridad | `"alta"` (string) | Type error en comparaciones | Pydantic valida tipo automáticamente |
| prioridad | `null` | Si es requerido, error inesperado | `...` (required) o `default=3` |
| fecha_limite | `"2020-01-01"` | Fecha pasada, imposible cumplir | `@field_validator`: >= today |
| fecha_limite | `"ayer"` | Formato inválido | Usar `date` type (Pydantic parsea) |
| fecha_limite | `"9999-12-31"` | Fecha irreal, lógica rota | `@field_validator`: <= 10 años futuro |
| etiquetas | `null` | TypeError al iterar | `default_factory=list` |
| etiquetas | `["A"*200, ...]` | Etiquetas enormes, BD overflow | `@field_validator`: max_length por tag |
| etiquetas | `["tag1"]*100` | Demasiadas etiquetas, UI rota | `max_length=10` (lista) |
| etiquetas | `["TAG", "Tag", "tag"]` | Duplicados por case | `@field_validator`: lowercase + unique |

**Acción**:
1. Copia la tabla a un archivo `edge_cases.md`
2. Prioriza por severidad (crítico → medio → bajo)
3. Decide cuáles implementar ahora vs después

---

### Paso 2: Diseñar Modelo Pydantic Base

**Prompt para IA**:
```
Rol: Pydantic Expert
Contexto: Modelo TareaRequest para API REST
Campos:
- nombre: str (1-100 chars)
- prioridad: int (1-5, default 3)
- fecha_limite: date opcional
- etiquetas: list[str] (max 10, default [])
Objetivo: Genera modelo Pydantic v2 con Field() validations
Requisitos:
- Type hints completos
- Docstring con ejemplo de uso
- Descriptions en español para OpenAPI
- Examples para cada campo
Restricciones: Pydantic v2 syntax
```

**Output esperado**:
```python
from pydantic import BaseModel, Field
from typing import List
from datetime import date

class TareaRequest(BaseModel):
    """Modelo para crear/actualizar tareas con validaciones robustas.

    Example:
        >>> tarea = TareaRequest(
        ...     nombre="Estudiar Pydantic",
        ...     prioridad=1,
        ...     fecha_limite=date(2025, 12, 31),
        ...     etiquetas=["python", "educación"]
        ... )
    """

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre descriptivo de la tarea (1-100 caracteres)",
        examples=["Estudiar Pydantic", "Refactorizar API", "Escribir tests"]
    )

    prioridad: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Prioridad: 1 (urgente) a 5 (baja). Default: 3 (normal)"
    )

    fecha_limite: date | None = Field(
        default=None,
        description="Fecha límite opcional en formato YYYY-MM-DD"
    )

    etiquetas: List[str] = Field(
        default_factory=list,
        max_length=10,
        description="Lista de etiquetas (máximo 10)"
    )
```

**Validación manual**:
- [ ] Type hints correctos (`str`, `int`, `date | None`, `List[str]`)
- [ ] Docstring con ejemplo ejecutable
- [ ] Descriptions en español (para la API)
- [ ] Examples útiles (no genéricos)

---

### Paso 3: Generar Validadores Custom con IA

**Para cada edge case complejo**, genera un `@field_validator`.

#### Ejemplo 1: Validar nombre (no solo espacios, sanitizar)

**Prompt**:
```
Rol: Pydantic Expert
Contexto: TareaRequest con campo nombre: str
Objetivo: Genera @field_validator que:
1. Strip espacios al inicio/fin
2. Rechaza si solo espacios o vacío
3. Sanitiza caracteres peligrosos: < > & " '
4. Capitaliza primera letra
Requisitos:
- Pydantic v2 (@field_validator, @classmethod)
- Mensaje error en español
- Docstring explicativo
Formato: Código Python listo para copiar
```

**Output esperado**:
```python
@field_validator('nombre')
@classmethod
def validar_y_sanitizar_nombre(cls, v: str) -> str:
    """Valida y limpia el nombre de la tarea.

    Reglas:
    - Elimina espacios al inicio/fin
    - Rechaza nombres vacíos o solo espacios
    - Sanitiza caracteres peligrosos (<, >, &, ", ')
    - Capitaliza primera letra

    Args:
        v: Nombre a validar

    Returns:
        Nombre validado y limpio

    Raises:
        ValueError: Si nombre vacío o solo espacios
    """
    # 1. Limpiar espacios
    v = v.strip()

    # 2. Validar no vacío
    if not v:
        raise ValueError('El nombre no puede estar vacío o contener solo espacios')

    # 3. Sanitizar caracteres peligrosos
    caracteres_peligrosos = {
        '<': '',
        '>': '',
        '&': 'y',
        '"': '',
        "'": ''
    }
    for char, reemplazo in caracteres_peligrosos.items():
        v = v.replace(char, reemplazo)

    # 4. Capitalizar
    return v.capitalize()
```

**Validación**:
1. ✅ ¿Usa `@field_validator` (Pydantic v2)?
2. ✅ ¿Mensaje error claro en español?
3. ✅ ¿Docstring explica qué hace?
4. ⚠️ **Test manual**: Ejecuta con varios inputs

```python
# Test mental:
TareaRequest(nombre="  hola  ")  # → "Hola"
TareaRequest(nombre="<script>")  # → "Script"
TareaRequest(nombre="   ")  # → ValueError
```

---

#### Ejemplo 2: Validar fecha_limite (no pasada, max 10 años)

**Prompt**:
```
Rol: Pydantic Expert
Contexto: TareaRequest con fecha_limite: date | None
Objetivo: Genera @field_validator que:
1. Si None, lo permite (campo opcional)
2. Si date, valida que >= hoy
3. Si date, valida que <= 10 años en futuro
Requisitos: Pydantic v2, mensaje error español
```

**Output**:
```python
from datetime import date, timedelta

@field_validator('fecha_limite')
@classmethod
def validar_fecha_limite(cls, v: date | None) -> date | None:
    """Valida que la fecha límite sea futura y razonable.

    Reglas:
    - None es permitido (campo opcional)
    - Fecha debe ser >= hoy
    - Fecha debe ser <= 10 años en futuro

    Args:
        v: Fecha a validar (o None)

    Returns:
        Fecha validada (o None)

    Raises:
        ValueError: Si fecha es pasada o muy lejana
    """
    if v is None:
        return v

    hoy = date.today()
    max_futuro = hoy + timedelta(days=10*365)

    if v < hoy:
        raise ValueError(
            f'La fecha límite no puede estar en el pasado '
            f'(recibido: {v}, hoy: {hoy})'
        )

    if v > max_futuro:
        raise ValueError(
            f'La fecha límite no puede ser más de 10 años en el futuro '
            f'(recibido: {v}, máximo: {max_futuro})'
        )

    return v
```

---

#### Ejemplo 3: Validar etiquetas (lowercase, unique, max length)

**Prompt**:
```
Rol: Pydantic Expert
Contexto: etiquetas: List[str]
Objetivo: @field_validator que:
1. Convierte a lowercase
2. Strip espacios
3. Elimina duplicados
4. Rechaza etiquetas > 50 chars
5. Rechaza lista vacía si prioridad <= 2 (este va en @model_validator)
```

**Output**:
```python
@field_validator('etiquetas')
@classmethod
def normalizar_etiquetas(cls, v: List[str]) -> List[str]:
    """Normaliza y valida lista de etiquetas.

    Reglas:
    - Convierte a minúsculas
    - Elimina espacios extras
    - Elimina duplicados (mantiene orden)
    - Máximo 50 caracteres por etiqueta

    Args:
        v: Lista de etiquetas

    Returns:
        Lista de etiquetas normalizadas

    Raises:
        ValueError: Si alguna etiqueta > 50 chars
    """
    # 1. Normalizar: lowercase + strip
    etiquetas_normalizadas = [tag.lower().strip() for tag in v]

    # 2. Validar longitud por etiqueta
    for tag in etiquetas_normalizadas:
        if len(tag) > 50:
            raise ValueError(
                f'Etiqueta muy larga: "{tag}" ({len(tag)} chars). '
                f'Máximo: 50 caracteres'
            )

    # 3. Eliminar duplicados (mantener orden)
    etiquetas_unicas = []
    vistos = set()
    for tag in etiquetas_normalizadas:
        if tag not in vistos:
            etiquetas_unicas.append(tag)
            vistos.add(tag)

    return etiquetas_unicas
```

---

### Paso 4: Model Validators (Validaciones entre Campos)

A veces necesitas validar **relaciones entre campos**.

**Caso**: Si prioridad <= 2 (urgente), entonces fecha_limite es obligatoria y etiquetas no pueden estar vacías.

**Prompt**:
```
Rol: Pydantic Expert
Contexto: TareaRequest con prioridad, fecha_limite, etiquetas
Objetivo: @model_validator que valide:
1. Si prioridad <= 2 → fecha_limite obligatoria
2. Si prioridad <= 2 → etiquetas no vacías
Requisitos: Pydantic v2 (@model_validator mode='after')
```

**Output**:
```python
from pydantic import model_validator

class TareaRequest(BaseModel):
    # ... campos anteriores ...

    @model_validator(mode='after')
    def validar_tareas_urgentes(self):
        """Tareas urgentes requieren fecha límite y etiquetas.

        Si prioridad <= 2 (urgente/alta):
        - fecha_limite es obligatoria
        - etiquetas no puede estar vacía

        Raises:
            ValueError: Si tarea urgente sin fecha o etiquetas
        """
        if self.prioridad <= 2:
            if self.fecha_limite is None:
                raise ValueError(
                    f'Las tareas urgentes (prioridad {self.prioridad}) '
                    'requieren una fecha límite'
                )

            if not self.etiquetas:
                raise ValueError(
                    f'Las tareas urgentes (prioridad {self.prioridad}) '
                    'requieren al menos una etiqueta para clasificación'
                )

        return self
```

---

### Paso 5: Generar Tests de Edge Cases con IA

**Prompt para IA**:
```
Rol: QA Tester Python
Contexto: TareaRequest con validaciones Pydantic
Objetivo: Genera 15 tests pytest que DEBEN FALLAR (edge cases)
Formato: Código pytest con:
- Test name descriptivo
- pytest.raises con ValidationError o ValueError
- Mensaje match para validar error correcto
Requisitos: Usar pytest, Pydantic ValidationError
```

**Output esperado**:
```python
import pytest
from pydantic import ValidationError
from datetime import date, timedelta
from api.models import TareaRequest

# === Tests de campo 'nombre' ===

def test_nombre_vacio_falla():
    """Nombre vacío debe fallar validación."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        TareaRequest(nombre="")

def test_nombre_solo_espacios_falla():
    """Nombre con solo espacios debe fallar."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        TareaRequest(nombre="   ")

def test_nombre_excede_max_length_falla():
    """Nombre > 100 caracteres debe fallar."""
    with pytest.raises(ValidationError):
        TareaRequest(nombre="A" * 101)

def test_nombre_sanitiza_caracteres_peligrosos():
    """Caracteres peligrosos deben ser removidos."""
    tarea = TareaRequest(nombre="<script>alert()</script>")
    assert "<" not in tarea.nombre
    assert ">" not in tarea.nombre
    assert tarea.nombre == "Scriptalert()"  # Capitalizado

# === Tests de campo 'prioridad' ===

def test_prioridad_menor_que_1_falla():
    """Prioridad < 1 debe fallar."""
    with pytest.raises(ValidationError):
        TareaRequest(nombre="Test", prioridad=0)

def test_prioridad_mayor_que_5_falla():
    """Prioridad > 5 debe fallar."""
    with pytest.raises(ValidationError):
        TareaRequest(nombre="Test", prioridad=6)

def test_prioridad_default_es_3():
    """Si no se especifica, prioridad debe ser 3."""
    tarea = TareaRequest(nombre="Test")
    assert tarea.prioridad == 3

# === Tests de campo 'fecha_limite' ===

def test_fecha_pasada_falla():
    """Fecha en el pasado debe fallar."""
    fecha_ayer = date.today() - timedelta(days=1)
    with pytest.raises(ValueError, match="no puede estar en el pasado"):
        TareaRequest(nombre="Test", fecha_limite=fecha_ayer)

def test_fecha_muy_futura_falla():
    """Fecha > 10 años debe fallar."""
    fecha_lejana = date.today() + timedelta(days=11*365)
    with pytest.raises(ValueError, match="más de 10 años"):
        TareaRequest(nombre="Test", fecha_limite=fecha_lejana)

def test_fecha_none_es_valida():
    """Fecha None debe ser permitida."""
    tarea = TareaRequest(nombre="Test", fecha_limite=None)
    assert tarea.fecha_limite is None

# === Tests de campo 'etiquetas' ===

def test_etiquetas_se_convierten_a_minusculas():
    """Etiquetas deben ser lowercase."""
    tarea = TareaRequest(nombre="Test", etiquetas=["PYTHON", "Django"])
    assert tarea.etiquetas == ["python", "django"]

def test_etiquetas_duplicadas_se_eliminan():
    """Duplicados deben ser removidos."""
    tarea = TareaRequest(nombre="Test", etiquetas=["python", "PYTHON", "Python"])
    assert tarea.etiquetas == ["python"]  # Solo una

def test_etiqueta_muy_larga_falla():
    """Etiqueta > 50 chars debe fallar."""
    with pytest.raises(ValueError, match="muy larga"):
        TareaRequest(nombre="Test", etiquetas=["A" * 51])

def test_etiquetas_default_es_lista_vacia():
    """Default debe ser lista vacía, no None."""
    tarea = TareaRequest(nombre="Test")
    assert tarea.etiquetas == []
    assert isinstance(tarea.etiquetas, list)

# === Tests de model_validator (relaciones entre campos) ===

def test_tarea_urgente_sin_fecha_falla():
    """Prioridad 1-2 requiere fecha límite."""
    with pytest.raises(ValueError, match="requieren una fecha límite"):
        TareaRequest(nombre="Test", prioridad=1, fecha_limite=None)

def test_tarea_urgente_sin_etiquetas_falla():
    """Prioridad 1-2 requiere al menos 1 etiqueta."""
    mañana = date.today() + timedelta(days=1)
    with pytest.raises(ValueError, match="requieren al menos una etiqueta"):
        TareaRequest(
            nombre="Test",
            prioridad=1,
            fecha_limite=mañana,
            etiquetas=[]
        )

def test_tarea_normal_sin_fecha_es_valida():
    """Prioridad 3+ puede no tener fecha."""
    tarea = TareaRequest(nombre="Test", prioridad=3, fecha_limite=None)
    assert tarea.fecha_limite is None  # OK
```

---

### Paso 6: Ejecutar Tests y Refinar

```bash
# Ejecutar todos los tests de validación
pytest tests/test_validaciones.py -v

# Ver coverage de validadores
pytest tests/test_validaciones.py --cov=api.models --cov-report=term-missing
```

**Si algún test falla**:
1. Lee el error message
2. Ajusta el validator
3. Re-ejecuta test
4. Itera hasta verde

---

## 🎓 Checklist de Validación Completa

Antes de dar por terminadas las validaciones:

### Validaciones Básicas (Field)
- [ ] Todos los campos tienen type hints
- [ ] Campos requeridos usan `...`
- [ ] Campos opcionales tienen `default=...` o `default_factory=...`
- [ ] Limits numéricos (`ge`, `le`, `gt`, `lt`)
- [ ] Límites de longitud (`min_length`, `max_length`)
- [ ] Descriptions en español para OpenAPI
- [ ] Examples útiles para cada campo

### Validadores Custom (@field_validator)
- [ ] Nombres descriptivos (`validar_nombre_seguro` no `val1`)
- [ ] Docstrings con reglas claras
- [ ] Mensajes de error en español
- [ ] Syntax Pydantic v2 (`@field_validator`, `@classmethod`)
- [ ] Return type correcto (mismo que el campo)

### Model Validators (@model_validator)
- [ ] Validaciones de relaciones entre campos
- [ ] `mode='after'` (valida después de field_validators)
- [ ] Return `self` al final

### Tests
- [ ] Al menos 15 tests de edge cases
- [ ] Cobertura > 80% de validadores
- [ ] Tests para casos exitosos también
- [ ] Tests con `pytest.raises` para errores esperados

### Documentación
- [ ] Swagger UI (`/docs`) muestra validaciones
- [ ] Ejemplos ejecutables en Swagger
- [ ] Mensajes de error claros en respuestas 422

---

## 🚨 Red Flags de Validaciones Generadas por IA

### Red Flag #1: Validador que cambia tipo

```python
# ❌ MAL: Cambia tipo de int a str
@field_validator('prioridad')
def val(cls, v):
    return str(v)  # prioridad ahora es str, no int
```

### Red Flag #2: Validaciones contradictorias

```python
# ❌ MAL: Campo requerido pero acepta None
nombre: str | None = Field(..., min_length=1)
```

### Red Flag #3: Regex sin explicación

```python
# ❌ MAL: Regex críptico
@field_validator('email')
def val(cls, v):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', v):
        raise ValueError("Inválido")  # ¿Por qué?
```

✅ **Mejor**: Usa tipos built-in de Pydantic
```python
from pydantic import EmailStr

class Usuario(BaseModel):
    email: EmailStr  # Valida automáticamente
```

### Red Flag #4: Performance horrible

```python
# ❌ MAL: Llamada API en validador (slow!)
@field_validator('username')
def val(cls, v):
    response = requests.get(f"https://api.com/check/{v}")  # ⚠️ Lento
    if not response.ok:
        raise ValueError("Username no disponible")
    return v
```

---

## 💡 Tips Avanzados

### Tip 1: Reutilizar Validadores

```python
from typing import Annotated
from pydantic import AfterValidator

def sanitizar_string(v: str) -> str:
    return v.strip().capitalize()

# Reutilizar en múltiples campos
StringSanitizado = Annotated[str, AfterValidator(sanitizar_string)]

class TareaRequest(BaseModel):
    nombre: StringSanitizado
    descripcion: StringSanitizado
```

### Tip 2: Validar con Dependencias Externas (con caché)

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def es_palabra_valida(palabra: str) -> bool:
    """Cache de palabras válidas (evita lookups repetidos)."""
    return palabra in diccionario_palabras

@field_validator('nombre')
def nombre_valido(cls, v: str) -> str:
    if not es_palabra_valida(v):
        raise ValueError(f"'{v}' no es una palabra válida")
    return v
```

### Tip 3: Mensajes de Error Personalizados Globalmente

```python
from pydantic import ConfigDict

class TareaRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Auto-strip en todos los strings
        str_min_length=1,  # Mínimo 1 char global
        validate_assignment=True,  # Validar en asignaciones (no solo __init__)
    )
```

---

## 📚 Recursos Adicionales

**Documentación**:
- [Pydantic v2 Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Pydantic Field Types](https://docs.pydantic.dev/latest/concepts/types/)
- [FastAPI Request Validation](https://fastapi.tiangolo.com/tutorial/body/)

**Agentes educacionales**:
- [Python Best Practices Coach](../../.claude/agents/educational/python-best-practices-coach.md) (type hints, docstrings)
- [FastAPI Design Coach](../../.claude/agents/educational/fastapi-design-coach.md) (response models, validation)

**Herramientas**:
```bash
# Validar tipos estáticamente
mypy api/models.py

# Tests de validación
pytest tests/test_validaciones.py -v --cov

# Ver schema OpenAPI generado
uvicorn api:app --reload
# Abrir http://localhost:8000/docs
```

---

**Recuerda**: La validación no es paranoia, es **ingeniería defensiva**. Cada edge case que detectes ahora es un bug que NO llegará a producción.
