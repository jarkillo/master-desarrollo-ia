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

### Módulo 1 – Fundamentos del desarrollo (3 semanas)
**Objetivos:**
- Pensamiento computacional → descomponer problemas.
- Ecosistema dev moderno: terminal, Git, GitHub, IDEs.
- Fundamentos de programación (estructuras de control, funciones, modularidad).
- Buenas prácticas: Clean Code, refactor, testing inicial.
- (Bonus) – Testing ampliado y primeras nociones de SOLID

**Mini-proyecto:**
- **CLI app sencilla** (ej. gestor de gastos, inventario o TODOs):
  - Implementación manual.
  - Refactor con Clean Code.
  - Tests básicos unitarios.
  - Uso de la IA para refactor y generación de tests.

---

### Módulo 2 – Ingeniería y Arquitectura (2 semanas)
**Objetivos:**
- Ciclo de vida del software (ágil, backlog, sprints).
- Principios SOLID y paradigmas de programación.
- Arquitecturas: monolito modular, microservicios, eventos.

**Mini-proyecto:**
- **Mini-API REST** con arquitectura limpia:
  - 2–3 endpoints básicos.
  - Aplicación de SOLID.
  - ADRs (Architecture Decision Records).
  - Diagramas generados con ayuda de IA.
  - Agents configurados para revisar commits bajo SOLID.

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

