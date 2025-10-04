# 🧭 Glosario – Clase 2

**SOLID** → conjunto de 5 principios de diseño para mantener el código claro, escalable y fácil de mantener:

- **S**ingle Responsibility Principle (SRP): cada módulo o clase debe tener un motivo único para cambiar.
- **O**pen/Closed: abierto a extenderse, cerrado a romperse.
- **L**iskov Substitution: si algo se comporta como un tipo, debe poder reemplazarlo sin errores.
- **I**nterface Segregation: mejor varias interfaces pequeñas que una enorme.
- **D**ependency Inversion: depender de abstracciones, no de implementaciones concretas.

**Paradigmas de programación** → formas distintas de pensar el código:

- **Imperativo:** dices *cómo* hacerlo paso a paso.
- **Orientado a objetos:** modelas entidades con clases.
- **Funcional:** transformas datos con funciones puras.
    
    Python puede combinar los tres.
    

**TDD (Test Driven Development)** → desarrollo guiado por tests.

1. Escribes un test que falla (**Red**)
2. Escribes el código mínimo para hacerlo pasar (**Green**)
3. Limpias y refactorizas (**Refactor**)

**Historia de usuario** → descripción breve de una necesidad:

> “Como usuario quiero crear tareas vía API para gestionarlas desde apps externas.”
> 

**Contrato** → lo que el test exige que la API cumpla. Si el comportamiento cambia, el test falla.

**FastAPI** → framework ligero de Python para crear APIs rápidas y con validación automática mediante *Pydantic*.

**Pydantic BaseModel** → define cómo debe lucir el cuerpo de una petición (qué campos, tipos, validaciones).

**Field(..., min_length=1)** → regla de validación: el campo no puede estar vacío.

**status_code=201** → código HTTP que significa “creado con éxito”.

**pytest** → herramienta para ejecutar tests automáticamente y mostrar qué pasa.

**TestClient** → cliente HTTP de FastAPI para probar endpoints sin lanzar el servidor real.

**`__init__.py`** → archivo (puede estar vacío) que le dice a Python que una carpeta es un paquete importable.

**`conftest.py`** → archivo que configura pytest antes de ejecutar los tests; aquí usamos uno para arreglar las rutas de importación.

**`sys.path`** → lista interna de rutas donde Python busca módulos.

`sys.path.insert(0, str(raiz_proyecto))` → añade la carpeta raíz del proyecto a esa lista para que los imports funcionen.

**Entorno virtual (`venv`)** → sandbox que guarda las dependencias de tu proyecto sin ensuciar tu instalación global de Python.

**requirements.txt** → lista de librerías instaladas (y sus versiones) en tu entorno virtual.

**SRP aplicado** → en esta clase:

- El test comprueba solo el contrato.
- El endpoint crea solo una tarea.
- El modelo valida solo los datos.