# Guía de Deployment - Railway & Vercel

Esta guía te ayudará a deployar tu aplicación full-stack paso a paso.

## 🚀 Quick Start

### 1. Prerequisites

- Cuenta en [Railway](https://railway.app) (usa GitHub auth)
- Cuenta en [Vercel](https://vercel.com) (usa GitHub auth)
- Repositorio en GitHub con el código de esta clase
- [Railway CLI](https://docs.railway.app/develop/cli) (opcional)
- [Vercel CLI](https://vercel.com/cli) (opcional)

### 2. Backend Deployment (Railway)

#### Step 1: Crear Proyecto en Railway

1. Ve a [railway.app/new](https://railway.app/new)
2. Click **Deploy from GitHub repo**
3. Selecciona tu repositorio
4. Railway detectará automáticamente el `Procfile`

#### Step 2: Configurar Environment Variables

En Railway Dashboard → **Variables**:

```bash
JWT_SECRET=<genera-con-openssl-rand-hex-32>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
FRONTEND_URL=https://tu-app.vercel.app  # Lo configurarás después
MODE=production
```

**Generar JWT_SECRET**:
```bash
openssl rand -hex 32
```

#### Step 3: Deploy

Railway auto-deploya cuando detecta el Procfile. Espera 1-2 minutos.

#### Step 4: Verificar

```bash
# Obtén tu URL de Railway (algo como https://xxx.railway.app)
curl https://tu-api.railway.app/health

# Deberías ver:
# {
#   "status": "ok",
#   "timestamp": "2025-10-23T...",
#   "version": "1.0.0",
#   "environment": "production"
# }
```

#### Step 5: Configurar Custom Domain (Opcional)

Railway → **Settings** → **Domains** → **Generate Domain** o **Custom Domain**

---

### 3. Frontend Deployment (Vercel)

#### Step 1: Instalar Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Deploy desde CLI

```bash
cd frontend

# Login
vercel login

# Deploy a production
vercel --prod
```

Vercel te dará una URL como `https://tu-app.vercel.app`

#### Step 3: Configurar Environment Variable

En Vercel Dashboard:
1. Ve a **Settings** → **Environment Variables**
2. Agregar:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://tu-api.railway.app` (la URL de Railway)
   - **Environment**: Production

#### Step 4: Re-deploy

```bash
vercel --prod
```

O en dashboard: **Deployments** → **Redeploy**

#### Step 5: Actualizar FRONTEND_URL en Railway

Ahora que tienes la URL de Vercel, actualiza en Railway:
1. Railway Dashboard → **Variables**
2. Editar `FRONTEND_URL`: `https://tu-app.vercel.app`
3. Railway redeploya automáticamente

---

## 🔍 Troubleshooting

### Error: CORS Policy

**Síntoma**:
```
Access to fetch at 'https://api.railway.app/auth/login' from origin 'https://myapp.vercel.app'
has been blocked by CORS policy
```

**Solución**:
1. Verificar que `FRONTEND_URL` en Railway coincida EXACTAMENTE con la URL de Vercel
2. Re-deploy Railway
3. Verificar con curl:
   ```bash
   curl -X OPTIONS https://tu-api.railway.app/auth/login \
     -H "Origin: https://tu-app.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -v
   ```
   Debe retornar: `Access-Control-Allow-Origin: https://tu-app.vercel.app`

---

### Error: JWT_SECRET missing

**Síntoma**:
```
ValueError: Missing required environment variables: JWT_SECRET
```

**Solución**:
1. Railway Dashboard → **Variables**
2. Agregar `JWT_SECRET` con valor generado:
   ```bash
   openssl rand -hex 32
   ```
3. Railway redeploya automáticamente

---

### Error: Frontend no conecta a backend

**Síntoma**:
```
Network Error: Connection refused
```

**Solución**:
1. Verificar que `VITE_API_URL` en Vercel esté configurado correctamente
2. Re-deploy Vercel
3. Verificar en DevTools → Network → Check que la URL del request sea correcta

---

### Error: 401 Unauthorized en todas las requests

**Síntoma**:
Login funciona pero luego todas las requests dan 401.

**Solución**:
1. Verificar que el token se guarda en localStorage (DevTools → Application → Local Storage)
2. Verificar que Axios interceptor agrega el header (DevTools → Network → Request Headers → Authorization)
3. Si el token expira rápido, ajustar `JWT_EXPIRATION_MINUTES` en Railway

---

## 📊 Monitoring

### Railway Logs

**Ver logs en tiempo real**:
```bash
railway logs
```

O en Railway Dashboard → **Deployments** → Click deployment → **View Logs**

**Qué buscar**:
- `✅ All required environment variables are set` (startup correcto)
- `CORS configured for origins: ['https://...']` (CORS configurado)
- Requests HTTP con status codes (200, 401, etc.)

---

### Vercel Logs

**Ver logs de build**:
Vercel Dashboard → **Deployments** → Click deployment → **Build Logs**

**Ver logs de runtime**:
Vercel Dashboard → **Functions** → Click function → **Logs**

---

## 🎯 Production Checklist

Antes de considerar tu app "production-ready", verifica:

### Backend (Railway)

- [ ] Health check responde 200 OK
- [ ] JWT_SECRET generado con `openssl rand -hex 32`
- [ ] CORS configurado con URL exacta de frontend
- [ ] MODE=production configurado
- [ ] Logs accesibles en Railway dashboard
- [ ] Tests pasan localmente antes de deploy

### Frontend (Vercel)

- [ ] Build completa sin errores (`npm run build`)
- [ ] Bundle size <150KB gzipped
- [ ] VITE_API_URL apunta al backend correcto
- [ ] Login/Register funcionan end-to-end
- [ ] Protected routes redirigen correctamente
- [ ] No console.log en producción (verificar DevTools)
- [ ] HTTPS funciona (certificado SSL válido)

### Testing

- [ ] Login desde frontend en producción funciona
- [ ] Dashboard muestra datos del usuario
- [ ] Logout y re-login funciona
- [ ] Token se persiste en localStorage
- [ ] Refresh de página mantiene sesión
- [ ] Intentar acceder a dashboard sin auth redirige a login

---

## 🔄 Workflow de Updates

### Actualizar Backend

1. Hacer cambios en código
2. Commit y push a GitHub
   ```bash
   git add .
   git commit -m "feat: agregar nuevo endpoint"
   git push origin main
   ```
3. Railway auto-deploya (webhook de GitHub)
4. Verificar en Railway logs que deploy fue exitoso

### Actualizar Frontend

1. Hacer cambios en código
2. Commit y push a GitHub
   ```bash
   git add .
   git commit -m "feat: agregar nuevo componente"
   git push origin main
   ```
3. Vercel auto-deploya (webhook de GitHub)
4. Verificar en Vercel deployments que build pasó

---

## 💡 Tips & Best Practices

### 1. Environment Variables

- **NUNCA** commitees secrets al repo (usa `.env.example` sin valores reales)
- Genera JWT_SECRET diferente para cada environment (dev, staging, prod)
- Usa variables de entorno para URLs (facilita cambios sin rebuild)

### 2. Deployment Strategy

- **Development**: Push a `dev` branch → Preview deployment en Vercel
- **Production**: Merge a `main` → Production deployment automático
- Testea en preview deployment antes de mergear a main

### 3. Monitoring

- Configura [UptimeRobot](https://uptimerobot.com) para monitorear `/health`
- Alerta si health check falla por 5+ minutos
- Revisa logs diariamente en Railway/Vercel

### 4. Rollback

- **Railway**: Dashboard → Deployments → Click deployment anterior → Rollback
- **Vercel**: Dashboard → Deployments → Click deployment anterior → Promote to Production

### 5. Performance

- Usa Vercel Analytics (gratis) para monitorear Core Web Vitals
- Railway muestra CPU/Memory usage en dashboard
- Si Railway free tier se queda sin recursos, considera upgrade a Hobby ($5/month)

---

## 🚨 Common Mistakes

### 1. CORS Wildcard en Producción

❌ **Mal**:
```python
allow_origins=["*"]  # Nunca uses esto con allow_credentials=True
```

✅ **Bien**:
```python
FRONTEND_URL = os.getenv("FRONTEND_URL")
allow_origins=[FRONTEND_URL]  # URL específica
```

### 2. Secrets en Código

❌ **Mal**:
```python
JWT_SECRET = "mi-secret-super-seguro"  # Hardcoded
```

✅ **Bien**:
```python
JWT_SECRET = os.getenv("JWT_SECRET")  # Desde environment variable
```

### 3. Too Many Workers en Free Tier

❌ **Mal**:
```
gunicorn -w 8 ...  # 8 workers en 512MB RAM = OOM
```

✅ **Bien**:
```
gunicorn -w 2 ...  # 2 workers para free tier
```

Ajusta `Procfile` según tu plan:
- Free tier: 1-2 workers
- Hobby ($5/month): 2-4 workers
- Pro ($20/month): 4-8 workers

---

## 📚 Next Steps

- [ ] Configurar custom domain
- [ ] Agregar Sentry para error tracking
- [ ] Configurar GitHub Actions CI/CD
- [ ] Agregar PostgreSQL (Module 5 - Clase 5)
- [ ] Configurar rate limiting
- [ ] Agregar caching (Redis)

---

## 🆘 Getting Help

- **Railway Discord**: [railway.app/discord](https://railway.app/discord)
- **Vercel Discord**: [vercel.com/discord](https://vercel.com/discord)
- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
