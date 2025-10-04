**Prioridad (en tareas)**

Un campo nuevo que añadimos a cada tarea, para indicar si es “alta”, “media” o “baja”. Nos sirve para filtrar lo urgente de lo menos importante.

**Valor por defecto**

Cuando una función tiene un parámetro opcional y, si no lo pasas, se rellena automáticamente con un valor.

Ejemplo: en `agregar_tarea(..., prioridad="media")`, si no pasas prioridad, se usará “media”.

**Convención del guion bajo (`_`)**

En Python, si una función o variable empieza por `_`, significa: “esto es interno, no lo uses desde fuera”.

No es una regla obligatoria, solo una convención para humanos y programas automáticos.

**Backfill**

Truco para mantener compatibilidad con datos viejos. Si cargas un `tareas.json` antiguo que no tiene el campo `prioridad`, lo añadimos al vuelo con un valor por defecto.

**Filtro**

Cuando pedimos a una función que devuelva solo parte de los datos que cumple una condición. En este caso, `listar_tareas(..., prioridad="alta")` devuelve únicamente las tareas urgentes.

**SRP (Single Responsibility Principle)**

El primer principio de SOLID que hemos aplicado. Significa que cada función debe tener un único motivo para cambiar.

Ejemplo: `agregar_tarea` se encarga solo de crear y guardar; `listar_tareas` solo de devolver y filtrar.

**Historia de usuario**

Una descripción en lenguaje natural de lo que necesita un usuario. Ejemplo: *“Como usuario quiero ver solo las tareas urgentes para no perder lo importante”*. Esa historia luego se convierte en un test.

**Test de contrato**

Un test que actúa como acuerdo: define cómo debe responder una función en un caso concreto. Si el código cambia y no cumple el test, sabes que rompiste el contrato.