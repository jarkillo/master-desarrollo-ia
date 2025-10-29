# Ejercicio Clase 2: Refactorización con IA y Persistencia JSON

## 🎯 Objetivos

1. **Refactorizar código existente** con ayuda de IA (mejorar sin romper)
2. **Agregar persistencia JSON** guiado por IA
3. **Aplicar separación de responsabilidades** (presentación vs lógica vs datos)
4. **Aprender a pedir refactorizaciones incrementales** (paso a paso, no todo de golpe)

---

## 📋 Pre-requisitos

Antes de empezar necesitas:

1. ✅ `tareas.py` funcional de Clase 1 (versión básica en memoria)
2. ✅ Python 3.12+
3. ✅ Acceso a Claude Code o asistente de IA
4. ✅ Conocimiento básico de funciones Python

---

## 🔨 Parte 1: Refactorización Incremental con IA (40 min)

### Tarea 1.1: Análisis del Código Actual

**Objetivo**: Identificar qué puede mejorarse ANTES de pedir refactorización.

**Prompt para análisis**:

```
Tengo este código de un CLI de tareas en Python:

[PEGA TU CÓDIGO AQUÍ]

Analiza el código y dame:

1. Puntos fuertes (qué está bien hecho)
2. Code smells (problemas de diseño):
   - Funciones largas
   - Responsabilidades mezcladas
   - Código duplicado
   - Variables con nombres poco claros
3. Sugerencias de refactorización priorizadas (1=más importante)

No refactorices aún, solo analiza.
```

**Anota en `analisis_codigo.md`**:

```markdown
# Análisis del Código - Clase 2

## Puntos Fuertes
1.
2.
3.

## Problemas Detectados
| Problema | Severidad (1-5) | Dónde está |
|----------|-----------------|------------|
|          |                 |            |

## Prioridades de Refactorización
1. [Más urgente]
2.
3.
```

---

### Tarea 1.2: Refactorización Paso 1 - Separar Lógica de Presentación

**Objetivo**: Crear una capa de lógica separada de la UI.

**Prompt efectivo**:

```
Voy a refactorizar mi código en pasos. Paso 1: separar lógica de presentación.

Código actual:
[PEGA CÓDIGO AQUÍ]

Tarea:
1. Crea una clase `GestorTareas` con la lógica de negocio:
   - agregar_tarea(nombre: str) -> int
   - listar_tareas() -> list[dict]
   - completar_tarea(id: int) -> bool
   - eliminar_tarea(id: int) -> bool

2. Mantén las funciones de UI separadas (mostrar_menu, etc.)

3. Usa type hints en todas las funciones

4. Agrega docstrings explicando qué hace cada método

Restricciones:
- NO agregues persistencia aún (en memoria)
- Mantén la misma funcionalidad
- Código debe seguir ejecutando igual desde `main()`

Explica por qué esta separación es importante.
```

**Valida el resultado**:

```markdown
# Checklist - Refactorización Paso 1

- [ ] ¿Existe la clase `GestorTareas`?
- [ ] ¿Las funciones de UI solo manejan input/output?
- [ ] ¿La lógica de tareas está en la clase?
- [ ] ¿Todos los métodos tienen type hints?
- [ ] ¿Todos los métodos tienen docstrings?
- [ ] ¿El programa sigue funcionando igual?
```

---

### Tarea 1.3: Refactorización Paso 2 - Validaciones

**Objetivo**: Agregar validación robusta de datos.

**Prompt**:

```
Paso 2: Agregar validaciones a mi GestorTareas.

Validaciones necesarias:
1. agregar_tarea:
   - Nombre no vacío (min 3 caracteres)
   - Raise ValueError con mensaje claro si falla

2. completar_tarea / eliminar_tarea:
   - ID debe existir
   - Raise KeyError si no existe

3. Agregar un método privado `_validar_nombre(nombre: str) -> None`

Actualiza solo la clase GestorTareas, no toques la UI aún.

Muestra cómo probar las validaciones con ejemplos.
```

**Prueba las validaciones**:

```python
# test_validaciones.py
gestor = GestorTareas()

# Debe fallar
try:
    gestor.agregar_tarea("")  # Nombre vacío
except ValueError as e:
    print(f"✅ Validación funciona: {e}")

# Debe fallar
try:
    gestor.completar_tarea(999)  # ID inexistente
except KeyError as e:
    print(f"✅ Validación funciona: {e}")
```

---

## 💾 Parte 2: Agregar Persistencia JSON con IA (40 min)

### Tarea 2.1: Diseño de Persistencia

**Objetivo**: Planificar la persistencia ANTES de implementar.

**Prompt de diseño**:

```
Necesito agregar persistencia JSON a mi GestorTareas.

Requisitos:
1. Guardar tareas automáticamente después de cada operación
2. Cargar tareas al iniciar el programa
3. Manejar casos edge:
   - Archivo no existe (primera ejecución)
   - Archivo corrupto (JSON inválido)
   - Permisos de escritura

Pregunta:
¿Dónde debe estar la lógica de persistencia?

Opciones:
A) Dentro de GestorTareas
B) En una clase separada RepositorioTareas
C) En funciones globales

Dame pros/contras de cada opción y recomienda la mejor para este nivel de complejidad.
```

**Anota en `diseno_persistencia.md`**:

```markdown
# Diseño de Persistencia

## Opciones Evaluadas
[Copia aquí la respuesta de la IA]

## Decisión Final
Elegí: [A/B/C]

Razón:
-
-

## Estructura del JSON
```json
{
  "tareas": [
    {
      "id": 1,
      "nombre": "Comprar leche",
      "completada": false
    }
  ],
  "proximo_id": 2
}
```
```

---

### Tarea 2.2: Implementación con IA

**Prompt de implementación**:

```
Implementa persistencia JSON para mi GestorTareas.

Código actual:
[PEGA CÓDIGO DE GestorTareas]

Requisitos:
1. Crear clase `RepositorioJSON`:
   - __init__(self, ruta_archivo: str)
   - guardar(tareas: list[dict], proximo_id: int) -> None
   - cargar() -> tuple[list[dict], int]  # (tareas, proximo_id)

2. Modificar `GestorTareas`:
   - Recibir RepositorioJSON en __init__
   - Llamar a repositorio.guardar() después de cada operación
   - Cargar datos en __init__

3. Manejo de errores:
   - FileNotFoundError → crear archivo vacío
   - JSONDecodeError → loggear error, empezar con lista vacía
   - PermissionError → mostrar mensaje claro

4. Usar pathlib en lugar de strings para rutas

Muestra el código completo y un ejemplo de uso.
```

---

### Tarea 2.3: Testing de Persistencia

**Objetivo**: Verificar que la persistencia funciona.

**Pruebas manuales**:

```bash
# Prueba 1: Primera ejecución
1. Elimina tareas.json si existe
2. Ejecuta el programa
3. Agrega 2 tareas
4. Cierra el programa
5. Verifica que tareas.json existe

# Prueba 2: Persistencia
6. Ejecuta el programa de nuevo
7. Verifica que las 2 tareas siguen ahí

# Prueba 3: Archivo corrupto
8. Abre tareas.json y escribe "corrupto"
9. Ejecuta el programa
10. Debería crear archivo nuevo sin crashear
```

**Anota resultados** en `test_persistencia.md`.

---

## 🎨 Parte 3: Mejora de UX con IA (30 min)

### Tarea 3.1: Mejorar la Interfaz

**Prompt**:

```
Mejora la interfaz de usuario de mi CLI de tareas:

Mejoras necesarias:
1. Colores en consola (rojo=error, verde=éxito, amarillo=info)
   - Usa códigos ANSI escape
   - Crea funciones: print_error, print_success, print_info

2. Formato de lista de tareas más visual:
   ```
   ═══════════════════════════════
          📋 MIS TAREAS
   ═══════════════════════════════
   [1] ✅ Comprar leche
   [2] ⬜ Estudiar Python
   ═══════════════════════════════
   ```

3. Confirmación antes de eliminar:
   "¿Seguro que quieres eliminar '[nombre]'? (s/n)"

Actualiza solo las funciones de UI, no toques GestorTareas ni RepositorioJSON.
```

---

## 📊 Parte 4: Comparación Antes/Después (15 min)

### Tarea 4.1: Análisis de Mejoras

Crea `REFACTORIZACION_CLASE2.md`:

```markdown
# Refactorización - Clase 2

## Código Inicial (Clase 1)
**Características**:
- Líneas de código: ___
- Funciones: ___
- Clases: ___
- Persistencia: ❌

**Problemas**:
1.
2.
3.

## Código Refactorizado (Clase 2)
**Características**:
- Líneas de código: ___
- Funciones: ___
- Clases: ___
- Persistencia: ✅ JSON

**Mejoras**:
1. Separación de responsabilidades (UI / Lógica / Datos)
2.
3.

## Métricas de Calidad

| Aspecto | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Mantenibilidad | 3/10 | 8/10 | +5 |
| Legibilidad | 5/10 | 9/10 | +4 |
| Testabilidad | 2/10 | 8/10 | +6 |
| Robustez | 4/10 | 8/10 | +4 |

## Lecciones sobre Refactorización con IA

**Lo que funcionó bien**:
-
-

**Lo que fue difícil**:
-
-

**Próximos pasos**:
-
-
```

---

## 🎯 Entregables

Al final de este ejercicio debes tener:

1. ✅ `tareas_refactorizado.py` - Código con separación de capas
2. ✅ `repositorio.py` - Clase RepositorioJSON
3. ✅ `analisis_codigo.md` - Análisis inicial
4. ✅ `diseno_persistencia.md` - Decisiones de diseño
5. ✅ `test_persistencia.md` - Pruebas de persistencia
6. ✅ `REFACTORIZACION_CLASE2.md` - Comparación antes/después
7. ✅ `tareas.json` - Archivo de datos generado

---

## 🎯 Criterios de Éxito

Has completado exitosamente si:

1. ✅ El código tiene 3 capas claramente separadas (UI, Lógica, Datos)
2. ✅ La persistencia JSON funciona correctamente
3. ✅ Maneja errores sin crashear (archivos corruptos, permisos, etc.)
4. ✅ La UI es más visual y amigable que la versión de Clase 1
5. ✅ Todas las funciones tienen type hints y docstrings
6. ✅ Entiendes por qué cada refactorización fue necesaria

---

## 💭 Reflexión Final (10 min)

Responde en `reflexion_clase2.md`:

```markdown
# Reflexión - Clase 2

## ¿Qué aprendí sobre refactorización con IA?

**Ventajas de refactorizar paso a paso**:
1.
2.

**Desafíos encontrados**:
1.
2.

## ¿Cuándo refactorizar?

**Señales de que el código necesita refactorización**:
-
-
-

**Cuándo NO refactorizar**:
-
-

## Comparación: Refactorizar manualmente vs con IA

**IA me ayudó a**:
1.
2.

**Yo aporté** (lo que la IA no puede hacer):
1.
2.

## Siguiente paso

En Clase 3 aprenderemos **testing con pytest**. Con código bien estructurado como este, ¡escribir tests será mucho más fácil!
```

---

## 🔗 Recursos Adicionales

- 📘 **Agentes Educacionales**:
  - Python Best Practices Coach: `.claude/agents/educational/python-best-practices-coach.md`
  - Clean Architecture Enforcer: `.claude/agents/educational/clean-architecture-enforcer.md`
- 📚 **PEP 8**: https://pep8.org
- 🎓 **Refactoring Catalog**: https://refactoring.com/catalog/
- 📖 **JSON en Python**: https://docs.python.org/3/library/json.html

---

**Tiempo estimado total**: 2.5 horas

**Siguiente clase**: Clase 3 - Clean Code y Testing (tests unitarios con pytest)
