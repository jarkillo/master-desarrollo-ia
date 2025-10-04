# 📖 Glosario - Clase 3

### **Clean Code**

Manera de escribir código que es claro, fácil de leer y mantener. La idea no es solo que el programa funcione, sino que **otro humano (o tú mismo en 6 meses)** pueda entenderlo sin sufrir.

**Nombres claros**

Dar a variables, funciones y constantes nombres que explican lo que hacen (`cargar_tareas` mejor que `ct()`). El nombre debe contar la historia.

**Funciones pequeñas (Single Responsibility)**

Cada función debe hacer una sola cosa. Si una función hace más de una acción distinta, se divide en varias. Así se entiende y se prueba mejor.

**Eliminar comentarios redundantes**

Un comentario que repite lo que ya se ve en el código sobra. Ejemplo: `# abrimos archivo en lectura` cuando el código dice `open("archivo", "r")`.

Los comentarios buenos son los que explican una decisión o un contexto, no lo obvio.

**Evitar duplicación (DRY: Don’t Repeat Yourself)**

Si copias el mismo bloque de código en varios sitios, conviene convertirlo en una función o constante. Así, si cambias algo, solo lo cambias en un sitio.

**Separación de capas**

Dividir el programa en partes con responsabilidades distintas:

- Lógica (agregar, completar, listar).
- Acceso a datos (guardar y cargar JSON).
- Interfaz (lo que imprime en pantalla o recibe de la terminal).

**Test unitario**

Un mini-programa que comprueba si una función concreta hace lo esperado. Por ejemplo: “si agrego una tarea, ¿la lista tiene 1 elemento más?”.

**unittest**

Librería de Python que viene de serie para escribir y ejecutar tests. Te da herramientas como `assertEqual`, `assertTrue`, `assertFalse`.

**assert**

Una afirmación en un test. Es como decir: *“asegúrate de que esto sea verdad”*.

Ejemplos:

- `assertEqual(x, 5)` → comprueba que `x` es 5.
- `assertTrue(condición)` → comprueba que condición es verdadera.
- `assertFalse(condición)` → comprueba que condición es falsa.

**setUp / tearDown**

Funciones especiales en los tests:

- `setUp` se ejecuta antes de cada prueba, para preparar el entorno.
- `tearDown` se ejecuta después, para limpiar (borrar archivos temporales, por ejemplo).

**Archivo temporal (`tempfile`)**

Un archivo que se crea solo para las pruebas y luego se borra, así no tocas tus datos reales.

**Refactor**

Cambiar el código para que sea más limpio o legible, **sin alterar su comportamiento**. Con los tests como red de seguridad, puedes refactorizar sin miedo.

**Código de salida (exit code)**

Número que devuelve un programa cuando termina:

- `0` → todo bien.
- `1` o más → error.
    
    Esto se usa mucho en scripts y CI/CD.