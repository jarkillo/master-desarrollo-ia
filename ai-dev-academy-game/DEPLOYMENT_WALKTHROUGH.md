# 🚀 Guía Paso a Paso: Deployment del AI Dev Academy Game

**Última actualización**: 2025-11-02
**Estimado**: 1-2 horas
**Prerrequisitos verificados**: ✅ Docker Desktop instalado, ✅ GitHub repo listo

---

## 🎯 ¿Qué vamos a hacer?

Vamos a desplegar tu juego en **producción gratis** usando:
- **Railway** para el backend (FastAPI)
- **Vercel** para el frontend (React)

**Resultado final**: 2 URLs públicas donde cualquiera puede jugar tu game.

---

## 📚 Antes de Empezar: Conceptos Clave

### ¿Qué es Railway?
Railway es una plataforma que ejecuta tu código backend en la nube. Piénsalo como "una computadora en internet" que corre tu API 24/7.

**Analogía**: Es como tener un servidor dedicado en tu casa, pero sin tener que mantenerlo tú.

### ¿Qué es Vercel?
Vercel es una plataforma optimizada para aplicaciones frontend (React, Next.js, etc.). Sirve tu HTML/CSS/JS desde una CDN global ultra-rápida.

**Analogía**: Es como tener tu sitio web alojado en 100 servidores alrededor del mundo simultáneamente.

### ¿Qué es Docker?
Docker empaqueta tu aplicación con todas sus dependencias en un "contenedor". Esto asegura que funcione igual en desarrollo y producción.

**Analogía**: Es como un contenedor de transporte marítimo: puedes mover tu app de un lugar a otro y siempre funcionará igual.

### ¿Por qué este orden?
1. Primero desplegamos el **backend** (Railway) → obtenemos su URL
2. Luego desplegamos el **frontend** (Vercel) → configuramos la URL del backend
3. Finalmente conectamos ambos con **CORS**

---

## 📋 Fase 1: Preparación Local (5 minutos)

### Paso 1.1: Verificar que Docker Build funciona

Ya lo hicimos y está ✅. Tu Docker image se creó correctamente:

```
ai-dev-academy-backend:test
Size: 319MB (esto es bueno, no es muy pesada)
```

### Paso 1.2: Verificar que tu código está en GitHub

```bash
# Verifica que tengas remote configurado
git remote -v

# Deberías ver algo como:
# origin  https://github.com/tu-usuario/master-ia-manu.git (fetch)
# origin  https://github.com/tu-usuario/master-ia-manu.git (push)
```

Si todo está OK, continuamos. 🚀

---

## 🏗️ Fase 2: Deploy Backend a Railway (20-30 min)

### Paso 2.1: Crear cuenta en Railway

1. Ve a https://railway.app
2. Click en "Start a New Project" o "Login with GitHub"
3. Autoriza Railway a acceder a tu GitHub (esto es seguro, es como darle permisos a Vercel)

**Tip**: Usa "Login with GitHub" para conectar automáticamente tu repo.

### Paso 2.2: Crear nuevo proyecto

**Opción A: Desde el Dashboard Web (Recomendado para primera vez)**

1. Click en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Busca tu repositorio `master-ia-manu` (o como lo hayas llamado)
4. Click en el repo para seleccionarlo

**Railway te preguntará**: "¿Qué directorio quieres desplegar?"
- **Respuesta**: `ai-dev-academy-game/backend`

**Railway te preguntará**: "¿Cómo quieres buildear?"
- **Respuesta**: "Dockerfile" (Railway detectará automáticamente el Dockerfile)

5. Click en "Deploy"

**Opción B: Usando Railway CLI (Para usuarios avanzados)**

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login a Railway
railway login

# Ir al directorio del backend
cd ai-dev-academy-game/backend

# Inicializar proyecto
railway init

# Desplegar
railway up
```

### Paso 2.3: Configurar Variables de Entorno en Railway

Esto es **CRÍTICO**. Sin estas variables, tu API no funcionará correctamente.

1. En el dashboard de Railway, click en tu proyecto
2. Ve a la pestaña "Variables"
3. Agrega las siguientes variables (click en "+ New Variable"):

```
ENVIRONMENT=production
DATABASE_URL=sqlite:///./ai_dev_academy.db
ALLOWED_ORIGINS=http://localhost:5173
SECRET_KEY=TEMPORAL_CHANGE_LATER
API_TITLE=AI Dev Academy API
API_VERSION=1.0.0
```

**⚠️ IMPORTANTE sobre `ALLOWED_ORIGINS`**:
- Por ahora dejamos `http://localhost:5173` (temporal)
- Lo cambiaremos más tarde cuando tengamos la URL de Vercel

**⚠️ IMPORTANTE sobre `SECRET_KEY`**:
- Este valor temporal es OK por ahora
- Generaremos uno seguro después con OpenSSL

### Paso 2.4: Verificar el Deployment

Railway empezará a buildear automáticamente. Verás logs en tiempo real.

**Tiempos esperados**:
- Build: ~3-5 minutos (primera vez)
- Deploy: ~30 segundos

**Cómo saber si funcionó**:
1. En Railway, ve a "Deployments"
2. Verás un deployment con status "Success" ✅
3. Railway te dará una URL automática: `https://[nombre-random].up.railway.app`

**Ejemplo de URL**: `https://ai-dev-academy-production.up.railway.app`

### Paso 2.5: Probar el Backend

Copia la URL que te dio Railway y prueba estos endpoints:

```bash
# Health check (debe responder {"status":"healthy"})
curl https://TU-URL.railway.app/health

# Root endpoint (debe responder con info de la API)
curl https://TU-URL.railway.app/

# API Docs (abre en navegador)
https://TU-URL.railway.app/docs
```

Si ves la documentación de Swagger, ¡funciona! 🎉

**Guarda esta URL**, la necesitarás para el frontend.

---

## 🎨 Fase 3: Deploy Frontend a Vercel (20-30 min)

### Paso 3.1: Crear cuenta en Vercel

1. Ve a https://vercel.com
2. Click en "Sign Up"
3. Selecciona "Continue with GitHub"
4. Autoriza Vercel

### Paso 3.2: Importar Proyecto desde GitHub

1. En el dashboard de Vercel, click en "Add New..." → "Project"
2. Busca tu repositorio `master-ia-manu`
3. Click en "Import"

### Paso 3.3: Configurar el Proyecto

Vercel te mostrará un formulario de configuración. Rellénalo así:

**Framework Preset**:
- Selecciona "Vite" (Vercel lo detectará automáticamente)

**Root Directory**:
- Click en "Edit" junto a "Root Directory"
- Escribe: `ai-dev-academy-game/frontend`
- Click en "Continue"

**Build Settings** (esto ya debería estar correcto por vercel.json):
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

**Environment Variables** (MUY IMPORTANTE):

Click en "Environment Variables" y agrega:

```
VITE_API_URL = https://TU-URL-DE-RAILWAY.railway.app
VITE_DEFAULT_PLAYER_ID = 1
VITE_ENVIRONMENT = production
```

**⚠️ CRÍTICO**: Reemplaza `TU-URL-DE-RAILWAY` con la URL real que obtuviste en Paso 2.5

**⚠️ NO pongas `/` al final de VITE_API_URL**:
- ✅ Correcto: `https://ai-dev-academy.up.railway.app`
- ❌ Incorrecto: `https://ai-dev-academy.up.railway.app/`

### Paso 3.4: Deploy

1. Click en "Deploy"
2. Vercel empezará a buildear

**Tiempos esperados**:
- Build: ~2-3 minutos
- Deploy: ~15 segundos

### Paso 3.5: Obtener URL de Vercel

Cuando termine, Vercel te dará una URL:

**Ejemplo**: `https://ai-dev-academy-game.vercel.app`

**Guarda esta URL**, la necesitarás para configurar CORS.

### Paso 3.6: Probar el Frontend (Va a fallar, es normal)

Abre la URL de Vercel en tu navegador.

**¿Qué va a pasar?**:
- ✅ El frontend carga
- ❌ NO funciona (errores CORS en consola)

**Esto es NORMAL**. Continuamos al siguiente paso para arreglarlo.

---

## 🔗 Fase 4: Conectar Frontend ↔ Backend con CORS (10 min)

### ¿Qué es CORS y por qué falla?

**CORS** = Cross-Origin Resource Sharing

**Analogía**: Es como un guardia de seguridad que solo deja entrar a personas en una lista.

Ahora mismo, tu backend (Railway) solo permite requests desde `http://localhost:5173` (desarrollo). Necesitamos agregar la URL de Vercel a la "lista de permitidos".

### Paso 4.1: Actualizar ALLOWED_ORIGINS en Railway

1. Ve a Railway dashboard
2. Click en tu proyecto backend
3. Ve a "Variables"
4. Busca `ALLOWED_ORIGINS`
5. Edita el valor a:

```
https://TU-URL-DE-VERCEL.vercel.app
```

**⚠️ IMPORTANTE**:
- NO pongas `http://` (debe ser `https://`)
- NO pongas `/` al final
- Copia la URL exacta de Vercel

**Ejemplo correcto**:
```
ALLOWED_ORIGINS=https://ai-dev-academy-game.vercel.app
```

### Paso 4.2: Redeploy del Backend

Railway detectará el cambio y hará redeploy automáticamente (~30 segundos).

**Cómo verificar**:
- Ve a "Deployments" en Railway
- Verás un nuevo deployment "in progress"
- Espera a que diga "Success"

### Paso 4.3: Verificar que CORS funciona

1. Abre tu frontend en Vercel: `https://TU-URL.vercel.app`
2. Abre DevTools (F12)
3. Ve a la pestaña "Console"

**¿Qué buscamos?**:
- ❌ Antes veías: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`
- ✅ Ahora NO deberías ver errores CORS

4. Ve a la pestaña "Network"
5. Recarga la página (F5)
6. Busca requests a tu API de Railway
7. Deberían tener status **200 OK** ✅

Si ves status 200, ¡funciona! 🎉

---

## ✅ Fase 5: Testing End-to-End (15 min)

### Paso 5.1: Verificar Health del Backend

```bash
curl https://TU-URL.railway.app/health
```

**Esperado**: `{"status":"healthy"}`

### Paso 5.2: Probar Bug Hunt Game

1. Abre frontend en Vercel
2. Click en "Start Bug Hunt"
3. Selecciona dificultad "Easy"
4. Debería cargar el código con bugs
5. Intenta jugar:
   - Selecciona líneas con bugs
   - Click en "Submit"
   - Verifica que muestre resultados
   - Verifica que otorgue XP

### Paso 5.3: Verificar Leaderboard

1. En el frontend, ve a "Leaderboard"
2. Debería mostrar tu score
3. Verifica que los datos persistan (recarga la página)

### Paso 5.4: Cross-Browser Testing

Prueba en:
- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari (si tienes Mac)

### Paso 5.5: Mobile Testing

Abre la URL de Vercel en tu móvil:
- ✅ Responsive design funciona
- ✅ Puedes jugar en touch screen

---

## 🎯 Fase 6: Optimizaciones Opcionales (15-30 min)

### Opción 1: Custom Domain (Opcional)

**En Vercel**:
1. Ve a "Settings" → "Domains"
2. Agrega tu dominio (ej: `ai-dev-academy.tudominio.com`)
3. Sigue instrucciones DNS

**En Railway**:
1. Ve a "Settings" → "Domains"
2. Agrega tu dominio (ej: `api.tudominio.com`)
3. Sigue instrucciones DNS

**Luego actualiza ALLOWED_ORIGINS** en Railway:
```
ALLOWED_ORIGINS=https://ai-dev-academy.tudominio.com,https://ai-dev-academy-game.vercel.app
```

### Opción 2: SECRET_KEY Seguro

Genera un secret key seguro:

```bash
# En WSL o Git Bash
openssl rand -hex 32
```

Copia el resultado y actualiza `SECRET_KEY` en Railway.

### Opción 3: PostgreSQL (Para persistencia real)

**⚠️ Limitación actual**: SQLite en Railway es **efímero** (datos se pierden en redeploy).

**Solución**:
1. En Railway, click en "New" → "Database" → "PostgreSQL"
2. Railway creará automáticamente `DATABASE_URL`
3. No necesitas cambiar código (SQLAlchemy lo maneja automáticamente)

**Trade-off**: PostgreSQL consume más recursos del tier gratuito.

---

## 📝 Fase 7: Documentación (10 min)

### Paso 7.1: Guardar URLs de Producción

Actualiza `DEPLOYMENT_CHECKLIST.md` con tus URLs reales:

```markdown
## Production URLs

- **Frontend**: https://ai-dev-academy-game.vercel.app
- **Backend**: https://ai-dev-academy-production.up.railway.app
- **API Docs**: https://ai-dev-academy-production.up.railway.app/docs
```

### Paso 7.2: Actualizar README

Agrega badges y links a producción:

```markdown
## 🌐 Demo en Vivo

- **Juega aquí**: https://ai-dev-academy-game.vercel.app
- **API Docs**: https://ai-dev-academy-production.up.railway.app/docs
```

---

## 🚨 Troubleshooting

### Error: "CORS policy blocked"

**Síntoma**: Frontend no puede conectarse al backend

**Solución**:
1. Verifica `ALLOWED_ORIGINS` en Railway
2. Asegura que sea `https://` (no `http://`)
3. Sin `/` al final
4. Espera a que Railway redeploy (~30s)
5. Clear cache del navegador (Ctrl+Shift+R)

### Error: "Failed to fetch"

**Síntoma**: Frontend no puede llamar al backend

**Solución**:
1. Verifica `VITE_API_URL` en Vercel
2. Prueba el backend directamente: `curl https://TU-URL.railway.app/health`
3. Verifica logs de Railway (puede estar crasheado)

### Error: Build falla en Railway

**Síntoma**: Railway no puede buildear la imagen Docker

**Solución**:
1. Verifica que `Dockerfile` esté en `backend/`
2. Verifica que `requirements.txt` esté completo
3. Revisa logs de Railway para ver el error exacto

### Error: Build falla en Vercel

**Síntoma**: Vercel no puede buildear React

**Solución**:
1. Verifica Root Directory: `ai-dev-academy-game/frontend`
2. Verifica que `package.json` tenga `"build": "tsc && vite build"`
3. Revisa logs de Vercel para errores de TypeScript

### Frontend carga pero no hay datos

**Síntoma**: Juego carga pero leaderboard vacío, no hay módulos

**Solución**:
1. Backend puede estar sin datos iniciales
2. Railway resetea SQLite en cada deploy
3. Considera migrar a PostgreSQL (ver Fase 6, Opción 3)

---

## 📊 Métricas de Éxito

Marca cada item cuando esté completo:

- [ ] Backend desplegado en Railway
- [ ] Health endpoint responde: `curl https://TU-URL.railway.app/health`
- [ ] API Docs accesibles en navegador
- [ ] Frontend desplegado en Vercel
- [ ] Frontend carga sin errores
- [ ] NO hay errores CORS en DevTools
- [ ] Bug Hunt game funciona end-to-end
- [ ] Leaderboard muestra datos
- [ ] XP se otorga correctamente
- [ ] Funciona en Chrome/Edge
- [ ] Funciona en Firefox
- [ ] Funciona en móvil (responsive)
- [ ] URLs documentadas en DEPLOYMENT_CHECKLIST.md
- [ ] README actualizado con links

---

## 🎉 ¡Deployment Completo!

Si todos los checkboxes están marcados, ¡felicidades! Has desplegado exitosamente tu aplicación full-stack a producción.

**Próximos pasos**:
- Comparte la URL con amigos/compañeros
- Monitoriza logs en Railway/Vercel
- Considera configurar alertas (UptimeRobot, Sentry)
- Documenta el proceso para futuros deploys

---

## 📚 Recursos Útiles

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Docker Docs**: https://docs.docker.com
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Vite Deployment**: https://vite.dev/guide/static-deploy.html

---

**¿Necesitas ayuda?**
- Revisa logs en Railway: Settings → Deployments → [latest] → View Logs
- Revisa logs en Vercel: Deployments → [latest] → Function Logs
- GitHub Issues de tu repo
- Stack Overflow: tags `railway`, `vercel`, `fastapi`, `vite`

---

**Creado**: 2025-11-02
**Versión**: 1.0
**Proyecto**: AI Dev Academy Game
**Stack**: FastAPI + React + Docker + Railway + Vercel
