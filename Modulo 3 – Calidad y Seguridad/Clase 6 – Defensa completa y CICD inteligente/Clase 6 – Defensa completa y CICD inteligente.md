# 🎬 Clase 6 – Defensa completa y CI/CD inteligente (cerrando el ciclo DevSecOps)

Vamos a comenzar la **Clase 6 del Módulo 3**, y para mantener la línea de lo que ya hemos hecho —código que se defiende, seguridad básica, auditoría con IA, JWT y defensa activa— esta clase va a cerrar el bloque de **Calidad y Seguridad** preparando el terreno para el módulo de infraestructura y despliegue.

### 🧩 El problema

Tu API ya se defiende sola, protege sus endpoints, audita su propio código y revisa dependencias.

Pero todavía dependes de ti para desplegar y vigilar lo que pasa **después** del merge.

> “El código no está seguro hasta que el entorno donde vive también lo está.”
> 

¿Y si una actualización rompe la API en producción?

¿Y si el pipeline falla, pero nadie lo nota?

¿Y si el servidor ejecuta una versión vieja?

Aquí damos el paso de **automatizar la defensa completa**: desde que haces `git push` hasta que la API vive en su entorno final.

---

## 🧠 Concepto

Esto ya es **DevSecOps maduro**:

- CI/CD que no solo prueba, sino **vigila**.
- Despliegue controlado y **reversible**.
- Notificaciones automáticas de fallos y auditorías.
- Variables de entorno seguras y rotatorias.

Tu pipeline debe comportarse como un **sistema inmune**: detectar, aislar y reportar anomalías.

---

## ⚙️ Aplicación manual – Paso a paso

### 1. Monitoreo de CI/CD con alertas

Puedes añadir notificaciones de fallos (por ejemplo, vía Slack o Discord) para que no dependas de revisar GitHub cada hora.

```yaml
- name: Notificar fallo al canal de alertas
  if: failure()
  uses: Ilshidur/action-slack@v2
  with:
    args: "⚠️ CI falló en ${{ github.repository }} – revisa el log."
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

```

Con esto, cualquier fallo en tests, auditorías o seguridad te llega al instante.

---

### 2. Variables de entorno seguras en despliegue

Nunca metas secretos en el YAML.

Usa los **secrets** de GitHub (ya lo aprendiste en la Clase 2) para inyectar valores en tiempo de ejecución:

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
  JWT_SECRET: ${{ secrets.JWT_SECRET }}
  MODE: "prod"

```

Así el pipeline usa las claves sin exponerlas.

---

### 3. Despliegue controlado (simulado)

Para no depender aún de un servidor real, puedes crear una simulación de despliegue en el CI:

```yaml
- name: Despliegue simulado
  run: |
    echo "Desplegando API en entorno seguro..."
    pytest --maxfail=1 --disable-warnings -q
    echo "✅ Despliegue simulado completado."
```

Esto te prepara para el módulo siguiente, donde el despliegue será real.

---

## 🤖 Aplicación con IA

Tu asistente IA puede ayudarte a mantener la seguridad viva en el pipeline.

Prompt reutilizable:

```
Rol: Ingeniero DevSecOps y observabilidad.
Contexto: Proyecto FastAPI con CI/CD, JWT y auditorías.
Objetivo: Mejorar el pipeline CI/CD para añadir:
- Notificación de errores.
- Despliegue seguro.
- Revisión de variables de entorno.
Entrega: YAML actualizado + checklist de seguridad.

```

La IA puede proponerte mejoras como:

- Integrar Dependabot para actualizaciones automáticas.
- Añadir Sentry para reportar errores en producción.
- Revisar logs con IA (resúmenes automáticos por PR).

Lo veremos con más detalle más adelante

---

## 🧪 Mini-proyecto

1. Crea la rama `feature/devsecops-final`.
2. Añade alertas y variables seguras al pipeline.
3. Simula el despliegue en CI.
4. Documenta en `notes.md`:
    - Qué agregaste al YAML.
    - Qué parte automatizaste con IA.
    - Qué alertas o reportes funcionaron.

---

## ✅ Checklist de cierre del Módulo 3

- [ ]  Tu CI/CD incluye alertas y validaciones de seguridad.
- [ ]  Usas secrets y variables seguras.
- [ ]  Sabes auditar tu proyecto automáticamente.
- [ ]  Tus pipelines fallan si algo está inseguro.
- [ ]  Has documentado la defensa completa de tu API.

---

La historia que comenzó con un CLI humilde termina aquí con un **sistema vivo**, capaz de defenderse, revisarse y mejorar sin intervención humana constante.

En el siguiente módulo, **Infraestructura y Cloud**, veremos cómo desplegar todo esto en entornos reales (AWS, Render o Railway), conectando bases de datos y LLMOps.