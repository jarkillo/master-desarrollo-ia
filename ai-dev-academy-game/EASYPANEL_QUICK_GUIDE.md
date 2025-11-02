# 🚀 Guía Rápida - Deployment en Easypanel

## 🔧 Configuración en Easypanel

### 1. Build Settings

```yaml
# Docker Compose File:
docker-compose.production.yml

# Build Command:
docker-compose -f docker-compose.production.yml build

# Start Command:
docker-compose -f docker-compose.production.yml up -d
```

### 2. Variables de Entorno

```bash
VITE_API_URL=/api
DATABASE_URL=sqlite:///./data/game.db
```

### 3. Configurar Dominio

- Domain: `tudominio.com`
- Service: `frontend`
- Port: `80`
- SSL: ✅ Enable

## ✅ Solución al Error de Puerto 80

**Error:**
```
Bind for 0.0.0.0:80 failed: port is already allocated
```

**Causa:** Easypanel usa Traefik en puerto 80

**Solución:** Usar `docker-compose.production.yml` que NO mapea puertos externos

## 📝 Checklist

- [ ] Usar docker-compose.production.yml
- [ ] Añadir variable VITE_API_URL=/api
- [ ] Configurar dominio
- [ ] Habilitar SSL
- [ ] Crear volumen backend-data

## 🔗 URLs Después del Deploy

- Frontend: https://tudominio.com
- Backend Health: https://tudominio.com/api/health
- API Docs: https://tudominio.com/api/docs
