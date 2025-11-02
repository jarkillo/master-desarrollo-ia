# 🚀 Deployment con Easypanel en tu VPS

**Stack**: Easypanel + Docker + VPS propio
**Tiempo estimado**: 30-45 minutos
**Ventajas**: Control total, sin límites, datos persisten, gratis (solo pagas el VPS)

---

## 📚 ¿Qué es Easypanel?

Easypanel es un panel de control moderno para VPS que facilita el deployment de aplicaciones Docker. Es como tener tu propio Heroku/Railway/Vercel pero en tu servidor.

**Analogía**: Es como tener Docker Desktop pero en la nube con interfaz web bonita.

---

## 🎯 Arquitectura del Deployment

```
Tu VPS con Easypanel
├── Backend Container (FastAPI:8000)
│   └── SQLite Database (persistent volume)
├── Frontend Container (Nginx:80)
│   └── React build servido por Nginx
└── Easypanel Panel (Puerto 3000)
```

**Todo en un solo servidor**, comunicación directa entre containers.

---

## 📋 Prerrequisitos

- ✅ VPS con Easypanel instalado
- ✅ Dominio apuntando a tu VPS (opcional pero recomendado)
- ✅ Docker Desktop en tu máquina local (para testear)
- ✅ Git con acceso a tu repositorio

---

## 🏗️ Opción 1: Deployment con Docker Compose (Recomendado)

Esta opción despliega backend + frontend juntos con un solo comando.

### Paso 1: Preparar Variables de Entorno

En tu VPS, crea el archivo `.env`:

```bash
# Conectarse a tu VPS por SSH
ssh usuario@tu-vps-ip

# Crear directorio para el proyecto
mkdir -p ~/ai-dev-academy-game
cd ~/ai-dev-academy-game

# Clonar el repositorio
git clone https://github.com/tu-usuario/master-ia-manu.git .

# Ir al directorio del juego
cd ai-dev-academy-game

# Crear archivo .env desde el template
cp .env.production.example .env

# Editar el .env
nano .env
```

**Contenido del `.env`**:

```bash
# Frontend URL (tu dominio o IP del VPS)
FRONTEND_URL=http://tu-vps-ip

# Backend URL (mismo VPS, puerto 8000)
BACKEND_URL=http://tu-vps-ip:8000

# Secret key (generar uno seguro)
SECRET_KEY=tu-secret-key-aqui-min-32-chars
```

**Generar SECRET_KEY seguro**:

```bash
# En tu VPS
openssl rand -hex 32
# Copia el resultado y pégalo en SECRET_KEY
```

### Paso 2: Configurar Docker Compose Override para Easypanel

**⚠️ CRÍTICO**: Easypanel usa su propio proxy (Traefik) en el puerto 80. Necesitamos evitar conflictos de puertos.

```bash
# Copiar override específico para Easypanel
cp docker-compose.override.example.yml docker-compose.override.yml
```

**¿Qué hace esto?**
- Quita la exposición directa de puertos (Easypanel los maneja)
- Deja que el proxy de Easypanel maneje el routing
- Evita el error: "Bind for 0.0.0.0:80 failed: port is already allocated"

**NOTA**: Este archivo override solo debe usarse en VPS con Easypanel. En desarrollo local, NO lo copies.

### Paso 3: Build y Deploy con Docker Compose

```bash
# Asegúrate de estar en ai-dev-academy-game/
cd ~/ai-dev-academy-game/ai-dev-academy-game

# Build y levantar los containers
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f

# Ver solo logs del backend
docker-compose logs -f backend

# Ver solo logs del frontend
docker-compose logs -f frontend
```

**Tiempos esperados**:
- Build backend: ~3-5 minutos (primera vez)
- Build frontend: ~4-6 minutos (primera vez)
- Deploy: ~10 segundos

### Paso 4: Verificar que está funcionando

```bash
# Health check del backend
curl http://localhost:8000/health
# Esperado: {"status":"healthy"}

# Health check del frontend
curl http://localhost/health
# Esperado: healthy

# Ver containers corriendo
docker-compose ps

# Deberías ver:
# ai-dev-academy-backend   Up   8000/tcp, healthy
# ai-dev-academy-frontend  Up   80/tcp, healthy
```

### Paso 5: Abrir puertos en el firewall

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 80/tcp
sudo ufw allow 8000/tcp
sudo ufw status

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### Paso 6: Probar desde tu navegador

```
Frontend: http://tu-vps-ip
Backend API Docs: http://tu-vps-ip:8000/docs
```

**Si funciona**: ¡Deployment completo! 🎉

---

## 🎨 Opción 2: Deployment con Easypanel UI

Si prefieres usar la interfaz de Easypanel:

### Paso 2.1: Crear Proyecto en Easypanel

1. Abre Easypanel: `http://tu-vps-ip:3000`
2. Login con tus credenciales
3. Click en "Create Project"
4. Nombre: `ai-dev-academy-game`

### Paso 2.2: Crear Servicio Backend

1. En el proyecto, click "Add Service"
2. Tipo: "App from GitHub"
3. Conecta tu GitHub (si no está conectado)
4. Selecciona tu repo: `tu-usuario/master-ia-manu`
5. Branch: `main` o `dev`
6. Build Pack: "Dockerfile"
7. Dockerfile Path: `ai-dev-academy-game/backend/Dockerfile`
8. Port: `8000`

**Variables de Entorno**:
```
ENVIRONMENT=production
DATABASE_URL=sqlite:///./data/ai_dev_academy.db
ALLOWED_ORIGINS=http://tu-vps-ip
SECRET_KEY=[generar con openssl rand -hex 32]
API_TITLE=AI Dev Academy API
API_VERSION=1.0.0
```

9. Enable "Persistent Volume":
   - Mount Path: `/app/data`
   - Size: 1GB

10. Click "Deploy"

### Paso 2.3: Crear Servicio Frontend

1. Click "Add Service" nuevamente
2. Tipo: "App from GitHub"
3. Mismo repo
4. Build Pack: "Dockerfile"
5. Dockerfile Path: `ai-dev-academy-game/frontend/Dockerfile`
6. Port: `80`

**Build Arguments**:
```
VITE_API_URL=http://tu-vps-ip:8000
VITE_DEFAULT_PLAYER_ID=1
VITE_ENVIRONMENT=production
```

7. Click "Deploy"

### Paso 2.4: Configurar Dominio (Opcional)

En Easypanel:

1. Ve al servicio Frontend
2. Click en "Domains"
3. Agrega tu dominio: `game.tudominio.com`
4. Easypanel configurará automáticamente SSL con Let's Encrypt

Luego actualiza el backend:

**En Variables de Entorno del Backend**:
```
ALLOWED_ORIGINS=https://game.tudominio.com
```

---

## 🔧 Testeo Local con Docker Desktop

Antes de desplegar al VPS, puedes testear localmente:

### En Windows con Docker Desktop:

```bash
# Abrir PowerShell o Git Bash
cd ai-dev-academy-game

# Crear .env local
copy .env.production.example .env

# Editar .env:
# FRONTEND_URL=http://localhost
# BACKEND_URL=http://localhost:8000
# SECRET_KEY=test-secret-key-32-chars-minimum

# Build y levantar
docker-compose up --build

# En otra terminal, testear
curl http://localhost:8000/health
curl http://localhost/health

# Abrir en navegador
start http://localhost
```

**Si funciona local**, funcionará en el VPS.

---

## ✅ Post-Deployment: Validación

### Script de Validación

```bash
# En tu VPS
chmod +x ai-dev-academy-game/scripts/validate-deployment.sh

# Ejecutar
./ai-dev-academy-game/scripts/validate-deployment.sh

# Ingresa:
# Backend URL: http://tu-vps-ip:8000
# Frontend URL: http://tu-vps-ip
```

### Validación Manual

```bash
# Backend Health
curl http://tu-vps-ip:8000/health

# Frontend Health
curl http://tu-vps-ip/health

# API Docs
curl http://tu-vps-ip:8000/docs

# Bug Hunt API
curl -X POST http://tu-vps-ip:8000/api/minigames/bug-hunt/start \
  -H "Content-Type: application/json" \
  -d '{"player_id": 1, "difficulty": "easy"}'
```

### En Navegador

1. Abre `http://tu-vps-ip`
2. F12 → Console
3. Verifica NO hay errores CORS
4. Prueba Bug Hunt game
5. Verifica XP se otorga
6. Check Leaderboard

---

## 🔄 Actualizar la Aplicación

### Con Docker Compose:

```bash
# SSH a tu VPS
ssh usuario@tu-vps-ip

# Ir al directorio
cd ~/ai-dev-academy-game/ai-dev-academy-game

# Pull últimos cambios
git pull origin main

# Rebuild y redeploy
docker-compose down
docker-compose up -d --build

# Ver logs
docker-compose logs -f
```

### Con Easypanel UI:

1. Push cambios a GitHub
2. En Easypanel, click "Redeploy" en cada servicio
3. Easypanel hace pull automático y rebuild

---

## 📊 Monitoreo

### Ver Logs

```bash
# Con Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# Últimas 100 líneas
docker-compose logs --tail=100 backend
```

### Ver Recursos

```bash
# CPU y Memoria de containers
docker stats

# Espacio en disco
docker system df

# Limpiar imágenes antiguas
docker system prune -a
```

### Con Easypanel

1. Ve al servicio en Easypanel
2. Click en "Logs" para ver logs en tiempo real
3. Click en "Metrics" para ver CPU/Memoria

---

## 🚨 Troubleshooting

### Error: "Cannot connect to backend"

**Síntoma**: Frontend carga pero no se conecta al backend

**Solución**:
```bash
# Verificar backend está UP
docker-compose ps
curl http://localhost:8000/health

# Verificar VITE_API_URL en frontend build
docker-compose logs frontend | grep VITE_API_URL

# Verificar CORS
docker-compose logs backend | grep CORS
```

### Error: "Port already in use"

**Síntoma**: `docker-compose up` falla con "port 80 already in use"

**Solución**:
```bash
# Ver qué está usando el puerto 80
sudo lsof -i :80
sudo lsof -i :8000

# Matar proceso si es necesario
sudo kill -9 [PID]

# O cambiar puertos en docker-compose.yml:
# ports:
#   - "8080:80"  # frontend en puerto 8080
#   - "8001:8000"  # backend en puerto 8001
```

### Error: "Database file is locked"

**Síntoma**: SQLite error al escribir

**Solución**:
```bash
# SQLite no maneja bien múltiples writers
# Asegura que solo hay un container backend corriendo
docker-compose ps

# Si ves múltiples backends:
docker-compose down
docker-compose up -d
```

### Migrar a PostgreSQL (Recomendado para producción)

SQLite funciona bien para desarrollo/testing, pero PostgreSQL es mejor para producción con múltiples usuarios.

```bash
# Agregar PostgreSQL al docker-compose.yml
# Ver archivo: docker-compose.postgres.yml (ejemplo completo abajo)
```

**docker-compose.postgres.yml** (ejemplo):

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: ai-dev-academy-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=ai_dev_academy
      - POSTGRES_USER=gameuser
      - POSTGRES_PASSWORD=change-me-secure-password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    # ... (mismo que antes)
    environment:
      - DATABASE_URL=postgresql://gameuser:change-me-secure-password@postgres:5432/ai_dev_academy
    depends_on:
      - postgres

volumes:
  postgres-data:
```

---

## 🔐 Seguridad

### Mejores Prácticas

1. **Usa HTTPS**: Configura SSL con Let's Encrypt (Easypanel lo hace automático)
2. **Cambia SECRET_KEY**: Nunca uses el valor por defecto
3. **Firewall**: Solo abre puertos necesarios (80, 443, 3000, 8000)
4. **Updates**: Mantén Docker y el sistema actualizados

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Actualizar Docker
sudo apt install docker-ce docker-ce-cli containerd.io
```

5. **Backups**: Backup del volumen de base de datos

```bash
# Backup SQLite database
docker-compose exec backend tar czf /tmp/backup.tar.gz /app/data
docker cp ai-dev-academy-backend:/tmp/backup.tar.gz ./backup-$(date +%Y%m%d).tar.gz

# Restore
docker cp ./backup-20250102.tar.gz ai-dev-academy-backend:/tmp/
docker-compose exec backend tar xzf /tmp/backup-20250102.tar.gz -C /
```

---

## 📊 Métricas de Éxito

- [ ] Backend responde en `http://tu-vps-ip:8000/health`
- [ ] Frontend accesible en `http://tu-vps-ip`
- [ ] API Docs accesibles en `http://tu-vps-ip:8000/docs`
- [ ] NO hay errores CORS en console
- [ ] Bug Hunt game funciona
- [ ] XP se otorga correctamente
- [ ] Leaderboard muestra datos
- [ ] Datos persisten entre reinicios
- [ ] Containers se reinician automáticamente si fallan

---

## 🎉 Deployment Completo

Si todos los checkboxes están marcados, ¡felicidades!

Tu juego está desplegado en producción en tu propio VPS con control total.

**URLs para compartir**:
- Frontend: `http://tu-vps-ip` o `https://game.tudominio.com`
- API: `http://tu-vps-ip:8000/docs`

---

## 📚 Comandos de Referencia Rápida

```bash
# Deployment
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Parar
docker-compose down

# Actualizar
git pull && docker-compose up -d --build

# Backup
docker-compose exec backend tar czf /tmp/backup.tar.gz /app/data
docker cp ai-dev-academy-backend:/tmp/backup.tar.gz ./backup.tar.gz

# Cleanup
docker system prune -a

# Stats
docker stats
```

---

**Creado**: 2025-11-02
**Versión**: 1.0
**Stack**: Easypanel + Docker + VPS
**Costo**: Solo el VPS (~$5-10/mes)
