# Clase 1: Fundamentos de IA en Desarrollo

**Duración**: 6 horas
**Objetivo**: Comprender qué es la IA en desarrollo y hacer tu primer contacto con herramientas de IA para programación

---

## Índice

1. [¿Qué es un Asistente de Código IA?](#parte-1-qué-es-un-asistente-de-código-ia)
2. [Instalación de Herramientas](#parte-2-instalación-de-herramientas-desde-cero)
3. [Primer Contacto con Claude Code](#parte-3-primer-contacto-con-claude-code)
4. [Prompt Engineering Básico](#parte-4-prompt-engineering-básico)
5. [Ejercicios Prácticos](#parte-5-ejercicios-prácticos)
6. [Proyecto Final](#proyecto-final-de-clase)

---

## Parte 1: ¿Qué es un Asistente de Código IA?

### 1.1 Introducción (30 min)

#### ¿Qué NO es IA en desarrollo?

❌ **No es magia** - No escribe código perfecto automáticamente
❌ **No reemplaza pensar** - Necesitas saber qué quieres construir
❌ **No es infalible** - Comete errores, genera código incorrecto

#### ¿Qué SÍ es IA en desarrollo?

✅ **Copiloto inteligente** - Te ayuda a escribir código más rápido
✅ **Tutor 24/7** - Explica conceptos cuando no entiendes
✅ **Generador de boilerplate** - Código repetitivo al instante
✅ **Revisor de código** - Segunda opinión sobre tu implementación
✅ **Debugger asistente** - Ayuda a entender errores

#### Analogía

Imagina que aprendes a cocinar:

- **Sin IA**: Buscas recetas en Google, lees libros, pruebas y error
- **Con IA**: Tienes un chef experto al lado que:
  - Te explica técnicas
  - Te ayuda a elegir ingredientes
  - Te corrige si vas a quemar algo
  - **Pero TÚ sigues cocinando**

---

### 1.2 Tipos de Herramientas IA para Desarrollo (30 min)

#### 1. **Code Completion** (Autocompletado inteligente)

**GitHub Copilot**:
- Se integra en tu editor (VS Code, Cursor, etc.)
- Sugiere código mientras escribes
- Funciona con comentarios: escribes lo que quieres, genera el código

```python
# Ejemplo: Escribes el comentario
# Función que calcula el factorial de un número

# Copilot sugiere automáticamente:
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

**Ventajas**:
- ✅ Rápido, integrado en flujo de trabajo
- ✅ Aprende de tu estilo de código

**Limitaciones**:
- ⚠️ Sugerencias línea por línea, no ve el "big picture"
- ⚠️ Puede sugerir código incorrecto si contexto es confuso

---

#### 2. **Chat-Based Assistants** (Asistentes conversacionales)

**Claude Code (este CLI)**:
- Terminal/consola
- Conversación sobre tu código
- Puede leer archivos, ejecutar comandos, generar código completo
- Contexto amplio (todo el proyecto)

**ChatGPT / Claude Web**:
- Interfaz web
- Útil para explicaciones, pseudocódigo, arquitectura
- No integrado con tu proyecto

**Ventajas**:
- ✅ Conversaciones largas, contexto amplio
- ✅ Explicaciones detalladas
- ✅ Puede razonar sobre arquitectura completa

**Limitaciones**:
- ⚠️ No ejecuta código
- ⚠️ Puede "alucinar" (inventar cosas que no existen, esto todas)

---

#### 3. **IDE Integrado** (Cursor IDE)

**Cursor**:
- Editor de código (fork de VS Code)
- Copilot + Chat integrado
- Cmd+K: Edita inline
- Cmd+L: Chat lateral
- "Composer": Edita múltiples archivos

**Ventajas**:
- ✅ Todo en uno (editor + IA)
- ✅ Puede editar directamente archivos
- ✅ Entiende contexto del proyecto

**Limitaciones**:
- ⚠️ Requiere aprender nuevo editor
- Genera dependencia
- Tan automatico que es fácil que dejes de leer

---

#### Comparación Rápida

| Herramienta | Mejor para | Nivel |
|-------------|-----------|-------|
| **GitHub Copilot** | Autocompletar mientras escribes | Principiante |
| **Claude Code CLI** | Proyectos completos, automatización | Intermedio |
| **Cursor IDE** | Desarrollo diario con IA integrado | Intermedio |
| **ChatGPT Web** | Aprender conceptos, diseñar soluciones | Principiante |

---

### 1.3 Modelos de Lenguaje: ¿Qué hay detrás? (20 min)

#### ¿Qué es un LLM (Large Language Model)?

Un modelo entrenado con millones de líneas de código y texto para:
- Predecir qué código viene después
- Entender patrones de programación
- Generar código coherente

**Modelos principales**:

- **GPT-5** (OpenAI): Usado por GitHub Copilot, ChatGPT, Cursor
- **Claude** (Anthropic): Usado por Claude Code, Cursor
- **Codex**: Versión especializada de GPT para código (parecido a claude code

#### Limitaciones Críticas

⚠️ **Conocimiento hasta fecha de corte**:
- Claude por ejemplo: Enero 2025
- Puede no conocer librerías muy nuevas
- APIs pueden haber cambiado

⚠️ **Hallucinations** (Alucinaciones):
```python
# IA puede inventar funciones que NO existen:
resultado = mi_libreria.funcion_magica()  # ← NO EXISTE

# SIEMPRE verifica:
# 1. ¿Esta función existe en la documentación?
# 2. ¿El código realmente funciona?
```

⚠️ **Límite de contexto**:
- No puede leer proyectos gigantes completos
- Debes darle contexto relevante
- Aprenderemos a manejar esto (Módulo 0, Clase 5)

⚠️ **No entiende runtime**:
```python
# IA ve código, no el resultado de ejecutarlo
x = calcular_algo_complejo()
# IA NO sabe qué valor tiene x después de ejecutar
```

---

### 1.4 Cuándo usar y cuándo NO usar IA (20 min)

#### ✅ USA IA cuando:

1. **Escribir boilerplate** (código repetitivo):
   ```python
   # Crear modelos Pydantic
   # Escribir tests básicos
   # Generar documentación
   ```

2. **Aprender conceptos nuevos**:
   ```
   "Explica qué es async/await en Python con ejemplos simples"
   ```

3. **Debuggear errores**:
   ```
   "Tengo este error: [paste error]
   Código: [paste código]
   ¿Qué está pasando?"
   ```

4. **Refactorizar código existente**:
   ```
   "Refactoriza esta función para usar list comprehensions"
   ```

5. **Code review (segunda opinión)**:
   ```
   "Revisa este código, ¿hay problemas de seguridad?"
   ```

---

#### ❌ NO uses IA cuando:

1. **Aprendiendo un concepto por PRIMERA vez**:
   ```
   ❌ "Escribe un algoritmo de búsqueda binaria"
   ✅ Implementa tú primero, LUEGO pide a IA que lo revise
   ```

2. **Código crítico de seguridad** sin revisar:
   ```python
   # ❌ NO copies auth code de IA sin entender
   # ✅ Genera boilerplate, TÚ revisas cada línea
   ```

3. **Decisiones de arquitectura**:
   ```
   ❌ "Diseña la arquitectura completa de mi app"
   ✅ TÚ decides arquitectura, IA ayuda a implementar
   ```

4. **Cuando no entiendes lo que hace**:
   ```python
   # ❌ Copiar código que no entiendes
   # ✅ Pedir a IA que explique línea por línea
   ```

---

## Parte 2: Instalación de Herramientas (DESDE CERO)

### 2.1 Python Installation (30 min)

#### Windows

**Paso 1**: Descargar Python
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.12.x (versión estable más reciente)
3. **IMPORTANTE**: Marcar "Add Python to PATH" durante instalación

**Paso 2**: Verificar instalación
```bash
# Abrir PowerShell o Command Prompt
python --version
# Debería mostrar: Python 3.12.x

# Verificar pip
pip --version
```

#### macOS

**Opción 1 - Homebrew** (recomendado):
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.12

# Verificar
python3 --version
```

**Opción 2 - Instalador oficial**:
1. Descargar de https://www.python.org/downloads/macos/
2. Ejecutar instalador
3. Verificar en Terminal

#### Linux (Ubuntu/Debian)

```bash
# Actualizar repositorios
sudo apt update

# Instalar Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip

# Verificar
python3.12 --version
```

---

### 2.2 Git Installation (20 min)

#### Windows

**Opción 1 - Git for Windows**:
1. Descargar: https://git-scm.com/download/win
2. Ejecutar instalador (usar opciones por defecto)
3. Verificar:
```bash
git --version
```

**Opción 2 - GitHub Desktop** (interfaz gráfica):
1. Descargar: https://desktop.github.com/
2. Instalar y autenticarse con GitHub

#### macOS

```bash
# Usando Homebrew
brew install git

# Verificar
git --version
```

#### Linux

```bash
sudo apt install git

# Verificar
git --version
```

#### Configuración inicial (TODOS los OS)

```bash
# Configurar nombre
git config --global user.name "Tu Nombre"

# Configurar email
git config --global user.email "tu@email.com"

# Verificar configuración
git config --list
```

---

### 2.3 Claude Code CLI Installation (30 min)

#### Prerequisitos

- ✅ Python 3.10+ instalado
- ✅ Cuenta en Anthropic (https://www.anthropic.com)
- ✅ API Key de Claude (se obtiene en https://console.anthropic.com)

#### Instalación

**Todos los sistemas operativos**:

```bash
# Opción 1: Desde PyPI (recomendado)
pip install claude-code

# Opción 2: Desde npm (si prefieres Node)
npm install -g @anthropics/claude-code

# Verificar instalación
claude --version
```

#### Configuración

**Paso 1**: Obtener API Key
1. Ir a https://console.anthropic.com
2. Crear cuenta o login
3. Ir a "API Keys"
4. Crear nueva key
5. **COPIAR** la key (solo se muestra una vez)

**Paso 2**: Configurar en tu sistema

**Windows (PowerShell)**:
```powershell
# Configurar API key en variable de entorno
$env:ANTHROPIC_API_KEY = "tu-api-key-aqui"

# Para que persista (agregar a perfil):
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "tu-api-key-aqui", "User")
```

**macOS/Linux (bash/zsh)**:
```bash
# Editar archivo de configuración de shell
# Para bash:
echo 'export ANTHROPIC_API_KEY="tu-api-key-aqui"' >> ~/.bashrc
source ~/.bashrc

# Para zsh (macOS default):
echo 'export ANTHROPIC_API_KEY="tu-api-key-aqui"' >> ~/.zshrc
source ~/.zshrc

# Verificar
echo $ANTHROPIC_API_KEY
```

**Paso 3**: Primer comando

```bash
# Test simple
claude "Hola, di 'Instalación exitosa'"

# Si funciona, verás respuesta de Claude
```

---

### 2.4 Cursor IDE Installation (OPCIONAL) (20 min)

#### ¿Instalar Cursor?

**Ventajas**:
- Todo en uno (editor + IA)
- Mejor para desarrollo diario

**Desventajas**:
- Requiere aprender nuevo editor
- OPCIONAL para este curso (puedes usar VS Code + Copilot)

#### Instalación

1. Ir a https://cursor.sh
2. Descargar para tu OS
3. Instalar
4. Abrir Cursor
5. Configurar con tu API key de Claude (Settings → Extensions → Claude)

---

## Parte 3: Primer Contacto con Claude Code (1 hora)

### 3.1 Comandos Básicos (30 min)

#### Comando 1: Pregunta simple

```bash
claude "¿Qué es Python?"
```

**Respuesta esperada**: Explicación de Python

---

#### Comando 2: Generar código

```bash
claude "Escribe un script Python que salude al usuario por su nombre"
```

**Ejemplo de output**:
```python
nombre = input("¿Cómo te llamas? ")
print(f"¡Hola, {nombre}!")
```

---

#### Comando 3: Explicar código

Crea archivo `ejemplo.py`:
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

```bash
claude "Explica qué hace el código en ejemplo.py línea por línea"
```

---

#### Comando 4: Debuggear error

```bash
claude "Tengo este error:

Traceback (most recent call last):
  File 'test.py', line 5, in <module>
    resultado = dividir(10, 0)
ZeroDivisionError: division by zero

¿Qué está pasando y cómo lo arreglo?"
```

---

### 3.2 Interacción Conversacional (30 min)

Claude Code permite conversaciones:

```bash
# Mensaje 1
claude "Necesito crear un programa que gestione una lista de tareas"

# Claude responderá con preguntas o sugerencias
# Puedes continuar:

# Mensaje 2
claude "Sí, que permita añadir, listar y marcar como completadas"

# Mensaje 3
claude "Quiero guardar las tareas en un archivo JSON"
```

---

## Parte 4: Prompt Engineering Básico (1 hora)

### 4.1 Anatomía de un Buen Prompt (20 min)

#### Estructura básica

```
[ROL] + [OBJETIVO] + [CONTEXTO] + [RESTRICCIONES]
```

#### Ejemplo malo ❌

```
"Haz un programa"
```

**Problemas**:
- No especifica qué programa
- No da contexto
- Resultado: IA adivina y probablemente falla

---

#### Ejemplo bueno ✅

```
Rol: Eres un instructor de Python para principiantes

Objetivo: Crea un programa simple que gestione una lista de compras

Contexto:
- El usuario nunca ha programado antes
- Debe ser fácil de entender
- Solo usar Python básico (listas, input, print)

Restricciones:
- NO usar clases
- NO usar librerías externas
- Incluir comentarios explicativos
- Máximo 30 líneas de código
```

**Resultado**: Código simple, bien comentado, apropiado para principiante

---

### 4.2 Pattern: Rol + Objetivo (20 min)

#### Pattern 1: Expert Role

```
"Eres un experto en [TECNOLOGÍA].
Explica [CONCEPTO] como si yo tuviera [NIVEL DE CONOCIMIENTO]."
```

**Ejemplo**:
```
"Eres un experto en Python.
Explica qué son las list comprehensions como si yo supiera programación básica pero nunca las haya usado."
```

---

#### Pattern 2: Specific Task

```
"Necesito [TAREA ESPECÍFICA].
Requisitos:
- [Requisito 1]
- [Requisito 2]
Formato: [Cómo quiero el resultado]"
```

**Ejemplo**:
```
"Necesito una función que valide emails.
Requisitos:
- Debe tener @ y dominio
- Retornar True/False
- Incluir docstring
Formato: Solo la función, con type hints"
```

---

### 4.3 Iteración de Prompts (20 min)

**Concepto**: No esperes el prompt perfecto a la primera

#### Ejemplo de iteración

**Intento 1**:
```
"Escribe una función de Fibonacci"
```

**Resultado**: Implementación recursiva

---

**Intento 2** (refinamiento):
```
"La función anterior es muy lenta para números grandes.
Reescríbela usando programación dinámica (memoization)"
```

**Resultado**: Implementación con caché

---

**Intento 3** (optimización):
```
"Ahora añade:
- Type hints
- Docstring explicando complejidad
- Tests con pytest"
```

**Resultado**: Función completa, profesional

---

## Parte 5: Ejercicios Prácticos (1.5 horas)

### Ejercicio 1: Primera Interacción (15 min)

**Objetivo**: Familiarizarte con Claude Code

**Tareas**:
1. Pregunta a Claude: "Explica qué es Git en 3 párrafos"
2. Pide que genere un script Python que imprima números del 1 al 10
3. Pide que explique el código generado línea por línea

**Entregable**: Copia las respuestas en un archivo `ejercicio1.md`

---

### Ejercicio 2: Mejorar un Prompt (20 min)

**Dado este prompt malo**:
```
"haz calculadora"
```

**Tu tarea**:
1. Reescribirlo siguiendo estructura [Rol + Objetivo + Contexto + Restricciones]
2. Generar el código con Claude usando tu prompt mejorado
3. Comparar: ¿El resultado es mejor?

**Entregable**:
- `prompt_original.txt`
- `prompt_mejorado.txt`
- `calculadora.py` (código generado)
- `reflexion.md` (qué cambió y por qué es mejor)

---

### Ejercicio 3: Debugging Asistido (25 min)

**Código con bug**:
```python
def calcular_promedio(numeros):
    suma = 0
    for num in numeros:
        suma + num  # ← Bug aquí
    return suma / len(numeros)

resultado = calcular_promedio([10, 20, 30])
print(f"Promedio: {resultado}")
```

**Tareas**:
1. Ejecuta el código (¿cuál es el resultado?)
2. Pide a Claude que encuentre el bug
3. Pide que explique POR QUÉ es un bug
4. Pide la versión corregida
5. Pide que genere tests para evitar este bug en futuro

**Entregable**:
- `bug_original.py`
- `bug_corregido.py`
- `test_promedio.py`
- `explicacion_bug.md`

---

### Ejercicio 4: Code Review (30 min)

**Código funcionando pero mejorable**:
```python
def p(n):
    l = []
    for i in range(2, n):
        is_p = True
        for j in range(2, i):
            if i % j == 0:
                is_p = False
                break
        if is_p:
            l.append(i)
    return l

print(p(20))
```

**Tareas**:
1. ¿Qué hace este código? (pregunta a Claude)
2. Pide code review enfocado en:
   - Nombres de variables
   - Claridad
   - Eficiencia
3. Pide versión mejorada con:
   - Nombres descriptivos
   - Docstring
   - Type hints
   - Mejor algoritmo si es posible

**Entregable**:
- `codigo_original.py`
- `codigo_mejorado.py`
- `cambios.md` (lista de mejoras y por qué)

---

## Proyecto Final de Clase (1 hora)

### Objetivo

Crear tu primer script útil con ayuda de IA, pero **TÚ diseñas y TÚ entiendes**.

### Especificación

**Programa**: Generador de Contraseñas Seguras

**Requisitos**:
1. Pedir longitud deseada (mínimo 8)
2. Generar contraseña aleatoria con:
   - Mayúsculas
   - Minúsculas
   - Números
   - Símbolos
3. Validar que tiene al menos uno de cada tipo
4. Copiar al portapapeles (opcional, usar librería `pyperclip`)
5. Opción de generar múltiples contraseñas

### Proceso (IMPORTANTE)

**NO pidas a IA que haga todo junto. Divide el trabajo**:

#### Paso 1: Diseño (TÚ)
- Escribe en papel o archivo `diseño.md`:
  - ¿Qué funciones necesito?
  - ¿Qué inputs/outputs tiene cada una?
  - ¿Qué validaciones necesito?

#### Paso 2: Implementación (TÚ + IA)
- Función por función, pide a IA que genere
- Ejemplo de prompt:
  ```
  "Escribe una función Python que:
  - Se llame validar_longitud
  - Reciba un número como parámetro
  - Valide que sea >= 8
  - Retorne True/False
  - Incluya docstring y type hints"
  ```

#### Paso 3: Integración (TÚ)
- Junta las funciones
- Crea el flujo principal
- Pide ayuda a IA si te atascas

#### Paso 4: Testing (TÚ + IA)
- Prueba manualmente el programa
- Pide a IA que genere tests con pytest
- **TÚ debes entender qué testean**

#### Paso 5: Refinamiento (TÚ + IA)
- Pide code review a IA
- Aplica mejoras que tengan sentido
- **No apliques mejoras que no entiendas**

---

### Entregables

1. **`generador_contraseñas.py`**: Código final funcionando
2. **`test_generador.py`**: Tests (al menos 3)
3. **`diseño.md`**: Tu diseño inicial
4. **`prompts_usados.md`**: Qué prompts usaste y para qué
5. **`reflexion.md`**: Documento de 1 página:
   - ¿Qué hizo IA?
   - ¿Qué hiciste tú?
   - ¿Qué aprendiste?
   - ¿En qué ayudó IA?
   - ¿En qué NO ayudó?
   - Si lo hicieras de nuevo, ¿qué cambiarías?

---

## Evaluación

### Criterios

**Comprensión (40%)**:
- ¿Entiendes qué es IA en desarrollo y qué no?
- ¿Sabes cuándo usar y NO usar IA?
- ¿Puedes explicar tu código?

**Uso de IA (30%)**:
- ¿Prompts bien estructurados?
- ¿Iteraste para mejorar resultados?
- ¿Revisaste código generado críticamente?

**Código (30%)**:
- ¿Funciona correctamente?
- ¿Está bien estructurado?
- ¿Tiene tests?

### Señales de éxito

✅ Usaste IA pero entiendes TODO el código
✅ Diseñaste tú, IA ayudó a implementar
✅ Iteraste prompts cuando resultado no fue bueno
✅ Cuestionaste y mejoraste sugerencias de IA

### Señales de alerta

❌ Copiaste código que no entiendes
❌ Pediste a IA que haga todo sin tu diseño
❌ No probaste si el código funciona
❌ No sabes explicar qué hace una función

---

## Recursos Adicionales

### Documentación
- Claude Code: https://docs.anthropic.com/claude/docs/
- Prompt Engineering: https://www.promptingguide.ai

### Lecturas recomendadas
- "The Pragmatic Programmer" (principios que no cambian con IA)
- "Clean Code" (código legible incluso generado por IA)

### Práctica adicional
- Leetcode (resolver problemas, comparar tu solución vs IA)
- Project Euler (matemáticas + programación)

---

## Próxima Clase

**Clase 2: Git + Cursor + Flujo de Trabajo IA**

Prepárate para:
- Crear tu primer repositorio
- Configurar Cursor IDE
- Flujo de trabajo: Git + IA
- Conventional commits con IA

**Prerequisitos**:
- ✅ Python instalado
- ✅ Git instalado
- ✅ Claude Code funcionando
- ✅ Haber completado proyecto de esta clase

---

## Notas Finales

**Recuerda**:

1. **IA es una herramienta, no un atajo** - Debes entender lo que hace
2. **SIEMPRE revisa el código** - IA comete errores
3. **Aprende fundamentos primero** - IA acelera, no reemplaza conocimiento
4. **Itera tus prompts** - Pocas veces sale perfecto a la primera

**Mentalidad correcta**:
- ✅ "IA me ayuda a aprender más rápido"
- ✅ "IA me hace más productivo porque entiendo mejor"
- ❌ "IA hace todo por mí"
- ❌ "No necesito entender, solo copiar"

**¡Bienvenido al desarrollo con IA!** 🚀
