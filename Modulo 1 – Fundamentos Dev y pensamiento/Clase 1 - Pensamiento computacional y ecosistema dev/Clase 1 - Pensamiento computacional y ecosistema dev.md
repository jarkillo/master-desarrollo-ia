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

---

## 🤖 Python Manual vs AI-Assisted (30 min)

Ahora que tienes el esqueleto manual funcionando, es el momento perfecto para entender **cuándo usar IA y cuándo no**.

### El mismo problema, dos caminos

Imagina que te piden: *"Crea una CLI que gestione tareas con persistencia en JSON"*.

Puedes resolverlo de **dos formas completamente diferentes**:

#### Camino 1: Manual (lo que acabas de hacer)
1. Empiezas con `sys.argv` básico
2. Añades condiciones `if/elif/else`
3. Entiendes **cada línea** que escribes
4. Cuando algo falla, sabes exactamente dónde buscar
5. El código es **tuyo**, lo construiste pieza a pieza

**Resultado**: Código simple, comprensible, pero básico.

#### Camino 2: IA-Asistido (lo que veremos ahora)
1. Escribes un prompt estructurado
2. La IA genera código completo con `argparse`, manejo de errores, timestamps, etc.
3. Ejecutas, funciona... pero **¿entiendes todo lo que hace?**
4. Cuando algo falla, tienes que leer código que NO escribiste
5. El código es **del modelo**, tú lo adaptaste

**Resultado**: Código robusto, production-ready, pero complejo.

---

### Tabla comparativa: Manual vs IA

| Aspecto               | Manual (sys.argv)                | IA-Asistido (argparse + features)    |
|----------------------|----------------------------------|--------------------------------------|
| **Velocidad**        | Lento (2-3 horas aprendiendo)    | Rápido (5 minutos generando)        |
| **Comprensión**      | Alta (línea a línea)             | Media (necesitas leer y entender)    |
| **Calidad inicial**  | Básica (esqueleto mínimo)        | Alta (production-ready)              |
| **Escalabilidad**    | Requiere refactor manual         | Ya incluye estructura escalable      |
| **Aprendizaje**      | Profundo (construyes músculo)    | Superficial (peligro de dependencia) |
| **Debugging**        | Fácil (sabes qué hace cada línea)| Complejo (código desconocido)        |
| **Mantenimiento**    | Fácil (código simple)            | Requiere entender arquitectura       |
| **Features extra**   | Solo lo que pediste              | IA añade extras (¿necesarios?)       |

---

### ¿Cuándo usar cada uno?

#### Usa el camino MANUAL cuando:
✅ Estás **aprendiendo** un concepto nuevo (como ahora con CLI)
✅ Es código **crítico** (seguridad, lógica de negocio compleja)
✅ Necesitas **comprensión profunda** del comportamiento
✅ El proyecto es **pequeño** y simple
✅ Quieres **control total** sobre cada decisión

**Ejemplo**: Estás aprendiendo cómo funciona `sys.argv` → hazlo manual.

#### Usa el camino IA-ASISTIDO cuando:
✅ Ya conoces el concepto y quieres **ir rápido**
✅ Necesitas **boilerplate** (código repetitivo que ya has escrito mil veces)
✅ Quieres **explorar** diferentes soluciones rápidamente
✅ El código es **no crítico** (utilidades, scripts de desarrollo)
✅ Tienes la capacidad de **revisar y entender** lo que genera la IA

**Ejemplo**: Necesitas parsing de argumentos con `argparse` (ya lo conoces) → usa IA.

---

### La regla de oro

**Nunca uses IA para algo que no entenderías si lo leyeras línea a línea.**

Si la IA genera código que te suena a chino, **STOP**:
1. Vuelve al camino manual
2. Aprende el concepto básico primero
3. Cuando lo domines, entonces usa IA para acelerarte

**Analogía del chef**:
- **Manual** = aprender a cocinar desde cero (cortar, cocinar, sazonar)
- **IA** = usar un robot de cocina cuando ya sabes cocinar

El robot es genial **si sabes cocinar**. Si no, solo produces comida que no entiendes.

---

### 🎯 Ejercicio Práctico: IA Primero, Manual Después (20 min)

Vamos a poner en práctica la comparación manual vs IA con un ejercicio concreto.

#### Reto

Necesitamos una función `validar_comando(comando)` que:
- Reciba un string (el comando del usuario)
- Devuelva `True` si el comando es válido (`"listar"`, `"agregar"`, o `"completar"`)
- Devuelva `False` en caso contrario

#### Parte A: IA Primero (5 min)

1. **Abre tu IA favorita** (ChatGPT, Claude, Copilot, etc.)

2. **Usa este prompt** (cópialo exactamente):
```
Crea una función en Python llamada validar_comando que reciba un string
y devuelva True si está en ['listar', 'agregar', 'completar'],
False en caso contrario.

Solo la función, sin explicaciones.
```

3. **Ejecuta el código** que te genere en un archivo `validar_ia.py`:
```python
# Pega aquí lo que te generó la IA
```

4. **Pruébala**:
```bash
python
>>> from validar_ia import validar_comando
>>> validar_comando("listar")
True
>>> validar_comando("borrar")
False
```

5. **Reflexión** (escríbela en un comment):
```python
# ¿Qué hizo la IA que no esperabas?
# ¿Usó alguna estructura de datos que no conocías?
# ¿El código es legible para ti?
```

#### Parte B: Manual Después (10 min)

Ahora, **SIN MIRAR** la solución de la IA, implementa tú mismo la función en `validar_manual.py`.

Pistas:
- Puedes usar `if/elif/else`
- Puedes usar `in` con una lista
- Puedes usar un set (si lo conoces)

```python
def validar_comando(comando):
    # Tu implementación aquí
    pass
```

**Prueba tu versión**:
```bash
python
>>> from validar_manual import validar_comando
>>> validar_comando("listar")
True
>>> validar_comando("borrar")
False
```

#### Parte C: Comparación (5 min)

Ahora **sí**, compara ambas versiones:

1. **Abre ambos archivos** lado a lado
2. **Anota las diferencias**:
   - ¿Cuál es más corta?
   - ¿Cuál es más legible?
   - ¿Cuál manejaría mejor edge cases (ej: `None`, espacios extra)?
   - ¿Cuál entiendes mejor?

3. **Aprendizaje clave**:
   - Si la IA usó algo que NO entiendes → anótalo y búscalo
   - Si tu versión manual tiene bugs → compara con la IA para aprender
   - **Lo ideal**: combinar lo mejor de ambas

**Ejemplo de reflexión**:
```python
# Mi versión: if/elif/else (3 líneas, clara pero repetitiva)
# IA versión: comando in ['listar', 'agregar', 'completar'] (1 línea, Pythonic)
#
# Aprendí: el operador 'in' con listas es más elegante que if/elif
# Decisión: adoptaré la versión IA porque la entiendo Y es mejor
```

---

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

## 🐛 Debugging con IA (20 min)

Todos cometemos errores al programar. La diferencia está en cómo los encontramos y solucionamos.

Vamos a comparar **debugging manual** vs **debugging con IA** para que entiendas cuándo usar cada uno.

### Escenario: Código con bugs

Imagina que escribiste este código y al ejecutarlo obtienes un error:

```python
import sys

if len(sys.argv) < 2:
    print("Uso: python tareas.py <comando>")
else:
    comando = sys.argv[1]

    if comando = "listar":  # 🐛 BUG 1: = en vez de ==
        print("Aquí se mostrarían las tareas")

    elif comando == "agregar":
        if len(sys.argv) < 3:
            print("Error: falta el texto de la tarea")
        else:
            tarea = sys.argv[2]
            print(f"Tarea agregada: {tarea"})  # 🐛 BUG 2: falta cerrar f-string

    elif comando == "completar":
        if len(sys.argv) < 3:
            print("Error: falta el ID de la tarea")
        else:
            task_id = sys.argv[2]
            print(f"Tarea {task_id} completada")

    else:
        print("Comando no reconocido")
```

**Error al ejecutar**:
```
  File "tareas_bugs.py", line 8
    if comando = "listar":
               ^
SyntaxError: invalid syntax
```

---

### Método 1: Debugging Manual (Sin IA) - 2-5 minutos

**Pasos**:
1. **Leer el mensaje de error**: `SyntaxError: invalid syntax` en línea 8
2. **Ir a la línea 8**: `if comando = "listar":`
3. **Analizar**: ¿Qué está mal? Ah, `=` es asignación, necesito `==` para comparar
4. **Corregir** y volver a ejecutar

**Ventajas**:
✅ Aprendes a leer errores (habilidad crítica)
✅ Entrenas tu "ojo clínico" para detectar bugs
✅ Memoria muscular: no cometerás el mismo error otra vez

**Desventajas**:
❌ Puede llevar más tiempo si no sabes interpretar el error
❌ Si hay múltiples bugs, los descubres uno por uno

---

### Método 2: Debugging con IA - 30 segundos

**Prompt efectivo**:
```
Tengo este código Python que da error al ejecutarlo:

[pegar código completo]

Error:
  File "tareas_bugs.py", line 8
    if comando = "listar":
               ^
SyntaxError: invalid syntax

¿Qué está mal y cómo lo corrijo?
```

**Respuesta de IA** (ejemplo):
```
El error está en la línea 8. Usas = (asignación) en vez de == (comparación).

Corrección:
    if comando == "listar":

Además, detecto otro bug en la línea 14:
    print(f"Tarea agregada: {tarea"})
Falta cerrar la f-string correctamente:
    print(f"Tarea agregada: {tarea}")

Código corregido completo:
[código sin errores]
```

**Ventajas**:
✅ **Instantáneo**: detecta TODOS los bugs a la vez
✅ **Explica** el error (útil si no lo entendías)
✅ Te da el código corregido

**Desventajas**:
❌ **Peligro de dependencia**: "la IA lo arregla, yo no aprendo"
❌ Pierdes práctica en leer errores
❌ Si usas IA siempre, no desarrollas debugging skills

---

### ¿Cuándo usar cada método?

#### Debugging MANUAL cuando:
✅ El error es simple y puedes entenderlo
✅ Estás **aprendiendo** (como ahora)
✅ Quieres entrenar debugging skills
✅ El código es tuyo y lo entiendes bien

#### Debugging IA cuando:
✅ El error es críptico y no sabes qué significa
✅ Llevas >10 minutos atascado
✅ El código es ajeno (legacy code que no escribiste)
✅ Quieres validar tu hipótesis de qué está mal

---

### 🎯 Ejercicio Práctico: Encuentra 3 Bugs

Crea un archivo `tareas_bugs.py` con el código de arriba (con los 2 bugs).

**Desafío**:
1. **SIN IA** (5 min): Ejecuta el código, lee el error, corrígelo. ¿Cuántos bugs encontraste?
2. **CON IA** (2 min): Ahora pasa el código a la IA y pide que encuentre TODOS los bugs
3. **Compara**: ¿Encontraste los mismos bugs? ¿La IA detectó algo que se te escapó?

**Reflexión**:
```python
# Sin IA encontré: [escribe cuántos]
# Con IA encontró: [escribe cuántos]
#
# Aprendizaje: [¿Qué bug no viste? ¿Por qué la IA lo detectó?]
```

---

### Prompts Efectivos para Debugging

❌ **Prompts MALOS**:
- "Este código no funciona" (sin código, sin error)
- "Ayuda" (demasiado vago)
- "Hay un bug aquí" (sin especificar dónde ni qué hace)

✅ **Prompts BUENOS**:
```
Tengo este código Python [pegar código].

Al ejecutar `python tareas.py listar` obtengo este error:
[pegar error completo con traceback]

¿Qué está mal y cómo lo corrijo?
```

```
Este código debería imprimir las tareas, pero imprime una lista vacía siempre:
[pegar código]

Datos de prueba: [explicar qué esperas vs qué obtienes]

¿Dónde está el bug?
```

**Regla de oro**: Cuanto más **contexto** des (código + error + comportamiento esperado), mejor ayuda te dará la IA.

---

## ♻️ Refactoring Asistido (20 min)

**Refactorizar** = mejorar el código sin cambiar su comportamiento.

Es como reorganizar tu armario: la ropa es la misma, pero ahora está más ordenada y encuentras las cosas más rápido.

### Por qué refactorizar

El código "feo" funciona, pero:
- ❌ Es difícil de leer
- ❌ Es difícil de modificar
- ❌ Tiene lógica repetida
- ❌ Viola principios de código limpio (como Single Responsibility)

Refactorizar convierte código "que funciona" en código "que funciona Y es mantenible".

---

### Código "feo" inicial

Este código funciona, pero tiene problemas:

```python
import sys

if len(sys.argv) < 2:
    print("Uso: python tareas.py <comando>")
else:
    comando = sys.argv[1]

    if comando == "listar":
        print("=== LISTA DE TAREAS ===")
        print("[ ] 1. Estudiar Git")
        print("[ ] 2. Hacer ejercicio")
        print("[x] 3. Leer documentación")

    elif comando == "agregar":
        if len(sys.argv) < 3:
            print("Error: falta el texto de la tarea")
        else:
            tarea = sys.argv[2]
            print(f"Tarea agregada: {tarea}")
            print("Total de tareas: 4")

    elif comando == "completar":
        if len(sys.argv) < 3:
            print("Error: falta el ID")
        else:
            task_id = sys.argv[2]
            print(f"Tarea {task_id} marcada como completada")
            print("¡Buen trabajo!")

    else:
        print("Comando no reconocido")
```

**Problemas**:
1. Todo el código está en el nivel principal (no hay funciones)
2. La lógica de validación se repite (`if len(sys.argv) < 3`)
3. Los mensajes están mezclados con la lógica
4. Imposible testear sin ejecutar el script completo

---

### Refactoring Manual Guiado (Paso a paso)

Vamos a mejorar esto **manualmente** primero para que entiendas el proceso.

#### Paso 1: Extraer función de uso
```python
def mostrar_uso():
    """Muestra cómo usar el programa"""
    print("Uso: python tareas.py <comando>")
```

#### Paso 2: Extraer funciones por comando
```python
def comando_listar():
    """Lista todas las tareas"""
    print("=== LISTA DE TAREAS ===")
    print("[ ] 1. Estudiar Git")
    print("[ ] 2. Hacer ejercicio")
    print("[x] 3. Leer documentación")

def comando_agregar(tarea):
    """Agrega una nueva tarea"""
    print(f"Tarea agregada: {tarea}")
    print("Total de tareas: 4")

def comando_completar(task_id):
    """Marca una tarea como completada"""
    print(f"Tarea {task_id} marcada como completada")
    print("¡Buen trabajo!")
```

#### Paso 3: Refactorizar el main
```python
import sys

def main():
    if len(sys.argv) < 2:
        mostrar_uso()
        return

    comando = sys.argv[1]

    if comando == "listar":
        comando_listar()

    elif comando == "agregar":
        if len(sys.argv) < 3:
            print("Error: falta el texto de la tarea")
        else:
            comando_agregar(sys.argv[2])

    elif comando == "completar":
        if len(sys.argv) < 3:
            print("Error: falta el ID")
        else:
            comando_completar(sys.argv[2])

    else:
        print("Comando no reconocido")

if __name__ == "__main__":
    main()
```

**Mejoras logradas**:
✅ Cada función tiene UNA responsabilidad (Single Responsibility Principle)
✅ El código principal es más corto y legible
✅ Ahora puedes testear cada función por separado
✅ Añadir nuevos comandos es más fácil

---

### Refactoring con IA (5 min)

Ahora veamos cómo la IA haría el refactoring.

**Prompt efectivo**:
```
Refactoriza este código Python siguiendo el principio de Single Responsibility:
- Extrae comandos a funciones separadas
- Crea una función main()
- Añade docstrings a cada función

Código:
[pegar código "feo"]

Mantén el mismo comportamiento exacto.
```

**Respuesta típica de IA**:
La IA generará algo similar a lo que hicimos manualmente, pero probablemente añada extras:
- Mejor manejo de errores
- Constantes para comandos válidos
- Posiblemente una función `validar_argumentos()`
- Type hints en funciones

---

### ¿Cuándo usar cada método?

#### Refactoring MANUAL cuando:
✅ Estás **aprendiendo** patrones de diseño (como ahora)
✅ El código es simple y entiendes qué mejorar
✅ Quieres practicar principios como SOLID
✅ Es un refactor pequeño (1-2 funciones)

#### Refactoring IA cuando:
✅ El código es **grande** y tedioso de refactorizar
✅ Ya conoces el principio pero quieres ver **diferentes aproximaciones**
✅ Quieres refactorizar código legacy que no escribiste
✅ Necesitas refactorizar múltiples archivos a la vez

---

### 🎯 Ejercicio Práctico: Refactor Challenge

**Tu misión**: Refactoriza el código "feo" de dos formas.

#### Parte A: Manual (10 min)
1. Copia el código "feo" en `tareas_refactor_manual.py`
2. Aplica los 3 pasos del refactoring guiado
3. Ejecuta y verifica que funciona igual

#### Parte B: Con IA (5 min)
1. Pasa el código "feo" original a la IA con el prompt de arriba
2. Guarda el resultado en `tareas_refactor_ia.py`
3. Ejecuta y verifica que funciona

#### Parte C: Comparación (5 min)
1. **Compara ambas versiones**:
   - ¿Cuál tiene mejor estructura?
   - ¿La IA añadió algo que no pensaste?
   - ¿Hay algo de la versión IA que NO entiendes?

2. **Crea versión híbrida** (`tareas_refactor_hybrid.py`):
   - Toma lo mejor de tu versión manual
   - Adopta las mejoras de IA que entiendas
   - **Rechaza** lo que no entiendas o sea over-engineering

**Reflexión final**:
```python
# De mi versión manual usé: [qué conservaste]
# De la versión IA adopté: [qué mejoras tomaste]
# De la versión IA rechacé: [qué descartaste y por qué]
```

---

### Lección Clave: La IA propone, tú decides

**No copies código de IA a ciegas.**

Proceso correcto:
1. IA genera refactoring
2. **Tú lo lees** línea a línea
3. **Entiendes** cada cambio
4. **Decides** qué adoptar
5. **Adaptas** a tu estilo/necesidades

La IA puede sugerir usar `argparse`, `dataclasses`, `enum`, `typing`... todo genial, pero si no entiendes esas herramientas, **no las uses todavía**.

**Regla de oro**: Solo refactoriza hacia código que **entiendes completamente**.

---

## 🚀 Proyecto Final: CLI App con y sin IA (60 min)

Este es el proyecto integrador de la clase, donde aplicarás TODO lo aprendido.

### Estructura del proyecto

Tu carpeta `cli-tareas/` debe tener esta estructura al final:

```
cli-tareas/
├── tareas.py                    # ✅ Ya existe - Esqueleto manual básico
├── tareas_bugs.py               # 🐛 Código con bugs (ejercicio debugging)
├── tareas_refactor_antes.py     # ♻️ Código "feo" (ejercicio refactoring)
├── tareas_manual_refactor.py    # ♻️ Tu refactoring manual
├── tareas_ia_refactor.py        # ♻️ Refactoring generado por IA
├── tareas_hybrid.py             # 🎯 Versión híbrida (manual + IA, lo mejor de ambos)
├── COMPARACION.md               # 📝 Tu reflexión sobre manual vs IA
└── prompts_usados.md            # 📝 Historial de prompts (buenos y malos)
```

---

### Paso 1: Implementación Manual (Ya hecho ✅)

Ya tienes `tareas.py` con el esqueleto básico usando `sys.argv`.

---

### Paso 2: Debugging Challenge (10 min)

1. **Crea** `tareas_bugs.py` con el código bugueado de la sección "Debugging con IA"
2. **Intenta** encontrar los bugs manualmente (5 min)
3. **Usa IA** para validar (2 min)
4. **Reflexiona** en el mismo archivo (3 min)

---

### Paso 3: Refactoring Challenge (20 min)

1. **Manual** (10 min):
   - Copia `tareas_refactor_antes.py` a `tareas_manual_refactor.py`
   - Refactoriza siguiendo los 3 pasos guiados
   - Ejecuta y verifica

2. **Con IA** (5 min):
   - Pasa `tareas_refactor_antes.py` a la IA con el prompt de refactoring
   - Guarda el resultado en `tareas_ia_refactor.py`
   - Ejecuta y verifica

3. **Versión híbrida** (5 min):
   - Crea `tareas_hybrid.py`
   - Combina lo mejor de ambas versiones
   - Solo incluye código que entiendes

---

### Paso 4: Versión IA Avanzada (10 min)

Ahora, usa IA para crear una versión "production-ready" completa.

**Prompt efectivo** (guárdalo en `prompts_usados.md`):

````markdown
# Prompts Usados

## Prompt 1: Versión Production-Ready

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

## Resultado:

[Aquí pegarás lo que generó la IA]

## Reflexión:

¿Qué generó la IA que no esperabas?
¿Hay algo que no entiendes?
¿Qué adoptarías para tu versión híbrida?
````

---

### Paso 5: Documento de Comparación (15 min)

Crea `COMPARACION.md` con este template:

````markdown
# Comparación: Manual vs IA vs Híbrido

## 1. Versión Manual (`tareas.py`)

**Ventajas**:
- [Escribe 2-3 ventajas que experimentaste]

**Desventajas**:
- [Escribe 2-3 desventajas]

**Lo que aprendí**:
- [Qué aprendiste haciendo esto manualmente]

---

## 2. Versión IA (`tareas_ia_completo.py`)

**Ventajas**:
- [Qué hizo la IA que fue impresionante]

**Desventajas**:
- [Qué generó que no necesitabas o no entendías]

**Lo que me sorprendió**:
- [Features inesperados que añadió la IA]

---

## 3. Versión Híbrida (`tareas_hybrid.py`)

**De la versión manual conservé**:
- [Qué partes mantuviste de tu código manual]

**De la versión IA adopté**:
- [Qué mejoras de la IA integraste]

**Decisiones de diseño**:
- [Por qué elegiste esta combinación]

---

## 4. Reflexión Final

**¿Cuál usarías en un proyecto real?**
- [Tu respuesta razonada]

**¿Cuándo usarías solo IA?**
- [Escenarios donde IA sola es suficiente]

**¿Cuándo evitarías la IA?**
- [Cuándo es mejor ir 100% manual]

**Principal aprendizaje de esta clase**:
- [Tu mayor insight sobre desarrollo manual vs IA-asistido]
````

---

### Paso 6: Historial de Prompts (5 min)

Ya iniciaste `prompts_usados.md` en el Paso 4. Ahora añade:

````markdown
## Prompts que NO funcionaron bien

### Prompt malo #1:
```
Crea una app de tareas
```

**Problema**: Demasiado vago, la IA no sabe qué framework, qué features, qué nivel de complejidad.

**Resultado**: Código genérico que no sirve.

---

### Prompt malo #2:
```
Mejora este código [pegar código]
```

**Problema**: "Mejorar" es subjetivo. ¿Mejorar qué? ¿Performance? ¿Legibilidad? ¿Features?

**Resultado**: La IA hace cambios aleatorios que tal vez no quieres.

---

## Lecciones sobre Prompt Engineering

1. **Especificidad** > Generalidad
2. **Contexto** es crítico (lenguaje, versión, frameworks)
3. **Output claro**: especifica formato, estructura, qué incluir/excluir
4. **Constraints** ayudan: "solo usa stdlib", "máximo 100 líneas", "sin dependencias"
````

---

### Criterios de Éxito

Has completado el proyecto si tienes:
✅ 7 archivos Python funcionando
✅ `COMPARACION.md` con reflexión completa
✅ `prompts_usados.md` con ejemplos buenos y malos
✅ Al menos 3 versiones ejecutables (manual, IA, híbrida)
✅ Commits organizados en Git (cada paso un commit)

---

### Git Workflow para este proyecto

```bash
# Paso 1: Rama de trabajo
git checkout -b feature/cli-tareas-completo

# Paso 2: Commits incrementales
git add cli-tareas/tareas_bugs.py
git commit -m "feat(M1-C1): añadir ejercicio debugging con bugs intencionales"

git add cli-tareas/tareas_manual_refactor.py
git commit -m "feat(M1-C1): refactorizar versión manual con funciones"

git add cli-tareas/tareas_ia_refactor.py
git commit -m "feat(M1-C1): añadir refactoring generado por IA"

git add cli-tareas/tareas_hybrid.py cli-tareas/COMPARACION.md
git commit -m "feat(M1-C1): crear versión híbrida y documento comparativo"

git add cli-tareas/prompts_usados.md
git commit -m "docs(M1-C1): documentar prompts usados y lecciones"

# Paso 3: Push y PR
git push origin feature/cli-tareas-completo
gh pr create --base dev --title "feat(M1-C1): Proyecto CLI con comparación Manual vs IA"
```

---

👉 **Próximos pasos** (después del proyecto):

1. Revisa la documentación de `argparse` (lo que usó la IA)
2. Lee sobre el patrón Repository (separar persistencia de lógica)
3. Investiga cómo hacer tests para CLIs en Python (pytest)

En la siguiente clase profundizaremos en estos conceptos, pero con base en lo que ya construiste aquí.

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