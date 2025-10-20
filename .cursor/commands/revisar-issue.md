# Comando: revisar [JAR-XX]

## Objetivo
Autorevisión de calidad y creación de Pull Request.

## Proceso

### 1. Ejecutar checklist de calidad

```bash
# Tests
pytest tests/ -v
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

# 4. Crear PR
gh pr create --base dev \
  --title "[JAR-XX] Título" \
  --body-file pr.md

# 5. Actualizar Linear
Mover issue a "In Review"
Añadir link del PR

## Output esperado
✅ PR creado con checklist completo
✅ Issue actualizada en Linear
✅ Listo para code review