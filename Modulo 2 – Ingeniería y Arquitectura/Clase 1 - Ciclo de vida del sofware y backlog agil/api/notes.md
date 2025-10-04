# 📌 Backlog inicial – Mini API de Tareas (Módulo 2)

Este documento recoge las primeras **historias de usuario** y el **backlog técnico** para la API de tareas.

---

## 🧑‍🤝‍🧑 Historias de usuario

1. **Como usuario quiero crear tareas vía API**, para poder gestionarlas desde apps externas.
2. **Como usuario quiero listar mis tareas**, para ver su estado de un vistazo.
3. **Como usuario quiero marcar tareas como completadas**, para llevar control de lo que ya hice.

---

## 📋 Backlog inicial (MVP)

- **Configurar entorno base de FastAPI**
  - Criterios de aceptación:
    - Proyecto inicializado con FastAPI.
    - Endpoint de salud `/health` que devuelve `{status: "ok"}`.

- **Endpoint: Crear tarea**
  - Criterios de aceptación:
    - POST `/tareas` con body `{ "nombre": "texto" }`.
    - Devuelve JSON con `id`, `nombre`, `completada=false`.

- **Endpoint: Listar tareas**
  - Criterios de aceptación:
    - GET `/tareas` devuelve lista de tareas.
    - Incluye estado `completada`.

- **Endpoint: Completar tarea**
  - Criterios de aceptación:
    - PATCH `/tareas/{id}/completar`.
    - Devuelve tarea actualizada con `completada=true`.

- **Tests básicos de integración**
  - Criterios de aceptación:
    - Tests que cubran los 3 endpoints.
    - Ejecutables con `pytest`.

- **ADRs (Architecture Decision Records) iniciales**
  - Criterios de aceptación:
    - Documento ADR explicando por qué usamos FastAPI.
    - Documento ADR sobre cómo persistiremos datos en esta fase (JSON en archivo vs. DB).

---

## ✅ Siguiente paso

- Abrir PR con este backlog.  
- A partir de aquí, cada clase de este módulo atacará un punto del backlog: primero arquitectura y SOLID, luego implementación de los endpoints, después diagramas y ADRs.
