# Ejercicio Clase 1: Primera Aplicación CLI con Asistencia de IA

## 🎯 Objetivos

1. **Usar IA como copiloto** para escribir tu primera aplicación Python
2. **Comparar código manual vs asistido por IA** (velocidad, calidad, aprendizaje)
3. **Aprender a validar código generado** por IA (no aceptar ciegamente)
4. **Dominar prompts efectivos** para obtener mejores resultados

---

## 📋 Pre-requisitos

Antes de empezar:

1. **Python 3.12+ instalado** y funcionando
2. **Editor configurado** (VS Code recomendado)
3. **Acceso a Claude Code** u otro asistente de IA
4. **Terminal abierta** en la carpeta de tu proyecto

---

## 🚀 Parte 1: Tu Primera App - Manualmente (30 min)

### Tarea 1.1: Construir CLI de Tareas SIN IA

**Objetivo**: Experimentar el proceso "tradicional" para comparar luego.

**Requisitos**:
- Crear `tareas_manual.py`
- Funciones: agregar, listar, eliminar tareas
- Almacenamiento en memoria (lista Python)
- Menú interactivo con input()

**Instrucciones**:

```python
# tareas_manual.py - Escribe esto TÚ MISMO, sin IA

tareas = []

def mostrar_menu():
    # Tu código aquí
    pass

def agregar_tarea():
    # Tu código aquí
    pass

def listar_tareas():
    # Tu código aquí
    pass

def main():
    # Tu código aquí
    pass

if __name__ == "__main__":
    main()
```

**Anota en `notes.md`**:
- ⏱️ Tiempo que te tomó: _____ minutos
- 🤔 Dudas que tuviste (sintaxis, estructura, etc.)
- ❌ Errores que encontraste al ejecutar
- ✅ Qué funcionó bien

---

## 🤖 Parte 2: Tu Segunda App - Con IA (20 min)

### Tarea 2.1: Construir CLI de Tareas CON IA

**Objetivo**: Usar IA para acelerar y aprender nuevos patrones.

**Prompt efectivo** (copia esto en Claude Code):

```
Necesito crear una aplicación CLI en Python para gestionar tareas.

Requisitos:
- Menú interactivo con opciones: agregar, listar, completar, eliminar
- Almacenar tareas en memoria (lista de diccionarios)
- Cada tarea tiene: id (autoincremental), nombre, completada (bool)
- Validar input del usuario (no vacío)
- Opción para salir del programa

Restricciones:
- Python puro (sin librerías externas)
- Código limpio con funciones separadas
- Docstrings en cada función
- Variables con nombres descriptivos

Formato esperado:
```python
# tareas_ia.py
# Código generado aquí
```

Explícame las decisiones de diseño que tomaste.
```

**Instrucciones**:

1. **Copia el prompt** en tu asistente de IA
2. **Lee el código generado** línea por línea
3. **Pregunta sobre partes que no entiendas**:
   ```
   ¿Por qué usaste enumerate() aquí?
   ¿Qué hace el if __name__ == "__main__"?
   ```
4. **Ejecuta el código** y prueba todas las opciones
5. **Pide mejoras** si encuentras bugs:
   ```
   Cuando ingreso una tarea vacía, el programa crashea. ¿Puedes agregar validación?
   ```

**Anota en `notes.md`**:
- ⏱️ Tiempo que te tomó: _____ minutos
- 📚 Nuevos conceptos que aprendiste (enumerate, docstrings, etc.)
- ✨ Qué te sorprendió del código generado
- 🐛 Errores que la IA cometió (si los hubo)

---

## 🔍 Parte 3: Comparación Manual vs IA (15 min)

### Tarea 3.1: Análisis de Diferencias

Crea una tabla en `COMPARACION_CLASE1.md`:

```markdown
# Comparación: Manual vs IA

## Métricas

| Aspecto | Manual | Con IA | Ganador |
|---------|--------|--------|---------|
| Tiempo de desarrollo | ___ min | ___ min | _____ |
| Líneas de código | ___ | ___ | _____ |
| Funciones creadas | ___ | ___ | _____ |
| Complejidad (1-10) | ___ | ___ | _____ |
| Bugs encontrados | ___ | ___ | _____ |

## Calidad del Código

**Manual**:
- ✅ Fortalezas:
- ❌ Debilidades:

**Con IA**:
- ✅ Fortalezas:
- ❌ Debilidades:

## Aprendizaje

**¿Qué aprendí usando IA que no sabía antes?**
1.
2.
3.

**¿Qué errores cometió la IA?**
1.
2.
```

---

## 💡 Parte 4: Prompts Efectivos (20 min)

### Tarea 4.1: Experimentar con Variaciones de Prompts

Prueba estos 3 prompts y compara resultados:

**Prompt Vago** ❌:
```
Haz un programa de tareas en Python
```

**Prompt Específico** ✅:
```
Crea un CLI de gestión de tareas en Python con:
- Menú interactivo
- Funciones: agregar, listar, completar, eliminar
- Persistencia en memoria (lista)
- Validación de entrada
- Código comentado
```

**Prompt Detallado con Contexto** ✅✅:
```
Contexto: Soy estudiante de un máster en IA Development. Esta es mi primera app Python.

Tarea: Crear un CLI de gestión de tareas con estas características:

Funcionalidad:
- Agregar tarea (nombre obligatorio, mínimo 3 caracteres)
- Listar tareas (mostrar id, nombre, estado completada)
- Completar tarea (por id)
- Eliminar tarea (por id)
- Salir

Restricciones técnicas:
- Python 3.12 puro (sin librerías externas)
- Almacenamiento en memoria (lista de diccionarios)
- Validación robusta de input
- Manejo de errores (try/except)

Formato del código:
- Docstrings en funciones
- Type hints básicos
- Nombres descriptivos (snake_case)
- Separación clara de responsabilidades

Por favor, explica las decisiones de diseño importantes.
```

**Anota en `prompts_clase1.md`**:

```markdown
# Comparación de Prompts - Clase 1

## Prompt Vago
**Resultado**: [Describe qué generó]
**Problemas**: [Qué faltó]

## Prompt Específico
**Resultado**: [Describe qué generó]
**Mejoras**: [Qué mejoró vs anterior]

## Prompt Detallado
**Resultado**: [Describe qué generó]
**Calidad**: [Por qué este es mejor]

## Lecciones Aprendidas
1. Siempre incluir...
2. Nunca olvidar...
3. Los prompts efectivos tienen...
```

---

## 🎓 Parte 5: Validación Crítica del Código IA (15 min)

### Tarea 5.1: Checklist de Validación

**Objetivo**: Aprender a NO confiar ciegamente en IA.

Revisa el código generado con esta lista:

```markdown
# Checklist de Validación de Código IA

## Funcionalidad ✅/❌
- [ ] ¿El programa ejecuta sin errores?
- [ ] ¿Todas las funciones hacen lo que prometen?
- [ ] ¿Maneja correctamente inputs inválidos?
- [ ] ¿Tiene casos edge (lista vacía, ids inexistentes)?

## Calidad de Código ✅/❌
- [ ] ¿Los nombres de variables son claros?
- [ ] ¿Las funciones son pequeñas y enfocadas?
- [ ] ¿Tiene comentarios donde es necesario?
- [ ] ¿Evita código duplicado?

## Seguridad Básica ✅/❌
- [ ] ¿Valida input del usuario?
- [ ] ¿Maneja excepciones apropiadamente?
- [ ] ¿No crashea con inputs inesperados?

## Aprendizaje ✅/❌
- [ ] ¿Entiendo cada línea de código?
- [ ] ¿Puedo explicar por qué funciona?
- [ ] ¿Podría modificarlo sin romperlo?
```

**Ejercicio práctico**:

1. Toma el código generado por IA
2. Intenta romperlo:
   - Ingresa strings vacíos
   - Usa ids negativos
   - Presiona Enter sin escribir
3. **Anota qué falló** en `bugs_encontrados.md`
4. **Pide a la IA que lo arregle**:
   ```
   Encontré un bug: cuando ingreso un id que no existe, el programa crashea.
   ¿Puedes agregar validación?
   ```

---

## 📊 Entregables

Al final de este ejercicio debes tener:

1. ✅ `tareas_manual.py` - Tu versión sin IA
2. ✅ `tareas_ia.py` - Versión generada con IA
3. ✅ `COMPARACION_CLASE1.md` - Análisis de diferencias
4. ✅ `prompts_clase1.md` - Comparación de prompts
5. ✅ `bugs_encontrados.md` - Bugs detectados y cómo se arreglaron
6. ✅ `notes.md` - Reflexiones y aprendizajes

---

## 🎯 Criterios de Éxito

Has completado este ejercicio exitosamente si:

1. ✅ Tienes ambas versiones funcionando (manual e IA)
2. ✅ Entiendes las diferencias entre los enfoques
3. ✅ Puedes explicar cada línea del código generado por IA
4. ✅ Identificaste al menos 2 mejoras que la IA hizo vs tu código manual
5. ✅ Encontraste al menos 1 error o limitación en el código de IA
6. ✅ Escribiste un prompt detallado que genera código de calidad

---

## 💭 Reflexión Final (10 min)

Responde en `reflexion_clase1.md`:

```markdown
# Reflexión - Clase 1

## ¿Qué aprendí sobre usar IA para programar?

1. **Ventajas**:
   -
   -

2. **Limitaciones**:
   -
   -

3. **Cuándo usar IA**:
   -
   -

4. **Cuándo NO usar IA**:
   -
   -

## ¿Cómo cambió mi forma de pensar sobre programación?

[Tu respuesta aquí]

## Siguiente paso: ¿Qué quiero aprender sobre IA + código?

[Tu respuesta aquí]
```

---

## 🔗 Recursos Adicionales

- 📘 **Guía de Prompts Efectivos**: `prompts_usados.md`
- 🤖 **Agentes Educacionales**: Ver `.claude/agents/educational/`
- 📚 **PEP 8 Style Guide**: https://pep8.org
- 🎓 **Módulo 0**: Si no hiciste el Módulo 0, revísalo para fundamentos de IA

---

**Tiempo estimado total**: 2 horas

**Siguiente clase**: Clase 2 - Fundamentos de programación (refactorización con IA)
