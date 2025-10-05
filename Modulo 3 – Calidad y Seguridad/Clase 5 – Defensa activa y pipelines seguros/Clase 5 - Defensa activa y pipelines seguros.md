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