# 🚀 Quick Deploy Commands - Copy & Paste Ready

Esta guía contiene todos los comandos necesarios para deployment, listos para copy-paste.

---

## 📋 Pre-Deployment Checks

```bash
# Verificar Docker está instalado y corriendo
docker --version
docker info

# Verificar repositorio Git
git remote -v
git status

# Testear Docker build localmente (opcional pero recomendado)
cd ai-dev-academy-game/backend
docker build -t ai-dev-academy-backend:test .
cd ../..
```

---

## 🏗️ Railway Backend Deployment

### Opción A: UI Web (Recomendado para primera vez)

1. Ve a https://railway.app
2. Click "Login with GitHub"
3. Click "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repo
5. Root Directory: `ai-dev-academy-game/backend`
6. Railway detecta Dockerfile automáticamente

### Opción B: CLI (Más rápido después de la primera vez)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy desde el directorio backend
cd ai-dev-academy-game/backend
railway init
railway up

# Obtener URL del deployment
railway domain
```

### Variables de Entorno en Railway

```
ENVIRONMENT=production
DATABASE_URL=sqlite:///./ai_dev_academy.db
ALLOWED_ORIGINS=http://localhost:5173
SECRET_KEY=TEMPORAL_CHANGE_LATER
API_TITLE=AI Dev Academy API
API_VERSION=1.0.0
```

**⚠️ Importante**: `ALLOWED_ORIGINS` lo actualizarás después con la URL de Vercel

### Validar Backend

```bash
# Reemplaza YOUR-RAILWAY-URL con tu URL real
RAILWAY_URL="https://YOUR-RAILWAY-URL.railway.app"

# Health check
curl $RAILWAY_URL/health

# Root endpoint
curl $RAILWAY_URL/

# API Docs (abrir en navegador)
echo "API Docs: $RAILWAY_URL/docs"
```

---

## 🎨 Vercel Frontend Deployment

### Opción A: UI Web (Recomendado)

1. Ve a https://vercel.com
2. Click "Login with GitHub"
3. Click "Add New..." → "Project"
4. Import tu repositorio
5. Configuración:
   - Framework: Vite
   - Root Directory: `ai-dev-academy-game/frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

### Opción B: CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy desde el directorio frontend
cd ai-dev-academy-game/frontend
vercel --prod
```

### Variables de Entorno en Vercel

```
VITE_API_URL=https://YOUR-RAILWAY-URL.railway.app
VITE_DEFAULT_PLAYER_ID=1
VITE_ENVIRONMENT=production
```

**⚠️ Crítico**:
- Reemplaza `YOUR-RAILWAY-URL` con tu URL real de Railway
- NO pongas `/` al final de VITE_API_URL

---

## 🔗 Configurar CORS

Después de obtener la URL de Vercel, actualiza `ALLOWED_ORIGINS` en Railway:

```
ALLOWED_ORIGINS=https://YOUR-VERCEL-URL.vercel.app
```

**⚠️ Importante**:
- Debe ser `https://` (no `http://`)
- Sin `/` al final
- Railway hará redeploy automático (~30 segundos)

---

## ✅ Post-Deployment Validation

### Opción A: Script Automático (Linux/WSL/Git Bash)

```bash
# Hacer script ejecutable
chmod +x ai-dev-academy-game/scripts/validate-deployment.sh

# Ejecutar validación
./ai-dev-academy-game/scripts/validate-deployment.sh
```

### Opción B: Script Automático (PowerShell en Windows)

```powershell
# Ejecutar validación
.\ai-dev-academy-game\scripts\validate-deployment.ps1
```

### Opción C: Validación Manual

```bash
# Reemplaza con tus URLs reales
RAILWAY_URL="https://YOUR-RAILWAY-URL.railway.app"
VERCEL_URL="https://YOUR-VERCEL-URL.vercel.app"

# Test 1: Backend Health
curl $RAILWAY_URL/health
# Esperado: {"status":"healthy"}

# Test 2: Backend Root
curl $RAILWAY_URL/
# Esperado: JSON con info de la API

# Test 3: API Docs
echo "Abrir en navegador: $RAILWAY_URL/docs"

# Test 4: Frontend
echo "Abrir en navegador: $VERCEL_URL"

# Test 5: Bug Hunt API
curl -X POST $RAILWAY_URL/api/minigames/bug-hunt/start \
  -H "Content-Type: application/json" \
  -d '{"player_id": 1, "difficulty": "easy"}'
```

### Validación en Navegador

1. Abre frontend: `https://YOUR-VERCEL-URL.vercel.app`
2. Presiona F12 (DevTools)
3. Ve a pestaña "Console"
4. **Verifica NO hay errores CORS**
5. Prueba Bug Hunt:
   - Click "Start Bug Hunt"
   - Selecciona dificultad
   - Juega y verifica que funciona
   - Verifica que otorga XP
6. Ve a Leaderboard y verifica que muestra datos

---

## 🔧 Optimizaciones Opcionales

### Generar SECRET_KEY Seguro

```bash
# Linux/WSL/Git Bash
openssl rand -hex 32

# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

Copia el resultado y actualiza `SECRET_KEY` en Railway.

### Migrar a PostgreSQL (Para persistencia real)

En Railway Dashboard:
1. Click "New" → "Database" → "PostgreSQL"
2. Railway crea automáticamente `DATABASE_URL`
3. Backend lo usa automáticamente (sin cambios de código)

**Trade-off**: PostgreSQL usa más recursos del tier gratuito.

### Custom Domain

**Vercel**:
```
Settings → Domains → Add Domain
```

**Railway**:
```
Settings → Domains → Add Custom Domain
```

Luego actualiza `ALLOWED_ORIGINS` en Railway:
```
ALLOWED_ORIGINS=https://your-custom-domain.com,https://your-vercel-url.vercel.app
```

---

## 📝 Actualizar Documentación

### Guardar URLs en DEPLOYMENT_CHECKLIST.md

```markdown
## Production URLs

- **Frontend**: https://ai-dev-academy-game.vercel.app
- **Backend**: https://ai-dev-academy-production.up.railway.app
- **API Docs**: https://ai-dev-academy-production.up.railway.app/docs
```

### Actualizar README Principal

```markdown
## 🌐 Demo en Vivo

- **Juega aquí**: https://ai-dev-academy-game.vercel.app
- **API Docs**: https://ai-dev-academy-production.up.railway.app/docs
```

---

## 🚨 Troubleshooting Quick Fixes

### Error CORS

```bash
# Verificar ALLOWED_ORIGINS en Railway
# Debe ser: https://YOUR-VERCEL-URL.vercel.app (sin / al final)

# Esperar redeploy de Railway (~30s)

# Clear cache del navegador
# Ctrl+Shift+R (Chrome/Edge)
# Ctrl+F5 (Firefox)
```

### Error "Failed to fetch"

```bash
# Verificar backend está UP
curl https://YOUR-RAILWAY-URL.railway.app/health

# Verificar VITE_API_URL en Vercel
# Debe ser: https://YOUR-RAILWAY-URL.railway.app (sin / al final)

# Revisar logs de Railway
railway logs
```

### Build Falla en Railway

```bash
# Verificar Dockerfile existe
ls ai-dev-academy-game/backend/Dockerfile

# Verificar requirements.txt
ls ai-dev-academy-game/backend/requirements.txt

# Testear build localmente
cd ai-dev-academy-game/backend
docker build -t test .
```

### Build Falla en Vercel

```bash
# Verificar Root Directory configurado
# Debe ser: ai-dev-academy-game/frontend

# Verificar package.json tiene build script
cat ai-dev-academy-game/frontend/package.json | grep build

# Testear build localmente
cd ai-dev-academy-game/frontend
npm install
npm run build
```

---

## 📊 Deployment Checklist

Marca cada item cuando esté completo:

```
[ ] Backend desplegado en Railway
[ ] Backend health check OK: curl https://YOUR-URL.railway.app/health
[ ] API Docs accesibles en navegador
[ ] Frontend desplegado en Vercel
[ ] Frontend carga sin errores
[ ] NO hay errores CORS en DevTools
[ ] Bug Hunt game funciona end-to-end
[ ] Leaderboard muestra datos
[ ] XP se otorga correctamente
[ ] Funciona en Chrome/Edge
[ ] Funciona en Firefox
[ ] Funciona en móvil
[ ] SECRET_KEY generado y actualizado
[ ] URLs documentadas en DEPLOYMENT_CHECKLIST.md
[ ] README actualizado con links
```

---

## 🔗 Links Útiles

- **Railway Dashboard**: https://railway.app/dashboard
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Docker Hub**: https://hub.docker.com

---

## 🎉 Comandos de Celebración

Cuando todo esté funcionando:

```bash
# Compartir URLs
echo "🎮 Juega aquí: https://YOUR-VERCEL-URL.vercel.app"
echo "📚 API Docs: https://YOUR-RAILWAY-URL.railway.app/docs"
echo ""
echo "✅ Deployment completo! 🎉"
```

---

**Creado**: 2025-11-02
**Versión**: 1.0
**Propósito**: Quick reference para deployment manual del AI Dev Academy Game
