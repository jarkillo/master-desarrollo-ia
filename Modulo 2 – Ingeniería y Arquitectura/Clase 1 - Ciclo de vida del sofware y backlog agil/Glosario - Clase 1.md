# 📖 Glosario – Clase 1

- **Ciclo de vida del software**: El conjunto de fases por las que pasa un proyecto, desde la idea inicial hasta su mantenimiento. Incluye planificación, desarrollo, pruebas, despliegue y feedback.
- **Backlog**: Lista priorizada de tareas, features, bugs y mejoras que se quieren implementar en el proyecto. Es la “fuente de verdad” de qué hay que hacer.
- **Sprint**: Periodo corto y definido de trabajo (normalmente 1–2 semanas) en el que el equipo selecciona un subconjunto del backlog y se compromete a completarlo.
- **Entrega (Incremento)**: El resultado tangible al final de un sprint. Debe ser un producto funcionando, aunque sea muy básico (ejemplo: una API con un solo endpoint `/health`).
- **Feedback**: La retroalimentación que se obtiene tras una entrega. Sirve para ajustar prioridades y mejorar el producto en el siguiente sprint.
- **Historia de usuario**: Forma de describir una necesidad desde el punto de vista del usuario. Se escribe en formato “Como [rol], quiero [objetivo] para [beneficio]”. Ejemplo: *“Como usuario quiero crear tareas vía API para poder gestionarlas desde apps externas.”*
- **Criterios de aceptación**: Condiciones específicas que deben cumplirse para que una historia de usuario se considere terminada. Ejemplo: *“El endpoint POST `/tareas` devuelve JSON con id, nombre y completada=false.”*
- **MVP (Minimum Viable Product)**: La versión más pequeña del producto que aún aporta valor real al usuario. En este módulo, el MVP es una API con tres endpoints básicos (crear, listar, completar tareas).
- **ADR (Architecture Decision Record)**: Documento corto donde se justifica una decisión de arquitectura (ejemplo: “Usamos FastAPI en lugar de Flask por X motivo”). Ayuda a entender por qué se tomaron decisiones técnicas.