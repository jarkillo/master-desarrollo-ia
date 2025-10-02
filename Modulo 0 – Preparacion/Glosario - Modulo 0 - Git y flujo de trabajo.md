# Glosario — Módulo 0: Git & Flujo de trabajo

**Repositorio local**: Copia del proyecto en tu máquina. Contiene tu `.git` con toda la historia.

**Repositorio remoto**: Copia alojada en un servidor (p. ej., GitHub). El remoto por defecto suele llamarse **`origin`**.

**`origin`**: Nombre corto del remoto principal. `git remote -v` lo lista.

**Rama (branch)**: Línea de trabajo aislada. Ej.: `main`, `feature/descripcion-manu`.

**`main`**: Rama principal estable del repo.

**HEAD**: Puntero a tu commit/rama actual (en qué “foto” estás).

**Área de staging (index)**: Zona intermedia para preparar cambios antes del commit. `git add` mueve archivos aquí.

**Commit**: Foto atómica de cambios + mensaje. `git commit -m "feat: …"`

**SHA**: Identificador único (hash) de un commit. Git razona por SHAs.

**Clone**: Descarga un repo remoto a local. `git clone <url>`

**Fetch**: Trae referencias y commits del remoto **sin** mezclarlos. `git fetch`

**Pull**: `fetch + merge` (o `fetch + rebase` si lo configuras). Actualiza tu rama. `git pull origin main`

**Push**: Sube tus commits locales al remoto. `git push origin <rama>`

**Rama de seguimiento (tracking)**: Pareja local↔remoto (p. ej., `main` ↔ `origin/main`).

**Diff**: Muestra diferencias entre commits/ramas/working dir. `git diff main..feature/x`

**Estado (status)**: Cambios no trackeados, en staging y rama actual. `git status`

**.gitignore**: Patrones de archivos que Git no debe trackear.

**Merge**: Une historias creando (a veces) un commit de merge. Seguro y común en equipo. `git merge feature/x`

**Fast-forward**: Tipo de merge donde `main` solo “avanza el puntero” sin crear commit de merge (línea recta).

**Rebase**: Reaplica tus commits como si hubieran nacido sobre otra base (historia lineal). `git rebase origin/main`

- **`-continue` / `-abort`** (rebase): Para seguir tras resolver conflictos o cancelar el rebase.

**Squash**: Combinar varios commits en uno. En GitHub: **Squash & Merge** crea un **commit nuevo** en `main`.

**Fully merged**: Estado en el que los SHAs de una rama están contenidos en la otra. Tras **Squash**, **no** lo están (por eso `-d` se queja).

**Pull Request (PR)**: Propuesta de cambios entre ramas en GitHub para revisión y merge (no es un comando de git).

**Code review**: Revisión de un PR por otra persona (o tú mismo con ojos críticos).

**Estrategias de merge** (GitHub):

- **Merge commit**: conserva commits tal cual + commit de merge.
- **Squash & Merge**: aplasta commits en uno (historial limpio).
- **Rebase & Merge**: reescribe commits sobre `main` y mergea sin commit de merge.

**Conflicto**: Git no puede fusionar automáticamente líneas cambiadas en ambos lados. Se resuelve editando, `git add`, y luego `git merge --continue` o `git rebase --continue`.

- **`-force-with-lease`**: Empuja reescritura de historia de forma segura (no pisas trabajo ajeno). `git push --force-with-lease`

**Borrado de ramas**:

- Seguro: `git branch -d rama` (solo si está fully merged).
- Forzado: `git branch -D rama` (útil tras Squash).
- Remoto: `git push origin --delete rama`
    
    **FETCH_HEAD**: Referencia temporal creada por `git fetch/pull` apuntando a lo último traído del remoto.
    

**`git fetch --prune`**: Limpia referencias remotas obsoletas (ramas borradas en el servidor).

**`fetch.prune true`**: Config global para podar automáticamente al hacer `fetch/pull`.

```bash
git config --global fetch.prune true

```

**Convencional Commits**: Estándar para mensajes: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`…

**CI (Integración Continua)**: Automatiza tests y checks en cada PR/push (mantiene `main` sano).

**GUI de VS Code para Git**: Interfaz gráfica encima de los mismos comandos; útil para staging selectivo, diffs y resolver conflictos.

**Cursor/VS Code**: IDEs; en este curso, también entrenas a la IA a darte recetas Git reproducibles.

---

## Mini-recetas relacionadas (copy-paste)

**Sincronizar `main` local tras mergear en GitHub**

```bash
git switch main
git pull origin main

```

**Eliminar una rama tras Squash & Merge**

```bash
git branch -D feature/descripcion-manu
git push origin --delete feature/descripcion-manu   # si sigue en remoto
git fetch --prune

```

**Actualizar tu feature con `main` (historial limpio)**

```bash
git fetch origin
git switch feature/mis-cambios
git rebase origin/main
# resolver conflictos → git add <archivos> → git rebase --continue
git push --force-with-lease

```

**Ver qué ramas ya están fusionadas en `main`**

```bash
git branch --merged main

```

**Abrir un PR (flujo recomendado)**

```bash
git switch -c feature/docs-mod0-ajustes
# editar archivos
git add .
git commit -m "docs(mod0): añade glosario de Git"
git push -u origin feature/docs-mod0-ajustes
# abrir PR en GitHub y usar Squash & Merge

```

# Checklist — Módulo 0 · Flujo Git práctico

## ✅ Setup (una sola vez)

- [ ]  `git config --global user.name "Tu Nombre"`
- [ ]  `git config --global user.email "tu@email.com"`
- [ ]  `git config --global init.defaultBranch main`
- [ ]  `git config --global fetch.prune true` *(limpia ramas remotas borradas)*
- [ ]  `git remote -v` comprobado (que `origin` apunte a GitHub)

## 🛠️ Flujo diario de trabajo

- [ ]  Crear rama corta: `git switch -c <prefix>/<nombre-corto>`
    
    *prefix sugerido: `feature/`, `fix/`, `docs/`*
    
- [ ]  Hacer cambios pequeños y atómicos
- [ ]  Añadir al staging: `git add -p` *(o `git add .` si procede)*
- [ ]  Commit claro (Conventional Commits):
    
    `docs(mod0): añade glosario de Git`
    
- [ ]  Push inicial de la rama: `git push -u origin <rama>`

## 🔀 Mantener la rama al día (si `main` avanzó)

- [ ]  `git fetch origin`
- [ ]  `git rebase origin/main` en tu rama
    
    *resolver conflictos → `git add <arch>` → `git rebase --continue`*
    
- [ ]  Subir rebase: `git push --force-with-lease`

## 🔎 Abrir y revisar PR

- [ ]  Abrir PR en GitHub contra `main` (descripción breve y checklist de lo que cambia)
- [ ]  Pasar CI/checks (si hay)
- [ ]  Revisar diff final en GitHub (auto-review)

## ✅ Merge y sincronización

- [ ]  **Squash & Merge** en GitHub (historial limpio)
- [ ]  Local:
    - [ ]  `git switch main`
    - [ ]  `git pull origin main`
    - [ ]  Borrar rama local (si fue squash): `git branch -D <rama>`
    - [ ]  Borrar rama remota (opcional): `git push origin --delete <rama>`

## 🧹 Mantenimiento semanal

- [ ]  Ver ramas fusionadas: `git branch --merged main`
- [ ]  Podar referencias: `git fetch --prune`
- [ ]  Revisar commits ruidosos y ajustar mensajes en futuros PR (squash)

## 🚨 Emergencias y conflictos

- [ ]  Ver diferencias antes de borrar: `git diff main..<rama>`
- [ ]  Si `git branch -d` se queja tras squash → usar `git branch -D <rama>`
- [ ]  Conflicto en rebase/merge:
    - [ ]  Editar archivos marcados `<<<<<<`, `======`, `>>>>>>`
    - [ ]  `git add <arch>` → `git rebase --continue` (o `git merge --continue`)
    - [ ]  Si te lías: `git rebase --abort` y vuelves a empezar
- [ ]  Push que reescribe historia: **siempre** `-force-with-lease` (no `-force` a secas)

## 🧭 Convenciones rápidas

- [ ]  Nombres de rama: `feature/mod0-git-flujos`, `docs/mod0-glosario`
- [ ]  Tipos de commit: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- [ ]  Regla simple:
    
    *Si el cambio necesita 2+ frases para explicarse → **rama + PR**.
    Si es typo/enlace roto → puede ir directo a `main`.*
    

---

### 📎 Mini-plantilla de PR (pegar en descripción)

- [ ]  Objetivo del cambio
- [ ]  Qué toca (archivos/secciones)
- [ ]  Cómo probarlo
- [ ]  Riesgos/notas

---

### 🤖 Prompts de IA (opcionales, para pegar en tu `prompts.md`)

```
Rol: Git coach senior.
Tarea: Mi rama está detrás de main y quiero actualizarla con historial limpio.
Formato: Dame comandos exactos y riesgos.
Contexto: Estoy en <mi-rama> y uso GitHub con Squash & Merge.

```

```
Rol: Revisor de PRs.
Tarea: Revisa este diff (te pego snippets) y dime si hay problemas de consistencia, naming o estructura.
Formato: Lista de observaciones accionables y cómo arreglarlas.

```

```
Rol: Asistente de resolución de conflictos.
Tarea: Tengo este conflicto (te pego el bloque con <<<<<< y >>>>>>).
Formato: Indica qué parte conservar, por qué, y el comando siguiente (add/continue).

```