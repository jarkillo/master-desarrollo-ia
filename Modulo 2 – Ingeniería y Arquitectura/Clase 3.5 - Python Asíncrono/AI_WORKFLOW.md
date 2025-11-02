# AI Workflow - Python Asíncrono

**Objetivo**: Integración del 40% de contenido con asistentes de IA para aprender async/await efectivamente.

## 🤖 Agentes Recomendados

Para esta clase, usa los siguientes agentes educativos del repositorio:

1. **Python Best Practices Coach** (`.claude/agents/educational/python-best-practices-coach.md`)
   - Revisa patrones async/await
   - Valida uso correcto de coroutines
   - Detecta anti-patrones (blocking calls, missing await)

2. **FastAPI Design Coach** (`.claude/agents/educational/fastapi-design-coach.md`)
   - Revisa endpoints async vs sync
   - Valida dependency injection async
   - Optimiza patrones FastAPI async

3. **Performance Optimizer** (`.claude/agents/educational/performance-optimizer.md`)
   - Analiza cuándo usar async vs sync
   - Detecta oportunidades de paralelización
   - Revisa uso eficiente de `asyncio.gather()`

## 📋 Workflow Paso a Paso

### Fase 1: Generación de Código Async con IA

#### 1.1 Prompt para Crear Primera Coroutine

```
Ayúdame a crear mi primera coroutine async en Python. Quiero:

1. Una función async que simule una operación I/O de 2 segundos
2. Otra función que ejecute la coroutine y mida el tiempo
3. Explicación de por qué usar await asyncio.sleep() en vez de time.sleep()

Contexto: Estoy aprendiendo async Python para usar con FastAPI.
```

**Objetivo**: Genera código base y entiende conceptos fundamentales.

**Validación con Agent**:
```bash
# Usa Python Best Practices Coach para revisar
claude-code --agent python-best-practices-coach "Revisa este código async y dame feedback educativo"
```

#### 1.2 Prompt para Comparar Sync vs Async

```
Genera dos versiones del mismo código:

Versión 1 (Sync): Descarga 5 URLs secuencialmente con requests
Versión 2 (Async): Descarga 5 URLs en paralelo con httpx.AsyncClient

Incluye:
- Medición de tiempo en ambas
- Comentarios explicando las diferencias
- Cuándo usar cada versión

URLs de ejemplo: https://jsonplaceholder.typicode.com/posts/{1-5}
```

**Objetivo**: Visualizar la mejora de performance con async.

#### 1.3 Prompt para FastAPI Async Endpoint

```
Ayúdame a crear un endpoint FastAPI async que:

1. Consulte 3 servicios externos en paralelo (simulado con asyncio.sleep)
2. Use asyncio.gather() para ejecutar en paralelo
3. Maneje errores si algún servicio falla
4. Retorne un consolidado de los 3 servicios

Incluye:
- Tipado correcto con Pydantic
- Manejo de timeouts
- Logs de debug
```

**Objetivo**: Aplicar async en contexto FastAPI real.

**Validación con Agent**:
```bash
# Usa FastAPI Design Coach
claude-code --agent fastapi-design-coach "Revisa este endpoint async y sugiere mejoras"
```

### Fase 2: Debugging Async con IA

#### 2.1 Prompt para Detectar Problemas

```
Analiza este código async y encuentra problemas:

[PEGA TU CÓDIGO AQUÍ]

Busca específicamente:
1. Coroutines que no están siendo "awaited"
2. Uso de funciones blocking (time.sleep, requests.get, etc.)
3. Oportunidades de paralelización con gather()
4. Potenciales deadlocks o race conditions
5. Manejo de errores inadecuado

Dame explicación educativa de cada problema encontrado.
```

**Objetivo**: Aprender a identificar anti-patrones async.

#### 2.2 Prompt para Optimizar Performance

```
Tengo este código async que funciona pero es lento:

[PEGA TU CÓDIGO]

¿Cómo puedo:
1. Reducir el tiempo de ejecución usando paralelización?
2. Evitar blocking calls?
3. Implementar caching si aplica?
4. Usar asyncio.gather() eficientemente?

Dame la versión optimizada con explicación.
```

**Validación con Agent**:
```bash
# Usa Performance Optimizer
claude-code --agent performance-optimizer "Analiza este código async y sugiere optimizaciones"
```

### Fase 3: Testing Async con IA

#### 3.1 Prompt para Generar Tests

```
Genera tests con pytest-asyncio para esta función async:

[PEGA TU FUNCIÓN ASYNC]

Incluye tests para:
1. Caso exitoso
2. Timeout
3. Manejo de errores
4. Múltiples llamadas concurrentes
5. Fixtures async si son necesarias

Usa @pytest.mark.asyncio para marcar tests async.
```

**Objetivo**: Aprender testing de código async.

#### 3.2 Prompt para Test de Performance

```
Ayúdame a crear un test que verifique:

1. Mi función async es más rápida que la versión sync
2. Ejecutar N tareas en paralelo tarda ~lo mismo que 1 tarea
3. El timeout funciona correctamente

Usa time.time() para medir y assert para validar.
```

### Fase 4: Refactoring Sync → Async con IA

#### 4.1 Prompt para Convertir Código

```
Convierte este código síncrono a asíncrono:

[PEGA CÓDIGO SYNC]

Requiero:
1. Identificar qué partes se benefician de async (I/O)
2. Cambiar a librerías async (requests → httpx, open → aiofiles)
3. Agregar async/await apropiadamente
4. Usar asyncio.gather() donde sea posible
5. Mantener la misma funcionalidad

Explica cada cambio realizado.
```

**Objetivo**: Aprender a refactorizar código existente.

**Validación con Agent**:
```bash
# Usa Python Best Practices Coach
claude-code --agent python-best-practices-coach "Revisa esta conversión sync→async"
```

## 🎯 Ejercicios Guiados con IA

### Ejercicio 1: Rate Limiter con IA

**Contexto**: Necesitas un rate limiter async para tu API.

**Prompt Inicial**:
```
Ayúdame a implementar un rate limiter async para FastAPI que:

1. Limite requests por usuario a 10 por minuto
2. Use asyncio.Lock para thread-safety
3. Almacene timestamps en memoria
4. Se use como dependencia FastAPI

Dame la implementación con explicación paso a paso.
```

**Prompt de Mejora**:
```
El rate limiter funciona pero quiero:

1. Agregar sliding window en vez de fixed window
2. Persistir datos en Redis (async)
3. Configurar límites por endpoint

¿Cómo lo mejoro?
```

**Validación con Agent**:
```bash
claude-code --agent fastapi-design-coach "Revisa mi rate limiter async"
```

### Ejercicio 2: Sistema de Notificaciones con IA

**Prompt Inicial**:
```
Diseña un sistema de notificaciones async que:

1. Envíe a 3 canales: email, SMS, push
2. Ejecute envíos en paralelo
3. Reintente automáticamente si falla (max 3 intentos)
4. Registre logs de éxito/error
5. Tenga timeout de 5 segundos por canal

Incluye:
- Clase NotificationService
- Métodos async para cada canal
- Lógica de reintentos
- Endpoint FastAPI que lo use

Estructura completa con código funcional.
```

**Prompt de Testing**:
```
Genera tests pytest-asyncio para el NotificationService que verifiquen:

1. Envío exitoso a todos los canales
2. Reintentos funcionan correctamente
3. Timeout se aplica correctamente
4. Logs se registran adecuadamente
5. Envíos en paralelo son más rápidos que secuenciales

Usa mocks para simular servicios externos.
```

### Ejercicio 3: Web Scraper Async con IA

**Prompt Inicial**:
```
Ayúdame a crear un web scraper async que:

1. Descargue 50 páginas web en paralelo
2. Extraiga títulos de cada página
3. Use asyncio.Queue para gestionar URLs
4. Tenga workers concurrentes (5 workers)
5. Maneje errores por página sin detener todo
6. Implemente rate limiting (max 10 requests/segundo)

Usa httpx.AsyncClient y BeautifulSoup.

Incluye:
- Clase AsyncWebScraper
- Worker function
- Main function que orquesta
- Manejo de errores robusto
```

**Prompt de Optimización**:
```
El scraper funciona pero:

1. Algunas páginas tardan mucho → necesito timeout
2. Quiero cachear resultados → usar Redis
3. Necesito respetar robots.txt → validar antes de scrapear
4. Quiero barra de progreso → usar tqdm

¿Cómo integro estas mejoras?
```

**Validación con Agent**:
```bash
claude-code --agent performance-optimizer "Analiza este web scraper async y optimiza"
```

## 🔍 Prompts para Conceptos Específicos

### Entender Event Loop

```
Explica el event loop de Python como si tuviera 10 años.

Luego dame:
1. Analogía simple (ej: director de orquesta)
2. Diagrama de flujo en ASCII
3. Ejemplo de código que muestra el event loop en acción
4. Qué pasa cuando bloqueas el event loop

Hazlo educativo y memorable.
```

### Async vs Multiprocessing vs Threading

```
Tengo una aplicación que necesita procesar 100 tareas.

Explícame:
1. Cuándo usar async
2. Cuándo usar multiprocessing
3. Cuándo usar threading

Con ejemplos concretos:
- I/O-bound (llamadas API)
- CPU-bound (cálculos matemáticos)
- Mixed workload (I/O + CPU)

Dame tabla comparativa y código de ejemplo.
```

### Debugging Async

```
Mi código async tiene este error:

"RuntimeWarning: coroutine 'mi_funcion' was never awaited"

Explica:
1. ¿Qué significa este error?
2. ¿Por qué ocurre?
3. ¿Cómo lo soluciono?
4. ¿Cómo lo prevengo en el futuro?

Dame 3 ejemplos de código incorrecto y su corrección.
```

## 🎓 Prompts para Profundizar

### Avanzado: Context Managers Async

```
Enseñame async context managers:

1. Qué son y para qué sirven
2. Diferencia con context managers normales
3. Cuándo usarlos (conexiones DB, archivos, HTTP clients)
4. Cómo crearlos con __aenter__ y __aexit__

Incluye ejemplos prácticos con:
- aiofiles para archivos
- httpx.AsyncClient para HTTP
- asyncpg para base de datos
```

### Avanzado: Async Generators

```
Explica async generators en Python:

1. Diferencia entre generator normal y async generator
2. Cuándo usarlos (streaming, procesamiento de datos grandes)
3. yield vs yield await
4. Consumir con async for

Ejemplos:
- Stream de datos desde API paginada
- Procesamiento de archivos CSV grandes
- WebSocket streaming
```

### Avanzado: Asyncio Internals

```
Profundiza en el funcionamiento interno de asyncio:

1. Cómo funciona el event loop a bajo nivel
2. Diferencia entre Task, Future, y Coroutine
3. Qué es un event loop policy
4. Cómo asyncio maneja I/O con select/epoll/kqueue

No quiero solo teoría, dame ejemplos de código que muestren estos conceptos.
```

## 🛠️ Workflow Completo de Desarrollo

### Paso 1: Planificación con IA

```
Voy a crear un endpoint FastAPI que [DESCRIBE TU FUNCIONALIDAD].

Ayúdame a planificar:
1. ¿Qué partes deben ser async?
2. ¿Qué librerías async necesito?
3. ¿Cómo estructuro el código?
4. ¿Qué patrones async debo usar?
5. ¿Qué edge cases debo considerar?

Dame un plan paso a paso antes de codear.
```

### Paso 2: Implementación con IA

```
Siguiendo el plan anterior, ayúdame a implementar:

[PEGA EL PLAN]

Genera código completo con:
- Type hints
- Docstrings
- Manejo de errores
- Logging
- Comentarios explicativos

Hazlo educativo, quiero aprender mientras codifico.
```

### Paso 3: Review con Agentes

```bash
# Usa múltiples agentes para review completo
claude-code --agent python-best-practices-coach "Revisa este código async"
claude-code --agent fastapi-design-coach "Revisa el diseño FastAPI"
claude-code --agent performance-optimizer "Optimiza el performance"
```

### Paso 4: Testing con IA

```
Genera suite de tests completa para este código:

[PEGA TU CÓDIGO]

Incluye:
- Tests unitarios (funciones individuales)
- Tests de integración (flujo completo)
- Tests de performance (verify async is faster)
- Tests de error handling
- Fixtures necesarias

Usa pytest-asyncio y coverage.
```

### Paso 5: Documentación con IA

```
Genera documentación para este código async:

[PEGA TU CÓDIGO]

Incluye:
- README con explicación
- Docstrings completas
- Ejemplos de uso
- Diagramas de flujo (ASCII art)
- Troubleshooting común

Hazlo completo y profesional.
```

## 📊 Métricas de Aprendizaje

Usa IA para evaluar tu progreso:

```
He escrito este código async. Evalúa mi dominio de async Python en escala 1-10:

[PEGA TU CÓDIGO]

Criterios:
1. Uso correcto de async/await
2. Paralelización efectiva
3. Manejo de errores
4. Performance optimization
5. Code quality

Dame feedback constructivo y ejercicios para mejorar.
```

## 🎯 Checklist de Integración IA (40%)

- [ ] Usé IA para generar al menos 2 ejercicios
- [ ] Validé código con Python Best Practices Coach
- [ ] Usé FastAPI Design Coach para endpoints
- [ ] Optimicé performance con Performance Optimizer
- [ ] Generé tests con ayuda de IA
- [ ] Pedí explicaciones de conceptos difíciles
- [ ] Refactoricé código sync→async con IA
- [ ] Debuggué errores async con IA

## 💡 Tips para Usar IA Efectivamente

1. **Sé específico**: En vez de "ayúdame con async", di "ayúdame a convertir esta función sync a async usando httpx"

2. **Pide explicaciones**: Siempre termina con "explica cada cambio realizado"

3. **Itera**: Empieza simple, luego pide mejoras incrementales

4. **Valida con agentes**: Usa los agentes educativos para feedback de calidad

5. **Aprende, no copies**: Entiende cada línea antes de usarla

---

**🤖 Recuerda**: La IA es tu par de programación, no tu sustituto. Usa estos prompts para **aprender**, no solo para obtener código.
