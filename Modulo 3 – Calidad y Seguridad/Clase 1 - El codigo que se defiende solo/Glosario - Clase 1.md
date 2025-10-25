# 🧭 Glosario – Clase 1

**Cobertura de código (Coverage)** → métrica que mide qué porcentaje de tu código está siendo probado por los tests. Si tienes 93% de cobertura, significa que el 93% de tus líneas de código se ejecutan cuando corren los tests.

**pytest-cov** → plugin de pytest que mide la cobertura de código y te muestra qué líneas no están testeadas.

```bash
pytest --cov=api --cov-report=term-missing
```

**term-missing** → opción de pytest-cov que muestra específicamente qué líneas de código no están cubiertas por tests (ej. `15-16` significa que las líneas 15 y 16 no tienen tests).

**Linter** → herramienta que revisa tu código en busca de problemas de estilo, bugs potenciales y código mal escrito, sin ejecutarlo. Como un corrector ortográfico para código.

- **flake8**: linter clásico de Python
- **ruff**: linter moderno y ultra rápido que además puede auto-corregir problemas

**CI (Continuous Integration)** → sistema automatizado que ejecuta tests, linters y validaciones cada vez que haces push o abres un PR. Si algo falla, GitHub no deja pasar el cambio.

**Pipeline** → secuencia automatizada de pasos que ejecuta el CI (tests → cobertura → linter → seguridad).

**SQL Injection** → vulnerabilidad crítica donde un atacante puede ejecutar comandos SQL maliciosos concatenando strings en queries.

```python
# ❌ VULNERABLE
query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"

# ✅ SEGURO (parámetros preparados)
query = "SELECT * FROM usuarios WHERE nombre = ?"
cursor.execute(query, (nombre,))
```

**Secretos hardcoded** → error grave de seguridad donde contraseñas, API keys o tokens quedan escritos directamente en el código (y en git para siempre).

```python
# ❌ NUNCA
JWT_SECRET = "mi-secreto-123"

# ✅ SIEMPRE
JWT_SECRET = os.getenv("JWT_SECRET")
```

**Validación con Pydantic** → uso de modelos Pydantic para asegurar que los datos de entrada cumplen requisitos específicos (tipo, longitud, formato).

**Field(..., min_length=1)** → validador de Pydantic que exige que un campo string no esté vacío.

```python
class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
```

**CVE (Common Vulnerabilities and Exposures)** → identificador único para vulnerabilidades de seguridad conocidas en software. Ej: CVE-2021-32677 es una vulnerabilidad específica en una versión antigua de FastAPI.

**ORM (Object-Relational Mapping)** → herramienta como SQLAlchemy que te permite trabajar con bases de datos usando objetos Python en lugar de escribir SQL manualmente. Más seguro porque previene SQL injection.

**XSS (Cross-Site Scripting)** → ataque donde un usuario malicioso inyecta código JavaScript en tu app (ej. `<script>alert('hack')</script>`). Se previene validando y sanitizando inputs.

**bandit** → herramienta de seguridad que escanea tu código Python en busca de vulnerabilidades comunes (secretos hardcoded, SQL injection, etc.).

```bash
bandit -r api/ -ll
```

**safety check** → herramienta que escanea tus dependencias (requirements.txt) en busca de versiones con vulnerabilidades conocidas (CVEs).

**detect-secrets** → herramienta que busca secretos hardcoded en tu código (API keys, passwords, tokens) antes de que lleguen a git.

**Dependabot** → bot de GitHub que automáticamente crea PRs para actualizar dependencias cuando detecta versiones con vulnerabilidades.

**Security Hardening Mentor** → agente educacional especializado (disponible en `.claude/agents/educational/`) que audita tu código buscando anti-patrones de seguridad y te enseña a corregirlos.

**Anti-patrones de seguridad** → errores comunes de programación que introducen vulnerabilidades:
- SQL injection (concatenar strings en queries)
- Secretos hardcoded (passwords en el código)
- Validación insuficiente (aceptar cualquier input)
- Dependencias vulnerables (versiones antiguas con CVEs)
- Logging de datos sensibles (imprimir passwords)

**.env** → archivo (nunca en git) que contiene variables de entorno con valores sensibles (secrets, passwords, API keys). Se carga con `python-dotenv`.

```python
# .env (NUNCA hacer commit de este archivo)
JWT_SECRET=abc123xyz
DATABASE_URL=postgresql://...

# api/config.py
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
```

**DoS (Denial of Service)** → ataque donde se sobrecarga el sistema enviando requests masivos o con datos gigantes. Se previene validando tamaños máximos.

```python
nombre: str = Field(..., max_length=200)  # Previene strings gigantes
```

**CI Pipeline con calidad** → workflow que no solo ejecuta tests, sino que valida:
- ✅ Tests pasan
- ✅ Cobertura ≥ 80%
- ✅ Linter (sin errores de estilo)
- ✅ Bandit (sin vulnerabilidades)
- ✅ Safety (dependencias seguras)

**--cov-fail-under=80** → flag de pytest-cov que hace que el CI falle si la cobertura está por debajo del 80%. Es tu red de seguridad automática.
