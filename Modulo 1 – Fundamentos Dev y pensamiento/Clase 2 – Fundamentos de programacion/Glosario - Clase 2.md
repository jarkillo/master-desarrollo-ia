# Glosario - Clase 2

### Glosario

- **Estructuras de control**: piezas del lenguaje que permiten cambiar el flujo del programa según condiciones (`if/elif/else`) o repetir bloques (`for`, `while`).
- **Función**: bloque de código con un nombre propio que puede recibir parámetros y devolver resultados. Permite dividir un programa en piezas pequeñas, fáciles de mantener y reutilizar.
- **Persistencia**: capacidad de un programa de guardar datos para que sigan existiendo después de cerrarlo. Aquí lo hacemos con archivos JSON.
- **JSON (JavaScript Object Notation)**: formato de texto ligero para almacenar y transmitir datos estructurados en pares clave–valor. Ejemplo:
    
    ```json
    [{"id": 1, "nombre": "Estudiar IA", "completada": false}]
    
    ```
    
- **`sys.argv`**: lista de Python con los argumentos que pasamos en la terminal. Ejemplo:
    
    `python tareas.py agregar "estudiar"` → `sys.argv = ["tareas.py", "agregar", "estudiar"]`.
    
- **`argparse`**: librería estándar de Python para crear interfaces de línea de comandos más robustas, con subcomandos, validación automática y mensajes de ayuda.
- **Subcomando**: palabra clave dentro de un CLI que representa una acción. Ejemplo: `listar`, `agregar`, `completar`.
- **Parámetro / argumento**: valores que el usuario pasa a un comando o subcomando. Ejemplo: `python tareas.py agregar "estudiar Git"` → `"estudiar Git"` es un argumento.
- **ID incremental**: número único que identifica a cada tarea. Se genera de forma automática (ej. `max(id)+1`).
- **Flujo Entrada–Procesamiento–Salida**: esquema básico de todo programa:
    1. **Entrada** (lo que el usuario escribe en terminal).
    2. **Procesamiento** (la lógica del programa).
    3. **Salida** (lo que el programa imprime o guarda).
- **Capa de acceso a datos (I/O)**: funciones dedicadas a leer y escribir en archivos. Separarlas evita mezclar la lógica del negocio con detalles técnicos.
- **CLI (Command Line Interface)**: interfaz de un programa que funciona en la terminal, en lugar de un entorno gráfico.
- **Workflow con Git**: flujo de trabajo con ramas y PRs (Pull Requests). Ejemplo:
    - `feature/cli-json` → versión manual.
    - `feature/cli-argparse` → versión refactorizada con IA.