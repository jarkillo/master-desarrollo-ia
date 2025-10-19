# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Added
- Nueva sección 4.5 "Security Hardening Mentor" en Módulo 3, Clase 4
  - Flujo pedagógico: "IA genera → Agentes revisan → Estudiante aprende → Itera"
  - Integración de 3 agentes educacionales:
    - Python Best Practices Coach (type hints, secrets management)
    - FastAPI Design Coach (DI avanzado, response models, rate limiting)
    - API Design Reviewer (RESTful principles, RFC compliance)
  - Checklist de seguridad JWT expandido (40+ items en 6 categorías)
  - Ejercicio práctico de auditoría con agentes paso a paso
  - Ejemplo de iteración completo (código inicial → feedback → refactorizado)
  - Meta-aprendizaje: aprendizaje proactivo vs reactivo
  - Recursos: Links a agentes educacionales, RFCs, herramientas de auditoría

### Changed
- Checklist de Clase 4 expandido de 5 items a 40+ items organizados en:
  - Fundamentos JWT (4 items)
  - Seguridad Crítica (7 items)
  - Calidad y Buenas Prácticas (6 items)
  - Auditoría con IA (5 items)
  - Testing y CI/CD (6 items)
  - Meta-aprendizaje (4 items)

## [2025-10-19]

### Added
- JAR-215: Integración de AI en Clase 4 (JWT Authentication) completada
- PR #44 creado: feat(M3-C4): Security Hardening Mentor con flujo pedagógico IA
- Branch: `feature/jar-215-m3-4-ai-integration`
- Commit: `0a84f11` - 315 insertions, 7 deletions

### Documentation
- Archivo modificado: `Modulo 3 – Calidad y Seguridad/Clase 4/Clase 4 - Seguridad avanzada y autenticación con JWT.md`
- Agentes educacionales utilizados:
  - `.claude/agents/educational/python-best-practices-coach.md`
  - `.claude/agents/educational/fastapi-design-coach.md`
  - `.claude/agents/educational/api-design-reviewer.md`

### Linear
- Issue JAR-215 actualizada a "In Progress"
- Comentario agregado con resumen completo de implementación

---

## Formato de entradas

### Added
Para nuevas funcionalidades.

### Changed
Para cambios en funcionalidades existentes.

### Deprecated
Para funcionalidades que pronto serán eliminadas.

### Removed
Para funcionalidades eliminadas.

### Fixed
Para corrección de bugs.

### Security
Para invitar a usuarios a actualizar en caso de vulnerabilidades.

### Documentation
Para cambios en documentación.

### Linear
Para actualizaciones en issues de Linear.
