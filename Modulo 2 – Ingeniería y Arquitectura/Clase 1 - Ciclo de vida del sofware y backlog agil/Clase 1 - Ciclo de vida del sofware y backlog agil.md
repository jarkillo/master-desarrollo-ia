# Clase 1 - Ciclo de vida del software y backlog ágil

En el **Módulo 1** la trama fue clara:

- **Clase 1**: aprendiste a pensar como dev → descomponer problemas, usar la terminal, y montar un CLI mínimo con `sys.argv`.
- **Clase 2**: le diste persistencia → tu CLI ya guardaba datos en JSON, con funciones bien separadas. La IA te mostró `argparse` y modularidad.
- **Clase 3**: apareció la disciplina → Clean Code y los primeros tests unitarios (`unittest`). Descubriste que refactorizar sin red de seguridad es un salto al vacío.
- **Clase 4 (bonus)**: probaste a escalar tu CLI con nuevas features (prioridades). Aquí los tests se convirtieron en alarma y guía. Viste el primer principio **SOLID** (SRP: Single Responsibility Principle).

Esa historia termina con tu CLI convertido en un pequeño **motor fiable**: tiene lógica separada, tests que lo protegen y ya no es un juguete que se rompe al primer soplido.

Ahora viene el **Módulo 2**: imagina que tu jefe te dice:

*"El CLI está guay… pero necesitamos una API para que el equipo de frontend pueda usarlo en una app web."*

Aquí empieza la nueva aventura: pasar de un **script individual** a un **servicio de software con arquitectura**.

Eso significa pensar en:

- **El ciclo de vida del software** (no solo escribir código, sino gestionarlo con backlog, sprints y entregas).
- **Principios SOLID completos** (no solo SRP).
- **Arquitecturas**: cuándo un monolito es suficiente, cuándo separar en módulos o microservicios, y cómo documentar decisiones (ADRs).

Mini-spoiler: igual que tu CLI empezó con `sys.argv` y terminó con tests y capas, ahora tu API empezará con un endpoint mínimo y terminará con una **mini-arquitectura limpia**.

---

Antes de seguir, una nota:

La mayoría de cursos de “IA para devs” empiezan con lo llamativo: prompts mágicos, agentes encadenados, autogpt’s que hacen café mientras tú ves Netflix. Suena espectacular… hasta que pruebas a usarlos en un proyecto real y el castillo se te cae encima porque no entiendes qué está pasando bajo el capó.

Aquí hicimos justo lo contrario: primero construiste **músculo de dev**. Aprendiste a pensar en problemas como ordenadores, a escribir un CLI que guarda cosas, a refactorizar y a testear. Puede sonar “más básico” que tener un ejército de agentes en cinco minutos, pero la diferencia es brutal: **tú sabes lo que está pasando**.

Ahora la IA se vuelve mucho más poderosa. Porque no vas a usarla como un generador de líneas mágicas, sino como un **equipo de juniors** que te ayudan siguiendo tus reglas:

- Un agente puede ser tu tester, que genera y ejecuta tests automáticamente.
- Otro agente puede actuar como arquitecto, sugiriendo cómo dividir módulos y dejando ADRs documentados.
- Incluso puedes tener un PM virtual que convierte historias de usuario en issues de GitHub.

Ese es el hype real: no es que la IA te quite trabajo, es que te multiplica, pero solo si tienes los fundamentos para dirigirla. Y justo eso es lo que estamos haciendo: te has ganado el derecho a que la IA trabaje contigo como **copiloto disciplinado**, no como mago impredecible.

Así que ahora sí: pasamos del **CLI de juguete** a una **API de verdad**, con backlog ágil, SOLID aplicado y agentes que te acompañan en el camino.

---

## Comencemos:

Genial, arrancamos **Clase 1 del Módulo 2 – Ciclo de vida del software y backlog ágil**.

## Concepto

Hasta ahora trabajabas casi en “modo artesano”: abres tu editor, picas código, haces commits y PRs. Eso está bien para un CLI pequeño, pero cuando construyes una API (aunque sea mini) ya necesitas **organizar el trabajo como un equipo**.

Ahí entra el **ciclo de vida del software**. Suena pomposo, pero en realidad es una coreografía simple:

1. **Backlog** → la lista de todo lo que queremos hacer (features, bugs, mejoras).
2. **Sprint** → elegir un subconjunto de ese backlog y comprometerte a completarlo en un período (1–2 semanas).
3. **Entrega** → al final del sprint, el producto tiene que “respirar”: algo que funcione, aunque sea pequeñito.
4. **Feedback** → revisas, corriges, ajustas prioridades, y arrancas otro sprint.

Con esto, no vas a estar meses programando en una cueva hasta enseñar algo: siempre tendrás un prototipo funcionando, listo para mostrar y probar.

## Aplicación manual

Vamos a simular el **primer backlog** para tu mini-API de tareas.

Historias de usuario (en formato clásico “Como… quiero… para…”):

- Como usuario quiero crear tareas vía API para gestionarlas desde apps externas.
- Como usuario quiero listar mis tareas para ver el estado.
- Como usuario quiero marcar tareas como completadas para llevar control.

Ese es tu **MVP (Minimum Viable Product)**: 3 endpoints básicos.

El backlog inicial también puede incluir cosas técnicas, como:

- Configurar un entorno de FastAPI.
- Documentar decisiones de arquitectura (ADRs).
- Preparar tests básicos de integración.

## Aplicación con IA

Aquí es donde la IA brilla. Puedes tratarla como un **Product Owner junior** que traduce tus historias en backlog técnico. Ejemplo de prompt:

```
Rol: Product Owner técnico.

Contexto: Tengo un mini-proyecto para una API REST de tareas con FastAPI.
Objetivo: Convierte estas historias de usuario en un backlog con issues de GitHub (cada issue con título, descripción y criterios de aceptación).

Historias:
- Como usuario quiero crear tareas vía API.
- Como usuario quiero listar mis tareas.
- Como usuario quiero marcar tareas como completadas.

Formato: Markdown con lista de issues.
```

La IA te devolverá algo parecido a un tablero inicial. Luego podrás pegarlo en GitHub Projects, Jira o Notion, y empezar a jugar como si fuese un proyecto real.

## Ejercicio práctico

1. Crea una rama `feature/backlog-api`.
2. Añade un archivo `Modulo2/api/notes.md`.
3. Dentro escribe las **3 historias de usuario** y el **backlog inicial** (puedes pedirle a la IA que lo expanda con criterios de aceptación).
4. Haz commit y PR. Ese será tu punto de partida para el módulo 2.

### Checklist rápida

- Entendiste qué es backlog y sprint.
- Tienes tus 3 historias de usuario como base del mini-proyecto.
- Tienes un `notes.md` con la primera versión del backlog.

---

Aquí acaba la primera clase: ya no hablamos solo de código, sino de **gestión del ciclo de vida**. En la siguiente nos meteremos en **SOLID y arquitectura limpia** para empezar a dar forma a la API.