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

---

## Términos de Arquitectura y Estructura de Proyectos

**Separation of Concerns (Separación de responsabilidades)**

Principio de diseño: cada parte del código se ocupa de UNA cosa específica.

Ejemplo:
- `cli.py` → Solo interfaz CLI
- `servicio.py` → Solo lógica de negocio
- `persistencia.py` → Solo lectura/escritura JSON

**Beneficio**: Si cambias JSON por DB, solo tocas `persistencia.py`.

**Clean Architecture Enforcer**

Agente educativo de IA que valida si tu código sigue principios de arquitectura limpia (capas separadas, dependency inversion, single responsibility).

**Uso**: Pides al agente que revise tu estructura de proyecto y te da feedback educativo.

**Antipatrón (Anti-pattern)**

Forma común de resolver un problema que parece buena pero causa más problemas después.

Ejemplos:
- **God Object**: Un archivo/clase que hace TODO (800 líneas mezclando CLI, lógica, persistencia)
- **Nombres genéricos**: `utils.py`, `helpers.py`, `manager.py` (no dice qué hace)
- **Tests mezclados**: Tests en la misma carpeta que código productivo

**God Object / God Class**

Antipatrón: Un archivo o clase que tiene demasiadas responsabilidades (hace de todo).

Problema: Si algo falla, no sabes dónde buscar. Difícil de testear y mantener.

Ejemplo ❌:
```
tareas.py  # 800 líneas: CLI + lógica + JSON + validaciones + emails
```

Solución ✅:
```
cli.py           # Solo interfaz
servicio.py      # Solo lógica
persistencia.py  # Solo JSON
```

**YAGNI (You Ain't Gonna Need It)**

Principio de diseño: "No vas a necesitarlo (aún)".

Significa: No agregues carpetas, clases o código "por si acaso lo necesitas después". Solo crea lo que necesitas HOY.

Ejemplo:
- Proyecto pequeño (150 líneas) → No necesitas carpeta `src/`
- Solo usas JSON → No necesitas `database/` ni `migrations/`

**Estructura plana vs. Estructura con carpetas**

**Estructura plana**: Todos los archivos en la raíz (OK para proyectos pequeños <200 líneas)
```
proyecto/
├── tareas.py
├── cli.py
└── test_tareas.py
```

**Estructura con carpetas**: Código organizado en carpetas (mejor para proyectos medianos/grandes)
```
proyecto/
├── src/
│   ├── tareas.py
│   └── cli.py
└── tests/
    └── test_tareas.py
```

**Decisión**: Depende del tamaño del proyecto y si planeas que crezca.

**Dependency Inversion (Inversión de dependencias)**

Principio SOLID: Las capas de alto nivel no deben depender de detalles de bajo nivel.

Ejemplo simple:
- ❌ `servicio.py` importa y usa `RepositorioJSON` directamente (acoplado a JSON)
- ✅ `servicio.py` usa una abstracción `Repositorio` (puede ser JSON, DB, memoria)

**Beneficio**: Puedes cambiar de JSON a DB sin tocar la lógica de negocio.

**Single Responsibility Principle (SRP)**

Principio SOLID: Cada clase/función/archivo debe tener UNA sola razón para cambiar.

Ejemplo:
- ❌ `ServicioTareas` hace: CRUD + estadísticas + exports + emails (4 responsabilidades)
- ✅ `ServicioTareas` solo hace CRUD
- ✅ `ServicioEstadisticas` solo hace analytics
- ✅ `ServicioExportacion` solo hace exports

**Clean Architecture (Arquitectura Limpia)**

Estilo de arquitectura que organiza código en capas independientes:

1. **Interfaz** (CLI, API) → Habla con el usuario
2. **Lógica de negocio** (Servicios) → Reglas del dominio
3. **Persistencia** (Repositorios) → Guarda/lee datos

**Regla clave**: Las capas internas (lógica) NO conocen las externas (CLI, API).