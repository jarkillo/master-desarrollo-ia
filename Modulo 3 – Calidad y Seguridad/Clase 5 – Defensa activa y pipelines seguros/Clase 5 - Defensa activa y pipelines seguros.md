# 🎬 Clase 5 – Defensa activa y pipelines seguros (DevSecOps inicial)

## 🧩 El problema

Hasta ahora tu código **se defiende** (tests, coverage, linters, auditoría Bandit, JWT…).

Pero sigue habiendo un agujero: **el entorno donde se ejecuta**.

Si alguien cambia una dependencia insegura, si tu pipeline instala una librería comprometida o si tu `.env` se filtra, el daño no lo para ningún test.

Esta clase trata de eso: **proteger la tubería, no solo el agua.**

> “No basta con escribir código limpio; hay que ejecutar código en entornos limpios.”
> 

---

## 🧠 Concepto

Esto es **DevSecOps**: integrar la seguridad en el ciclo DevOps.

Hasta ahora tenías CI (tests automáticos). Ahora añadiremos:

1. **Escaneo de dependencias** → evita instalar librerías vulnerables.
2. **Validación de secretos** → que tu pipeline no filtre claves.
3. **Protección de ramas** → solo se hace merge si todo pasa verde.

La idea no es paranoia: es confianza verificable.

---

## ⚙️ Aplicación manual

### 1. Escaneo de dependencias con `safety`

Instálalo y añadelo al requirements.txt:

```bash
pip install safety

# Lanza esto desde la raiz del proyecto
safety scan --full-report

```

Te dirá si alguna librería del `requirements.txt` tiene vulnerabilidades conocidas.

(Desde las ultimas versiones te va a pedir que te registres gratis o que loguees con tu cuenta)

Luego te pedira un nombre, puedes dejarlo por defecto

Una vez este todo listo, logueate en la web de safety y veras que te pide que lances

```sql
safety init
```

Esto comenzara la instalacion del firewall de safety y comenzará a escanear las dependencias

### CI en GitHub con Safety (sin navegador)

1. Una vez termine el escaneo, podrás continuar en la web y ver tus codebase configuradas
2. Te dará una API Key, copiala y añadela a Github Actions Secrets como SAFETY_API_KEY
3. Añade la Action oficial al yaml de tests (el de .github/workflows)

```yaml
      - name: Auditoría de dependencias (Safety)
        uses: pyupio/safety-action@v1
        with:
          api-key: ${{ secrets.SAFETY_API_KEY }}

```

La Action respeta tu **política** (la misma que viste en consola) y fallará/pasará conforme a ella. [GitHub](https://github.com/pyupio/safety-action?utm_source=chatgpt.com)

Así GitHub te avisa si subes una versión con huecos de seguridad.

Aunque no nos vamos a meter en esto ahora. SI ya tienes cursor instalado, te habras dado cuenta de que te permite añadir un MCP a cursor.

```sql
{
  "mcpServers": {
    "safety-mcp": {
      "url": "https://mcp.safetycli.com/sse?api-key=TU API KEY"
    }
  }
}
```

Si te ves preparado añadelo en cursor config MCP

Si no has usado nunca cursor o otros agentes de IA, no te preocupes, volveremos a esto cuando toque

---

### 2. Detección de secretos accidentales

GitHub ya incluye una función nativa para detectar claves o tokens subidos por error.

Pero puedes añadir una verificación manual con **gitleaks** o **trufflehog**.

Ejemplo rápido (usando gitleaks en el pipeline):

```yaml
- name: Detección de secretos
  uses: zricethezav/gitleaks-action@v2
  with:
    args: detect --source . --no-git
```

Esto revisa tus commits y evita que pase un PR si encuentra algo con pinta de clave o token.

---

### 3. Ramas protegidas

Ve a tu repo → *Settings → Branches → Branch protection rules*.

Marca:

- Require pull request reviews before merging
- Require status checks to pass before merging

Ahora ningún cambio pasa sin revisión y sin que el CI lo apruebe.

---

## 🤖 Aplicación con IA (40%)

**Ver workflow completo**: `AI_WORKFLOW.md` incluye:

- **Fase 1**: Generación automática de GitHub Actions workflows con seguridad integrada
- **Fase 2**: Configuración de Gitleaks con reglas personalizadas (.gitleaks.toml)
- **Fase 3**: Setup de Dependabot para auto-updates de dependencias
- **Fase 4**: Branch protection rules y deployment strategies
- **5 ejercicios prácticos** guiados con IA (105 min total)
- **Prompts reutilizables** para generación, troubleshooting y optimización
- **Validación con agentes educativos** (checklists de revisión)

### Agentes Educativos Integrados

Los siguientes agentes educativos están disponibles para validar tu trabajo en esta clase:

**Python Best Practices Coach** (`.claude/agents/educational/python-best-practices-coach.md`):
- Valida scripts de CI/CD y configuraciones de workflows
- Revisa que los scripts de seguridad sigan convenciones Pythonic
- Detecta patrones anti-seguridad en código de pipeline

**Docker Infrastructure Guide** (`.claude/agents/educational/docker-infrastructure-guide.md`):
- Revisa configuraciones de deployment y Dockerfiles
- Valida prácticas de seguridad en contenedores (non-root, secrets, etc.)
- Optimiza health checks y restart policies

### Flujo de Trabajo Recomendado con IA

1. **Generación del pipeline base** (15 min):
   - Usa prompts del AI_WORKFLOW.md para crear el workflow inicial
   - La IA genera `.github/workflows/ci_security.yml` con Safety + Gitleaks

2. **Configuración de Gitleaks** (20 min):
   - Genera `.gitleaks.toml` con reglas personalizadas
   - Configura allowlist para falsos positivos (docs, examples)
   - Valida con Python Best Practices Coach

3. **Setup de Dependabot** (20 min):
   - Crea `.github/dependabot.yml` para auto-updates diarios
   - Configura grupos de seguridad para dependencias críticas
   - Establece límites de PRs abiertos simultáneos

4. **Branch protection** (15 min):
   - Configura reglas en GitHub Settings vía prompts guiados
   - Requiere status checks (CI + security scans)
   - Habilita auto-merge para Dependabot PRs

5. **Validación final** (35 min):
   - Ejecuta checklists de validación con agentes educativos
   - Revisa que todos los escaneos pasen
   - Documenta decisiones de seguridad en notes.md

### Prompt Rápido para Empezar

```
Rol: Ingeniero DevSecOps senior con experiencia en GitHub Actions.
Contexto: Proyecto FastAPI con tests, CI, auditoría Bandit y JWT.
Actualmente tengo .github/workflows/ci.yml básico con pytest.

Objetivo:
- Fortalecer el pipeline con escaneo de dependencias (Safety) y secretos (Gitleaks).
- Integrar Dependabot para auto-updates de seguridad.
- Configurar branch protection rules en main y dev.

Entrega:
1. YAML completo de .github/workflows/ci_security.yml con:
   - Safety scan con API key desde secrets
   - Gitleaks con GITHUB_TOKEN automático
   - Upload de artifacts para reportes
2. Archivo .gitleaks.toml con reglas personalizadas (allowlist para docs/, tests/fixtures/)
3. Configuración de .github/dependabot.yml para Python con updates diarios
4. Instrucciones paso a paso para configurar branch protection en GitHub UI

Formato: Código completo + explicaciones breves de cada decisión de seguridad.
```

**Ver más prompts y ejercicios detallados en**: `AI_WORKFLOW.md`

---

## 🧪 Mini-proyecto

1. Crea la rama `feature/devsecops-basico`.
2. Añade al pipeline una etapa con `safety` y `gitleaks`.
3. Ejecuta el CI y verifica que pasa.
4. Protege tu rama `main` desde GitHub.
5. Documenta en `notes.md`:
    - Qué vulnerabilidad detectó `safety`.
    - Qué archivos marcó `gitleaks`.
    - Qué mejora harías en tu pipeline.

---

## ✅ Checklist final

- [ ]  Has integrado escaneo de dependencias y secretos.
- [ ]  Tu CI falla si hay vulnerabilidades o claves expuestas.
- [ ]  Entiendes cómo aplicar DevSecOps sin sobrecargar el flujo.
- [ ]  Tu rama principal está protegida por CI y revisión.
- [ ]  Has documentado tu auditoría en `notes.md`.

## Errores en los test:

```sql
Warning: Unexpected input(s) 'args', valid inputs are ['']
Run zricethezav/gitleaks-action@v2
[user] is an individual user. No license key is required.
gitleaks version: 8.24.3
Version to install: 8.24.3 (target directory: /tmp/gitleaks-8.24.3)
Downloading gitleaks from https://github.com/zricethezav/gitleaks/releases/download/v8.24.3/gitleaks_8.24.3_linux_x64.tar.gz
/usr/bin/tar xz --warning=no-unknown-keyword --overwrite -C /tmp/gitleaks-8.24.3 -f /tmp/gitleaks.tmp
/usr/bin/tar --posix -cf cache.tzst --exclude cache.tzst -P -C /home/runner/work/master-ia-manu/master-ia-manu --files-from manifest.txt --use-compress-program zstdmt
Sent 5717455 of 5717455 (100.0%), 14.0 MBs/sec
event type: pull_request
Error: 🛑 GITHUB_TOKEN is now required to scan pull requests. You can use the automatically created token as shown in the [README](https://github.com/gitleaks/gitleaks-action#usage-example). For more info about the recent breaking update, see [here](https://github.com/gitleaks/gitleaks-action#-announcement).
```

## Qué pasa

- Tu workflow usa una acción de Gitleaks **con `args`**, pero **esa versión ya no acepta `args`**.
- Además, **en PRs exige `GITHUB_TOKEN`** o peta.

## Parche

Si lo quieres como **paso dentro de tu CI existente**, mételo **después** del `checkout`:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0

- name: Secret scanning
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```

## Por qué (rápido)

- **`fetch-depth: 0`**: Gitleaks necesita ver el historial para detectar secretos.
- **`GITHUB_TOKEN`**: desde hace poco lo requieren en PRs.
- **Sin `args`**: la acción v2 no usa `with: args:`; si luego quieres reglas, añade un `.gitleaks.toml`.

## Comprobación en 30s

1. Commit & push del YAML.
2. Abre/actualiza un PR → el job **Gitleaks** debe correr sin ese error.
3. Si falla por “falsos positivos”, creamos `.gitleaks.toml` o `.gitleaksignore` y afinamos.

## 🧩 Qué es ese `GITHUB_TOKEN`

GitHub **ya te lo da gratis y automático** en cada workflow.

No tienes que crearlo ni copiarlo de ningún sitio.

Solo tienes que **usarlo bien** dentro del YAML.

Por defecto, GitHub Actions genera un token temporal para cada ejecución, y lo expone en la variable:

```
${{ secrets.GITHUB_TOKEN }}

```

Ese token tiene permisos limitados, pero suficientes para:

- Acceder al código del repo.
- Leer/escribir en los PR.
- Comentar en issues.
- Ejecutar acciones (como Gitleaks, Dependabot, etc).

---

## ✅ Cómo se usa

En tu YAML, **no lo creas tú** — simplemente lo pasas así:

```yaml
- name: Secret scanning
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```

Y ya está.

No lo copias de ningún sitio, **GitHub lo inyecta automáticamente** al ejecutar el workflow.

---

## ⚙️ ¿Y si quisiera usar uno propio?

Si en algún momento necesitas un **token personal** (por ejemplo, porque el automático no tiene permisos para otro repo o organización), entonces sí lo creas tú:

1. Ve a tu perfil → **Settings → Developer settings → Personal access tokens → Tokens (classic)**.
2. Crea uno nuevo con permisos:
    - `repo`
    - `workflow`
3. Copia el token (solo se muestra una vez).
4. Entra a tu repositorio → **Settings → Secrets and variables → Actions → New repository secret**
5. Llámalo, por ejemplo, `MY_GITHUB_TOKEN`
    
    Y pega ahí el valor.
    

Entonces podrías usarlo así en el YAML:

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.MY_GITHUB_TOKEN }}

```

---

## 💡 En resumen

| Situación | Qué hacer |
| --- | --- |
| Workflow del propio repo | Solo pon `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` |
| Workflow que necesita más permisos o accede a otro repo | Crea un token manual y guárdalo en `Settings → Secrets` |