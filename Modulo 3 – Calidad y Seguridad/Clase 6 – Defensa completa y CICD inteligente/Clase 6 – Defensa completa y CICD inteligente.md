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

## 🤖 Aplicación con IA – Security Hardening Mentor

En esta clase, la IA no solo te ayuda a escribir código, sino que actúa como **mentor de seguridad** para enseñarte a detectar vulnerabilidades en código generado por IA.

### 🎯 Concepto: Security Hardening Mentor

Un "Security Hardening Mentor" es un agente de IA especializado que:

1. **Revisa tu código** desde perspectiva de seguridad
2. **Detecta anti-patrones** de seguridad (secrets hardcoded, SQL injection, XSS, etc.)
3. **Explica el "por qué"** de cada vulnerabilidad (no solo el "qué")
4. **Propone soluciones** con ejemplos de código seguro
5. **Enseña principios** de seguridad aplicables a otros contextos

**Diferencia clave**: No es solo un linter automático. Es un **profesor interactivo** que te ayuda a desarrollar intuición de seguridad.

---

### 🧪 Ejercicio Práctico: IA genera código, tú auditas

Este ejercicio te enseña la habilidad más crítica del desarrollo con IA: **auditar código generado**.

#### **Paso 1: Genera código inseguro con IA**

Usa este prompt con tu asistente IA (Claude, ChatGPT, etc.):

```
Crea un endpoint FastAPI para /admin/users que:
- Acepte un user_id como query parameter
- Consulte una base de datos con SQL directo
- Retorne los datos del usuario
- Incluya JWT básico sin validación de roles

Hazlo rápido, sin preocuparte por seguridad.
```

**⚠️ IMPORTANTE**: El objetivo es que la IA genere código con vulnerabilidades para que tú las identifiques.

#### **Paso 2: Audita el código generado**

La IA probablemente generó algo así:

```python
# ❌ CÓDIGO INSEGURO (generado por IA)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from api.seguridad_jwt import obtener_usuario_actual

router = APIRouter()

@router.get("/admin/users")
async def get_user(
    user_id: str,  # ⚠️ Sin validación
    current_user: dict = Depends(obtener_usuario_actual)  # ⚠️ Sin verificación de rol
):
    # ⚠️ SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = '{user_id}'"

    # ⚠️ Ejecuta consulta directa sin parametrización
    result = db.execute(text(query))
    user = result.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ⚠️ Expone información sensible sin filtrado
    return {
        "id": user.id,
        "email": user.email,
        "password_hash": user.password_hash,  # ⚠️ CRÍTICO: Expone hash de contraseña
        "role": user.role
    }
```

#### **Paso 3: Identifica las vulnerabilidades**

Usa el **Security Hardening Checklist** (abajo) para auditar el código:

| ⚠️ Vulnerabilidad | Ubicación | Severidad | Impacto |
|------------------|-----------|-----------|---------|
| **SQL Injection** | Línea 13 (`query = f"SELECT..."`) | 🔴 Crítica | Un atacante puede ejecutar `' OR '1'='1` y extraer toda la tabla |
| **Falta validación de rol** | Línea 10 (solo verifica JWT, no el rol) | 🔴 Crítica | Usuarios normales pueden acceder a `/admin/users` |
| **Exposición de secrets** | Línea 21 (`password_hash`) | 🟠 Alta | Expone hashes que pueden crackearse |
| **Sin validación de entrada** | Línea 9 (`user_id: str`) | 🟡 Media | Acepta cualquier string sin validación |

#### **Paso 4: Corrige con Security Hardening Mentor**

Usa este prompt para que la IA te enseñe a corregir:

```
Actúa como Security Hardening Mentor.

Tengo este código [pega el código inseguro].

Para cada vulnerabilidad:
1. Explica POR QUÉ es peligrosa (con ejemplo de ataque)
2. Muestra cómo explotarla (educativo)
3. Dame el código corregido con comentarios explicativos
4. Enséñame el principio de seguridad subyacente

Usa un tono educativo, no condescendiente.
```

**Código corregido** (que la IA debe generar):

```python
# ✅ CÓDIGO SEGURO (corregido con Security Hardening Mentor)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.seguridad_jwt import obtener_usuario_actual, verificar_rol_admin
from api.modelos import User
from pydantic import BaseModel, Field

router = APIRouter()

# ✅ Modelo de respuesta que NO expone información sensible
class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    # ✅ Nota: NO incluimos password_hash

@router.get("/admin/users", response_model=UserResponse)
async def get_user(
    user_id: int = Query(..., ge=1, description="ID del usuario (debe ser positivo)"),  # ✅ Validación con Pydantic
    current_user: dict = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    # ✅ PASO 1: Verificar que el usuario actual es administrador
    if not verificar_rol_admin(current_user):
        raise HTTPException(
            status_code=403,
            detail="Solo administradores pueden acceder a esta información"
        )

    # ✅ PASO 2: Consulta parametrizada (previene SQL injection)
    # ORM de SQLAlchemy gestiona la parametrización automáticamente
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # ✅ PASO 3: Respuesta filtrada (solo campos seguros)
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role
    )
```

**Lecciones aprendidas**:

1. **SQL Injection**: SIEMPRE usa consultas parametrizadas u ORM. NUNCA concatenes strings en SQL.
2. **Autorización != Autenticación**: JWT valida identidad, pero necesitas verificar permisos explícitamente.
3. **Principio de mínimo privilegio**: Solo expone los datos necesarios, nunca más.
4. **Validación de entrada**: Usa Pydantic para validar tipos, rangos y formatos.

---

### 📋 Security Hardening Checklist

Usa esta checklist al auditar código generado por IA:

#### **🔴 Críticas (bloquean despliegue)**

- [ ] **SQL Injection**: ¿Usa consultas parametrizadas u ORM?
- [ ] **Secrets hardcoded**: ¿Alguna API key, password o token en el código?
- [ ] **Exposición de información sensible**: ¿Devuelve password_hash, tokens, etc.?
- [ ] **Falta de autenticación**: ¿Endpoints críticos tienen `Depends(obtener_usuario_actual)`?
- [ ] **Falta de autorización**: ¿Verifica roles/permisos además de JWT?

#### **🟠 Altas (corregir antes de merge)**

- [ ] **Validación de entrada**: ¿Usa Pydantic con reglas (`Field(min_length=1, max_length=100)`)?
- [ ] **CORS abierto**: ¿`allow_origins=["*"]` en producción?
- [ ] **Rate limiting ausente**: ¿Endpoints públicos sin límite de requests?
- [ ] **Logging de información sensible**: ¿Se loguean contraseñas, tokens, PII?
- [ ] **Errores verbosos**: ¿Los 500 exponen stack traces en producción?

#### **🟡 Medias (mejorar en refactor)**

- [ ] **Sin HTTPS forzado**: ¿Permite HTTP en producción?
- [ ] **Headers de seguridad ausentes**: ¿Falta `X-Content-Type-Options`, `X-Frame-Options`?
- [ ] **Timeouts ausentes**: ¿Conexiones DB sin timeout?
- [ ] **Sin paginación**: ¿Endpoints retornan arrays sin límite?
- [ ] **Documentación de seguridad**: ¿README explica autenticación y permisos?

---

### 🎓 Prompt Avanzado: Security Hardening Mentor

Usa este prompt para crear tu propio mentor de seguridad en cualquier sesión:

```
Actúa como Security Hardening Mentor con estas capacidades:

1. DETECCIÓN: Identifica vulnerabilidades OWASP Top 10, CWE, y malas prácticas.
2. EDUCACIÓN: Explica el "por qué" detrás de cada vulnerabilidad con ejemplos de ataque reales.
3. CORRECCIÓN: Proporciona código seguro con comentarios explicativos línea por línea.
4. PRINCIPIOS: Enseña principios transferibles (Defense in Depth, Least Privilege, etc.).
5. CONTEXTO: Adapta consejos al stack tecnológico (FastAPI, JWT, SQLAlchemy).

Formato de respuesta:
---
🔴 VULNERABILIDAD DETECTADA: [Nombre]
📍 Ubicación: [Línea/función]
⚠️ Severidad: [Crítica/Alta/Media]
💥 Impacto: [Qué puede pasar]
🛠️ Ejemplo de ataque: [Código de exploit educativo]
✅ Solución: [Código corregido con explicaciones]
📚 Principio: [Concepto de seguridad subyacente]
---

Tono: Educativo, alentador, técnicamente preciso. Nunca condescendiente.

Código a auditar:
[Pega aquí el código generado por IA]
```

---

### 🔧 Mejoras del Pipeline CI/CD con IA

Tu asistente IA puede ayudarte a automatizar la seguridad en el pipeline:

**Prompt para mejorar el pipeline**:

```
Rol: Ingeniero DevSecOps y observabilidad.
Contexto: Proyecto FastAPI con CI/CD, JWT y auditorías (Bandit, Safety, Gitleaks).
Objetivo: Mejorar `.github/workflows/ci_quality.yml` para añadir:
1. Notificación de errores (Slack/Discord)
2. Variables de entorno seguras (validar que no hay secrets hardcoded)
3. Despliegue simulado con rollback automático si fallan tests de seguridad
4. Resumen de auditoría en comentarios del PR

Entrega: YAML actualizado + explicación de cada paso.
```

**Mejoras sugeridas por IA**:

- **Dependabot**: Actualizaciones automáticas de dependencias con auditoría de seguridad
- **Sentry**: Reportar errores en producción con contexto de seguridad
- **CodeQL**: Análisis estático de seguridad en cada PR
- **SBOM Generation**: Software Bill of Materials para auditorías de compliance

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