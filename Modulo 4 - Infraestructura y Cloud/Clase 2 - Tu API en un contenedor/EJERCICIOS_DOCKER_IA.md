# Ejercicios Prácticos: Docker + IA

## 🎯 Objetivo

Estos ejercicios te ayudarán a dominar Docker usando IA como asistente, progresando desde conceptos básicos hasta optimizaciones avanzadas.

---

## 📚 Ejercicio 1: De Local a Docker (30 min)

### Objetivo
Containerizar una API existente usando IA, entendiendo cada capa del Dockerfile.

### Contexto
Tienes una API FastAPI funcional en local que necesitas containerizar para compartirla con el equipo.

### Tareas

**Paso 1: Análisis con IA**
```
Rol: DevOps consultant
Contexto: API FastAPI con las siguientes características:
- Python 3.12
- Dependencias en requirements.txt
- Ejecuta con: uvicorn api.api:app --host 0.0.0.0 --port 8000
- Variables de entorno en .env

Tareas:
1. Analizar qué archivos deben copiarse al contenedor
2. Identificar qué archivos NO deben copiarse
3. Sugerir estructura de .dockerignore
4. Explicar el orden óptimo de comandos en Dockerfile

Entrega: Análisis detallado + razonamiento de cada decisión
```

**Paso 2: Generación de Dockerfile**
```
Rol: Docker specialist
Objetivo: Crear Dockerfile para FastAPI con best practices
Requisitos:
- Imagen base: python:3.12-slim
- Instalar dependencias antes de copiar código (cache optimization)
- Exponer puerto 8000
- Usuario no-root
- Health check endpoint /health

Entrega: Dockerfile comentado explicando cada línea
```

**Paso 3: Validación**

Construye y ejecuta:
```bash
docker build -t mi-api:v1 .
docker run -d -p 8000:8000 --name mi-api mi-api:v1
curl http://localhost:8000/health
```

Usa IA para troubleshooting si algo falla:
```
Rol: Docker troubleshooting expert
Contexto: Mi contenedor falla al iniciar
Error: [pegar error aquí]
Dockerfile:
```dockerfile
[pegar Dockerfile]
```

Logs:
```
[pegar docker logs mi-api]
```

Tareas:
1. Identificar causa raíz del error
2. Sugerir solución específica
3. Explicar por qué ocurrió
4. Proveer comando de validación

Entrega: Diagnóstico + solución + prevención
```

**Criterios de aceptación**:
- [ ] Dockerfile funcional
- [ ] .dockerignore configurado
- [ ] Contenedor inicia correctamente
- [ ] Health check responde 200 OK
- [ ] Entiendes cada línea del Dockerfile

---

## 🚀 Ejercicio 2: Docker Compose para Stack Completo (45 min)

### Objetivo
Orquestar API + PostgreSQL + Redis usando docker-compose generado con IA.

### Contexto
Tu API necesita conectarse a una base de datos PostgreSQL y usar Redis para caché. Actualmente corres todo en local pero quieres orquestar los 3 servicios.

### Tareas

**Paso 1: Diseño del stack con IA**
```
Rol: Solutions architect especializado en microservicios
Contexto: Necesito orquestar 3 servicios:
1. API FastAPI (puerto 8000)
2. PostgreSQL 16 (puerto 5432, persistencia de datos)
3. Redis 7 (puerto 6379, caché)

Requisitos:
- API debe esperar a que DB esté healthy antes de iniciar
- Variables de entorno en archivo .env
- Volúmenes para persistencia de DB y Redis
- Health checks obligatorios en todos los servicios
- Networking automático (servicios se comunican por nombre)

Tareas:
1. Diseñar arquitectura del docker-compose
2. Explicar cómo se comunicarán los servicios
3. Definir estrategia de health checks
4. Sugerir configuración de volúmenes

Entrega: Diagrama de arquitectura + justificación de decisiones
```

**Paso 2: Generación de docker-compose.yml**
```
Rol: Docker Compose expert
Objetivo: Crear docker-compose.yml basado en el diseño anterior
Especificaciones:
- API: build desde Dockerfile local, depends_on DB y Redis
- DB: PostgreSQL 16-alpine, health check con pg_isready
- Redis: Redis 7-alpine, health check con redis-cli ping
- Networking: red automática llamada "app-network"
- Volúmenes: postgres_data, redis_data

Restricciones:
- No usar environment directo (usar env_file: .env)
- Restart policy: unless-stopped
- Health checks con intervals razonables (10-30s)

Entrega: docker-compose.yml completo + .env.template
```

**Paso 3: Testing del stack**

1. Iniciar servicios:
   ```bash
   docker-compose up -d
   ```

2. Verificar health:
   ```bash
   docker-compose ps  # Todos deben estar "healthy"
   ```

3. Probar conectividad:
   ```bash
   # API responde
   curl http://localhost:8000/health

   # DB accesible desde API
   docker-compose exec api python -c "import psycopg2; print('DB OK')"

   # Redis accesible desde API
   docker-compose exec api python -c "import redis; r=redis.Redis(host='redis'); r.ping(); print('Redis OK')"
   ```

4. Validar persistencia:
   ```bash
   # Insertar dato en DB
   # Reiniciar todo
   docker-compose down
   docker-compose up -d
   # Verificar que dato persiste
   ```

**Paso 4: Troubleshooting con IA**

Si algo falla, usa IA:
```
Rol: DevOps troubleshooting specialist
Contexto: Docker Compose stack falla
Síntoma: [Describir síntoma, ej: "API no puede conectar a DB"]
docker-compose.yml:
```yaml
[pegar configuración]
```

Logs relevantes:
```
[docker-compose logs api]
[docker-compose logs db]
```

Tareas:
1. Diagnosticar causa raíz
2. Explicar el problema de networking/timing/configuración
3. Sugerir 2-3 soluciones
4. Proveer comandos de validación

Entrega: Fix específico + explicación técnica
```

**Criterios de aceptación**:
- [ ] Stack completo levanta con `docker-compose up`
- [ ] Todos los servicios están "healthy"
- [ ] API puede conectarse a DB y Redis
- [ ] Datos persisten después de `docker-compose down && up`
- [ ] Validado con Docker Infrastructure Guide agent

---

## ⚡ Ejercicio 3: Optimización con Multi-Stage Builds (40 min)

### Objetivo
Reducir el tamaño de tu imagen Docker >50% usando multi-stage builds generados con IA.

### Contexto
Tu Dockerfile actual genera una imagen de ~500MB porque incluye todas las dependencias de desarrollo (pytest, black, ruff, etc.). En producción solo necesitas las de runtime.

### Tareas

**Paso 1: Baseline measurement**

```bash
# Construir imagen actual
docker build -t api-tareas:baseline .

# Medir tamaño
docker images api-tareas:baseline
# Anotar tamaño (ej: 527MB)
```

**Paso 2: Análisis de dependencias con IA**

```
Rol: Python dependency analyst
Contexto: requirements.txt con 25 dependencias
Objetivo: Identificar qué es runtime vs development

requirements.txt:
```
fastapi==0.118.0
uvicorn==0.37.0
pydantic==2.11.10
sqlalchemy==2.0.31
psycopg2-binary==2.9.9
redis==5.0.0
python-jose[cryptography]==3.3.0
# ... (pegar todas)
```

Tareas:
1. Clasificar cada dependencia en runtime/dev/test
2. Crear requirements-prod.txt (solo runtime)
3. Crear requirements-dev.txt (dev + test)
4. Estimar reducción de tamaño esperada

Entrega: 2 archivos requirements + análisis de reducción
```

**Paso 3: Generación de Dockerfile multi-stage**

```
Rol: Docker optimization specialist
Contexto: Necesito reducir imagen de 500MB a <150MB
Objetivo: Crear Dockerfile multi-stage con 2 etapas

Stage 1 (builder):
- Nombre: "builder"
- Instalar gcc y dependencias de compilación
- Crear virtualenv en /opt/venv
- Instalar requirements-prod.txt

Stage 2 (runtime):
- Imagen base: python:3.12-slim
- Copiar virtualenv del builder
- Copiar solo carpeta api/ (no tests, docs, etc)
- Usuario no-root (uid 1000)
- Health check incluido
- CMD con uvicorn

Restricciones:
- Sin apt-get en stage runtime (todo en builder)
- Usar .dockerignore para excluir archivos innecesarios
- Layers optimizadas (requirements antes que código)

Entrega: Dockerfile multi-stage + .dockerignore actualizado
```

**Paso 4: Build y comparación**

```bash
# Build optimizado
docker build -f Dockerfile.multistage -t api-tareas:optimized .

# Comparar tamaños
docker images | grep api-tareas

# Resultado esperado:
# api-tareas:baseline    527MB
# api-tareas:optimized   142MB  (73% reducción!)
```

**Paso 5: Validación funcional**

```bash
# Ejecutar imagen optimizada
docker run -d -p 8000:8000 --name api-opt api-tareas:optimized

# Probar funcionalidad
curl http://localhost:8000/health
curl http://localhost:8000/tareas

# Verificar que todo funciona igual
```

**Paso 6: Análisis de capas con IA**

```
Rol: Docker image analyst
Contexto: Quiero entender qué ocupa espacio en mi imagen
Objetivo: Analizar capas de la imagen optimizada

Ejecutar:
```bash
docker history api-tareas:optimized
```

Output:
```
[pegar output aquí]
```

Tareas:
1. Identificar las 5 capas más grandes
2. Explicar qué contiene cada una
3. Sugerir si hay optimizaciones adicionales posibles
4. Comparar con imagen baseline

Entrega: Análisis de capas + recomendaciones adicionales
```

**Criterios de aceptación**:
- [ ] Reducción de tamaño >50% respecto a baseline
- [ ] Imagen optimizada funciona correctamente
- [ ] Usuario no-root configurado
- [ ] Health check funcional
- [ ] Solo dependencias de runtime incluidas
- [ ] Validado con Docker Infrastructure Guide agent

---

## 🔧 Ejercicio 4: Debugging Avanzado con IA (35 min)

### Objetivo
Diagnosticar y resolver problemas comunes de Docker usando IA como asistente.

### Escenarios

#### Escenario A: Contenedor crashea al iniciar

**Síntomas**:
```bash
docker-compose up
# api_1 exited with code 1
```

**Logs**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**Tarea**: Usa IA para diagnosticar

```
Rol: Docker troubleshooting expert
Contexto: Contenedor falla con ModuleNotFoundError
Dockerfile:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.api:app"]
```

Logs:
```
ModuleNotFoundError: No module named 'fastapi'
```

Tareas:
1. Identificar por qué pip install no funcionó
2. Verificar si requirements.txt se copió correctamente
3. Sugerir cómo debuggear step by step
4. Proveer Dockerfile corregido

Entrega: Diagnóstico + solución + comandos de validación
```

#### Escenario B: Networking entre contenedores falla

**Síntomas**:
```bash
# Dentro del contenedor API
curl http://db:5432
# curl: (6) Could not resolve host: db
```

**Tarea**: Debug con IA

```
Rol: Docker networking specialist
Contexto: API no puede resolver hostname "db"
docker-compose.yml:
```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:16-alpine
```

Error:
```
Could not resolve host: db
```

Tareas:
1. Explicar por qué no se resuelve el hostname
2. Verificar configuración de networking
3. Sugerir comandos para debuggear networking
4. Proveer docker-compose.yml corregido

Comandos útiles:
```bash
docker network ls
docker network inspect [network-name]
docker-compose exec api cat /etc/hosts
docker-compose exec api ping db
```

Entrega: Diagnóstico de networking + solución
```

#### Escenario C: Variables de entorno no cargan

**Síntomas**:
```python
# En la API
os.getenv("DATABASE_URL")  # Returns None
```

**Tarea**: Debug con IA

```
Rol: Docker environment configuration expert
Contexto: Variables de entorno no se cargan en contenedor
.env file:
```
DATABASE_URL=postgresql://user:pass@db:5432/mydb
REDIS_URL=redis://redis:6379
```

docker-compose.yml:
```yaml
services:
  api:
    build: .
    env_file:
      - .env
```

Problema: os.getenv("DATABASE_URL") retorna None

Tareas:
1. Verificar que .env se esté cargando
2. Validar sintaxis de variables
3. Explicar precedencia de env variables en Docker
4. Proveer comandos de debugging

Comandos útiles:
```bash
docker-compose exec api env | grep DATABASE
docker-compose config  # Ver configuración final
```

Entrega: Diagnóstico + solución paso a paso
```

**Criterios de aceptación**:
- [ ] Los 3 escenarios diagnosticados correctamente
- [ ] Soluciones aplicadas y validadas
- [ ] Proceso de debugging documentado
- [ ] Comandos de debugging dominados

---

## 🏆 Ejercicio Final: Production-Ready Stack (60 min)

### Objetivo
Crear un stack completo listo para producción usando IA, aplicando todos los conceptos aprendidos.

### Requisitos del Stack

1. **API FastAPI**:
   - Multi-stage Dockerfile (<150MB)
   - Usuario no-root
   - Health check funcional
   - Logs a stdout

2. **PostgreSQL**:
   - Datos persistentes en volumen
   - Health check configurado
   - Credenciales en variables de entorno

3. **Redis**:
   - Datos persistentes
   - Health check
   - Configuración custom si es necesario

4. **Nginx** (bonus):
   - Reverse proxy para API
   - Servir archivos estáticos
   - HTTPS con certificado autofirmado

### Workflow con IA

**Fase 1: Diseño de arquitectura**
```
Rol: Solutions architect
Objetivo: Diseñar stack production-ready para FastAPI + PostgreSQL + Redis + Nginx
Requisitos:
- API escalable (preparada para múltiples instancias)
- Datos persistentes y backups automáticos
- Health checks en todos los servicios
- Logging centralizado
- Secrets management adecuado
- HTTPS en Nginx

Tareas:
1. Diseñar arquitectura de servicios
2. Definir estrategia de networking
3. Planear persistencia de datos
4. Configurar monitoring básico

Entrega: Diagrama + docker-compose.yml esqueleto
```

**Fase 2: Implementación**

Genera con IA:
1. Dockerfile multi-stage para API
2. docker-compose.yml completo
3. Configuración de Nginx
4. Scripts de inicialización de DB
5. Health checks custom

**Fase 3: Validación completa**

Usa Docker Infrastructure Guide agent para validar:
- [ ] Multi-stage builds optimizados
- [ ] Health checks completos
- [ ] Volúmenes correctamente configurados
- [ ] Networking seguro
- [ ] Secrets no hardcodeados
- [ ] Restart policies apropiadas
- [ ] Logging configurado

**Fase 4: Testing end-to-end**

```bash
# Iniciar stack
docker-compose up -d

# Verificar health
docker-compose ps  # Todos "healthy"

# Probar API vía Nginx
curl https://localhost/api/health

# Insertar datos
curl -X POST https://localhost/api/tareas -d '{"nombre":"Test"}'

# Verificar persistencia
docker-compose restart db
# Datos siguen ahí

# Revisar logs
docker-compose logs -f api
```

**Criterios de aceptación**:
- [ ] Stack completo funcional (API + DB + Redis + Nginx)
- [ ] Todos los servicios healthy
- [ ] HTTPS configurado
- [ ] Datos persisten entre reinicios
- [ ] Health checks funcionan
- [ ] Logging visible y útil
- [ ] Validado con Docker Infrastructure Guide
- [ ] Documentación completa del stack

---

## 📊 Rúbrica de Evaluación

| Ejercicio | Peso | Criterios |
|-----------|------|-----------|
| 1. Local a Docker | 20% | Dockerfile funcional, .dockerignore, troubleshooting básico |
| 2. Docker Compose | 25% | Stack orquestado, health checks, persistencia, networking |
| 3. Multi-Stage | 25% | Reducción >50%, funcionalidad completa, optimización |
| 4. Debugging | 15% | 3 escenarios resueltos, comandos dominados |
| 5. Production Stack | 15% | Stack completo, HTTPS, validación con agents |

**Total**: 100%

**Mínimo aprobatorio**: 70% (dominas Docker con IA como asistente)

---

## 🎯 Objetivos de Aprendizaje Alcanzados

Al completar estos ejercicios, habrás demostrado que puedes:

✅ **Generar Dockerfiles** con IA y entender cada línea
✅ **Orquestar servicios** con docker-compose generado con IA
✅ **Optimizar imágenes** usando multi-stage builds (>50% reducción)
✅ **Diagnosticar problemas** de containers con asistencia de IA
✅ **Validar configuraciones** usando agentes educativos especializados
✅ **Crear stacks production-ready** aplicando best practices

**Tiempo total estimado**: 3-4 horas
**Tiempo ahorrado con IA vs manual**: ~40-50% (~5-6 horas manual)

---

## 📚 Recursos de Apoyo

**Agentes educativos**:
- Docker Infrastructure Guide: `.claude/agents/educational/docker-infrastructure-guide.md`
- FastAPI Design Coach: `.claude/agents/educational/fastapi-design-coach.md`

**Documentación**:
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

**Comandos útiles**:
```bash
# Debugging
docker logs <container>
docker exec -it <container> /bin/bash
docker inspect <container>
docker stats

# Cleanup
docker system prune -a
docker volume prune

# Networking
docker network ls
docker network inspect <network>
```
