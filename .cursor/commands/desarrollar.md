## Objetivo
Implementar la issue siguiendo TDD y hacer commits con historia de usuario.

## Proceso

### 1. Crear branch
```bash
git checkout dev
git pull origin dev
git checkout -b feature/JAR-XX-descripcion-breve
```

### 2. Ciclo TDD (Red → Green → Refactor)

**RED**: Escribir tests que fallen
```bash
# Crear archivo de tests
touch tests/test_[modulo].py

# Escribir tests PRIMERO
# Ejecutar → deben fallar
pytest tests/test_[modulo].py -v
```

**GREEN**: Escribir código mínimo para pasar tests
```bash
# Implementar funcionalidad
# Ejecutar tests hasta que pasen
pytest tests/test_[modulo].py -v
```

**REFACTOR**: Mejorar código manteniendo tests verdes
```bash
# Limpiar código
black app/ tests/
flake8 app/ tests/
mypy app/

# Verificar tests siguen pasando
pytest
```

### 3. Hacer commits atómicos

**Formato obligatorio:**

**GREEN: Escribir código mínimo para pasar tests**
# Implementar funcionalidad
# Ejecutar tests hasta que pasen
pytest tests/test_[modulo].py -v

**REFACTOR: Mejorar código manteniendo tests verdes**
# Limpiar código
black app/ tests/
flake8 app/ tests/
mypy app/

# Verificar tests siguen pasando
pytest)
  - QUÉ: [descripción]
  - PARA QUÉ: [objetivo]
  - Tests: [X] tests, [Y]% cobertura
```

### 5. Push
```bash
git push origin feature/JAR-XX-descripcion-breve
```

## Reglas de Calidad

### Antes de cada commit:
- [ ] Tests escritos PRIMERO (TDD)
- [ ] Tests pasan (`pytest`)
- [ ] Cobertura >80% (`pytest --cov`)
- [ ] Linters OK (`black`, `flake8`, `mypy`)
- [ ] Sin código duplicado
- [ ] Funciones <50 líneas
- [ ] Tipado explícito
- [ ] Docstrings en español

### Seguridad (consultar `docs/SECURITY_CHECKLIST.md`):
- [ ] Inputs validados con Pydantic
- [ ] Contraseñas hasheadas (NUNCA texto plano)
- [ ] Sin datos sensibles en logs

## Output esperado
✅ Branch pusheado con commits atómicos
✅ Tests >80% cobertura
✅ CHANGELOG actualizado

**3. Hacer commits atómicos**
Formato obligatorio:

[JAR-XX] Título breve en imperativo

QUÉ: [Qué implementaste técnicamente]
POR QUÉ: [Razón de negocio/técnica]
PARA QUÉ: [Valor que aporta]

Tests: [X] tests, [Y]% cobertura -v
pytest --cov=app --cov-report=html tests/
# ¿Cobertura >80%? ✓

# Linters
black app/ tests/
flake8 app/ tests/
mypy app/
# ¿Todo OK? ✓

# Verificar commits
git log --oneline
# ¿Tienen formato [JAR-XX] QUÉ/POR QUÉ/PARA QUÉ? ✓
```

### 2. Checklist rápido

**Código:**
- [ ] TDD (tests antes que código)
- [ ] Cobertura >80%
- [ ] Linters sin errores
- [ ] Sin código duplicado
- [ ] Funciones <50 líneas
- [ ] Tipado explícito + docstrings

**Seguridad:**
- [ ] Inputs validados
- [ ] Contraseñas hasheadas
- [ ] Sin datos sensibles en logs

**Documentación:**
- [ ] CHANGELOG actualizado
- [ ] Docstrings claros

### 3. Crear Pull Request

**Template de PR:**
```markdown
## [JAR-XX] Título

Closes JAR-XX

### 🔄 Tipo
- [ ] ✨ Feature
- [ ] 🐛 Bugfix
- [ ] 🔒 Seguridad

### ✅ Checklist
- [ ] Tests escritos siguiendo TDD
- [ ] Cobertura >80%
- [ ] Linters OK
- [ ] Seguridad validada
- [ ] CHANGELOG actualizado

### 🧪 Tests
- Nuevos: [X] tests
- Cobertura: [Y]%
- Comando: `pytest tests/test_[archivo].py -v`

### 📝 Archivos
- `app/[archivo].py`
- `tests/test_[archivo].py`
- `CHANGELOG.md`
```

### 4. Crear PR
```bash
gh pr create --base dev \
  --title "[JAR-XX] Título" \
  --body-file pr.md
```

### 5. Actualizar Linear
- Mover issue a "In Review"
- Añadir link del PR

## Output esperado
✅ PR creado con checklist completo
✅ Issue actualizada en Linear
✅ Listo para code review

Ejemplo:

[JAR-29] Crear modelo User con hashing de contraseñas

QUÉ: Modelo SQLAlchemy User con campos base y métodos de verificación
POR QUÉ: Base necesaria para sistema de autenticación seguro
PARA QUÉ: Usuarios puedan registrarse y autenticarse de forma protegida

Tests: 12 tests, 94% cobertura

## 4. Actualizar CHANGELOG.md

### Added
- **YYYY-MM-DD**: [JAR-XX] Título (commit: abc1234)
  - QUÉ: [descripción]
  - PARA QUÉ: [objetivo]
  - Tests: [X] tests, [Y]% cobertura

## 5. Push

git push origin feature/JAR-XX-descripcion-breve

## Reglas de Calidad

Antes de cada commit:

[ ] Tests escritos PRIMERO (TDD)
[ ] Tests pasan (pytest)
[ ] Cobertura >80% (pytest --cov)
[ ] Linters OK (black, flake8, mypy)
[ ] Sin código duplicado
[ ] Funciones <50 líneas
[ ] Tipado explícito
[ ] Docstrings en español
Seguridad (consultar docs/SECURITY_CHECKLIST.md):
[ ] Inputs validados con Pydantic
[ ] Contraseñas hasheadas (NUNCA texto plano)
[ ] Sin datos sensibles en logs
Output esperado
✅ Branch pusheado con commits atómicos
✅ Tests >80% cobertura
✅ CHANGELOG actualizado



