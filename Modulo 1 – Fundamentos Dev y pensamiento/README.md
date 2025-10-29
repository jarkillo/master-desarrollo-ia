# Módulo 1 - Fundamentos Dev y Pensamiento

## Overview

Este módulo introduce los **fundamentos del desarrollo de software** y el **pensamiento computacional**, estableciendo las bases para el desarrollo asistido por IA. Los estudiantes aprenderán a construir aplicaciones CLI en Python, implementar tests, y aplicar principios de código limpio desde el inicio.

**Visión del módulo**: Transformar el pensamiento humano en código funcional, usando IA como asistente para acelerar el aprendizaje y la productividad.

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

1. **Pensar computacionalmente**: Descomponer problemas, identificar patrones, diseñar algoritmos
2. **Construir aplicaciones CLI**: Crear programas de línea de comandos funcionales en Python
3. **Aplicar Clean Code**: Escribir código legible, mantenible y siguiendo convenciones PEP 8
4. **Implementar testing**: Crear tests unitarios con pytest, entender TDD básico
5. **Usar IA efectivamente**: Aprovechar asistentes de IA para aprender y desarrollar más rápido
6. **Aplicar principios SOLID iniciales**: Introducción a SRP (Single Responsibility Principle)

## Prerrequisitos

- Conocimientos básicos de programación (variables, condicionales, bucles)
- Python 3.12+ instalado
- Editor de código (VS Code recomendado)
- Cuenta de GitHub
- Acceso a Claude Code o similar

## Estructura del Módulo

### Clase 1 - Pensamiento Computacional y Ecosistema Dev
**Duración**: 3h | **Tipo**: Fundamentos + Práctica

**Contenido**:
- Pensamiento computacional: descomposición, patrones, abstracción
- Ecosistema de desarrollo: Git, terminal, entorno virtual
- Primera aplicación CLI: gestor de tareas simple
- Uso de IA para acelerar el desarrollo

**Proyecto**: CLI de tareas con almacenamiento en memoria
- `cli-tareas/tareas.py` - Versión básica
- `cli-tareas-json/tareas-json.py` - Versión con persistencia JSON

**Artefactos**:
- `Glosario - Clase 1.md` - Términos clave
- `COMPARACION.md` - Comparación código manual vs asistido por IA
- `prompts_usados.md` - Prompts efectivos utilizados

### Clase 2 - Fundamentos de Programación
**Duración**: 3h | **Tipo**: Teoría + Práctica

**Contenido**:
- Tipos de datos y estructuras (listas, diccionarios)
- Funciones y modularización
- Manejo de archivos (JSON)
- Convenciones de código (PEP 8)

**Proyecto**: Refactorización del CLI de tareas
- Separación de responsabilidades
- Funciones reutilizables
- Validación de entrada

**Artefactos**:
- `Clase 2 – Fundamentos de programación.md` - Material teórico
- `Glosario - Clase 2.md` - Términos técnicos
- `notes.md` - Notas de clase

### Clase 3 - Clean Code y Testing Inicial
**Duración**: 3h | **Tipo**: Principios + Testing

**Contenido**:
- Principios de Clean Code (nombres, funciones, comentarios)
- Introducción a pytest
- Tests unitarios básicos
- Refactorización guiada por tests

**Proyecto**: CLI con tests unitarios
- `cli-tareas/tareas.py` - Código limpio y testeado
- `test_tareas_clase3.py` - Suite de tests completa

**Artefactos**:
- `Clase 3 – Clean Code y testing inicial.md` - Material teórico
- `Glosario - Clase 3.md` - Términos de testing
- `ejercicio_clase3_ai.md` - Ejercicio práctico con IA

### Clase 4 - Testing Ampliado y Primeros Principios SOLID
**Duración**: 3h | **Tipo**: Testing Avanzado + Arquitectura

**Contenido**:
- Testing avanzado con pytest (fixtures, parametrize)
- Cobertura de código
- Introducción a SOLID: SRP (Single Responsibility Principle)
- Separación de lógica de negocio y presentación

**Proyecto**: CLI con arquitectura mejorada
- Separación de capas (presentación, lógica, datos)
- Tests parametrizados para casos complejos
- Introducción a prioridades en tareas

**Artefactos**:
- `Clase 4 – Testing ampliado y primeros principios SOLID.md` - Material teórico
- `Glosario - Clase 4.md` - Términos de arquitectura
- `ejercicio_clase4_ai_avanzado.md` - Ejercicio de refactorización con IA

## Tecnologías Utilizadas

- **Python 3.12+**: Lenguaje principal
- **pytest 8.4.2**: Framework de testing
- **JSON**: Persistencia de datos simple
- **Git**: Control de versiones
- **Claude Code** (o similar): Asistente de IA

## Cómo Ejecutar los Proyectos

### Configuración inicial (una vez)

```bash
# Clonar el repositorio
git clone <url-repositorio>
cd master-ia-manu

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar una aplicación CLI

```bash
# Navegar a la clase específica
cd "Modulo 1 – Fundamentos Dev y pensamiento/Clase 1 - Pensamiento computacional y ecosistema dev/cli-tareas"

# Ejecutar la aplicación
python tareas.py
```

### Ejecutar tests

```bash
# Desde el directorio de una clase
cd "Modulo 1 – Fundamentos Dev y pensamiento/Clase 3 – Clean Code y testing inicial"

# Ejecutar tests
pytest -v

# Con cobertura
pytest --cov=. --cov-report=term-missing
```

## Progresión del Aprendizaje

Este módulo sigue una **progresión incremental**:

1. **Clase 1**: Construyes tu primera aplicación (pensamiento → código)
2. **Clase 2**: Refactorizas con mejores prácticas (código funcional → código limpio)
3. **Clase 3**: Añades tests para validar (código limpio → código confiable)
4. **Clase 4**: Aplicas arquitectura inicial (código confiable → código mantenible)

Cada clase **reutiliza y mejora** el código de la anterior, experimentando la evolución natural del software.

## Filosofía Pedagógica

**"Sentir el dolor antes de la solución"**

- Primero escribes código simple (y sientes las limitaciones)
- Luego refactorizas con principios (y entiendes por qué son necesarios)
- Los tests aparecen cuando necesitas confianza en los cambios
- La arquitectura surge cuando el código se vuelve difícil de mantener

**IA como acelerador, no como reemplazo**

- Usas IA para escribir código más rápido
- Pero entiendes cada línea que genera
- Los prompts efectivos vienen de entender qué necesitas
- La revisión crítica es tu responsabilidad

## Recursos Adicionales

- **Glosarios**: Cada clase tiene su glosario de términos técnicos
- **Prompts efectivos**: `prompts_usados.md` documenta prompts exitosos
- **Ejercicios con IA**: Ejercicios diseñados para practicar con asistentes
- **Comparaciones**: Código manual vs asistido para entender el valor de la IA

## Próximos Pasos

Después de completar este módulo:

➡️ **Módulo 2 - Arquitectura + Agent Orchestration**: Aprenderás FastAPI, arquitectura limpia, y patrones SOLID completos.

## Problemas Conocidos

- Los archivos JSON se crean en el directorio de ejecución (no hay gestión de rutas)
- No hay manejo robusto de errores en las primeras clases (se introduce progresivamente)
- El código de Clase 1-2 es intencionalmente simple (complejidad crece gradualmente)

## Contribuciones

Si encuentras errores o mejoras:

1. Crea un issue en el repositorio
2. Describe el problema con capturas/código
3. Sugiere la solución si es posible

---

**¿Listo para empezar?** Ve a [Clase 1 - Pensamiento computacional y ecosistema dev](./Clase%201%20-%20Pensamiento%20computacional%20y%20ecosistema%20dev/Clase%201%20-%20Pensamiento%20computacional%20y%20ecosistema%20dev.md) 🚀
