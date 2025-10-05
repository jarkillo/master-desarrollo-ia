# Máster de Desarrollo con IA

# Máster en Desarrollo con IA aplicada

Este repositorio recoge el programa, apuntes y proyectos prácticos del máster.  
Cada módulo termina con un mini-proyecto entregable que se reutiliza y evoluciona en el siguiente.  

---

## 📂 Programa de formación

### Módulo 0 – Preparación (1 semana)
**Objetivos:**
- Mentalidad de estudio y documentación → Notion / Markdown.
- Plantear problemas a la IA de forma estructurada (role prompting, chains simples).
- Setup del entorno: Git + IDE + Cursor + agentes básicos (`cursorrules.md`, `agents.md`).

**Mini-proyecto:**
- Repo base “playground” con:
  - Documentación viva en `/docs`.
  - `agents.md` y `cursorrules.md` iniciales.
  - Configuración mínima de Git y Cursor.

---

### Módulo 1 – Fundamentos del desarrollo (4 clases)
**Objetivos:**
- Pensamiento computacional y descomposición de problemas.
- Ecosistema dev moderno: terminal, Git, GitHub, IDEs.
- Fundamentos de programación, estructuras y persistencia.
- Buenas prácticas: Clean Code, refactor, testing básico.
- Introducción a principios SOLID y TDD.

**Clases:**
1. Pensamiento computacional y ecosistema dev.
2. Fundamentos de programación y persistencia JSON.
3. Clean Code y testing inicial.
4. Testing ampliado y primeros principios SOLID (SRP).

**Mini-proyecto:**
- CLI app de tareas:
  - Implementación manual.
  - Refactor con Clean Code.
  - Tests unitarios + TDD básico.
  - Ampliación con prioridades y SRP.

---

### Módulo 2 – Ingeniería y Arquitectura (6 clases)
**Objetivos:**
- Ciclo de vida del software, backlog ágil y gestión de entregas.
- Principios SOLID aplicados a APIs.
- Arquitectura limpia: separación de capas (API, servicio, repositorio).
- Open/Closed y Dependency Inversion (repositorios intercambiables).
- Tests de integración y control de contratos entre capas.
- Integración continua (CI) y control de calidad automatizado.

**Clases:**
1. Ciclo de vida del software y backlog ágil.
2. Principios SOLID y paradigmas de programación (TDD con FastAPI).
3. Arquitectura limpia.
4. Open/Closed y Dependency Inversion.
5. Integración y pruebas de arquitectura.
6. Integración continua y control de calidad.

**Mini-proyecto:**
- Mini API REST con FastAPI:
  - Endpoints `/tareas` con tests TDD.
  - Arquitectura limpia con inyección de dependencias.
  - Repositorios en memoria y JSON.
  - Pipeline CI con GitHub Actions.


---

### Módulo 3 – Calidad y Seguridad (3 semanas)
**Objetivos:**
- Testing avanzado: unitario, integración, E2E.
- Métricas y coverage con CI/CD (GitHub Actions).
- Seguridad básica: OWASP Top 10, JWT, .env seguros.
- Observabilidad: Sentry + resúmenes de errores con IA.

**Mini-proyecto:**
- **Refactor y endurecimiento de la API**:
  - Suite de tests completa.
  - CI/CD automatizado con coverage report.
  - JWT y variables de entorno seguras.
  - Auditoría automática de PRs con agents.
  - Observabilidad inicial con Sentry.

---

### Módulo 4 – Infraestructura y Cloud (2 semanas)
**Objetivos:**
- DevOps y CI/CD → pipelines de despliegue.
- Cloud computing: costes, proveedores, buenas prácticas.
- Bases de datos: relacionales, NoSQL y vectoriales.
- LLMOps: integración ligera con LangChain / mini-RAG.

**Mini-proyecto:**
- **API desplegada en la nube con DB conectada**:
  - Añadir base de datos relacional o NoSQL.
  - CI/CD con despliegue automático.
  - Documentación viva de queries y migraciones.
  - Endpoint `/ask` conectado a vector DB (mini-RAG).
  - Monitoreo básico de logs y alertas.

---

### Módulo 5 – Seguridad avanzada y Cierre (1 semana)
**Objetivos:**
- DevSecOps: seguridad desde el diseño.
- Ciberseguridad aplicada a IA: prompt injection, data poisoning, exfiltración.
- Auditoría de código con IA.

**Proyecto Final:**
- **Aplicación full stack pequeña** con:
  - Backend = API endurecida.
  - Frontend básico (dashboard en React/Vite).
  - CI/CD completo (build + test + deploy).
  - Seguridad avanzada (linters de seguridad, auditoría IA).
  - Documentación viva (changelog automático, diagramas Mermaid).
  - `agents.md` ampliado: equipo virtual (PM, tester, arquitecto, auditor).

---

## 🏁 Resultado final
Un repositorio completo que demuestra:
- Fundamentos sólidos de desarrollo.
- Arquitectura y principios de diseño aplicados.
- Seguridad y calidad integradas en el ciclo.
- CI/CD real con despliegue en cloud.
- IA usada en cada fase como copiloto, revisor y documentador.

