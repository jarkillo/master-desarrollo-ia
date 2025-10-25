# AI Workflow - Clase 2: Containerización Avanzada con IA

## 🎯 Objetivos de Aprendizaje con IA

En esta clase aprenderás a usar IA como asistente para:

1. **Generar docker-compose.yml** para orquestación multi-contenedor
2. **Crear multi-stage builds** para optimizar tamaño de imágenes
3. **Troubleshooting de contenedores** con asistencia de IA
4. **Validar configuraciones** usando agentes especializados

---

## 🔄 Workflow Completo: De Dockerfile a Docker Compose

### Fase 1: Generación de docker-compose con IA

**Contexto**: Ya tienes un Dockerfile funcional (Clase 1). Ahora necesitas orquestar múltiples servicios (API + Database + Redis).

#### Prompt 1: Generar docker-compose básico

```
Rol: Ingeniero DevOps experto en Docker Compose
Contexto: Tengo una API FastAPI en Docker (puerto 8000) y necesito añadir PostgreSQL y Redis
Objetivo: Crear docker-compose.yml para desarrollo local
Restricciones:
- Usar volúmenes para persistencia de datos
- Configurar networking automático entre servicios
- Variables de entorno en archivo .env separado
- Health checks para todos los servicios

Entrega: docker-compose.yml completo y .env.template
```

**Resultado esperado**:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./api:/app/api
    command: uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

#### Validación con Docker Infrastructure Guide

Después de generar el docker-compose, usa el agente educativo:

```bash
# Invocar Docker Infrastructure Guide agent
# El agente revisará:
# ✓ Health checks están configurados
# ✓ Volumes para persistencia de datos
# ✓ Networking está configurado correctamente
# ✓ Restart policies apropiadas
# ✓ Nombres de servicios son descriptivos
```

---

### Fase 2: Multi-Stage Builds con IA

**Problema**: Tu imagen Docker actual pesa 500MB+ porque incluye dependencias de desarrollo.

#### Prompt 2: Optimizar Dockerfile con multi-stage build

```
Rol: Especialista en optimización de Docker
Contexto: Mi Dockerfile actual genera una imagen de 500MB con todas las dependencias
Objetivo: Crear multi-stage build que separe build de runtime
Restricciones:
- Imagen final < 150MB
- Incluir solo dependencias de producción
- Usar Python 3.12-slim como base
- Copiar solo archivos necesarios en runtime

Entrega: Dockerfile multi-stage optimizado
```

**Resultado esperado**:

```dockerfile
# Stage 1: Builder (dependencias de desarrollo)
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements y crear virtualenv
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (solo lo necesario)
FROM python:3.12-slim

WORKDIR /app

# Copiar virtualenv del builder
COPY --from=builder /opt/venv /opt/venv

# Configurar PATH para usar virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar solo el código de la aplicación
COPY api/ ./api/

# Usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando de inicio
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Comparación de tamaños

Ejecuta y compara:

```bash
# Dockerfile original
docker build -f Dockerfile.original -t api-tareas:original .
docker images api-tareas:original

# Dockerfile multi-stage
docker build -f Dockerfile -t api-tareas:optimized .
docker images api-tareas:optimized

# Resultado esperado:
# original:   ~500MB
# optimized:  ~120-150MB  (70% reducción!)
```

---

### Fase 3: Troubleshooting con IA

#### Escenario 1: Contenedor no inicia

**Síntoma**: `docker-compose up` falla con error "Exited with code 1"

**Debugging asistido por IA**:

```
Rol: DevOps engineer experto en troubleshooting de Docker
Contexto: Mi contenedor de API falla al iniciar con código 1
Logs:
```
[Pegar logs del contenedor aquí]
```

Tareas:
1. Identificar la causa raíz del error
2. Sugerir 3 posibles soluciones ordenadas por probabilidad
3. Explicar cómo prevenir este error en el futuro

Entrega: Diagnóstico con soluciones paso a paso
```

**Comandos útiles para obtener información**:

```bash
# Ver logs del contenedor
docker-compose logs api

# Ver logs en tiempo real
docker-compose logs -f api

# Inspeccionar contenedor
docker inspect <container_id>

# Ejecutar comando dentro del contenedor (debugging)
docker-compose exec api /bin/bash

# Ver procesos en el contenedor
docker-compose exec api ps aux

# Ver variables de entorno
docker-compose exec api env
```

#### Escenario 2: API responde lento dentro de Docker

**Debugging de performance con IA**:

```
Rol: Especialista en performance de aplicaciones containerizadas
Contexto: Mi API responde en 2ms localmente pero 500ms en Docker
Objetivo: Identificar el cuello de botella
Información:
- Docker Desktop en Windows 11
- API FastAPI + SQLAlchemy
- Base de datos PostgreSQL en contenedor separado

Tareas:
1. Revisar configuración de networking en docker-compose
2. Verificar si hay problemas de I/O con volúmenes
3. Sugerir optimizaciones específicas para Windows

Entrega: Checklist de optimización con impacto esperado
```

---

### Fase 4: Validación Completa con Agentes

#### Checklist de Validación Docker Infrastructure Guide

Después de completar tu docker-compose y Dockerfile multi-stage, valida con:

```markdown
Validación con Docker Infrastructure Guide:

**Dockerfile Multi-Stage**:
- [ ] Usa multi-stage build para separar build de runtime
- [ ] Imagen final < 200MB
- [ ] Usuario no-root configurado
- [ ] Health check implementado
- [ ] Solo archivos necesarios en imagen final
- [ ] .dockerignore configurado

**docker-compose.yml**:
- [ ] Health checks en todos los servicios
- [ ] Depends_on con condition: service_healthy
- [ ] Volúmenes para persistencia de datos
- [ ] Networking automático configurado
- [ ] Variables de entorno en archivo .env
- [ ] Restart policies apropiadas (restart: unless-stopped)

**Seguridad**:
- [ ] No hay secretos hardcodeados en Dockerfile/docker-compose
- [ ] Imágenes base son versiones específicas (no :latest)
- [ ] Contenedores corren como usuario no-root
- [ ] Puertos expuestos solo los necesarios

**Performance**:
- [ ] Layers optimizadas (COPY requirements antes que código)
- [ ] pip install con --no-cache-dir
- [ ] apt-get con --no-install-recommends y rm -rf /var/lib/apt/lists/*
```

---

## 🎓 Ejercicios Prácticos con IA

### Ejercicio 1: De Docker a Docker Compose (20 min)

**Objetivo**: Migrar tu API de Dockerfile standalone a docker-compose con base de datos.

**Tareas**:
1. Usa IA para generar docker-compose.yml que incluya:
   - Servicio `api` (tu FastAPI app)
   - Servicio `db` (PostgreSQL 16-alpine)
   - Networking entre servicios
   - Persistencia de datos con volúmenes

2. Valida con Docker Infrastructure Guide que:
   - Health checks están configurados
   - Database está lista antes de que API inicie
   - Datos persisten después de `docker-compose down`

3. Prueba el sistema:
   ```bash
   docker-compose up -d
   docker-compose ps  # Verificar que todos están "healthy"
   curl http://localhost:8000/tareas  # API funciona
   docker-compose down -v  # Limpiar todo
   ```

**Criterios de aceptación**:
- [ ] docker-compose.yml funcional
- [ ] Base de datos accesible desde API
- [ ] Datos persisten entre reinicios (excepto con -v)
- [ ] Agent valida configuración sin errores críticos

---

### Ejercicio 2: Multi-Stage Build Challenge (30 min)

**Objetivo**: Optimizar tu Dockerfile actual usando multi-stage builds.

**Baseline**: Mide el tamaño actual
```bash
docker build -t api-tareas:original .
docker images api-tareas:original  # Anota el tamaño
```

**Tareas**:
1. Usa IA para crear Dockerfile multi-stage con:
   - Stage 1 (builder): Instala dependencias
   - Stage 2 (runtime): Solo lo necesario para ejecutar
   - Usuario no-root
   - Health check

2. Compara tamaños:
   ```bash
   docker build -t api-tareas:optimized .
   docker images api-tareas:optimized
   ```

3. Valida funcionalidad:
   ```bash
   docker run -p 8000:8000 api-tareas:optimized
   curl http://localhost:8000/health
   ```

**Criterios de aceptación**:
- [ ] Reducción de tamaño > 50%
- [ ] API funciona correctamente
- [ ] Contenedor corre como usuario no-root
- [ ] Health check responde correctamente
- [ ] Agent valida optimizaciones aplicadas

---

### Ejercicio 3: Troubleshooting Simulation (25 min)

**Objetivo**: Diagnosticar y resolver problemas comunes de Docker con IA.

**Escenarios preparados**:

#### Escenario A: Variable de entorno faltante
```yaml
# docker-compose.yml
services:
  api:
    build: .
    # ❌ Falta DATABASE_URL
    ports:
      - "8000:8000"
```

**Tarea**: Usa IA para diagnosticar por qué la API no puede conectar a la base de datos.

#### Escenario B: Volumen mal configurado
```yaml
volumes:
  - ./api:/app/api:ro  # ❌ Read-only impide writes de logs
```

**Tarea**: Debugging con IA para entender por qué fallan los logs.

#### Escenario C: Puerto ya en uso
```bash
# Error: bind: address already in use
```

**Tarea**: Usa IA para generar soluciones (cambiar puerto, matar proceso, usar otro host).

**Criterios de aceptación**:
- [ ] Todos los escenarios diagnosticados correctamente
- [ ] Soluciones aplicadas y validadas
- [ ] Documentado el proceso de debugging en notes.md

---

## 📚 Prompts Reutilizables

### Prompt: Generar docker-compose para stack completo

```
Rol: DevOps engineer con experiencia en microservicios
Contexto: Necesito orquestar [número] servicios: [lista de servicios]
Objetivo: Crear docker-compose.yml para desarrollo local
Restricciones:
- Networking automático entre servicios
- Health checks obligatorios
- Volúmenes para persistencia
- Variables de entorno en .env
- Restart policies configuradas

Stack técnico:
- [Servicio 1]: [Tecnología y versión]
- [Servicio 2]: [Tecnología y versión]

Entrega: docker-compose.yml + .env.template + README con instrucciones de inicio
```

### Prompt: Optimizar Dockerfile existente

```
Rol: Especialista en optimización de contenedores Docker
Contexto: Mi Dockerfile actual pesa [tamaño] y quiero reducirlo
Objetivo: Aplicar multi-stage build y best practices
Restricciones:
- Usar [imagen base] como runtime
- Incluir solo dependencias de producción
- Usuario no-root obligatorio
- Health check implementado
- Imagen final < [tamaño objetivo]

Dockerfile actual:
```
[Pegar Dockerfile aquí]
```

Entrega: Dockerfile optimizado con comentarios explicando cada mejora
```

### Prompt: Troubleshooting de contenedor

```
Rol: DevOps troubleshooting specialist
Contexto: Mi contenedor [nombre] falla al iniciar
Síntoma: [Descripción del error]
Logs:
```
[Pegar logs aquí]
```

Información adicional:
- docker-compose.yml: [Pegar configuración]
- Dockerfile: [Pegar si es relevante]
- Variables de entorno: [Listar sin valores sensibles]

Tareas:
1. Identificar causa raíz
2. Sugerir 3 soluciones ordenadas por probabilidad de éxito
3. Explicar cómo prevenir este error en el futuro
4. Comandos específicos de Docker para validar la solución

Entrega: Diagnóstico detallado + pasos de resolución + prevención
```

---

## 🔍 Validación Final con Agents

Antes de dar por completada la clase, ejecuta este checklist:

### Docker Infrastructure Guide Validation

```markdown
**Multi-Stage Builds**:
- [ ] ¿Dockerfile usa multi-stage build?
- [ ] ¿Imagen final < 200MB?
- [ ] ¿Solo dependencias de runtime en imagen final?
- [ ] ¿Layers optimizadas (requirements antes que código)?

**Docker Compose**:
- [ ] ¿Todos los servicios tienen health checks?
- [ ] ¿depends_on usa conditions (service_healthy)?
- [ ] ¿Volúmenes configurados para persistencia?
- [ ] ¿Variables de entorno en archivo .env?

**Seguridad**:
- [ ] ¿Contenedores corren como usuario no-root?
- [ ] ¿No hay secretos hardcodeados?
- [ ] ¿Imágenes base son versiones específicas (no :latest)?

**Networking**:
- [ ] ¿Servicios pueden comunicarse entre sí?
- [ ] ¿Puertos expuestos solo los necesarios?
- [ ] ¿DNS interno de Docker funciona? (service names)
```

### FastAPI Design Coach Validation

```markdown
**API Containerization**:
- [ ] ¿API responde correctamente en contenedor?
- [ ] ¿Health check endpoint funcional?
- [ ] ¿Variables de entorno se leen correctamente?
- [ ] ¿CORS configurado si hay frontend?
- [ ] ¿Logs se escriben a stdout/stderr (no archivos)?
```

---

## 🎯 Resultado Esperado

Al finalizar esta clase, deberías tener:

1. **docker-compose.yml** funcional con API + DB + Redis
2. **Dockerfile multi-stage** optimizado (<150MB)
3. **Troubleshooting skills** con asistencia de IA
4. **Configuraciones validadas** por agentes educativos
5. **Documentación** del proceso en notes.md

**Tamaño total del sistema containerizado**:
- Antes: 1 contenedor de ~500MB
- Después: 3 contenedores (~120MB API + ~200MB PostgreSQL + ~30MB Redis = ~350MB total)

---

## 📖 Recursos Adicionales

**Documentación oficial**:
- [Docker Compose documentation](https://docs.docker.com/compose/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Best practices for Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

**Agentes educativos**:
- Docker Infrastructure Guide: `.claude/agents/educational/docker-infrastructure-guide.md`
- FastAPI Design Coach: `.claude/agents/educational/fastapi-design-coach.md`

**Herramientas de debugging**:
- `docker logs <container>` - Ver logs del contenedor
- `docker exec -it <container> /bin/bash` - Shell interactivo
- `docker inspect <container>` - Inspeccionar configuración
- `docker stats` - Ver uso de recursos en tiempo real
- `docker-compose top` - Ver procesos de todos los servicios
