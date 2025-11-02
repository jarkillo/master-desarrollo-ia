# 🚀 Quick Start - Deployment en VPS con Docker

**TL;DR**: Comandos copy-paste para desplegar en tu VPS con Easypanel/Docker.

---

## ⚡ Deployment en 5 Minutos

### 1. Conectar a tu VPS

```bash
ssh usuario@tu-vps-ip
```

### 2. Clonar el Repositorio

```bash
cd ~
git clone https://github.com/tu-usuario/master-ia-manu.git
cd master-ia-manu/ai-dev-academy-game
```

### 3. Configurar Variables de Entorno

```bash
# Copiar template
cp .env.production.example .env

# Generar SECRET_KEY seguro
openssl rand -hex 32

# Editar .env
nano .env
```

**Contenido del `.env`**:

```bash
FRONTEND_URL=http://TU-VPS-IP
BACKEND_URL=http://TU-VPS-IP:8000
SECRET_KEY=resultado-del-comando-openssl-arriba
```

Guarda con `Ctrl+O`, `Enter`, `Ctrl+X`.

### 4. Deploy con Docker Compose

```bash
# Build y levantar containers
docker-compose up -d --build

# Ver logs
docker-compose logs -f
```

**Espera 5-8 minutos** mientras buildea (primera vez).

### 5. Abrir Puertos en Firewall

```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 8000/tcp

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 6. Verificar

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost/health

# Ver containers
docker-compose ps
```

### 7. Abrir en Navegador

```
Frontend: http://TU-VPS-IP
API Docs: http://TU-VPS-IP:8000/docs
```

**¡Listo!** 🎉

---

## 🔧 Testeo Local (antes de desplegar al VPS)

Con Docker Desktop en Windows:

```bash
# PowerShell o Git Bash
cd ai-dev-academy-game

# Copiar template
copy .env.production.example .env

# Editar .env:
# FRONTEND_URL=http://localhost
# BACKEND_URL=http://localhost:8000
# SECRET_KEY=test-key-32-chars-minimum-length

# Levantar
docker-compose up --build

# En otro terminal
curl http://localhost:8000/health
curl http://localhost/health

# Abrir navegador
start http://localhost
```

Si funciona local, funcionará en VPS.

---

## 📝 Comandos Útiles

### Ver Logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Últimas 50 líneas
docker-compose logs --tail=50
```

### Reiniciar Servicios

```bash
# Reiniciar todo
docker-compose restart

# Reiniciar solo backend
docker-compose restart backend

# Reiniciar solo frontend
docker-compose restart frontend
```

### Actualizar Aplicación

```bash
# Pull últimos cambios
git pull origin main

# Rebuild y redeploy
docker-compose down
docker-compose up -d --build
```

### Parar Aplicación

```bash
# Parar containers (mantiene volúmenes)
docker-compose stop

# Parar y eliminar containers (mantiene volúmenes)
docker-compose down

# Parar, eliminar containers y volúmenes (⚠️ borra datos)
docker-compose down -v
```

### Backup de Datos

```bash
# Backup SQLite database
docker-compose exec backend tar czf /tmp/backup.tar.gz /app/data
docker cp ai-dev-academy-backend:/tmp/backup.tar.gz ./backup-$(date +%Y%m%d).tar.gz

# Restaurar
docker cp ./backup-20250102.tar.gz ai-dev-academy-backend:/tmp/
docker-compose exec backend tar xzf /tmp/backup-20250102.tar.gz -C /
docker-compose restart backend
```

### Monitoreo

```bash
# Ver uso de recursos (CPU, RAM)
docker stats

# Ver espacio en disco
docker system df

# Limpiar imágenes no usadas
docker system prune -a
```

---

## 🚨 Troubleshooting Rápido

### Frontend no se conecta al backend

```bash
# 1. Verificar backend está UP
docker-compose ps backend
curl http://localhost:8000/health

# 2. Verificar CORS
docker-compose logs backend | grep CORS

# 3. Verificar VITE_API_URL
docker-compose logs frontend | grep VITE

# 4. Rebuild frontend si es necesario
docker-compose stop frontend
docker-compose up -d --build frontend
```

### Puerto 80 o 8000 ya en uso

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :80
sudo lsof -i :8000

# Opción 1: Matar proceso
sudo kill -9 [PID]

# Opción 2: Cambiar puerto en docker-compose.yml
# Edita:
# ports:
#   - "8080:80"  # frontend en 8080
#   - "8001:8000"  # backend en 8001
```

### Containers no inician

```bash
# Ver logs completos
docker-compose logs

# Ver errores específicos
docker-compose logs backend --tail=100
docker-compose logs frontend --tail=100

# Rebuild desde cero
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Base de datos corrupta

```bash
# Parar aplicación
docker-compose down

# Eliminar volumen (⚠️ borra datos)
docker volume rm ai-dev-academy-game_backend-data

# Reiniciar
docker-compose up -d
```

---

## 📊 Checklist de Deployment

- [ ] VPS accesible por SSH
- [ ] Docker y Docker Compose instalados
- [ ] Repositorio clonado en VPS
- [ ] `.env` configurado con valores correctos
- [ ] `SECRET_KEY` generado con openssl
- [ ] `docker-compose up -d --build` ejecutado
- [ ] Backend responde: `curl http://localhost:8000/health`
- [ ] Frontend responde: `curl http://localhost/health`
- [ ] Firewall abierto: puertos 80 y 8000
- [ ] Frontend accesible desde navegador
- [ ] NO hay errores CORS en console
- [ ] Bug Hunt game funciona
- [ ] Leaderboard muestra datos

---

## 🎯 Próximos Pasos

### Configurar Dominio (Opcional)

Si tienes un dominio (ej: `game.tudominio.com`):

1. **Apuntar DNS a tu VPS**:
   - Tipo A record: `game.tudominio.com` → `TU-VPS-IP`

2. **Actualizar `.env`**:
   ```bash
   FRONTEND_URL=https://game.tudominio.com
   BACKEND_URL=https://api.tudominio.com
   ```

3. **Configurar SSL con Let's Encrypt**:
   - Si usas Easypanel: automático
   - Si usas Docker: agregar nginx-proxy + letsencrypt companion

### Migrar a PostgreSQL (Para producción seria)

```bash
# Agregar PostgreSQL al docker-compose.yml
# Ver EASYPANEL_DEPLOYMENT.md sección "Migrar a PostgreSQL"
```

### Configurar Backups Automáticos

```bash
# Cron job para backup diario
crontab -e

# Agregar:
# 0 2 * * * /ruta/a/backup-script.sh
```

---

## 📚 Documentación Completa

- **Guía Completa**: `EASYPANEL_DEPLOYMENT.md`
- **Troubleshooting**: Ver sección en `EASYPANEL_DEPLOYMENT.md`
- **Docker Compose**: `docker-compose.yml`
- **Variables de Entorno**: `.env.production.example`

---

**Última actualización**: 2025-11-02
**Versión**: 1.0
**Stack**: Docker Compose + VPS
