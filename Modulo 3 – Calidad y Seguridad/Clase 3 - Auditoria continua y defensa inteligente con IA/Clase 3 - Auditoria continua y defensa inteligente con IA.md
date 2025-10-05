# 🎓 Clase 3 – Auditoria continua y defensa inteligente con IA

# 🧩 El punto de partida

Tu API ya:

- Tiene cobertura y linters (el código se defiende solo).
- Está protegida con API Key y validaciones Pydantic.
- Ejecuta CI automático en cada PR.

Pero aún depende **de ti** para darte cuenta si algo huele mal en el código.

Y tú eres humano. Te distraes, tienes sueño, o confías demasiado en el “ya pasaron los tests”.

**Aquí entra el siguiente paso de madurez:**

> Enseñar a la IA a auditar tu proyecto mientras tú duermes.
> 

---

## 🧠 Concepto: calidad como sistema vivo

La seguridad y la calidad no son “filtros” que se aplican al final.

Son **sistemas vivos** que observan, alertan y aprenden.

En un proyecto profesional, nadie revisa línea a línea los PRs.

Se confía en tres guardianes:

1. **Los tests** (aseguran que no rompes lo que ya existía).
2. **El CI/CD** (vigila que el proceso sea reproducible).
3. **Los auditores automáticos** (detectan patrones de riesgo o mala práctica).

Hoy tú vas a construir ese tercer guardián.

---

## ⚙️ Aplicación manual – cómo lo haría un dev senior

### Paso 1. Activar la auditoría de seguridad

Instala una herramienta como **bandit**, que analiza tu código en busca de fallos comunes (inyecciones, uso inseguro de `os.system`, contraseñas en texto plano...).

```bash
pip install bandit
bandit -r api/

```

Te devolverá algo como:

```
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'miclave123'
   Severity: High   Confidence: Medium
   Location: api/dependencias.py:10
```

Bandit no corrige —solo **te avisa**. (Esto puede que no te aparezca porque lo tenemos en un .env)

```sql
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.13.5
Run started:2025-10-05 16:37:50.122060

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 83
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
```

Si todo va bien, te dará esto.

Esto ya te convierte en un desarrollador que no “confía”, sino que **verifica**.

---

### Paso 2. Añadir la auditoría al CI

Dentro de tu `.github/workflows/ci_quality.yml` o en un archivo nuevo:

```yaml
      - name: Auditoría de seguridad
        working-directory: ${{ matrix.class_dir }}
        run: |
            pip install bandit
            bandit -r api/ -ll
```

Esto lanza la revisión automáticamente con cada PR.

Si detecta algo grave, el pipeline fallará.

Y nadie podrá hacer merge hasta arreglarlo. (Siempre que el repositorio este configurado así)

---

## 🤖 Aplicación con IA – cómo delegarlo con cabeza

No se trata de que la IA te diga “tu código es inseguro”.

Se trata de que le **pidas un informe técnico** y **lo traduzcas a acciones concretas**.

Prompt ejemplo:

```
Rol: Auditor de seguridad y calidad de código Python.
Contexto: Proyecto FastAPI con repositorios y CI configurado.
Objetivo: Revisa la carpeta `api/` y los tests.

Entrega:
- Riesgos de seguridad (alta / media / baja).
- Recomendaciones de refactor.
- Código que pueda mejorarse por legibilidad o separación de responsabilidades.
- Mejoras en el pipeline CI.
```

Con eso, la IA generará un informe tipo auditoría.

Luego tú eliges qué implementar o convertir en issues de GitHub.

Y puedes automatizar esa auditoría como *tarea recurrente del pipeline* (por ejemplo, una vez por semana).

---

## 🧩 Mini-proyecto de la clase

1. Crea la rama `feature/auditoria-continua`.
2. Instala y ejecuta `bandit` localmente.
3. Crea un nuevo workflow `.github/workflows/auditoria.yml` que:
    - Corra `bandit` sobre la carpeta `api/`.
    - Faille si detecta vulnerabilidades altas.
4. Pídele a la IA el informe de auditoría y anótalo en `notes.md`.
5. Abre PR con el título **“Auditoría de calidad automatizada”**.

---

## ✅ Checklist final

- [ ]  Has añadido un análisis de seguridad automático (bandit o similar).
- [ ]  Has generado un informe de auditoría con IA.
- [ ]  Tu pipeline CI avisa si hay código inseguro.
- [ ]  Entiendes cómo combinar pruebas, cobertura y análisis estático.
- [ ]  Tu código ahora no solo se defiende… **aprende a defenderse.**

---

## 🌱 Qué sigue

En la siguiente clase entraremos ya en **seguridad avanzada**:

JWT, cifrado y tokens temporales.

Pero no antes de tener una base sólida que te diga: *“puedo dormir tranquilo, si algo se rompe, el sistema me lo cuenta antes que el cliente.”*