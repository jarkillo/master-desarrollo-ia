# Scripts - Linear Issues Automation

Este directorio contiene scripts para automatizar la creación de issues en Linear.

---

## create_linear_issues.py

**Propósito**: Crear automáticamente las 42 issues del plan maestro en Linear.

### Setup

#### 1. Obtener Linear API Key

1. Ve a [Linear Settings → API](https://linear.app/settings/api)
2. Click en "Create new key"
3. Copia tu API key (empieza con `lin_api_...`)

#### 2. Encontrar tu Team Key

Tu team key está en la URL de Linear:
```
https://linear.app/TEAM_KEY/...
                    ^^^^^^^^
```

Por ejemplo, si tu URL es `https://linear.app/acme/team/DEV`, tu TEAM_KEY es `acme`.

#### 3. Configurar Environment Variables

```bash
# Copiar template
cp .env.template .env

# Editar .env y añadir:
# - Tu LINEAR_API_KEY
# - Tu LINEAR_TEAM_KEY
```

#### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Uso

```bash
# Desde la carpeta scripts/
python create_linear_issues.py
```

### Qué hace el script

1. ✅ **Conecta a Linear API** usando tu API key
2. ✅ **Encuentra tu team** por team key
3. ✅ **Crea/encuentra proyecto** "Master desarrollo con IA"
4. ✅ **Crea labels necesarios**:
   - Módulos: module-0, module-1, ... module-5
   - Tipos: content-creation, ai-integration, bug-fix, documentation, game
   - Prioridades: P0-critical, P1-high, P2-medium, P3-low
5. ✅ **Lee el plan** desde `docs/LINEAR_ISSUES_MASTER_PLAN.md`
6. ✅ **Crea todas las issues** (42 total) con:
   - Title completo
   - Description markdown
   - Labels asignados
   - Priority correcta
   - Vinculadas al proyecto

### Output Esperado

```
🚀 Linear Issues Creator
============================================================

🔍 Finding team: TEAM
✅ Team found: <team-id>

🔍 Finding/creating project: Master desarrollo con IA
✅ Found existing project: Master desarrollo con ía (<project-id>)

📋 Setting up labels...
  ✅ Created label: module-0
  ✅ Created label: module-1
  ...
✅ Labels ready: 20 labels

📖 Parsing master plan: ../docs/LINEAR_ISSUES_MASTER_PLAN.md
✅ Found 42 issues to create

🎯 Creating issues...
============================================================
✅ [1/42] Created: TEAM-1 - M1-1: Integrar AI Assistant en Clase 1...
✅ [2/42] Created: TEAM-2 - M1-2: Integrar AI Assistant en Clase 2...
✅ [3/42] Created: TEAM-3 - M1-3: Integrar AI en Clase 3...
✅ [4/42] Created: TEAM-4 - M1-4: Integrar AI en Clase 4...
✅ [5/42] Created: TEAM-5 - M2-1: Completar Clase 1...

📊 Progress: 5/42 issues created
------------------------------------------------------------
...

============================================================
🎉 SUMMARY
============================================================
✅ Successfully created: 42/42 issues
🔗 View project: https://linear.app/team/TEAM/project/master-desarrollo-con-ia
```

### Troubleshooting

**Error: LINEAR_API_KEY not found**
- Verifica que el archivo `.env` existe
- Verifica que pusiste tu API key correctamente

**Error: Team not found**
- Verifica tu TEAM_KEY en `.env`
- Asegúrate de que el team key es correcto (revisa URL de Linear)

**Error: Rate limit exceeded**
- El script incluye delays (0.5s entre requests)
- Si falla, espera un minuto y reintenta

**Error: GraphQL errors**
- Verifica que tu API key tiene permisos de escritura
- Verifica que tienes permisos en el team

### Dry Run (Simulación)

Si quieres ver qué se creará sin crear realmente:

```python
# Editar create_linear_issues.py
# En main(), después de parse issues:

print("\n📋 DRY RUN - Issues que se crearían:")
for idx, issue in enumerate(issues, 1):
    print(f"{idx}. {issue.title}")
    print(f"   Labels: {', '.join(issue.labels)}")
    print(f"   Priority: {issue.priority}, Estimate: {issue.estimate}")
    print()

return  # Exit antes de crear
```

---

## Próximos Scripts

- `update_linear_status.py`: Script para actualizar status de issues en batch
- `linear_report.py`: Generar reporte de progreso del proyecto
- `sync_github_linear.py`: Sincronizar GitHub PRs con Linear issues

---

## Referencias

- [Linear API Docs](https://developers.linear.app/)
- [Linear GraphQL Playground](https://linear.app/graphql)
- [Master Plan](../docs/LINEAR_ISSUES_MASTER_PLAN.md)
