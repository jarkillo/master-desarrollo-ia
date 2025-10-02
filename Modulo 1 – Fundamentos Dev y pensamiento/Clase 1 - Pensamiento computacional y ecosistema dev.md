# Modulo 1 - Fundamentos del desarrollo – Pensamiento

Ya tienes hecha la **Clase 0 – Introducción** (configuración, Git, primer PR y merge). Ahora toca la **Clase 1 del Módulo 1**: **Fundamentos del desarrollo – Pensamiento computacional y ecosistema dev**.

Para que quede claro el salto:

- **Clase 0**: dejar tu entorno listo y entender el flujo Git básico (repos, ramas, PRs, merge/rebase).
- **Clase 1**: empezar con lo que hace a un dev de verdad → descomponer problemas (pensamiento computacional), usar bien la terminal y seguir practicando Git con un proyecto mínimo.

Te propongo esta estructura para la segunda clase:

---

# Clase 1 – Pensamiento computacional y ecosistema dev

### Concepto

Un dev no piensa en “el programa entero”, sino en piezas pequeñas.

El **pensamiento computacional** es descomponer un problema grande en pasos simples que un ordenador pueda ejecutar:

- **Descomposición** → dividir en partes.
- **Reconocimiento de patrones** → detectar lo que se repite.
- **Abstracción** → ignorar lo irrelevante.
- **Algoritmos** → definir pasos concretos.

Ejemplo: “Quiero una app CLI que gestione tareas”

1. Añadir tarea.
2. Listar tareas.
3. Marcar como completada.
4. Guardar en un archivo JSON.

Ya tenemos un esquema mínimo para programar.

### Aplicación manual

- Crea una rama feature/tareas-app
- Crea en tu repo una carpeta `Modulo1/cli-tareas` *(Si lo prefieres puedes crear un repo para la aplicación e ir mejorandola a medida que avanzas el curso)*.

### 1. Pensamiento computacional aplicado al mini-proyecto

Queremos una **app de línea de comandos (CLI)** que gestione tareas.

Problema grande: *“quiero un gestor de tareas”*. (Esto es lo que pensaría un muggle)

Lo bajamos a pasos pequeños:

1. **Entrada** → el usuario escribe un comando (`agregar`, `listar`, `completar`).
2. **Procesamiento** → el programa interpreta qué comando es.
3. **Salida** → el programa responde (mostrar lista, añadir algo, marcar hecho).

Hasta aquí ni hemos escrito código, solo descompusimos el problema.

### 2. Manual (cómo lo haría un dev sin IA)

Primero pruebo el esqueleto más simple posible:

- Si escribo `python tareas.py listar`, quiero que me diga “Aquí se mostrarían las tareas”.
- Si escribo `python tareas.py agregar`, quiero que me diga “Aquí se agregaría una tarea”.
- Si escribo `python tareas.py completar` , quiero que me diga “Aquí se completaría una tarea”.

Eso se hace con un programa que mire los **argumentos de la terminal**.

En Python, esos argumentos se leen con `sys.argv`, que es una lista con lo que escribiste después de `python`.

Por ejemplo:

```bash
python tareas.py listar

```

→ `sys.argv` será `["tareas.py", "listar"]`.

Con esa lógica, el programa puede decidir qué hacer según el segundo elemento.

### 3. Código mínimo explicado

```python
import sys   # sys nos da acceso a los argumentos de la terminal

# Si el usuario no puso nada más después de "python tareas.py"
# Si hay menos de dos argumentos (El primero es el nombre del programa):
if len(sys.argv) < 2:
    print("Uso: python tareas.py <comando>") # Imprimimos en pantalla el mensaje

# En caso contrario:
else:
		# Creamos la variable comando y metemos dentro el argumento.
    comando = sys.argv[1]  # el segundo argumento: listar, agregar, etc.
    
    # Ojo, es sys.argv[1] porque en python empezamos desde el 0, es decir,
    # el primer argumento sería el [0] = tareas.py
    # el segundo argumento sería el [1] = listar / agregar / completar

		# Si el comando es listar
    if comando == "listar":
        print("Aquí se mostrarían las tareas") # Imprimimos el mensaje
    
    # Si es agregar
    elif comando == "agregar":
        print("Aquí se agregaría una tarea") # Imprimimos el mensaje
    
    # si es completar
    elif comando == "completar":
		    print("Aquí se completaría una tarea") # Imprimimos el mensaje
    
    # En caso contrario
    else:
        print("Comando no reconocido") # Avisamos del error

```

Con esto **no hacemos nada útil todavía**, pero ya tenemos un esqueleto.

Es como construir primero el chasis de un coche antes de meterle motor.

### 4. Aplicación con IA

Una vez que este esqueleto corre, puedes pedirle a la IA que lo amplíe.

Ejemplo de prompt:

```
Rol: Dev Python senior.
Tarea: Tengo un script CLI que recibe comandos agregar, listar y completar. Quiero que las tareas se guarden en un archivo JSON.
Formato: Dame el código base limpio y con comentarios.
```

La IA te dará un código más gordo con lectura/escritura en JSON.

Tú decides si aceptar todo, o copiar solo lo que entiendes.

Luego revisas y refactorizas tú, aplicando lo que vimos en Git (rama `feature/cli-tareas`, commit, PR, merge).

---

👉 Ejercicio de la clase:

1. Crea la carpeta `Modulo1/cli-tareas`.
2. Añade el `tareas.py` mínimo como el ejemplo.
3. Haz commit en una rama `feature/cli-tareas`.
4. Abre un PR y mergea.
5. Escribe un primer prompt para ampliar el script con JSON (guarda la conversación en `Modulo1/cli-tareas/notes.md`). (Esto es el resultado basico, luego iremos mejorando el mismo resultado con prompts mejores)

---

## ¡¡¡ Nota importante !!!

Si ya has usado la IA alguna vez para programar, te darás cuenta de varios aspectos:

- No hemos dicho que IA usar (spoiler: la que quieras)
- Estamos dando prompts muy genéricos, lo sabemos

Esto lo hacemos para no robarte el aprendizaje.

Cuando construyamos nuestra **CLI de tareas**, lo vamos a formalizar con **historias de usuario (si no sabes lo que es, no te preocupes, lo explicaremos más adelante)**:

Ejemplos de historias de usuario (para que lo veas por encima)

- *Como usuario quiero agregar tareas para no olvidarlas.*
- *Como usuario quiero listarlas para saber qué tengo pendiente.*
- *Como usuario quiero marcarlas como completadas para sentirme productivo.*

Ese formato de “**Como… quiero… para…**” funciona de maravilla en proyectos de desarrollo, pero mejor aún funciona con la IA.

Luego, para que el código sea verificable, pasamos esas historias a **escenarios Gherkin (también se explicará más adelante)**:

```gherkin
Feature: Gestión de tareas

  Scenario: Agregar una nueva tarea
    Given no tengo tareas
    When agrego la tarea "Estudiar Git"
    Then la lista de tareas debe contener "Estudiar Git"

  Scenario: Listar tareas existentes
    Given tengo una tarea "Estudiar Git"
    When ejecuto listar
    Then debo ver "Estudiar Git" en la salida

  Scenario: Completar tareas existentes
    Given He terminado la tarea "Estudiar Git"
    When ejecuto completar
    Then debo ver "Estudiar Git" completada y sentirme productivo

```

Esto no es solo documentación: sirve para automatizar tests con frameworks como **pytest-bdd** en Python o **cucumber** en otros lenguajes. (Si te suena a Chino, no te agobies)

---

### Y cómo encaja la IA

Una vez que tienes historias + escenarios, los *prompts* cambian de “dame un CLI” a:

```
Rol: Dev Python senior con experiencia en BDD.
Tarea: Implementa el código mínimo en Python para que este escenario Gherkin pase:
Given no tengo tareas
When agrego la tarea "Estudiar Git"
Then la lista de tareas debe contener "Estudiar Git"
Formato: Código en Python, con persistencia en un archivo JSON.
```

Ahora ya no es genérico: el prompt tiene **contexto de usuario**, **escenario verificable**, y la IA no se inventa tanto.

---

## Historias de usuario y TDD

Lo que acabamos de ver con las **historias de usuario** y los **escenarios Gherkin** se conecta directamente con una práctica clave en desarrollo moderno: **TDD (Test Driven Development)**.

La idea de TDD es casi filosófica:

1. **Escribes primero el test** que define cómo debería comportarse tu programa (antes de tener código real).
2. Luego escribes el **mínimo código necesario** para que ese test pase.
3. Finalmente, **refactorizas** para mejorar el código, manteniendo todos los tests verdes.

Ese ciclo se suele resumir como:

- **Red** → escribes un test que falla (porque aún no hay implementación).
- **Green** → escribes lo justo para que pase.
- **Refactor** → limpias el código sin romper nada.

¿Dónde entran las historias de usuario aquí?

- La historia en lenguaje natural (*“Como usuario quiero agregar tareas para no olvidarlas”*) nos da el **qué**.
- El escenario Gherkin (*“When agrego la tarea X, Then debería estar en la lista”*) nos da un **test verificable**.
- Ese test se convierte en la primera pieza del ciclo TDD.

Así, el camino es natural:

Historias de usuario → Escenarios Gherkin → Tests → Código mínimo → Refactor.

No lo vamos a aplicar todavía (porque primero necesitas dominar el esqueleto y Git), pero ya sabes por qué tanto bombo con Gherkin: no es solo “documentar bonito”, es **pensar en el comportamiento desde el principio**.


# Resultado del ejercicio

Vale, si has hecho lo que te he pedido y le has preguntado a la IA, te habrá devuelto un resultado parecido al que hay en 'cli-tareas/notes.md'

Buenísimo. Justo esto es lo que quería que vieras: la diferencia entre un **esqueleto mínimo hecho a mano** y un **código gordo “production ready” que la IA puede escupir en segundos**.

Fíjate en varios detalles de la respuesta:

- **Usa `argparse`** → en lugar de `sys.argv` crudo, te da parsing limpio con subcomandos (`agregar`, `listar`, `completar`). Esto ya es un salto de nivel: más ordenado, más escalable.

- **Persistencia JSON** → la IA monta lectura/escritura atómica, ids autoincrementales, manejo de errores de archivo corrupto… bastante más de lo que pediría un profe en una primera práctica.

- **Capas separadas**:
    - funciones de dominio (`op_agregar`, `op_listar`, `op_completar`),
    - funciones de persistencia (`cargar_tareas`, `guardar_tareas`),
    - CLI (`argparse`) como capa externa.
        
        Eso ya es arquitectura limpia en miniatura.
        
- **Extras**: salida en formato humano o JSON, timestamps ISO, mensajes de error consistentes. Es un ejemplo de cómo la IA mete features “de más”.

---

### Lo que quiero que saques de aquí

1. **Tu versión manual** → te da el músculo, entiendes `sys.argv`, condiciones básicas y flujo mínimo.
2. **Versión IA** → te enseña hacia dónde puedes llevarlo, pero si la usas *sin haber pasado por lo manual*, solo te vuelves dependiente.

Esto es justo el contraste que vamos a cultivar todo el máster:

- Tú aprendes el *camino largo* (manual, sencillo, entendible).
- La IA te da el *atajo brutal* (argparse, persistencia robusta).
- Luego tú decides qué adoptar y qué no.

---

### Siguiente paso

No tires todavía con todo este mamotreto. Haz tu rama `feature/cli-tareas` con el **esqueleto simple**.

Después, crea otra rama (`feature/cli-json`) y ahí ya pruebas el código de la IA, lo ejecutas, ves cómo se comporta, y vas entendiendo qué partes puedes simplificar.

Así terminas con **dos PRs distintos**:

- uno con lo básico,
- otro con lo “IA pro”.

Y en paralelo, preparamos las **historias de usuario + escenarios Gherkin** para empezar a ligar esto con **TDD**.