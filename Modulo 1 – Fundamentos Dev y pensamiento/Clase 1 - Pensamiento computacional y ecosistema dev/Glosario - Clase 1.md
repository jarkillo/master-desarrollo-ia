# 📖 Glosario – Clase 1

**Pensamiento computacional**

Forma de razonar como un programador: descomponer problemas, encontrar patrones, abstraer lo irrelevante y definir algoritmos (secuencia de pasos).

**CLI (Command Line Interface)**

Aplicación que se maneja desde la terminal, escribiendo comandos en lugar de usar botones gráficos.

**`sys.argv`**

Lista en Python que contiene los argumentos pasados al ejecutar un script.

Ejemplo: `python tareas.py listar` → `sys.argv = ["tareas.py", "listar"]`.

**Argumento**

Dato que pasas a un programa desde la línea de comandos. Sirve para indicar qué quieres que haga.

Ej: `listar`, `agregar`.

**Esqueleto**

Versión mínima de un programa que no resuelve el problema completo, pero ya marca la estructura básica.

**JSON (JavaScript Object Notation)**

Formato de texto ligero para almacenar y compartir datos. En este caso, lo usamos para guardar la lista de tareas.

**Persistencia**

Capacidad de un programa de guardar información en disco (por ejemplo en un archivo `.json`) para que siga disponible al cerrar el programa.

**`argparse`**

Módulo de Python que facilita la gestión de argumentos y comandos en una CLI. Es la versión “pro” de `sys.argv`.

**Historia de usuario**

Forma simple de expresar un requisito desde la perspectiva del usuario:

*“Como [usuario], quiero [acción] para [beneficio]”.*

**Gherkin**

Lenguaje estructurado para describir comportamientos de software mediante escenarios:

`Given` (dado), `When` (cuando), `Then` (entonces).

**TDD (Test Driven Development)**

Metodología de desarrollo basada en escribir primero los tests, luego el código mínimo para que pasen, y finalmente refactorizar. Ciclo: **Red → Green → Refactor**.

---

## 🤖 Términos de IA y Desarrollo Asistido

**AI-Assisted Development**

Desarrollo de software donde la IA actúa como copiloto (no piloto automático). El desarrollador mantiene el control y responsabilidad del código, pero usa IA para acelerar tareas repetitivas, explorar soluciones, y aprender patrones.

**Prompt Engineering**

Arte y ciencia de comunicarse efectivamente con modelos de IA para obtener resultados óptimos. Incluye especificar contexto, constraints, formato de output, y ejemplos. Un prompt bien diseñado marca la diferencia entre código genérico y código útil.

**Refactoring**

Proceso de mejorar la estructura interna del código sin cambiar su comportamiento externo. Objetivos: mejor legibilidad, mantenibilidad, reducción de duplicación, adherencia a principios como SOLID.

**Code Review**

Práctica de revisar código (propio o ajeno, manual o generado por IA) antes de integrarlo. Busca bugs, violaciones de estándares, oportunidades de mejora. Crítico cuando trabajas con código generado por IA: SIEMPRE revisa antes de usar.

**Boilerplate Code**

Código repetitivo y predecible necesario para que algo funcione, pero que no aporta lógica de negocio. Ejemplo: imports, configuración de logging, estructura básica de funciones. Ideal para generar con IA porque es estandarizado.

**Edge Cases**

Casos extremos o inusuales que el código debe manejar correctamente. Ejemplos: input vacío, None, valores negativos, strings con caracteres especiales. La IA suele ser buena detectando edge cases que no consideraste.