# Módulo 5 - Clase 4: Despliegue Full-Stack en Producción

Esta clase enseña cómo **llevar tu aplicación full-stack a producción** usando plataformas modernas de deployment. Aprenderás sobre build optimization, variables de entorno, health checks, monitoreo y las mejores prácticas para un despliegue robusto.

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Nuevas Tecnologías](#nuevas-tecnologías)
3. [Arquitectura de Deployment](#arquitectura-de-deployment)
4. [Preparación para Producción](#preparación-para-producción)
5. [Despliegue del Backend](#despliegue-del-backend)
6. [Despliegue del Frontend](#despliegue-del-frontend)
7. [🤖 AI Integration (40% del contenido)](#-ai-integration-40-del-contenido)
8. [Production Checklist](#production-checklist)
9. [Monitoreo y Debugging](#monitoreo-y-debugging)
10. [Ejercicios y Mejoras](#ejercicios-y-mejoras)
11. [Recursos Adicionales](#recursos-adicionales)

---

## Descripción del Proyecto

Desplegamos la aplicación de autenticación de la Clase 3 en producción usando:

### Backend Deployment

- ✅ **Railway** o **Render**: Hosting de la API FastAPI
- ✅ **Environment Variables**: Gestión segura de secrets (JWT_SECRET, DATABASE_URL)
- ✅ **Health Checks**: Endpoint `/health` para monitoreo
- ✅ **CORS Configuration**: Configuración para permitir frontend en otro dominio
- ✅ **Logging**: Logs estructurados para debugging
- ✅ **Gunicorn + Uvicorn**: Worker process management para producción

### Frontend Deployment

- ✅ **Vercel** o **Netlify**: Hosting del frontend React
- ✅ **Vite Build Optimization**: Tree-shaking, code splitting, compression
- ✅ **Environment Variables**: API URL configurable por entorno
- ✅ **CDN**: Distribución global automática
- ✅ **HTTPS**: Certificados SSL automáticos
- ✅ **Preview Deployments**: Deploy automático por PR

### DevOps

- ✅ **CI/CD**: GitHub Actions para tests pre-deployment
- ✅ **Rollback**: Despliegues atómicos con rollback instantáneo
- ✅ **Monitoring**: Logs y métricas de producción
- ✅ **Custom Domain**: Configuración de dominio personalizado (opcional)

---

## Nuevas Tecnologías

### Railway / Render (Backend PaaS)

**¿Qué es?** Plataforma como Servicio (PaaS) para desplegar aplicaciones backend sin configurar servidores.

**¿Por qué usarlo?**
- ✅ **Zero config**: Detecta FastAPI automáticamente
- ✅ **Environment variables**: UI amigable para secrets
- ✅ **Logs en vivo**: Debugging en producción
- ✅ **Health checks**: Reinicia si la app falla
- ✅ **HTTPS automático**: Certificados SSL incluidos

**Railway vs Render**:
- **Railway**: Más rápido, mejor DX, $5/mes de crédito gratis
- **Render**: Free tier más generoso, pero con cold starts

**Alternativas**: Heroku (caro), AWS Elastic Beanstalk, Google Cloud Run, Fly.io

### Vercel / Netlify (Frontend CDN + Edge)

**¿Qué es?** Plataforma especializada en desplegar aplicaciones frontend con CDN global.

**¿Por qué usarlo?**
- ✅ **Build automático**: Detecta Vite/React, ejecuta `npm run build`
- ✅ **CDN Global**: Tu app se sirve desde 300+ edge locations
- ✅ **HTTPS automático**: SSL certificates incluidos
- ✅ **Preview deploys**: Cada PR tiene su propia URL de preview
- ✅ **Rollback instantáneo**: Un clic para volver a versión anterior

**Vercel vs Netlify**:
- **Vercel**: Mejor integración con Next.js, edge functions más potentes
- **Netlify**: Más flexible, mejor free tier, redirects más simples

**Alternativas**: Cloudflare Pages, AWS S3 + CloudFront, GitHub Pages

### Gunicorn (WSGI Server)

**¿Qué es?** Process manager que ejecuta múltiples workers de tu app FastAPI.

**¿Por qué usarlo?**
- ✅ **Multiple workers**: Maneja más requests concurrentes
- ✅ **Worker restart**: Si un worker crashea, los demás siguen funcionando
- ✅ **Graceful reload**: Actualiza código sin downtime
- ✅ **Production-ready**: Estándar de la industria para Python web apps

**Comando típico**:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.api:app
```

**Alternativas**: Uvicorn solo (OK para low traffic), Hypercorn, Daphne

### Environment Variables en Producción

**¿Qué son?** Variables de configuración que se inyectan en runtime, no hardcodeadas en código.

**¿Por qué usarlas?**
- ✅ **Security**: Secrets no están en Git
- ✅ **Flexibility**: Misma app, diferentes configs (dev/staging/prod)
- ✅ **12-Factor App**: Siguiendo mejores prácticas de deployment

**Ejemplo backend**:
```python
import os
JWT_SECRET = os.getenv("JWT_SECRET")  # Desde Railway/Render
DATABASE_URL = os.getenv("DATABASE_URL")
MODE = os.getenv("MODE", "production")
```

**Ejemplo frontend**:
```typescript
const API_URL = import.meta.env.VITE_API_URL;  // Desde Vercel/Netlify
```

### Health Check Endpoint

**¿Qué es?** Endpoint simple que responde 200 OK si la app está funcionando.

**¿Por qué usarlo?**
- ✅ **Load balancer monitoring**: AWS/Railway usan esto para saber si tu app está viva
- ✅ **Automatic restart**: Si health check falla, la plataforma reinicia tu app
- ✅ **Database connectivity**: Puedes verificar DB connection en el health check

**Ejemplo FastAPI**:
```python
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
```

---

## Arquitectura de Deployment

### Flujo de Deployment Completo

```
Developer → Git Push → GitHub
                         ↓
                    GitHub Actions
                         ↓
                  Run Tests (pytest)
                         ↓
                    ¿Tests Pass?
                         ↓
                       Yes
                         ↓
        ┌────────────────┴────────────────┐
        ↓                                  ↓
   Railway (Backend)              Vercel (Frontend)
        ↓                                  ↓
   Build & Deploy                    Build & Deploy
   (gunicorn + uvicorn)               (vite build)
        ↓                                  ↓
   https://api.railway.app          https://app.vercel.app
        ↓                                  ↓
        └──────────────┬───────────────────┘
                       ↓
                 Users (Browser)
```

### Diagrama de Infraestructura

```
┌─────────────────────────────────────────────────────┐
│                      Internet                        │
└──────────────────────┬──────────────────────────────┘
                       ↓
           ┌───────────┴───────────┐
           ↓                       ↓
    ┌──────────────┐       ┌──────────────┐
    │   Vercel CDN │       │   Railway    │
    │              │       │              │
    │  React App   │←──────┤  FastAPI     │
    │  (Static)    │ CORS  │  + JWT Auth  │
    │              │       │              │
    │  - HTML/CSS  │       │  - Gunicorn  │
    │  - JS Bundle │       │  - Uvicorn   │
    │  - Images    │       │  - Health    │
    └──────────────┘       └──────────────┘
         ↓                        ↓
    Edge Locations          Environment Vars
    (300+ global)           (JWT_SECRET, etc)
```

### Flujo de Request en Producción

```
1. Usuario visita https://myapp.vercel.app
        ↓
2. Vercel CDN sirve HTML/CSS/JS (instantáneo)
        ↓
3. React app carga en browser
        ↓
4. User hace login → POST https://api.railway.app/auth/login
        ↓
5. Railway → FastAPI valida credenciales
        ↓
6. Genera JWT y retorna → 200 OK + token
        ↓
7. React guarda token en localStorage
        ↓
8. Requests subsecuentes → Authorization: Bearer <token>
```

---

## Preparación para Producción

### 1. Backend: Configuración de Producción

#### a) Crear archivo de variables de entorno

**`backend/.env.example`** (template para Railway/Render):
```bash
# JWT Configuration
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# CORS Configuration (frontend URL)
FRONTEND_URL=https://your-app.vercel.app

# Environment
MODE=production

# Database (para futuras clases)
# DATABASE_URL=postgresql://user:password@host:5432/dbname
```

#### b) Agregar Health Check Endpoint

**`backend/api/api.py`**:
```python
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Tareas API", version="1.0.0")

# CORS configurado para producción
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # URL específica en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint para Railway/Render monitoring."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ... resto de endpoints (auth, etc)
```

#### c) Crear `requirements.txt` completo

**`backend/requirements.txt`**:
```
fastapi==0.118.0
uvicorn[standard]==0.37.0
pydantic==2.11.10
python-jose[cryptography]==3.3.0
bcrypt==4.2.1
gunicorn==23.0.0
python-dotenv==1.0.1
```

#### d) Crear `Procfile` para Railway/Render

**`backend/Procfile`** (Railway y Render usan este archivo):
```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.api:app --bind 0.0.0.0:$PORT
```

**Explicación**:
- `-w 4`: 4 workers (ajusta según tu plan: 2-4 para free tier)
- `-k uvicorn.workers.UvicornWorker`: Worker class para ASGI (FastAPI)
- `--bind 0.0.0.0:$PORT`: Railway/Render inyectan variable PORT automáticamente

### 2. Frontend: Build Optimization

#### a) Configurar Environment Variables

**`frontend/.env.production`**:
```bash
VITE_API_URL=https://your-api.railway.app
```

**`frontend/.env.development`**:
```bash
VITE_API_URL=http://localhost:8000
```

#### b) Actualizar `vite.config.ts` para producción

**`frontend/vite.config.ts`**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    // Tree-shaking: elimina código no usado
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,  // Elimina console.log en producción
      },
    },
    // Code splitting: divide bundle en chunks
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          forms: ['react-hook-form', 'zod'],
        },
      },
    },
    // Compresión de assets
    reportCompressedSize: true,
    chunkSizeWarningLimit: 1000,
  },
  server: {
    port: 5173,
  },
  preview: {
    port: 4173,
  },
})
```

#### c) Actualizar service para usar environment variable

**`frontend/src/services/auth.service.ts`**:
```typescript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ... resto del código
```

#### d) Crear `netlify.toml` o `vercel.json`

**`frontend/netlify.toml`** (si usas Netlify):
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "20"
```

**`frontend/vercel.json`** (si usas Vercel):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## Despliegue del Backend

### Opción 1: Railway

#### 1. Crear cuenta en Railway

Ir a [railway.app](https://railway.app) y crear cuenta con GitHub.

#### 2. Crear nuevo proyecto

```bash
# Desde tu terminal
railway login
railway init

# Seleccionar "New Project"
# Seleccionar "Deploy from GitHub repo"
```

#### 3. Configurar variables de entorno

En Railway Dashboard:
1. Ir a **Variables**
2. Agregar:
   - `JWT_SECRET`: `tu-super-secret-key-genera-una-random` (usa `openssl rand -hex 32`)
   - `JWT_ALGORITHM`: `HS256`
   - `JWT_EXPIRATION_MINUTES`: `60`
   - `FRONTEND_URL`: `https://your-app.vercel.app` (lo configurarás después)
   - `MODE`: `production`

#### 4. Verificar deployment

Railway detecta `Procfile` automáticamente y despliega.

**Verificar health check**:
```bash
curl https://your-app.railway.app/health
# {"status":"ok","timestamp":"2025-10-23T...","version":"1.0.0"}
```

**Verificar logs**:
En Railway Dashboard → **Deployments** → **View Logs**

#### 5. Configurar custom domain (opcional)

Railway Dashboard → **Settings** → **Domains** → **Add Custom Domain**

---

### Opción 2: Render

#### 1. Crear cuenta en Render

Ir a [render.com](https://render.com) y crear cuenta con GitHub.

#### 2. Crear Web Service

1. Click **New** → **Web Service**
2. Conectar GitHub repo
3. Configurar:
   - **Name**: `tareas-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.api:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free (o Starter si necesitas 0 cold starts)

#### 3. Configurar Environment Variables

En Render Dashboard:
1. Ir a **Environment**
2. Agregar las mismas variables que Railway

#### 4. Deploy

Render auto-deploys cuando haces push a main.

**Verificar**:
```bash
curl https://tareas-api.onrender.com/health
```

⚠️ **Nota sobre Free Tier de Render**: Las apps free se "duermen" después de 15 minutos de inactividad (cold start de 30-60 segundos en el primer request).

---

## Despliegue del Frontend

### Opción 1: Vercel

#### 1. Instalar Vercel CLI

```bash
npm install -g vercel
```

#### 2. Deploy desde CLI

```bash
cd frontend

# Login
vercel login

# Deploy a producción
vercel --prod
```

#### 3. Configurar Environment Variable

En Vercel Dashboard:
1. Ir a **Settings** → **Environment Variables**
2. Agregar:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-api.railway.app`
   - **Environment**: Production

#### 4. Re-deploy para aplicar variable

```bash
vercel --prod
```

#### 5. Verificar

Abrir `https://your-app.vercel.app` y probar login.

**Verificar en DevTools**:
- Network tab → Check que requests van a Railway URL
- Console → No debe haber errores de CORS

---

### Opción 2: Netlify

#### 1. Instalar Netlify CLI

```bash
npm install -g netlify-cli
```

#### 2. Build local y deploy

```bash
cd frontend

# Build
npm run build

# Login
netlify login

# Deploy
netlify deploy --prod --dir=dist
```

#### 3. Configurar Environment Variable

En Netlify Dashboard:
1. **Site settings** → **Build & deploy** → **Environment**
2. Agregar:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-api.railway.app`

#### 4. Re-build

Netlify → **Deploys** → **Trigger deploy**

---

## 🤖 AI Integration (40% del contenido)

Esta sección demuestra cómo usar **IA como DevOps Engineer** para configurar deployment pipelines, optimizar builds y detectar problemas de producción.

### 1. Generación de Configuración de Deployment

#### Prompt para preparar backend para producción

```
Prepara mi backend FastAPI para despliegue en Railway:

Requisitos:
- Health check endpoint en /health que retorne status, timestamp, version
- CORS configurado para leer FRONTEND_URL desde environment variable
- Gunicorn con 4 workers usando UvicornWorker
- Crear Procfile con comando de producción
- requirements.txt con todas las dependencias (fastapi, uvicorn, gunicorn, python-jose, bcrypt)
- Logging estructurado con logging.basicConfig (INFO level en producción)
- Función para validar environment variables al startup

Environment variables esperadas:
- JWT_SECRET (required)
- JWT_ALGORITHM (default: HS256)
- JWT_EXPIRATION_MINUTES (default: 60)
- FRONTEND_URL (required)
- MODE (default: production)

Si alguna variable requerida falta, lanzar ValueError con mensaje claro.
```

**La IA generará**:
1. Health check endpoint completo
2. CORS configurado dinámicamente
3. `Procfile` optimizado
4. Función de validación de env vars
5. Logging configuration para producción

**Ejemplo de validación generada por IA**:
```python
import os
import logging

def validate_environment():
    """Valida que todas las env vars requeridas estén presentes."""
    required_vars = ["JWT_SECRET", "FRONTEND_URL"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Check your Railway/Render dashboard for environment configuration."
        )

    logging.info("✅ All required environment variables are set")

# En api.py al inicio
validate_environment()
```

---

#### Prompt para optimizar build de Vite

```
Optimiza mi configuración de Vite para producción:

Requisitos:
- Minificación agresiva con terser (eliminar console.log)
- Code splitting: separar vendor (react, react-dom, router) y forms (react-hook-form, zod)
- Tree-shaking de componentes no usados
- Compresión de assets
- Source maps solo para errors (no completos)
- Preload de critical chunks
- Optimización de imágenes (webp, lazy loading)

Genera vite.config.ts con comentarios explicando cada optimización y su impacto en bundle size.
```

**La IA generará**:
- `vite.config.ts` con todas las optimizaciones
- Comparación de bundle size (antes/después)
- Explicación de cada optimization flag
- Recomendaciones de análisis con `rollup-plugin-visualizer`

**Ejemplo generado**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true, filename: 'bundle-analysis.html' })
  ],
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,        // -5KB: elimina console.log
        drop_debugger: true,       // elimina debugger statements
        pure_funcs: ['console.info']  // elimina console.info específicamente
      }
    },
    rollupOptions: {
      output: {
        manualChunks: {
          // -30KB: vendor bundle separado (cacheable)
          vendor: ['react', 'react-dom', 'react-router-dom'],
          // -10KB: forms bundle (solo carga en páginas con forms)
          forms: ['react-hook-form', 'zod'],
        }
      }
    },
    sourcemap: 'hidden',  // Source maps solo para error reporting
    reportCompressedSize: true,
  }
})
```

---

### 2. Debugging de Problemas de Deployment

#### Prompt para diagnosticar CORS errors

```
Mi frontend en Vercel no puede conectar con backend en Railway.
Error en console: "CORS policy: No 'Access-Control-Allow-Origin' header"

Backend:
- FastAPI con CORSMiddleware
- URL: https://myapi.railway.app
- CORS configurado con allow_origins=["*"]

Frontend:
- React + Vite en Vercel
- URL: https://myapp.vercel.app
- Hace fetch a: https://myapi.railway.app/auth/login

Diagnostica el problema y dame pasos concretos para resolverlo.
```

**La IA diagnosticará**:
1. **Problema**: `allow_origins=["*"]` no funciona con `allow_credentials=True`
2. **Solución**: Especificar origin exacto del frontend
3. **Pasos**:
   - Configurar `FRONTEND_URL` en Railway
   - Actualizar CORS: `allow_origins=[FRONTEND_URL]`
   - Verificar que frontend incluye `credentials: 'include'` en axios
4. **Testing**: `curl -H "Origin: https://myapp.vercel.app" https://myapi.railway.app/health`

---

#### Prompt para optimizar cold starts

```
Mi API en Render free tier tiene cold starts de 60 segundos.

Context:
- FastAPI con JWT auth
- 15+ dependencies en requirements.txt (pandas, numpy, sklearn)
- Gunicorn con 4 workers

¿Cómo reduzco el tiempo de cold start? Dame optimizaciones concretas.
```

**La IA sugerirá**:
1. **Lazy imports**: Cargar pandas/sklearn solo cuando se usen
2. **Reduce workers**: 1-2 workers en free tier (menos memoria)
3. **Slim dependencies**: Remover deps no esenciales
4. **Health check optimization**: Cache de status por 30s
5. **Upgrade a paid tier**: Si cold starts son críticos ($7/month = 0 cold starts)

**Código generado**:
```python
# Lazy import de dependencias pesadas
@app.post("/predict")
def predict(data: PredictRequest):
    # Import solo cuando se usa este endpoint
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression

    # ... resto del código
```

---

### 3. Automatización con GitHub Actions

#### Prompt para CI/CD pipeline completo

```
Crea un GitHub Actions workflow para mi app full-stack:

Backend (FastAPI en Railway):
- Correr pytest con coverage mínimo 80%
- Linting con ruff
- Deploy a Railway solo si tests pasan
- Deploy solo en pushes a main

Frontend (React en Vercel):
- npm run build debe completar sin errores
- Tests de TypeScript (tsc --noEmit)
- Deploy a Vercel solo si build pasa
- Preview deployment en cada PR

Genera .github/workflows/deploy.yml con comments explicando cada step.
```

**La IA generará**:
```yaml
name: Deploy Full-Stack

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests
        run: |
          cd backend
          pytest --cov=api --cov-fail-under=80

      - name: Lint with ruff
        run: |
          cd backend
          ruff check api/

  deploy-backend:
    needs: test-backend
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@v2
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: backend

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Type check
        run: |
          cd frontend
          npx tsc --noEmit

      - name: Build
        run: |
          cd frontend
          npm run build

  deploy-frontend:
    needs: test-frontend
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./frontend
```

---

### 4. Monitoreo y Alertas con IA

#### Prompt para setup de Sentry

```
Integra Sentry en mi app full-stack para error tracking:

Backend (FastAPI):
- Capturar excepciones no manejadas
- Capturar errores 500
- Incluir contexto: user_id (desde JWT), endpoint, request body
- Filtrar información sensible (passwords, tokens)

Frontend (React):
- Capturar errores de componentes (Error Boundary)
- Capturar rechazos de promesas (network errors)
- Incluir contexto: user info, current route, browser info
- Source maps para stacktraces legibles

Genera código completo con comentarios educativos.
```

**La IA generará integración completa de Sentry** en ambos lados con scrubbing de datos sensibles.

---

### 5. Ejercicios Prácticos con IA

#### Ejercicio 1: Optimización de Bundle Size

**Prompt**:
```
Analiza mi bundle de React y sugiere optimizaciones:

Ejecuto `npm run build` y obtengo:
dist/index.html                   0.46 kB
dist/assets/index-CZlMvP14.css    5.23 kB │ gzip: 1.67 kB
dist/assets/index-DiwWXN24.js   183.42 kB │ gzip: 58.93 kB

El bundle es demasiado grande (183KB). ¿Cómo lo reduzco?

Dependencias: react, react-dom, react-router-dom, axios, react-hook-form, zod, lucide-react
```

**La IA te guiará**:
1. Code splitting de vendor
2. Lazy loading de rutas
3. Tree-shaking de lucide-react (importar iconos específicos)
4. Análisis con rollup-plugin-visualizer
5. Target bundle size: <100KB gzipped

---

#### Ejercicio 2: Configurar Custom Domain

**Prompt**:
```
Tengo un dominio comprado en Namecheap: myapp.com

Quiero:
- myapp.com → Frontend (Vercel)
- api.myapp.com → Backend (Railway)

Dame paso a paso cómo configurar DNS records y SSL certificates.
```

**La IA te dará**:
1. Configuración de DNS en Namecheap
2. Agregar custom domain en Vercel/Railway
3. Verificación de SSL certificates
4. Testing con `dig` y `curl`

---

## Production Checklist

Usa esta checklist antes de cada deployment a producción:

### Backend Checklist

- [ ] **Environment Variables**
  - [ ] `JWT_SECRET` configurado (generado con `openssl rand -hex 32`)
  - [ ] `FRONTEND_URL` apunta al dominio correcto de producción
  - [ ] `MODE=production` configurado
  - [ ] Todas las variables requeridas están en Railway/Render dashboard

- [ ] **Security**
  - [ ] CORS configurado con origin específico (no `["*"]`)
  - [ ] JWT expiration configurado (default: 60 minutos)
  - [ ] Passwords hasheados con bcrypt (nunca plaintext)
  - [ ] Secrets no están en código (usar env vars)

- [ ] **Performance**
  - [ ] Gunicorn con 2-4 workers (según plan)
  - [ ] Health check endpoint responde rápido (<100ms)
  - [ ] Logging configurado (INFO level, no DEBUG)

- [ ] **Testing**
  - [ ] Todos los tests pasan (`pytest --cov=api`)
  - [ ] Coverage mínimo 80%
  - [ ] Tests de endpoints protegidos (401 si no hay token)

- [ ] **Monitoring**
  - [ ] Health check verificado manualmente (`curl /health`)
  - [ ] Logs accesibles en Railway/Render dashboard
  - [ ] (Opcional) Sentry configurado para error tracking

### Frontend Checklist

- [ ] **Build**
  - [ ] `npm run build` completa sin errores
  - [ ] Bundle size <150KB gzipped (verificar con build output)
  - [ ] No warnings de TypeScript (`npx tsc --noEmit`)

- [ ] **Environment Variables**
  - [ ] `VITE_API_URL` apunta al backend correcto
  - [ ] Variable configurada en Vercel/Netlify dashboard
  - [ ] No hay URLs hardcodeadas en código

- [ ] **Functionality**
  - [ ] Login/Register funcionan en producción
  - [ ] Protected routes redirigen correctamente
  - [ ] Token se persiste en localStorage
  - [ ] Auto-logout funciona si token expira

- [ ] **Performance**
  - [ ] Code splitting configurado (vendor, forms chunks)
  - [ ] Lazy loading de rutas no críticas
  - [ ] Images optimizadas (webp, lazy loading)
  - [ ] No console.log en build de producción

- [ ] **Browser Testing**
  - [ ] Funciona en Chrome, Firefox, Safari
  - [ ] Mobile responsive (test en DevTools mobile view)
  - [ ] No errores en DevTools console
  - [ ] HTTPS funciona (certificado SSL válido)

### DevOps Checklist

- [ ] **Git**
  - [ ] Rama `main` protegida (requiere PR)
  - [ ] Pre-push hooks funcionan (tests, linting)
  - [ ] Commits siguen Conventional Commits

- [ ] **CI/CD**
  - [ ] GitHub Actions workflow configurado
  - [ ] Tests corren en cada PR
  - [ ] Deploy automático a producción (solo en main)

- [ ] **Monitoring**
  - [ ] Health check endpoint monitoreado
  - [ ] Logs revisables en dashboard
  - [ ] (Opcional) Uptime monitoring (UptimeRobot, Pingdom)

- [ ] **Rollback Plan**
  - [ ] Saber cómo hacer rollback en Railway/Vercel
  - [ ] Backup de environment variables
  - [ ] Documentación de versión anterior

---

## Monitoreo y Debugging

### 1. Railway Logs

**Ver logs en vivo**:
```bash
railway logs
```

**Filtrar errors**:
```bash
railway logs | grep ERROR
```

**Logs en Dashboard**:
Railway → **Deployments** → Click deployment → **View Logs**

**Qué buscar**:
- `✅ All required environment variables are set` (startup correcto)
- Requests HTTP: `200 POST /auth/login` (success)
- Errors: `500 Internal Server Error` (revisar stacktrace)

### 2. Vercel Logs

**Ver logs de build**:
Vercel Dashboard → **Deployments** → Click deployment → **Building**

**Ver logs de runtime**:
Vercel Dashboard → **Functions** → Click function → **Logs**

**Qué buscar**:
- Build time (debe ser <60 segundos)
- Bundle size (debe ser <150KB gzipped)
- Warnings de TypeScript

### 3. Debugging de CORS

**Síntoma**: Frontend no puede hacer requests, error en console:
```
Access to fetch at 'https://api.railway.app/auth/login' from origin 'https://myapp.vercel.app' has been blocked by CORS policy
```

**Diagnóstico**:
```bash
# Verificar que backend responde a preflight request
curl -X OPTIONS https://api.railway.app/auth/login \
  -H "Origin: https://myapp.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Debe retornar:
# Access-Control-Allow-Origin: https://myapp.vercel.app
```

**Solución**:
1. Verificar que `FRONTEND_URL` en Railway coincide con URL de Vercel
2. CORS debe tener `allow_credentials=True`
3. Frontend debe enviar `credentials: 'include'` en axios

### 4. Debugging de JWT

**Síntoma**: Login funciona pero requests a `/auth/me` dan 401

**Diagnóstico**:
1. Verificar que token se guarda en localStorage (DevTools → Application → Local Storage)
2. Verificar que Axios interceptor agrega header (DevTools → Network → Request Headers)
3. Decodificar JWT manualmente en [jwt.io](https://jwt.io) para verificar expiration

**Solución**:
```typescript
// Verificar que token se está enviando
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  console.log('Token:', token);  // DEBUG: verificar que existe
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 5. Health Check Monitoring

**Setup UptimeRobot** (free tier: 50 monitors):
1. Crear cuenta en [uptimerobot.com](https://uptimerobot.com)
2. **Add Monitor**:
   - Type: HTTP(S)
   - URL: `https://your-api.railway.app/health`
   - Monitoring Interval: 5 minutes
   - Alert Contacts: tu email
3. Recibir notificación si health check falla

---

## Ejercicios y Mejoras

### Nivel Básico

1. **Deploy completo**
   - Deploy backend a Railway
   - Deploy frontend a Vercel
   - Verificar que login funciona end-to-end

2. **Custom domain**
   - Configurar `myapp.com` en Vercel
   - Configurar `api.myapp.com` en Railway
   - Actualizar environment variables

3. **Production checklist**
   - Completar todos los items de la checklist anterior
   - Documentar cualquier issue encontrado

### Nivel Intermedio

4. **CI/CD con GitHub Actions**
   - Configurar workflow de deploy automático
   - Tests deben pasar antes de deploy
   - Preview deployments en cada PR

5. **Optimización de bundle**
   - Reducir bundle de React a <100KB gzipped
   - Lazy loading de rutas
   - Análisis con rollup-plugin-visualizer

6. **Error tracking con Sentry**
   - Integrar Sentry en backend y frontend
   - Probar error tracking con excepción intencional
   - Configurar alertas por email

### Nivel Avanzado

7. **Database en producción**
   - Agregar PostgreSQL en Railway
   - Migrar de repositorio in-memory a PostgreSQL
   - Configurar backups automáticos

8. **Rate limiting**
   - Agregar rate limiting a endpoints de auth
   - 5 requests/minuto por IP
   - Retornar 429 Too Many Requests

9. **Multi-region deployment**
   - Deploy backend a Railway (US) y Render (EU)
   - Load balancer con Cloudflare
   - Latency testing con `curl -w`

---

## Recursos Adicionales

### Plataformas de Deployment

- **Railway**: [docs.railway.app](https://docs.railway.app)
- **Render**: [render.com/docs](https://render.com/docs)
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **Netlify**: [docs.netlify.com](https://docs.netlify.com)

### Monitoring y Observability

- **Sentry** (error tracking): [docs.sentry.io](https://docs.sentry.io)
- **UptimeRobot** (uptime monitoring): [uptimerobot.com](https://uptimerobot.com)
- **LogRocket** (session replay): [logrocket.com](https://logrocket.com)

### Build Optimization

- **Vite Docs**: [vitejs.dev/guide/build](https://vitejs.dev/guide/build)
- **Rollup Visualizer**: [github.com/btd/rollup-plugin-visualizer](https://github.com/btd/rollup-plugin-visualizer)
- **Web.dev Performance**: [web.dev/fast](https://web.dev/fast)

### Security

- **OWASP Cheat Sheets**: [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org)
- **JWT Best Practices**: [jwt.io/introduction](https://jwt.io/introduction)

### DevOps

- **GitHub Actions**: [docs.github.com/actions](https://docs.github.com/en/actions)
- **12 Factor App**: [12factor.net](https://12factor.net)

---

## Glosario

- **PaaS**: Platform as a Service - Plataforma que gestiona infraestructura por ti
- **CDN**: Content Delivery Network - Red de servidores distribuidos globalmente
- **Edge Location**: Servidor de CDN cercano geográficamente al usuario
- **Cold Start**: Tiempo de inicialización de una app después de dormir (free tier)
- **Health Check**: Endpoint que verifica que tu app está viva
- **Environment Variable**: Variable de configuración inyectada en runtime
- **Build Optimization**: Proceso de reducir bundle size y mejorar performance
- **Tree-shaking**: Eliminar código no usado del bundle final
- **Code Splitting**: Dividir bundle en múltiples chunks para carga paralela
- **Gunicorn**: Process manager para Python web apps
- **Rollback**: Volver a una versión anterior del deployment
- **Preview Deployment**: Deployment temporal para cada PR (testing)

---

**Siguiente clase**: Módulo 5 - Clase 5: Base de Datos en Producción (PostgreSQL + Alembic migrations)

**Clase anterior**: [Módulo 5 - Clase 3: Autenticación Full-Stack](../Clase%203%20-%20Autenticacion%20Full-Stack/README.md)
