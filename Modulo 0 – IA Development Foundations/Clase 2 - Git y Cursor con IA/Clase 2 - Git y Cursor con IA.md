# Clase 2: Git + Cursor + Flujo de Trabajo con IA

**Duración**: 6 horas
**Prerequisito**: Clase 1 completada (Python, Git, Claude Code instalados)
**Objetivo**: Dominar Git desde cero y establecer flujo de trabajo con IA integrada

---

## Índice

1. [Git Fundamentals (Manual)](#parte-1-git-fundamentals-manual)
2. [Git con IA Assistant](#parte-2-git-con-ia-assistant)
3. [Cursor IDE Setup](#parte-3-cursor-ide-setup-opcional)
4. [Conventional Commits](#parte-4-conventional-commits)
5. [Proyecto: Repositorio del Máster](#proyecto-final)

---

## Parte 1: Git Fundamentals (Manual) - 2 horas

### 1.1 ¿Qué es Git y Por Qué Usarlo? (20 min)

#### Analogía: Videojuego con Save Points

Imagina que estás jugando un RPG:
- **Sin Git**: Si cometes un error, pierdes todo
- **Con Git**: Guardas progreso en cada punto importante, puedes volver atrás

#### Git NO es GitHub

| Git | GitHub |
|-----|--------|
| Sistema de control de versiones | Servicio web para alojar repositorios |
| Local en tu computadora | En la nube |
| Software (instalaste en Clase 1) | Sitio web (github.com) |

**Analogía**:
- **Git** = Word (programa para editar)
- **GitHub** = Google Drive (lugar para guardar en nube)

---

### 1.2 Conceptos Clave (30 min)

#### Repository (Repositorio)

Carpeta donde Git rastrea cambios.

```bash
# Crear repositorio nuevo
mkdir mi-proyecto
cd mi-proyecto
git init

# Output: "Initialized empty Git repository..."
```

**¿Qué pasó?** Git creó carpeta oculta `.git/` que guarda el historial.

---

#### Working Directory, Staging Area, Repository

```
Working Directory  →  Staging Area  →  Repository
(archivos editando)  (preparados)      (guardados)

     git add  →        git commit  →
```

**Analogía**:
1. **Working Directory**: Mesa donde trabajas
2. **Staging Area**: Caja donde pones cosas a enviar
3. **Repository**: Almacén donde se guardan permanentemente

---

#### Comandos Básicos

**Ver estado**:
```bash
git status
```

**Añadir archivos** (Working → Staging):
```bash
# Archivo específico
git add archivo.py

# Todos los archivos
git add .
```

**Guardar cambios** (Staging → Repository):
```bash
git commit -m "Mensaje descriptivo"
```

**Ver historial**:
```bash
git log
# o más compacto:
git log --oneline
```

---

### 1.3 Ejercicio Práctico Manual (40 min)

#### Paso 1: Crear proyecto

```bash
# Crear directorio
mkdir practica-git
cd practica-git

# Inicializar git
git init

# Verificar
git status
```

**Output esperado**:
```
On branch main
No commits yet
nothing to commit
```

---

#### Paso 2: Primer commit

```bash
# Crear archivo
echo "# Mi Proyecto Git" > README.md

# Ver estado
git status
# Verás: "Untracked files: README.md"

# Añadir a staging
git add README.md

# Ver estado otra vez
git status
# Verás: "Changes to be committed: new file: README.md"

# Commit
git commit -m "feat: add README"

# Ver historial
git log --oneline
```

---

#### Paso 3: Más commits

```bash
# Crear archivo Python
cat > main.py << 'EOF'
def saludar(nombre):
    return f"Hola, {nombre}!"

if __name__ == "__main__":
    print(saludar("Git"))
EOF

# Add y commit
git add main.py
git commit -m "feat: add greet function"

# Modificar archivo
echo "" >> main.py
echo "# TODO: añadir más funciones" >> main.py

# Ver diferencias
git diff

# Commit del cambio
git add main.py
git commit -m "docs: add TODO comment"

# Ver historial
git log --oneline
```

**Deberías ver**:
```
a1b2c3d docs: add TODO comment
e4f5g6h feat: add greet function
i7j8k9l feat: add README
```

---

#### Paso 4: Ver cambios específicos

```bash
# Ver qué cambió en un commit
git show <commit-id>

# Ver diferencias entre commits
git diff <commit-1> <commit-2>

# Ver cambios sin commit aún
git diff
```

---

### 1.4 Branching Básico (30 min)

#### ¿Qué son branches?

**Analogía**: Universos paralelos en tu código

- **main**: Línea principal (código en producción)
- **feature-X**: Rama para desarrollar feature X sin romper main
- **fix-bug**: Rama para arreglar bug

```
main:     A---B---C---D
               \
feature-X:      E---F---G
```

#### Comandos

**Crear branch**:
```bash
# Crear y cambiarse
git checkout -b feature-saludo-personalizado

# Verificar en qué branch estás
git branch
```

**Trabajar en branch**:
```bash
# Modificar código
cat > main.py << 'EOF'
def saludar(nombre, idioma="es"):
    saludos = {
        "es": f"Hola, {nombre}!",
        "en": f"Hello, {nombre}!",
        "fr": f"Bonjour, {nombre}!"
    }
    return saludos.get(idioma, saludos["es"])

if __name__ == "__main__":
    print(saludar("Git", "en"))
EOF

# Commit en esta branch
git add main.py
git commit -m "feat: add multi-language support"
```

**Volver a main**:
```bash
git checkout main

# Ver que main.py NO tiene los cambios
cat main.py  # Versión antigua
```

**Mergear branch**:
```bash
# Desde main, traer cambios de feature
git merge feature-saludo-personalizado

# Ahora main tiene los cambios
cat main.py  # Versión nueva
```

---

## Parte 2: Git con IA Assistant (1.5 horas)

### 2.1 Generar .gitignore con IA (15 min)

#### Sin IA (manual):
```bash
# Buscar template en Google
# Copiar y pegar
# Ajustar manualmente
```

#### Con IA:
```bash
claude "Genera un .gitignore para proyecto Python con:
- Virtual environments
- IDE files (VS Code, PyCharm)
- pytest cache
- Coverage reports
- .env files"
```

**IA genera**:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
.venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment variables
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

**Tú validas**: ¿Tiene todo lo necesario?

```bash
# Guardar en .gitignore
claude "..." > .gitignore

# Commit
git add .gitignore
git commit -m "chore: add gitignore"
```

---

### 2.2 Commit Messages con IA (30 min)

#### Problema: Mensajes vagos

```bash
# ❌ Malos ejemplos
git commit -m "fix"
git commit -m "changes"
git commit -m "update"
git commit -m "asdf"
```

**Problema**: En 6 meses, ¿sabrás qué cambió?

---

#### Solución: IA ayuda a escribir buenos mensajes

**Workflow**:

1. **Haces cambios**:
```bash
# Añades feature
cat >> main.py << 'EOF'

def despedirse(nombre):
    return f"Adiós, {nombre}!"
EOF
```

2. **ves qué cambió**:
```bash
git diff
```

3. **Pides ayuda a IA**:
```bash
claude "He añadido una función despedirse() a main.py.
¿Qué commit message siguiendo Conventional Commits debería usar?

Cambios:
$(git diff main.py)"
```

4. **IA sugiere**:
```
feat(main): add despedirse function

Adds goodbye functionality to complement saludar.
Returns formatted goodbye message in Spanish.
```

5. **Tú decides** si usar ese mensaje o ajustarlo:
```bash
git add main.py
git commit -m "feat(main): add despedirse function"
```

---

#### Ejercicio: Git Commit Helper Agent

Vamos a usar el agente que creamos:

```bash
# Ver cambios staged
git add .

# Invocar agente
claude --agent git-commit-helper "Ayúdame a escribir commit message para estos cambios"
```

El agente:
1. Ve tus cambios
2. Determina el type (feat/fix/docs/etc)
3. Sugiere mensaje
4. Explica por qué

---

### 2.3 Resolver Conflictos con IA (30 min)

#### ¿Qué es un conflicto?

Cuando dos branches modifican la misma línea de código.

```
main:     def saludar(nombre):
feature:  def saludar(nombre, formal=False):

Git: "¡No sé cuál versión usar!"
```

#### Crear conflicto (práctica):

**Terminal 1 (main)**:
```bash
git checkout main
echo "version = '1.0.0'" > version.py
git add version.py
git commit -m "feat: add version file"
```

**Terminal 2 (feature)**:
```bash
git checkout -b feature-version
echo "VERSION = '1.0.0-beta'" > version.py
git add version.py
git commit -m "feat: add VERSION constant"
```

**Merge (crea conflicto)**:
```bash
git checkout main
git merge feature-version

# Output: CONFLICT in version.py
```

**Ver conflicto**:
```bash
cat version.py
```

```python
<<<<<<< HEAD
version = '1.0.0'
=======
VERSION = '1.0.0-beta'
>>>>>>> feature-version
```

#### Resolver con IA:

```bash
claude "Tengo este conflicto de merge en version.py:

$(cat version.py)

Contexto:
- main branch: usa lowercase 'version'
- feature branch: usa UPPERCASE 'VERSION' y es beta

¿Cómo debería resolver? Sugiere código final."
```

**IA analiza y sugiere**:
```python
# Opción 1: Mantener ambas
version = '1.0.0'
VERSION = '1.0.0-beta'

# Opción 2: Una sola variable uppercase (PEP 8)
VERSION = '1.0.0'  # En main, '1.0.0-beta' se descarta

# Recomendación: Opción 2, variables de módulo en UPPERCASE
```

**Tú decides** cuál opción:
```bash
# Editar version.py con la solución elegida
echo "VERSION = '1.0.0'" > version.py

# Marcar como resuelto
git add version.py
git commit -m "merge: resolve version conflict, use UPPERCASE"
```

---

### 2.4 README Profesional con IA (15 min)

```bash
claude "Genera un README.md profesional para mi proyecto de práctica Git.

Proyecto:
- Nombre: practica-git
- Descripción: Proyecto para aprender Git + IA
- Features: saludar() multiidioma, despedirse()
- Tecnologías: Python 3.12
- Autor: [tu nombre]

Incluye:
- Badges
- Installation
- Usage
- Contributing
```

**IA genera README completo**.

**Tú revisas** y ajustas:
```bash
# Guardar
claude "..." > README.md

# Commit
git add README.md
git commit -m "docs: add comprehensive README"
```

---

## Parte 3: Cursor IDE Setup (OPCIONAL) - 1 hora

### 3.1 Instalación y Configuración (20 min)

**Nota**: Esto es OPCIONAL. Puedes usar VS Code + GitHub Copilot en su lugar.

#### Instalación

1. Descargar: https://cursor.sh
2. Instalar
3. Abrir Cursor
4. Importar configuración de VS Code (si tienes)

#### Configurar API Key

**Settings → Extensions → Claude**:
- Pegar tu `ANTHROPIC_API_KEY`
- Test connection

---

### 3.2 Features de Cursor (40 min)

#### Feature 1: Cmd/Ctrl + K (Inline Edit)

**Uso**:
1. Selecciona código
2. Cmd+K (Mac) o Ctrl+K (Windows/Linux)
3. Describe cambio
4. Cursor edita en línea

**Ejemplo**:
```python
# Código original
def saludar(nombre):
    return f"Hola, {nombre}!"

# Seleccionar función, Cmd+K, escribir:
"añade parámetro opcional 'idioma' con soporte para es/en/fr"

# Cursor genera:
def saludar(nombre, idioma="es"):
    saludos = {
        "es": f"Hola, {nombre}!",
        "en": f"Hello, {nombre}!",
        "fr": f"Bonjour, {nombre}!"
    }
    return saludos.get(idioma, saludos["es"])
```

---

#### Feature 2: Cmd/Ctrl + L (Chat)

Panel lateral para conversar sobre código:

**Ejemplo de conversación**:
```
Tú: "Explica cómo funciona git merge"
Cursor: [Explicación detallada]

Tú: "Dame ejemplo de merge con conflicto"
Cursor: [Ejemplo con código]

Tú: "Genera tests para mi función saludar"
Cursor: [Tests con pytest]
```

---

#### Feature 3: Composer (Multi-file)

Editar múltiples archivos a la vez:

**Ejemplo**:
```
Tú: "Refactoriza mi proyecto para tener estructura:
src/
  greetings.py (funciones saludar, despedirse)
  main.py (solo entry point)
tests/
  test_greetings.py

Mueve el código apropiadamente"
```

Cursor edita los 3 archivos automáticamente.

---

### 3.3 .cursorrules (Configuración de Proyecto) (bonus)

Archivo que le dice a Cursor cómo trabajar en TU proyecto.

```markdown
# .cursorrules

Este proyecto sigue:
- Python 3.12
- Type hints obligatorios
- Docstrings en Google style
- Tests con pytest
- Conventional Commits

Al generar código:
- Usa type hints: def func(x: int) -> str
- Añade docstrings explicativos
- Genera tests si es función pública

Al hacer commits:
- Usa conventional commits format
- Subject max 50 chars
- Body opcional si no es obvio
```

**Guardar** en `.cursorrules` en root del proyecto.

Ahora Cursor sigue estas reglas automáticamente.

---

## Parte 4: Conventional Commits (45 min)

### 4.1 ¿Por Qué Conventional Commits? (15 min)

**Problema**: Historial Git incomprensible

```bash
git log --oneline
# a1b2c3d update
# d4e5f6g fix
# g7h8i9j changes
# j0k1l2m stuff
```

**Con Conventional Commits**:
```bash
git log --oneline
# a1b2c3d feat(auth): add JWT refresh token support
# d4e5f6g fix(api): prevent SQL injection in search
# g7h8i9j docs(readme): add installation instructions
# j0k1l2m refactor(db): extract query logic to repository
```

**Beneficios**:
1. Historial legible
2. Changelog automático
3. Semantic versioning automático
4. Code review más fácil

---

### 4.2 Formato (15 min)

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types

| Type | Cuándo usar | Ejemplo |
|------|-------------|---------|
| **feat** | Nueva funcionalidad | `feat(api): add user registration` |
| **fix** | Bug fix | `fix(auth): prevent token expiration bypass` |
| **docs** | Solo documentación | `docs(readme): update installation steps` |
| **refactor** | Cambio sin new feature ni fix | `refactor(db): extract connection to class` |
| **test** | Añadir/corregir tests | `test(api): add edge cases for POST /users` |
| **chore** | Tareas de mantenimiento | `chore(deps): update fastapi to 0.100.0` |
| **perf** | Performance | `perf(db): add index on user_id` |
| **style** | Formato (no afecta lógica) | `style(api): format with black` |

#### Scope (opcional)

Componente: `(api)`, `(auth)`, `(db)`, `(tests)`, `(docs)`

#### Subject

- Imperativo: "add" no "added"
- Minúscula
- Sin punto final
- Max 50 caracteres

#### Body (opcional)

- Explica POR QUÉ, no QUÉ
- Wrap a 72 chars

#### Footer (opcional)

- Breaking changes: `BREAKING CHANGE: ...`
- Issue refs: `Closes #42`

---

### 4.3 Ejercicios Prácticos (15 min)

Para cada cambio, escribe el commit message correcto:

**Ejercicio 1**:
```
Cambio: Añadiste logging a todas las funciones de API
```

**Respuesta**:
```bash
git commit -m "feat(api): add logging to all endpoints"
```

---

**Ejercicio 2**:
```
Cambio: Arreglaste bug donde despedirse crasheaba con None
```

**Respuesta**:
```bash
git commit -m "fix(greetings): handle None in despedirse function"
```

---

**Ejercicio 3**:
```
Cambio: Actualizaste requirements.txt con nueva versión de pytest
```

**Respuesta**:
```bash
git commit -m "chore(deps): update pytest to 8.4.2"
```

---

## Proyecto Final: Repositorio del Máster (1 hora)

### Objetivo

Crear repositorio profesional para TODO tu trabajo del máster.

### Requisitos

1. **Estructura**:
```
master-ia-dev/
├── .gitignore (generado con IA)
├── README.md (profesional)
├── modulo-0/
│   ├── clase-1/
│   │   └── generador_contraseñas.py (de clase anterior)
│   └── clase-2/
│       └── practica-git/ (ejercicios de hoy)
├── .cursorrules (opcional, si usas Cursor)
└── docs/
    └── workflow.md (tu flujo de trabajo)
```

2. **README.md debe incluir**:
- Título y descripción
- Estructura del repositorio
- Cómo navegar las clases
- Tu progreso (tabla de checkboxes)

3. **Al menos 5 commits** siguiendo Conventional Commits

4. **Branch strategy**:
- `main`: código "estable"
- `dev`: trabajo en progreso
- `clase-X`: branches por clase

---

### Proceso (Paso a Paso)

**Paso 1: Crear repositorio**:
```bash
mkdir master-ia-dev
cd master-ia-dev
git init
```

**Paso 2: .gitignore con IA**:
```bash
claude "Genera .gitignore para proyecto educativo Python con Jupyter notebooks, múltiples virtual environments, y archivos de IDEs" > .gitignore

git add .gitignore
git commit -m "chore: add gitignore for Python project"
```

**Paso 3: README con IA**:
```bash
claude "Genera README.md profesional para mi repositorio del Máster en Desarrollo con IA.

Incluir:
- Título: Máster en Desarrollo con IA - Mi Viaje
- Descripción: Repositorio con mi progreso
- Estructura de módulos (0-5)
- Tabla de progreso con checkboxes
- Sección 'Cómo navegar'
- Tecnologías: Python 3.12, FastAPI, Claude Code
- Autor: [tu nombre]"  > README.md

git add README.md
git commit -m "docs: add comprehensive README"
```

**Paso 4: Estructura de carpetas**:
```bash
mkdir -p modulo-0/clase-1 modulo-0/clase-2 docs

# Mover proyecto de clase 1
cp ../generador_contraseñas.py modulo-0/clase-1/

# Mover ejercicios de hoy
cp -r practica-git modulo-0/clase-2/

git add .
git commit -m "feat: add module 0 structure with clase 1-2 projects"
```

**Paso 5: Documentar workflow**:
```bash
claude "Documenta mi flujo de trabajo Git + IA:
1. Hacer cambios en código
2. git diff para ver cambios
3. git add para staging
4. Usar git-commit-helper agent para mensaje
5. git commit
6. Repetir

Formato: Markdown con ejemplos" > docs/workflow.md

git add docs/workflow.md
git commit -m "docs: add Git + AI workflow documentation"
```

**Paso 6: Crear branch dev**:
```bash
git checkout -b dev

# Hacer cambio experimental
echo "# Experimento: Testing en dev branch" >> README.md

git add README.md
git commit -m "docs: add dev branch note"

# Volver a main
git checkout main

# Ver que main NO tiene el cambio
tail README.md
```

**Paso 7: GitHub (opcional pero recomendado)**:

1. Crear repo en GitHub.com
2. Conectar local con remote:
```bash
git remote add origin https://github.com/tu-usuario/master-ia-dev.git
git branch -M main
git push -u origin main
git push origin dev
```

---

### Entregables

1. **Repositorio Git** localmente funcionando
2. **Al menos 5 commits** con conventional commits
3. **README.md** profesional
4. **Branch strategy** (main + dev mínimo)
5. **Reflexión** (`docs/reflexion-clase-2.md`):
   ```markdown
   # Reflexión Clase 2

   ## ¿Qué aprendí de Git?
   - [tu respuesta]

   ## ¿Cómo me ayudó IA?
   - [ejemplos concretos]

   ## ¿Qué fue difícil?
   - [desafíos]

   ## Mi workflow ahora es...
   - [descripción]

   ## Próximos pasos
   - [qué quieres mejorar]
   ```

---

## Evaluación

### Criterios (100 puntos)

**Git Fundamentals** (40 puntos):
- Comandos básicos funcionan (add, commit, log)
- Entiende working dir / staging / repository
- Branches creadas y merged
- Conflictos resueltos correctamente

**AI Integration** (30 puntos):
- .gitignore generado con IA
- Commit messages con ayuda de IA
- README profesional generado
- Workflow documentado

**Conventional Commits** (20 puntos):
- Al menos 5 commits bien formateados
- Types correctos (feat/fix/docs)
- Subjects descriptivos
- No commits vagos ("update", "fix")

**Repositorio del Máster** (10 puntos):
- Estructura clara
- README completo
- Documentación de workflow

---

## Recursos Adicionales

### Documentación
- [Git Book](https://git-scm.com/book/en/v2) - Gratis, completo
- [Conventional Commits](https://www.conventionalcommits.org)
- [Cursor Docs](https://cursor.sh/docs)

### Práctica
- [Learn Git Branching](https://learngitbranching.js.org/) - Interactivo
- [Oh My Git!](https://ohmygit.org/) - Juego para aprender Git

### Cheatsheets
```bash
# Comandos esenciales
git status          # Ver estado
git add <file>      # Staging
git commit -m "msg" # Commit
git log --oneline   # Historial
git diff            # Ver cambios
git checkout -b <br># Crear branch
git merge <branch>  # Mergear

# Deshacer cambios
git restore <file>  # Descartar cambios (working)
git restore --staged <file> # Unstage
git reset HEAD~1    # Deshacer último commit (mantener cambios)
git revert <commit> # Revertir commit (crea nuevo commit)
```

---

## Próxima Clase

**Clase 3: Documentación y Pensamiento Estructurado**

Prepárate para:
- Markdown avanzado
- Mermaid diagrams
- Architecture Decision Records (ADRs)
- Documentación automática con IA

**Prerequisitos**:
- ✅ Repositorio del máster creado
- ✅ Git workflow establecido
- ✅ Conventional commits aplicados
- ✅ (Opcional) Cursor configurado

---

## Notas Finales

**Recuerda**:
1. **Git es manual primero** - Entiende comandos antes de automatizar
2. **IA acelera, no reemplaza** - Validas todo lo que IA genera
3. **Commits claros = futuro feliz** - Conventional commits son inversión
4. **Practica a diario** - Git se aprende usando

**Mentalidad correcta**:
- ✅ "Aprendo Git profundamente, IA me ayuda con mensajes/docs"
- ✅ "Entiendo cada commit que hago"
- ❌ "IA hace los commits por mí"
- ❌ "No necesito entender Git, solo copiar comandos"

¡Git es tu mejor amigo en desarrollo! 🚀
