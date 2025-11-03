# Clase 6.7: Writing Tools for AI Agents

## Índice

1. [Introducción](#introducción)
2. [Principios Fundamentales de Diseño de Tools](#principios-fundamentales-de-diseño-de-tools)
3. [Tool Schemas y Type Hints](#tool-schemas-y-type-hints)
4. [Input Validation en Tools](#input-validation-en-tools)
5. [Error Handling en Tools](#error-handling-en-tools)
6. [Tool Descriptions Efectivas](#tool-descriptions-efectivas)
7. [Composición de Tools](#composición-de-tools)
8. [Tools Asíncronos vs Síncronos](#tools-asíncronos-vs-síncronos)
9. [Rate Limiting y Resource Management](#rate-limiting-y-resource-management)
10. [Security Considerations en Tools](#security-considerations-en-tools)
11. [Testing de Tools](#testing-de-tools)
12. [Debugging: ¿Por qué el agente no usa mi tool?](#debugging-por-qué-el-agente-no-usa-mi-tool)
13. [Proyecto: Suite de Tools para Agente de Desarrollo](#proyecto-suite-de-tools-para-agente-de-desarrollo)

---

## Introducción

**¿Qué son los tools para agentes IA?**

Los **tools** (herramientas) son funciones que los agentes de IA pueden invocar para interactuar con el mundo exterior: APIs, bases de datos, sistemas de archivos, etc. Son el puente entre el razonamiento del agente y las acciones reales.

**¿Por qué es crítico diseñarlos bien?**

Un tool mal diseñado puede:
- Confundir al agente (no sabe cuándo usarlo)
- Desperdiciar tokens (retorna información irrelevante)
- Generar errores crípticos (el agente no sabe cómo corregir)
- Bloquear workflows (múltiples llamadas innecesarias)

**Visión de esta clase**: Aprender a diseñar tools que **guíen al agente hacia workflows eficientes**, siguiendo las best practices de Anthropic.

---

## Principios Fundamentales de Diseño de Tools

### 1. Diseñar para "Affordances" del Agente, No para APIs Tradicionales

**Diferencia clave**: Los agentes tienen **contexto limitado** (context window), pero memoria computacional abundante. Las APIs tradicionales asumen lo contrario.

**❌ Mal diseño**:
```python
def list_contacts() -> list[dict]:
    """Retorna TODOS los contactos (5000+ registros)"""
    return database.get_all_contacts()
```

**✅ Buen diseño**:
```python
def search_contacts(query: str, limit: int = 10) -> list[dict]:
    """Busca contactos relevantes según query (máximo 10 resultados)"""
    return database.search_contacts(query, limit)
```

**Razón**: El agente rara vez necesita **todos** los contactos. Retornar 5000 contactos consume tokens innecesariamente y dificulta que el agente encuentre la información relevante.

### 2. Consolidar Funcionalidad

Los tools deben manejar **múltiples operaciones discretas** bajo el capó.

**❌ Mal diseño (3 tools separados)**:
```python
def list_users() -> list[dict]: ...
def list_events(user_id: str) -> list[dict]: ...
def create_event(user_id: str, event_data: dict) -> dict: ...
```

**✅ Buen diseño (1 tool consolidado)**:
```python
def schedule_event(
    participant_emails: list[str],
    title: str,
    duration_minutes: int
) -> dict:
    """
    Busca disponibilidad de participantes y agenda evento automáticamente.

    Internamente:
    1. Encuentra usuarios por email
    2. Consulta calendarios para disponibilidad
    3. Crea evento en slot disponible
    """
    # ... lógica consolidada
```

**Ventaja**: El agente hace **1 llamada** en lugar de 3-5 llamadas secuenciales.

**Más ejemplos**:
- `search_logs(query: str)` en lugar de `read_logs() + filter_logs()`
- `get_customer_context(customer_id: str)` en lugar de `get_customer() + get_transactions() + get_notes()`

### 3. Priorizar Workflows de Alto Impacto

**No implementes tools para "cubrir" toda una API**. Enfócate en workflows específicos que tu agente **realmente necesita**.

**Pregunta clave**: ¿Qué tareas quiero que mi agente resuelva?

**Ejemplo**:
- **Agente de soporte técnico**: `search_tickets`, `get_customer_context`, `create_internal_note`
- **Agente de desarrollo**: `search_codebase`, `run_tests`, `create_git_branch`

**Anti-patrón**: Wrappear todos los endpoints de una API REST (90+ tools) sin evaluar cuáles son realmente útiles.

---

## Tool Schemas y Type Hints

### Identificadores Semánticos vs Identificadores Crípticos

**❌ Mal diseño**:
```python
def get_user(id: str) -> dict:
    """
    Args:
        id: User UUID (e.g., "a3f2e8d1-4c5b-6a7d-8e9f-0a1b2c3d4e5f")
    """
    pass
```

**Problemas**:
- UUIDs alfanuméricos son **difíciles de recordar** para agentes
- Aumentan **alucinaciones** (el agente inventa IDs que no existen)

**✅ Buen diseño**:
```python
def search_user_by_email(email: str) -> dict:
    """
    Busca usuario por email.

    Args:
        email: Email del usuario (e.g., "juan@empresa.com")

    Returns:
        {
            "name": "Juan Pérez",
            "email": "juan@empresa.com",
            "role": "developer",
            "team": "backend"
        }
    """
    pass
```

**Razón**: Los **identificadores semánticos** (emails, nombres) son más naturales para agentes que UUIDs arbitrarios.

### Parámetro `response_format` para Controlar Detalle

**Técnica avanzada**: Permitir que el agente elija el nivel de detalle de la respuesta.

```python
from enum import Enum
from typing import Literal

class ResponseFormat(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"

def search_slack_messages(
    query: str,
    limit: int = 10,
    response_format: ResponseFormat = ResponseFormat.CONCISE
) -> list[dict]:
    """
    Busca mensajes en Slack.

    Args:
        query: Texto a buscar
        limit: Máximo de resultados
        response_format:
            - "detailed": Incluye IDs, metadatos (para llamadas downstream)
            - "concise": Solo contenido esencial (ahorra tokens)

    Returns (concise):
        [
            {
                "text": "Fix bug in API endpoint",
                "author": "Ana",
                "timestamp": "2025-10-20"
            }
        ]

    Returns (detailed):
        [
            {
                "text": "Fix bug in API endpoint",
                "author": "Ana",
                "timestamp": "2025-10-20",
                "thread_ts": "1729468800.123456",  # Para responder en thread
                "channel_id": "C12345",             # Para operaciones downstream
                "user_id": "U67890"
            }
        ]
    """
    results = slack_api.search(query, limit)

    if response_format == ResponseFormat.CONCISE:
        return [
            {
                "text": msg["text"],
                "author": msg["user_name"],
                "timestamp": msg["ts"]
            }
            for msg in results
        ]
    else:
        return results  # Respuesta completa con IDs
```

**Ventajas**:
- **Ahorro de tokens**: Respuesta concisa consume ~1/3 de tokens que la detallada
- **Flexibilidad**: El agente decide según su necesidad (¿necesito más contexto o solo leer?)

### Formato de Respuesta: JSON, XML, Markdown

**Recomendación**: Los LLMs tienen **sesgo hacia formatos** que vieron en su training data.

**Experimenta con**:
- **JSON**: Estructurado, parseable, común en APIs
- **XML**: Mejor para jerarquías complejas
- **Markdown**: Más legible para agentes, bueno para documentos largos

**Ejemplo Markdown**:
```python
def get_project_status(project_id: str) -> str:
    """
    Retorna status del proyecto en formato Markdown.

    Returns:
        # Proyecto: API Refactor

        **Status**: En progreso (70%)

        ## Tasks Completadas
        - [x] Migrar endpoints a FastAPI
        - [x] Agregar validación Pydantic

        ## Tasks Pendientes
        - [ ] Añadir tests de integración
        - [ ] Deploy a staging

        ## Blockers
        - Database migration pending (bloqueado por DBA)
    """
    pass
```

**Ventaja Markdown**: El agente puede "leer" el status sin parsear JSON complejo.

---

## Input Validation en Tools

### 1. Nombres de Parámetros Específicos y Sin Ambigüedad

**❌ Ambiguo**:
```python
def get_user(user: str) -> dict:  # ¿Es email? ¿Es ID? ¿Es nombre?
    pass
```

**✅ Específico**:
```python
def get_user_by_email(email: str) -> dict:
    """
    Busca usuario por email exacto.

    Args:
        email: Email del usuario (formato: name@domain.com)
    """
    pass
```

### 2. Validación con Pydantic (Type Safety)

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class SearchContactsInput(BaseModel):
    """Schema de input para search_contacts tool."""

    query: str = Field(
        min_length=2,
        max_length=100,
        description="Texto a buscar (mínimo 2 caracteres)"
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Máximo de resultados (entre 1 y 50)"
    )

    search_field: Literal["name", "email", "company"] = Field(
        default="name",
        description="Campo donde buscar"
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        if "@" in v and "." not in v:
            raise ValueError(
                "Email inválido. Formato esperado: name@domain.com"
            )
        return v.strip()

def search_contacts(input_data: SearchContactsInput) -> list[dict]:
    """
    Busca contactos según criterios.

    Args:
        input_data: Parámetros validados por Pydantic

    Returns:
        Lista de contactos relevantes

    Raises:
        ValidationError: Si los inputs no cumplen el schema
    """
    # Pydantic ya validó los inputs antes de llegar aquí
    return database.search(
        query=input_data.query,
        field=input_data.search_field,
        limit=input_data.limit
    )
```

**Ventajas de Pydantic**:
- Validación automática de types
- Errores claros y descriptivos
- Conversión automática de tipos (e.g., `"10"` → `10`)
- Documentación auto-generada del schema

### 3. Mensajes de Error Accionables

**❌ Error críptico**:
```python
def create_event(date: str) -> dict:
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format")  # ¿Qué formato esperas?
```

**✅ Error accionable**:
```python
def create_event(date: str) -> dict:
    """
    Crea evento en fecha especificada.

    Args:
        date: Fecha en formato YYYY-MM-DD (e.g., "2025-10-23")
    """
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        # Mensaje que guía al agente a corregir
        raise ValueError(
            f"Formato de fecha inválido: '{date}'. "
            f"Formato esperado: YYYY-MM-DD (ejemplo: '2025-10-23'). "
            f"Intenta de nuevo con el formato correcto."
        )
```

**Principio**: El error debe **enseñar al agente cómo corregirse**.

---

## Error Handling en Tools

### Filosofía: Errores como Guía, No como Bloqueo

Los errores en tools deben:
1. **Comunicar el problema claramente**
2. **Sugerir la solución** (qué hacer diferente)
3. **Evitar stack traces** (no útiles para agentes)

### Patrón: Result Type (Success/Failure)

```python
from typing import Union, Literal
from pydantic import BaseModel

class ToolSuccess(BaseModel):
    status: Literal["success"] = "success"
    data: dict

class ToolError(BaseModel):
    status: Literal["error"] = "error"
    error_type: str
    message: str
    suggestion: str

ToolResult = Union[ToolSuccess, ToolError]

def search_logs(
    query: str,
    lines: int = 100
) -> ToolResult:
    """
    Busca en logs del sistema.

    Args:
        query: Regex o texto a buscar
        lines: Número de líneas de contexto (máx 1000)

    Returns:
        Success con líneas relevantes O Error con sugerencia
    """
    # Validar límite de lines
    if lines > 1000:
        return ToolError(
            error_type="validation_error",
            message=f"Límite de líneas excedido: {lines} (máximo 1000)",
            suggestion=(
                "Reduce el número de líneas a 1000 o menos. "
                "Alternativamente, usa filtros más específicos en tu query "
                "para reducir resultados."
            )
        )

    # Validar regex
    try:
        regex_pattern = re.compile(query)
    except re.error as e:
        return ToolError(
            error_type="regex_error",
            message=f"Regex inválido: {str(e)}",
            suggestion=(
                f"Tu query '{query}' no es un regex válido. "
                f"Intenta con búsqueda de texto simple (sin regex) "
                f"o corrige la sintaxis del regex."
            )
        )

    # Búsqueda exitosa
    results = log_system.search(regex_pattern, lines)
    return ToolSuccess(data={"lines": results, "count": len(results)})
```

### Manejo de Rate Limits

```python
from time import sleep
from functools import wraps

class RateLimitError(Exception):
    """Error cuando se excede rate limit."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit excedido. "
            f"Espera {retry_after} segundos antes de reintentar."
        )

def with_rate_limit_retry(max_retries: int = 3):
    """Decorator para reintentar automáticamente cuando hay rate limit."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    if attempt == max_retries - 1:
                        # Último intento fallido
                        return ToolError(
                            error_type="rate_limit_exceeded",
                            message=str(e),
                            suggestion=(
                                "El servicio está bajo alta carga. "
                                "Intenta de nuevo en unos minutos o "
                                "reduce la frecuencia de llamadas."
                            )
                        )
                    # Esperar antes de reintentar
                    sleep(e.retry_after)
            return ToolError(
                error_type="max_retries_exceeded",
                message=f"Fallaron {max_retries} intentos por rate limit",
                suggestion="Contacta al administrador del sistema"
            )
        return wrapper
    return decorator

@with_rate_limit_retry(max_retries=3)
def call_external_api(endpoint: str) -> dict:
    """Llama a API externa con retry automático en rate limit."""
    response = requests.get(endpoint)

    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        raise RateLimitError(retry_after)

    return response.json()
```

---

## Tool Descriptions Efectivas

### Anatomía de una Buena Description

```python
def search_codebase(
    query: str,
    file_pattern: str = "*.py",
    context_lines: int = 3
) -> list[dict]:
    """
    Busca código en el repositorio usando grep semántico.

    **Cuándo usar este tool:**
    - Necesitas encontrar dónde se define una función/clase
    - Quieres ver ejemplos de uso de una API
    - Buscas referencias a una variable/constante específica

    **NO usar para:**
    - Leer archivos completos (usa `read_file` en su lugar)
    - Listar todos los archivos (usa `list_files`)

    Args:
        query: Texto o regex a buscar
            Ejemplos:
            - "def calculate_total" (busca definición de función)
            - "import requests" (busca imports)
            - "class.*Task" (regex para clases que terminan en Task)

        file_pattern: Patrón glob para filtrar archivos
            Ejemplos:
            - "*.py" (solo Python)
            - "tests/**/*.py" (solo tests)
            - "api/endpoints/**" (solo en api/endpoints/)

        context_lines: Líneas de contexto antes/después del match
            Rango válido: 0-10
            Default: 3 (suficiente para entender contexto)

    Returns:
        Lista de matches con contexto:
        [
            {
                "file": "api/tasks.py",
                "line_number": 42,
                "match": "def calculate_total(items: list[Item]) -> float:",
                "context_before": ["    # Calculate sum of all items", "    total = 0"],
                "context_after": ["        total += item.price", "    return total"]
            }
        ]

    Raises:
        ValidationError: Si context_lines > 10
        RegexError: Si query es regex inválido

    **Relaciones con otros tools:**
    - Usa `read_file` después de encontrar el archivo correcto
    - Usa `get_function_definition` para ver función completa

    **Formato especializado:**
    Este tool soporta regex de Python. Escapa caracteres especiales:
    - Punto literal: "\\." no "."
    - Paréntesis literal: "\\(" no "("

    **Ejemplos de uso:**

    Ejemplo 1: Buscar definición de función
    >>> search_codebase(query="def process_payment", file_pattern="api/**/*.py")

    Ejemplo 2: Buscar imports de biblioteca específica
    >>> search_codebase(query="from fastapi import", context_lines=0)

    Ejemplo 3: Buscar clases que heredan de BaseModel
    >>> search_codebase(query="class.*\\(BaseModel\\)", file_pattern="models/*.py")
    """
    pass
```

### Checklist de una Buena Description

- [ ] **Propósito claro**: ¿Qué hace el tool?
- [ ] **Cuándo usarlo**: Casos de uso específicos
- [ ] **Cuándo NO usarlo**: Evitar confusión con otros tools
- [ ] **Args documentados**: Explicar cada parámetro con ejemplos
- [ ] **Returns documentados**: Estructura de la respuesta
- [ ] **Raises documentados**: Errores posibles
- [ ] **Ejemplos de uso**: 2-3 casos reales
- [ ] **Relaciones con otros tools**: ¿Qué tools usar antes/después?
- [ ] **Formatos especializados**: Regex, date formats, etc.
- [ ] **Nombres semánticos**: Sin ambigüedad

---

## Composición de Tools

### Tools que Llaman Tools

**Concepto**: Un tool de alto nivel puede orquestar múltiples tools de bajo nivel.

**Ejemplo: Tool de análisis de performance**

```python
def analyze_api_performance(endpoint: str) -> dict:
    """
    Analiza performance de un endpoint de la API.

    Internamente ejecuta:
    1. search_codebase() - Encuentra implementación del endpoint
    2. search_logs() - Busca requests recientes a ese endpoint
    3. calculate_stats() - Calcula percentiles de response time
    4. get_error_rate() - Obtiene tasa de errores

    Args:
        endpoint: Path del endpoint (e.g., "/api/tasks")

    Returns:
        {
            "endpoint": "/api/tasks",
            "implementation_file": "api/tasks.py:42",
            "requests_analyzed": 1000,
            "avg_response_time_ms": 45.3,
            "p95_response_time_ms": 120.5,
            "p99_response_time_ms": 250.8,
            "error_rate_percent": 0.5,
            "common_errors": ["Timeout", "ValidationError"],
            "recommendation": "Consider adding caching for GET requests"
        }
    """
    # 1. Encontrar implementación
    code_results = search_codebase(
        query=f'@app.get\\("{endpoint}"\\)',
        file_pattern="api/**/*.py"
    )

    if not code_results:
        return {"error": f"Endpoint {endpoint} not found"}

    impl_file = code_results[0]["file"]

    # 2. Buscar logs recientes
    log_results = search_logs(
        query=f'"GET {endpoint}"',
        lines=1000
    )

    # 3. Calcular estadísticas
    response_times = extract_response_times(log_results)
    stats = calculate_stats(response_times)

    # 4. Tasa de errores
    error_logs = search_logs(
        query=f'"GET {endpoint}".*"status":5',
        lines=100
    )
    error_rate = len(error_logs) / len(log_results) * 100

    # 5. Generar recomendación
    recommendation = generate_recommendation(stats, error_rate)

    return {
        "endpoint": endpoint,
        "implementation_file": impl_file,
        "requests_analyzed": len(log_results),
        **stats,
        "error_rate_percent": error_rate,
        "recommendation": recommendation
    }
```

**Ventaja**: El agente hace **1 llamada** y obtiene análisis completo, en lugar de orquestar 4-5 tools manualmente.

### Cuándo Componer vs Cuándo Separar

**Componer** cuando:
- El workflow es **siempre el mismo** (siempre necesitas los 3 pasos)
- Quieres **reducir el número de llamadas** del agente
- El workflow es **complejo** y quieres ocultarlo

**Separar** cuando:
- El agente necesita **flexibilidad** (a veces solo paso 1, a veces todos)
- Los tools individuales son **útiles por sí mismos**
- Quieres que el agente **aprenda el workflow** (educativo)

---

## Tools Asíncronos vs Síncronos

### Cuándo Usar Async

**Usa async** cuando:
- El tool hace **I/O lento** (llamadas HTTP, queries de DB, lectura de archivos grandes)
- Quieres **ejecutar múltiples tools en paralelo**
- El runtime lo soporta (FastAPI, aiohttp, etc.)

**Ejemplo async**:

```python
import asyncio
import aiohttp
from typing import List

async def search_multiple_apis(
    query: str,
    apis: List[str]
) -> dict:
    """
    Busca en múltiples APIs en paralelo.

    Args:
        query: Texto a buscar
        apis: Lista de APIs donde buscar (e.g., ["github", "stackoverflow", "docs"])

    Returns:
        Resultados de todas las APIs, ejecutadas en paralelo
    """
    async def search_api(api_name: str) -> dict:
        """Busca en una API específica."""
        url = f"https://api.{api_name}.com/search?q={query}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return {
                    "api": api_name,
                    "results": await response.json()
                }

    # Ejecutar búsquedas en paralelo
    tasks = [search_api(api) for api in apis]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filtrar errores
    successful_results = [
        r for r in results
        if not isinstance(r, Exception)
    ]

    return {
        "query": query,
        "apis_searched": len(apis),
        "successful": len(successful_results),
        "results": successful_results
    }
```

**Ventajas**:
- **Velocidad**: Buscar en 3 APIs toma el tiempo de la más lenta (no la suma de las 3)
- **Eficiencia**: El event loop maneja múltiples requests sin threads

### Consideraciones de Async en Tools

**Problema**: No todos los runtimes de agentes soportan async.

**Solución 1**: Wrapper sync para async tools

```python
def search_multiple_apis_sync(query: str, apis: list[str]) -> dict:
    """Wrapper síncrono para tool asíncrono."""
    return asyncio.run(search_multiple_apis(query, apis))
```

**Solución 2**: Detectar runtime y adaptar

```python
import inspect

def run_tool(tool_func, *args, **kwargs):
    """Ejecuta tool, detectando si es async o sync."""
    if inspect.iscoroutinefunction(tool_func):
        # Es async
        try:
            loop = asyncio.get_running_loop()
            # Ya hay un loop corriendo (e.g., FastAPI)
            return tool_func(*args, **kwargs)
        except RuntimeError:
            # No hay loop, crear uno
            return asyncio.run(tool_func(*args, **kwargs))
    else:
        # Es sync
        return tool_func(*args, **kwargs)
```

---

## Rate Limiting y Resource Management

### Rate Limiting por Tool

**Problema**: Un agente puede llamar el mismo tool 100 veces por segundo, saturando APIs externas.

**Solución: Rate limiter con Redis**

```python
import redis
from time import time
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def rate_limit(max_calls: int, window_seconds: int):
    """
    Decorator para limitar llamadas a un tool.

    Args:
        max_calls: Máximo de llamadas permitidas
        window_seconds: Ventana de tiempo en segundos

    Example:
        @rate_limit(max_calls=10, window_seconds=60)  # 10 llamadas por minuto
        def expensive_api_call(): ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tool_name = func.__name__
            key = f"rate_limit:{tool_name}"

            # Obtener timestamps de llamadas recientes
            now = time()
            window_start = now - window_seconds

            # Limpiar llamadas antiguas
            redis_client.zremrangebyscore(key, 0, window_start)

            # Contar llamadas en la ventana actual
            call_count = redis_client.zcard(key)

            if call_count >= max_calls:
                # Rate limit excedido
                oldest_call = redis_client.zrange(key, 0, 0, withscores=True)
                if oldest_call:
                    retry_after = int(oldest_call[0][1] + window_seconds - now)
                else:
                    retry_after = window_seconds

                return ToolError(
                    error_type="rate_limit_exceeded",
                    message=(
                        f"Rate limit excedido para {tool_name}: "
                        f"{max_calls} llamadas por {window_seconds}s"
                    ),
                    suggestion=(
                        f"Espera {retry_after} segundos antes de reintentar. "
                        f"Considera hacer llamadas menos frecuentes."
                    )
                )

            # Registrar llamada actual
            redis_client.zadd(key, {str(now): now})
            redis_client.expire(key, window_seconds)

            # Ejecutar tool
            return func(*args, **kwargs)

        return wrapper
    return decorator

# Uso
@rate_limit(max_calls=10, window_seconds=60)
def call_expensive_api(query: str) -> dict:
    """Tool con rate limit de 10 llamadas por minuto."""
    return external_api.search(query)
```

### Resource Management: Connection Pooling

**Problema**: Abrir/cerrar conexiones DB en cada llamada es costoso.

**Solución: Connection pool**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

# Crear engine con pool
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=10,          # Máximo 10 conexiones abiertas
    max_overflow=5,        # 5 conexiones adicionales si pool lleno
    pool_timeout=30,       # Esperar 30s por conexión disponible
    pool_recycle=3600      # Reciclar conexiones cada hora
)

SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db_session() -> Session:
    """Context manager para sesión de DB con connection pooling."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()  # Devuelve conexión al pool, no la cierra

def search_tasks_in_db(query: str) -> list[dict]:
    """Tool que usa connection pooling."""
    with get_db_session() as session:
        results = session.query(Task).filter(
            Task.name.contains(query)
        ).limit(10).all()

        return [
            {
                "id": task.id,
                "name": task.name,
                "status": task.status
            }
            for task in results
        ]
```

---

## Security Considerations en Tools

### 1. Validar TODOS los Inputs

**Nunca confíes en que el agente pasará inputs válidos.**

```python
from pathlib import Path
import re

def read_file(file_path: str) -> str:
    """
    Lee archivo del proyecto.

    SECURITY: Previene path traversal attacks.
    """
    # 1. Normalizar path
    path = Path(file_path).resolve()

    # 2. Validar que está dentro del proyecto
    project_root = Path(__file__).parent.parent.resolve()

    if not str(path).startswith(str(project_root)):
        raise ValueError(
            f"Path traversal detectado. "
            f"El archivo debe estar dentro de {project_root}"
        )

    # 3. Validar que existe
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    # 4. Validar que es archivo (no directorio)
    if not path.is_file():
        raise ValueError(f"{file_path} no es un archivo")

    # 5. Leer con límite de tamaño
    max_size_mb = 5
    if path.stat().st_size > max_size_mb * 1024 * 1024:
        raise ValueError(
            f"Archivo muy grande (>{max_size_mb}MB). "
            f"Usa read_file_chunked en su lugar."
        )

    return path.read_text()
```

### 2. Sanitizar Inputs para Comandos Shell

**NUNCA ejecutes comandos shell con inputs del agente directamente.**

```python
import subprocess
import shlex

def run_git_command(args: list[str]) -> str:
    """
    Ejecuta comando git con validación.

    SECURITY: Solo permite comandos git seguros.
    """
    # 1. Whitelist de comandos seguros
    safe_commands = ["status", "log", "diff", "branch", "show"]

    if not args or args[0] not in safe_commands:
        raise ValueError(
            f"Comando git no permitido: {args[0]}. "
            f"Comandos seguros: {safe_commands}"
        )

    # 2. Validar argumentos
    for arg in args:
        if any(char in arg for char in [";", "|", "&", "$", "`"]):
            raise ValueError(
                f"Argumento inválido (contiene caracteres peligrosos): {arg}"
            )

    # 3. Ejecutar con subprocess (NO shell=True)
    command = ["git"] + args

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {e.stderr}")
```

### 3. Secrets Management

**NUNCA retornes secrets en respuestas de tools.**

```python
import os
import re

def get_environment_config() -> dict:
    """
    Retorna configuración de entorno.

    SECURITY: Filtra secrets automáticamente.
    """
    config = dict(os.environ)

    # Patrones de secrets a ocultar
    secret_patterns = [
        r".*API_KEY.*",
        r".*SECRET.*",
        r".*PASSWORD.*",
        r".*TOKEN.*",
        r".*PRIVATE.*"
    ]

    for key in list(config.keys()):
        if any(re.match(pattern, key, re.IGNORECASE) for pattern in secret_patterns):
            config[key] = "***REDACTED***"

    return config
```

### 4. Auditoría de Llamadas a Tools

```python
import logging
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)

def audit_tool_call(func):
    """Decorator para auditar todas las llamadas a tools."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        timestamp = datetime.utcnow().isoformat()

        # Log de entrada
        logger.info(
            f"[AUDIT] Tool called: {tool_name}",
            extra={
                "timestamp": timestamp,
                "tool": tool_name,
                "args": args,
                "kwargs": kwargs
            }
        )

        try:
            result = func(*args, **kwargs)

            # Log de éxito
            logger.info(
                f"[AUDIT] Tool succeeded: {tool_name}",
                extra={
                    "timestamp": timestamp,
                    "tool": tool_name,
                    "status": "success"
                }
            )

            return result
        except Exception as e:
            # Log de error
            logger.error(
                f"[AUDIT] Tool failed: {tool_name}",
                extra={
                    "timestamp": timestamp,
                    "tool": tool_name,
                    "status": "error",
                    "error": str(e)
                }
            )
            raise

    return wrapper

@audit_tool_call
def delete_user(user_id: str) -> dict:
    """Tool crítico con auditoría automática."""
    # ... lógica de eliminación
    pass
```

---

## Testing de Tools

### 1. Tests Unitarios con Mocks

```python
import pytest
from unittest.mock import Mock, patch
from tools import search_contacts

def test_search_contacts_basic():
    """Test básico de search_contacts."""
    # Mock de la base de datos
    with patch("tools.database") as mock_db:
        mock_db.search_contacts.return_value = [
            {"name": "Juan", "email": "juan@test.com"},
            {"name": "Ana", "email": "ana@test.com"}
        ]

        # Ejecutar tool
        result = search_contacts(query="Juan", limit=10)

        # Assertions
        assert len(result) == 2
        assert result[0]["name"] == "Juan"

        # Verificar que se llamó al DB correctamente
        mock_db.search_contacts.assert_called_once_with("Juan", 10)

def test_search_contacts_limit_exceeded():
    """Test que valida límite de resultados."""
    result = search_contacts(query="test", limit=1000)

    # Debe retornar error por límite excedido
    assert result["status"] == "error"
    assert "límite" in result["message"].lower()
    assert "reduce" in result["suggestion"].lower()

def test_search_contacts_empty_query():
    """Test con query vacío."""
    with pytest.raises(ValueError) as exc_info:
        search_contacts(query="", limit=10)

    assert "mínimo 2 caracteres" in str(exc_info.value)
```

### 2. Integration Tests con DB Real

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tools import search_tasks_in_db
from models import Base, Task

@pytest.fixture
def test_db():
    """Fixture para DB de test en memoria."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed data
    session.add_all([
        Task(name="Fix bug in API", status="todo"),
        Task(name="Write tests", status="in_progress"),
        Task(name="Deploy to production", status="done")
    ])
    session.commit()

    yield session

    session.close()

def test_search_tasks_integration(test_db):
    """Test de integración con DB real."""
    with patch("tools.get_db_session", return_value=test_db):
        results = search_tasks_in_db(query="test")

        assert len(results) == 1
        assert results[0]["name"] == "Write tests"
        assert results[0]["status"] == "in_progress"
```

### 3. Property-Based Testing (Hypothesis)

```python
from hypothesis import given, strategies as st
import pytest

@given(
    query=st.text(min_size=2, max_size=100),
    limit=st.integers(min_value=1, max_value=50)
)
def test_search_contacts_never_crashes(query, limit):
    """
    Property test: search_contacts nunca debe crashear,
    sin importar el input (dentro de rangos válidos).
    """
    try:
        result = search_contacts(query=query, limit=limit)

        # Si retorna éxito, debe ser lista
        if result.get("status") == "success":
            assert isinstance(result["data"], list)
            assert len(result["data"]) <= limit

        # Si retorna error, debe tener mensaje y sugerencia
        if result.get("status") == "error":
            assert "message" in result
            assert "suggestion" in result
    except Exception as e:
        pytest.fail(f"Tool crashed with input query={query}, limit={limit}: {e}")
```

### 4. End-to-End Tests con Agente Real

```python
from anthropic import Anthropic

def test_tool_with_real_agent():
    """
    Test E2E: Verificar que un agente real puede usar el tool.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Definir tool schema para el agente
    tools = [
        {
            "name": "search_contacts",
            "description": "Busca contactos por nombre, email o empresa",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Texto a buscar (mínimo 2 caracteres)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Máximo de resultados (entre 1 y 50)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        }
    ]

    # Solicitud al agente
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[
            {
                "role": "user",
                "content": "Busca todos los contactos que trabajen en Anthropic"
            }
        ]
    )

    # Verificar que el agente llamó al tool correcto
    assert response.stop_reason == "tool_use"
    tool_use = next(
        block for block in response.content
        if block.type == "tool_use"
    )
    assert tool_use.name == "search_contacts"
    assert "anthropic" in tool_use.input["query"].lower()
```

---

## Debugging: ¿Por qué el agente no usa mi tool?

### Razones Comunes y Soluciones

**1. Description Ambigua**

**Síntoma**: El agente usa otro tool o dice "no sé cómo hacer eso".

**Diagnóstico**: Compara tu description con la de otros tools. ¿Hay overlap?

**Solución**:
```python
# ❌ Ambiguo
def get_data(id: str) -> dict:
    """Get data."""  # ¿Qué datos? ¿De dónde?
    pass

# ✅ Específico
def get_customer_data(customer_email: str) -> dict:
    """
    Obtiene datos completos de un cliente por su email.

    Incluye: perfil, historial de compras, notas de soporte.
    """
    pass
```

**2. Schema Mal Definido**

**Síntoma**: El agente intenta usar el tool pero genera inputs inválidos.

**Diagnóstico**: Revisa los errores de validación en logs.

**Solución**: Usa Pydantic schemas detallados con ejemplos.

**3. Nombre del Tool Críptico**

**Síntoma**: El agente "no encuentra" el tool.

**Solución**:
```python
# ❌ Críptico
def gtd(q: str) -> list:  # ¿Qué significa GTD?
    pass

# ✅ Descriptivo
def get_task_details(task_id: str) -> dict:
    pass
```

**4. Demasiados Tools Similares**

**Síntoma**: El agente usa el tool equivocado.

**Solución**: Consolidar tools o usar namespacing.

```python
# ❌ Confuso (3 tools separados)
def search_github_repos(): pass
def search_stackoverflow(): pass
def search_docs(): pass

# ✅ Consolidado con parámetro
def search_developer_resources(
    query: str,
    source: Literal["github", "stackoverflow", "docs"]
) -> dict:
    """Busca en fuentes de recursos para desarrolladores."""
    pass
```

### Técnica de Debugging: Transcript Analysis

**Paso 1**: Habilitar logging de todas las tool calls

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tool_calls.log"),
        logging.StreamHandler()
    ]
)
```

**Paso 2**: Revisar logs después de ejecutar agente

```log
2025-10-23 10:30:15 - Tools available: ['search_contacts', 'create_task', 'send_email']
2025-10-23 10:30:20 - Agent called: create_task
2025-10-23 10:30:20 - Tool input: {"name": "Follow up with Juan", "due_date": "2025-10-25"}
2025-10-23 10:30:21 - Tool output: {"id": 123, "status": "created"}
```

**Paso 3**: Analizar con Claude Code

```python
# Concatenar logs y pedirle a Claude que los analice
transcript = """
[logs completos aquí]
"""

prompt = f"""
Analiza este transcript de un agente usando tools.

Identifica:
1. ¿El agente eligió los tools correctos?
2. ¿Hay tools que NO usó pero debería haber usado?
3. ¿Los inputs fueron válidos?
4. ¿Hay oportunidades de consolidación de tools?

Transcript:
{transcript}
"""
```

**Claude puede detectar**:
- Tools con descriptions contradictorias
- Schemas confusos
- Oportunidades de consolidación
- Errores en la lógica del workflow

---

## Proyecto: Suite de Tools para Agente de Desarrollo

### Objetivo

Crear una **suite completa de tools** que un agente IA pueda usar para asistir en tareas de desarrollo de software.

### Tools Requeridos

#### 1. `search_codebase`
Buscar código en el repositorio usando grep semántico.

#### 2. `read_file`
Leer archivo completo con validación de seguridad.

#### 3. `edit_file`
Editar archivo aplicando diff o reemplazos.

#### 4. `run_tests`
Ejecutar suite de tests y retornar resultados.

#### 5. `create_git_branch`
Crear rama de Git para nueva feature.

#### 6. `git_commit`
Hacer commit con mensaje siguiendo convenciones.

#### 7. `search_github_issues`
Buscar issues en GitHub relacionados con un topic.

#### 8. `analyze_code_quality`
Ejecutar linters (ruff, bandit) y retornar issues.

### Implementación Completa

Ver archivos en `api/tools/`:
- `code_search.py` - Tools de búsqueda de código
- `file_ops.py` - Operaciones de archivos
- `git_ops.py` - Operaciones de Git
- `testing.py` - Ejecución de tests
- `quality.py` - Análisis de calidad

### Tests

Ver `tests/test_tools_*.py` para tests unitarios de cada tool.

### Uso con Agente

```python
from anthropic import Anthropic
from tools import get_all_tools

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = get_all_tools()  # Retorna lista de tool schemas

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "Busca todas las funciones que usan SQLAlchemy en el proyecto y lista posibles N+1 queries"
        }
    ]
)
```

---

## 🤖 Ejercicio Práctico con IA: Diseña tu Propio Tool

### Parte 1: Generación con IA (30 min)

**Prompt para Claude**:

```
Necesito diseñar un tool para un agente IA que gestiona un sistema de inventario.

El tool debe:
1. Buscar productos por nombre, categoría o SKU
2. Retornar stock disponible
3. Alertar si stock está bajo (< 10 unidades)
4. Sugerir productos relacionados si el buscado no tiene stock

Diseña:
- Nombre del tool
- Description completa (siguiendo best practices de Anthropic)
- Schema de input con Pydantic
- Schema de output
- Casos de error y mensajes accionables
- 3 ejemplos de uso

Formato: Código Python comentado
```

### Parte 2: Auditoría Manual (30 min)

**Checklist de auditoría**:

- [ ] **Nombre del tool**:
  - [ ] ¿Es descriptivo y sin ambigüedad?
  - [ ] ¿Usa verbos de acción (search, get, create)?

- [ ] **Description**:
  - [ ] ¿Explica cuándo usar el tool?
  - [ ] ¿Explica cuándo NO usarlo?
  - [ ] ¿Incluye ejemplos de uso?
  - [ ] ¿Documenta relaciones con otros tools?

- [ ] **Input schema**:
  - [ ] ¿Usa Pydantic para validación?
  - [ ] ¿Parámetros tienen nombres específicos (no ambiguos)?
  - [ ] ¿Incluye valores default razonables?
  - [ ] ¿Rangos de valores están validados?

- [ ] **Output schema**:
  - [ ] ¿Retorna solo información relevante?
  - [ ] ¿Usa identificadores semánticos (no UUIDs)?
  - [ ] ¿Formato es parseable (JSON, Markdown)?

- [ ] **Error handling**:
  - [ ] ¿Errores son accionables (dicen cómo corregir)?
  - [ ] ¿Evita stack traces técnicos?
  - [ ] ¿Sugiere alternativas cuando falla?

- [ ] **Security**:
  - [ ] ¿Valida TODOS los inputs?
  - [ ] ¿Previene injection attacks?
  - [ ] ¿No expone secrets en outputs?

### Parte 3: Iteración con IA (20 min)

**Prompt de mejora**:

```
Audité el tool que diseñaste. Aquí está el feedback:

[Pega tu checklist completada]

Refactoriza el tool para:
1. Corregir todos los ❌
2. Mejorar la description para ser más clara
3. Añadir un parámetro `response_format` (detailed/concise)
4. Agregar rate limiting con decorator

Muestra el código refactorizado.
```

### Parte 4: Testing con IA (20 min)

**Prompt para generar tests**:

```
Genera tests unitarios para este tool usando pytest.

Incluye:
1. Test happy path (input válido)
2. Test de validación (inputs inválidos)
3. Test de rate limiting
4. Test de respuesta concise vs detailed
5. Property-based test con Hypothesis

Usa mocks para dependencias externas (DB, APIs).
```

---

## Recursos Adicionales

### Artículos de Anthropic

- [Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) - **Artículo base de esta clase**
- [Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Function Calling Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#best-practices-for-tool-definitions)

### Librerías Útiles

- [Pydantic](https://docs.pydantic.dev/) - Validación de schemas
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) - Cliente Python para Claude
- [Hypothesis](https://hypothesis.readthedocs.io/) - Property-based testing
- [Redis](https://redis.io/) - Para rate limiting

### Proyectos de Ejemplo

- [Claude Code MCP Servers](https://github.com/modelcontextprotocol/servers) - Ejemplos de tools reales
- [Agent Skills Examples](https://docs.claude.com/claude-code/slash-commands) - Slash commands en Claude Code

---

## Conclusión

**Diseñar tools efectivos** es un skill crítico para desarrollar agentes IA productivos. Los principios clave son:

1. **Diseña para agentes**, no para APIs tradicionales
2. **Consolida funcionalidad** para reducir llamadas
3. **Descriptions claras** guían al agente
4. **Errores accionables** enseñan al agente a corregirse
5. **Valida todo** para seguridad
6. **Itera basado en evaluaciones** reales

**Next steps**:
- Implementa el proyecto de suite de tools
- Evalúa tus tools con agentes reales
- Lee el artículo de Anthropic completo
- Experimenta con diferentes formatos de respuesta

**Recuerda**: Más tools ≠ mejores resultados. **Unos pocos tools bien diseñados** superan a muchos tools mal pensados.
