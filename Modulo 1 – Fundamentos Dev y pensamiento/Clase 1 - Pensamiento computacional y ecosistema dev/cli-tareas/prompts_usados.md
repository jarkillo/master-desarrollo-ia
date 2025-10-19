# Historial de Prompts - Clase 1

Este documento registra todos los prompts usados durante la clase, tanto exitosos como fallidos.

---

## ✅ Prompts que FUNCIONARON bien

### Prompt #1: Versión Production-Ready

**Prompt**:
```
Crea una CLI de gestión de tareas en Python con las siguientes características:

**Requisitos funcionales**:
- Comando `agregar <texto>`: añade tarea
- Comando `listar`: muestra todas las tareas
- Comando `completar <id>`: marca tarea como completada
- Persistencia en archivo JSON
- IDs autoincrementales

**Requisitos técnicos**:
- Usar `argparse` para parsing de comandos
- Separar en funciones (dominio, persistencia, CLI)
- Manejo de errores (archivo corrupto, ID inexistente)
- Docstrings en todas las funciones
- Python 3.12

**Output esperado**:
- Un solo archivo `tareas_ia_completo.py` con todo el código
- Código limpio y comentado
```

**Resultado**:
[Pega aquí lo que generó la IA]

**Por qué funcionó**:
- ✅ Especificó lenguaje y versión (Python 3.12)
- ✅ Detalló requisitos funcionales claros
- ✅ Indicó estructura técnica (argparse, separación de concerns)
- ✅ Especificó formato de output (un solo archivo)
- ✅ Pidió docstrings (mejora legibilidad)

**Lo que aprendí**:
- [Escribe qué aprendiste de la respuesta de la IA]
- [¿Qué usó la IA que no conocías?]

---

### Prompt #2: Refactoring con Single Responsibility

**Prompt**:
```
Refactoriza este código Python siguiendo el principio de Single Responsibility:
- Extrae comandos a funciones separadas
- Crea una función main()
- Añade docstrings a cada función

Código:
[código "feo" pegado aquí]

Mantén el mismo comportamiento exacto.
```

**Resultado**:
[Pega aquí el código refactorizado]

**Por qué funcionó**:
- ✅ Especificó el principio SOLID a aplicar (Single Responsibility)
- ✅ Detalló qué hacer (extraer funciones, crear main)
- ✅ Constraint importante: "mantén el mismo comportamiento"
- ✅ Pidió docstrings para mejor documentación

**Lo que aprendí**:
- [Escribe qué aprendiste sobre refactoring]

---

### Prompt #3: Debugging Específico

**Prompt**:
```
Tengo este código Python que da error al ejecutarlo:

[código con bugs pegado]

Error:
  File "tareas_bugs.py", line 8
    if comando = "listar":
               ^
SyntaxError: invalid syntax

¿Qué está mal y cómo lo corrijo?
```

**Resultado**:
[Respuesta de la IA con explicación]

**Por qué funcionó**:
- ✅ Incluyó código completo
- ✅ Incluyó error exacto con traceback
- ✅ Pregunta específica ("qué está mal y cómo corregirlo")
- ✅ Contexto suficiente para que la IA entienda el problema

**Lo que aprendí**:
- [Qué bugs encontró la IA que no viste tú]

---

## ❌ Prompts que NO funcionaron bien

### Prompt Malo #1: Demasiado Vago

**Prompt**:
```
Crea una app de tareas
```

**Resultado**:
[Descripción del código que generó - probablemente muy genérico]

**Problema**:
- ❌ No especifica lenguaje (¿Python? ¿JavaScript? ¿Java?)
- ❌ No especifica tipo de app (¿CLI? ¿Web? ¿Móvil?)
- ❌ No indica features específicas
- ❌ No menciona persistencia o estructura

**Cómo mejorarlo**:
Usar el Prompt #1 de arriba con todos los detalles.

---

### Prompt Malo #2: "Mejorar" Sin Contexto

**Prompt**:
```
Mejora este código

[pegar código]
```

**Resultado**:
[La IA probablemente hizo cambios aleatorios]

**Problema**:
- ❌ "Mejorar" es subjetivo (¿performance? ¿legibilidad? ¿features?)
- ❌ No especifica qué principios seguir
- ❌ No indica constraints (mantener comportamiento, no añadir deps, etc.)

**Cómo mejorarlo**:
```
Refactoriza este código siguiendo Single Responsibility Principle.
Extrae funciones para cada comando.
Mantén el mismo comportamiento exacto.
No uses dependencias externas.
```

---

### Prompt Malo #3: Sin Código Ni Error

**Prompt**:
```
Este código no funciona, ayuda
```

**Resultado**:
[La IA no puede ayudar sin ver el código]

**Problema**:
- ❌ No incluye el código
- ❌ No incluye el error
- ❌ No especifica qué debería hacer vs qué hace

**Cómo mejorarlo**:
Usar el Prompt #3 de arriba con código + error + comportamiento esperado.

---

### Prompt Malo #4: Pedir Demasiado

**Prompt**:
```
Crea una CLI de tareas con persistencia en PostgreSQL, autenticación JWT,
API REST con FastAPI, frontend en React, tests con pytest, CI/CD con GitHub Actions,
deployment en AWS, monitoreo con Prometheus, y documentación en Swagger.
```

**Resultado**:
[Código genérico que no funciona o es incompleto]

**Problema**:
- ❌ Demasiadas tecnologías a la vez
- ❌ La IA no puede generar un proyecto completo así
- ❌ Mejor dividir en pasos incrementales

**Cómo mejorarlo**:
Dividir en prompts separados:
1. Primero: CLI básica con persistencia en archivo
2. Luego: Migrar persistencia a PostgreSQL
3. Luego: Añadir tests
4. Luego: API REST con FastAPI
5. etc.

---

## 📝 Lecciones sobre Prompt Engineering

### Principio 1: Especificidad > Generalidad

❌ "Crea una API"
✅ "Crea una API REST con FastAPI para [caso de uso específico]"

### Principio 2: Contexto es Rey

❌ "¿Cómo testeo esto?" (sin código)
✅ "Tengo esta función [código]. Usa pytest para testear [caso específico]"

### Principio 3: Formato de Output Claro

❌ "Explica SOLID"
✅ "Explica los 5 principios SOLID usando: Nombre, Definición, Ejemplo en Python, Anti-patrón común"

### Principio 4: Constraints Ayudan

❌ "Refactoriza esto"
✅ "Refactoriza esto siguiendo SRP, sin cambiar comportamiento, solo stdlib de Python"

### Principio 5: Dividir y Conquistar

❌ "Crea app completa con backend, frontend, DB, deploy"
✅ Dividir en 4 prompts separados, uno por componente

---

## 🎯 Template de Prompt Efectivo (Copia y Pega)

```
**Rol**: [Dev Python senior / Experto en X / etc.]

**Tarea**: [Descripción clara de qué quieres que haga]

**Requisitos funcionales**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Requisitos técnicos**:
- [Tecnología/framework específico con versión]
- [Patrón de diseño a seguir]
- [Constraints: sin dependencias, solo stdlib, etc.]

**Output esperado**:
- [Formato: archivo único, múltiples archivos, estructura específica]
- [Estilo: con comments, con docstrings, con tests, etc.]

**Código base** (si aplica):
[Pegar código existente]

**Comportamiento esperado** (si es debugging):
[Qué debería hacer vs qué hace]
```

---

## 📚 Recursos para Mejorar Prompts

- Módulo 0, Clase 5: Prompt Engineering Avanzado
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)

---

## 🧪 Ejercicio: Experimenta con Prompts

**Desafío**: Intenta generar el mismo código con 3 prompts de diferentes niveles de especificidad:
1. Prompt vago (malo)
2. Prompt mejorado (bueno)
3. Prompt muy específico (excelente)

Compara los resultados y documenta qué cambió.
