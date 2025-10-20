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

## 🤖 Aplicación con IA

Prompt práctico:

```
Rol: Ingeniero DevSecOps.
Contexto: Proyecto FastAPI con tests, CI, auditoría y JWT.
Objetivo:
- Fortalecer el pipeline con escaneo de dependencias y secretos.
- Mejorar reglas de protección de ramas.
Entrega:
- YAML de ejemplo con safety + gitleaks.
- Recomendaciones de configuración en GitHub.

```

La IA te devolverá versiones más completas (por ejemplo, incluir `pip-audit`, `trivy`, o integración con dependabot).

Tú decides hasta dónde llevarlo.

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

---

## 🤖 Security Hardening Mentor: IA como Auditor de Seguridad

En esta sección aprenderás a usar IA como un **auditor de seguridad proactivo**, no solo para generar código sino para **detectar vulnerabilidades** antes de que lleguen a producción.

### La filosofía: "Trust but Verify" (Confía pero Verifica)

La IA puede generar código rápido y funcional, pero **no siempre seguro**. Tu rol es:

1. **Usar IA para acelerar desarrollo** → Genera pipelines, validaciones, configuraciones
2. **Auditar el código generado** → Buscar anti-patterns de seguridad
3. **Iterar con IA** → Pedirle que corrija vulnerabilidades específicas
4. **Documentar lecciones aprendidas** → Construir tu propio checklist

> **Regla de oro**: Nunca mergees código generado por IA sin auditarlo manualmente.

---

### 🛡️ Ejercicio Práctico: "IA Genera, Tú Auditas"

#### Paso 1: Genera un Pipeline de Seguridad con IA

Usa este prompt en Claude Code u otro asistente IA:

```
Rol: Ingeniero DevSecOps
Contexto: API FastAPI con autenticación JWT (api/seguridad_jwt.py)
Objetivo: Crear workflow de GitHub Actions (.github/workflows/security-audit.yml) que incluya:
1. Safety scan (escaneo de dependencias)
2. Gitleaks (detección de secretos)
3. Bandit (análisis estático de código Python)
4. Validación de variables de entorno
5. Falla el pipeline si hay vulnerabilidades críticas

Entrega:
- YAML completo con comentarios explicativos
- Configuración de permisos mínimos necesarios
- Uso correcto de GITHUB_TOKEN
```

**Lo que recibirás**: Un workflow YAML completo generado por IA.

#### Paso 2: Audita el Código Generado

Revisa el YAML línea por línea usando este **Checklist de Auditoría de Seguridad**:

#### 🔍 Checklist de Auditoría de Seguridad (DevSecOps)

**Permisos y Tokens:**
- [ ] ¿Usa `GITHUB_TOKEN` correctamente?
- [ ] ¿Los permisos del token son mínimos necesarios (`permissions: read-only` por defecto)?
- [ ] ¿Los secretos están en `${{ secrets.X }}` y no hardcodeados?

**Escaneo de Dependencias (Safety):**
- [ ] ¿Instala `safety` o usa la action oficial (`pyupio/safety-action`)?
- [ ] ¿Valida con `--full-report` o configuración de política?
- [ ] ¿Falla el pipeline en vulnerabilidades críticas?

**Detección de Secretos (Gitleaks):**
- [ ] ¿Usa `gitleaks/gitleaks-action@v2` (no la versión antigua)?
- [ ] ¿Incluye `fetch-depth: 0` en el checkout para ver historial?
- [ ] ¿Pasa `GITHUB_TOKEN` como variable de entorno?
- [ ] ¿Tiene `.gitleaksignore` para falsos positivos?

**Análisis Estático (Bandit):**
- [ ] ¿Ejecuta `bandit -r api/ -ll` (nivel de severidad low/low mínimo)?
- [ ] ¿Excluye directorios de tests con `-x`?
- [ ] ¿Genera un reporte legible?

**Variables de Entorno:**
- [ ] ¿Valida que existan las variables críticas (`JWT_SECRET`, etc.)?
- [ ] ¿Los secrets vienen de GitHub Secrets, no del código?

**Protección de Ramas:**
- [ ] ¿El workflow se ejecuta en PRs (`on: pull_request`)?
- [ ] ¿Bloquea el merge si falla (`required: true` en branch protection)?

**Dockerfile (si aplica):**
- [ ] ¿Usa usuario no-root (`USER nonroot`)?
- [ ] ¿No expone secretos en layers (`ARG` vs `ENV`)?
- [ ] ¿Multi-stage build para reducir superficie de ataque?

#### Paso 3: Encuentra al Menos 3 Problemas

**Ejercicio**: La IA probablemente cometió al menos 3 errores. Los más comunes:

1. **Olvidar `fetch-depth: 0`** → Gitleaks no puede escanear historial
2. **Usar `args:` en gitleaks-action@v2** → Versión nueva no los acepta
3. **No validar variables de entorno antes de deployar** → Falla en runtime
4. **Permisos excesivos en GITHUB_TOKEN** → Violar principio de mínimo privilegio
5. **No excluir tests de Bandit** → Falsos positivos por código de prueba

**Tu trabajo**: Identifica qué problemas tiene el código generado y corrígelos manualmente.

#### Paso 4: Itera con la IA

Una vez identificados los problemas, pídele a la IA que los corrija:

```
El workflow que generaste tiene estos problemas:
1. Falta fetch-depth: 0 en el checkout para Gitleaks
2. Usa 'args:' en gitleaks-action@v2 (ya no se acepta)
3. No valida que JWT_SECRET exista antes de ejecutar

Corrígelo siguiendo las mejores prácticas de DevSecOps.
```

**Resultado esperado**: Un workflow corregido y más robusto.

---

### 🎯 Mini-Proyecto: Security Audit Completo

**Objetivo**: Implementar un pipeline de seguridad auditado por ti, generado por IA.

**Pasos**:

1. **Genera el workflow con IA** usando el prompt de arriba
2. **Crea una rama**: `feature/security-audit-ai`
3. **Audita el código** usando el checklist
4. **Corrige errores** (manualmente o iterando con IA)
5. **Ejecuta el pipeline** y verifica que pasa (o falla correctamente)
6. **Documenta en `SECURITY_AUDIT.md`**:
   ```markdown
   # Security Audit Report - Clase 5

   ## Código Generado por IA
   - Prompt usado: [tu prompt]
   - Asistente: [Claude Code / ChatGPT / etc]

   ## Vulnerabilidades Detectadas
   1. **[Problema 1]**: [Descripción]
      - Severidad: [Alta/Media/Baja]
      - Fix: [Cómo lo corregiste]

   2. **[Problema 2]**: [...]

   ## Lecciones Aprendidas
   - La IA no validó [X] porque [razón]
   - Siempre revisar [aspecto específico]
   - Prompt mejorado: [versión corregida del prompt]

   ## Checklist Final
   - [x] Pipeline pasa sin errores
   - [x] Gitleaks detecta secretos de prueba
   - [x] Safety identifica vulnerabilidades
   - [x] Bandit no genera falsos positivos
   ```

7. **Haz un PR** y verifica que el CI pase
8. **Refleja**: ¿Qué aprendiste de auditar código de IA?

---

### 🧠 Prompts Educativos para Seguridad

Usa estos prompts para profundizar tu aprendizaje:

#### Prompt 1: Análisis de Vulnerabilidades
```
Rol: Security Auditor
Contexto: Este archivo [api/seguridad_jwt.py] maneja autenticación JWT
Tarea: Analiza el código línea por línea y lista:
1. Vulnerabilidades potenciales
2. Anti-patterns de seguridad
3. Mejoras siguiendo OWASP Top 10

Formato: Tabla con [Línea | Problema | Severidad | Fix recomendado]
```

#### Prompt 2: Hardening de Dockerfile
```
Rol: Docker Security Expert
Contexto: Dockerfile en [ruta]
Tarea: Auditalo para:
1. Usuario root (debe ser no-root)
2. Secretos expuestos en layers
3. Imagen base vulnerable (recomendar alpine/distroless)
4. Multi-stage build para reducir tamaño

Entrega: Dockerfile corregido + explicación de cada cambio
```

#### Prompt 3: Configuración de GitHub Branch Protection
```
Rol: DevOps Engineer
Tarea: Dame las reglas exactas de branch protection para main/dev que incluyan:
1. Require PR reviews (¿cuántas?)
2. Require status checks (¿cuáles?)
3. Restrict who can push (¿quién?)
4. Require signed commits (¿sí/no?)

Justifica cada decisión para un proyecto educativo en producción.
```

---

### 🤝 Workflow: IA + Humano en Security Review

```
┌─────────────────────┐
│  IA genera código   │  → Rápido, cubre casos comunes
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Humano audita      │  → Busca edge cases, vulnerabilidades
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  IA corrige issues  │  → Itera basado en feedback humano
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Humano valida fix  │  → Asegura que la corrección es correcta
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Merge + Deploy     │  → Solo si pasa auditoría humana
└─────────────────────┘
```

**Regla crítica**: El humano tiene veto final. Si algo no te convence, no lo merges.

---

### 📚 Recursos para Profundizar

**OWASP (Open Web Application Security Project):**
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

**DevSecOps:**
- [DevSecOps Manifesto](https://www.devsecops.org/)
- [GitHub Security Best Practices](https://docs.github.com/en/actions/security-guides)

**Herramientas:**
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [Safety CLI](https://docs.safetycli.com/)
- [Bandit](https://bandit.readthedocs.io/)

---

### ✅ Checklist Final (40% IA integrada)

- [ ] Has generado un pipeline de seguridad con IA
- [ ] Has auditado el código generado usando el checklist
- [ ] Has encontrado y corregido al menos 3 vulnerabilidades
- [ ] Has iterado con IA para mejorar el código
- [ ] Has documentado el proceso en `SECURITY_AUDIT.md`
- [ ] Entiendes que **nunca debes confiar ciegamente en código generado por IA**
- [ ] Has probado el pipeline en un PR real
- [ ] Has configurado branch protection basado en estos checks

---

### 🔥 Reto Avanzado: Red Team vs Blue Team con IA

**Escenario**: Simula un ataque a tu API usando dos roles de IA.

**Red Team (Atacante - IA 1)**:
```
Rol: Penetration Tester
Objetivo: Encuentra vulnerabilidades en esta API FastAPI [api/api.py]
Técnicas: SQL Injection, JWT manipulation, rate limiting bypass, secret exposure
Entrega: Lista de 5 vulnerabilidades explotables con PoC (Proof of Concept)
```

**Blue Team (Defensor - IA 2 o tú)**:
```
Rol: Security Engineer
Objetivo: Corrige cada vulnerabilidad reportada por Red Team
Entrega: Código hardened + tests que demuestran que el ataque ya no funciona
```

**Resultado**: Un ciclo completo de security review con IA jugando ambos roles.

---

## 🎓 Reflexión Final

Al terminar esta clase, deberías ser capaz de:

1. **Generar código de seguridad con IA** (pipelines, validaciones, configs)
2. **Auditar críticamente ese código** (no confiar a ciegas)
3. **Iterar con IA para corregir** (prompts específicos y directos)
4. **Documentar lecciones aprendidas** (construir tu biblioteca de anti-patterns)

> **La IA es un copiloto experto, pero tú eres el capitán. Nunca sueltes los controles en temas de seguridad.**