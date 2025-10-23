# Backend Deployment Configuration

## Procfile Variants

Este directorio incluye diferentes configuraciones de Procfile según tu plan de hosting:

### 1. `Procfile` (Default - Hobby/Pro Tier)

```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.api:app --bind 0.0.0.0:$PORT
```

**Uso**: Railway Hobby ($5/month), Render Starter ($7/month), o superior

**Características**:
- 4 workers: Soporta hasta ~400 requests concurrentes
- Requiere: 1-2GB RAM
- Ventajas: Alta concurrencia, tolerancia a fallos (si 1 worker crashea, otros siguen)

### 2. `Procfile.free-tier` (Free Tier)

```
web: gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.api:app --bind 0.0.0.0:$PORT --timeout 120
```

**Uso**: Railway Free Tier, Render Free Tier

**Características**:
- 1 worker: ~100 requests concurrentes
- Requiere: 512MB RAM
- Timeout: 120s (para cold starts más lentos)

**Para usar en free tier**:
```bash
# Renombrar Procfile
mv Procfile Procfile.paid
mv Procfile.free-tier Procfile

# Commit y push
git add Procfile
git commit -m "chore: usar Procfile para free tier"
git push origin main
```

---

## Environment Variables

### Required (Producción)

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `JWT_SECRET` | Secret key para firmar JWT | `openssl rand -hex 32` |
| `FRONTEND_URL` | URL del frontend (CORS) | `https://myapp.vercel.app` |

### Optional (con defaults)

| Variable | Default | Descripción |
|----------|---------|-------------|
| `JWT_ALGORITHM` | `HS256` | Algoritmo JWT |
| `JWT_EXPIRATION_MINUTES` | `60` | Duración del token |
| `MODE` | `production` | Environment mode |

### Setup en Railway

1. Railway Dashboard → **Variables**
2. Click **+ New Variable**
3. Agregar cada variable
4. Railway auto-redeploys

### Setup en Render

1. Render Dashboard → **Environment**
2. Agregar variables en formato `KEY=value`
3. Click **Save Changes**

---

## Health Check Endpoint

### `/health`

**Response**:
```json
{
  "status": "ok",
  "timestamp": "2025-10-23T12:34:56.789Z",
  "version": "1.0.0",
  "environment": "production"
}
```

**Uso en monitoring**:
- Railway: Health check automático cada 30s
- Render: Health check cada 60s
- UptimeRobot: Configurar con esta URL

**Testing**:
```bash
curl https://your-api.railway.app/health
```

---

## Logging

### Configuración

El logging está configurado dinámicamente según `MODE`:

```python
logging.basicConfig(
    level=logging.INFO if os.getenv("MODE") == "production" else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Ver logs

**Railway**:
```bash
railway logs
```

O en Dashboard → **Deployments** → **View Logs**

**Render**:
Dashboard → **Logs**

### Qué buscar en logs

✅ **Startup exitoso**:
```
✅ All required environment variables are set
CORS configured for origins: ['https://myapp.vercel.app']
```

❌ **Error de environment variables**:
```
❌ Missing required environment variables: JWT_SECRET
ValueError: Missing required environment variables: JWT_SECRET
```

---

## Testing Pre-Deployment

Antes de deployar, ejecuta:

```bash
# Tests
pytest --cov=api --cov-fail-under=80

# Linting
ruff check api/

# Security audit
bandit -r api/ -ll

# Simular producción localmente
MODE=production uvicorn api.api:app --reload
```

---

## Performance Tuning

### Workers Calculation

**Regla general**: `workers = (2 x CPU cores) + 1`

**Memory per worker**: ~128-256MB para FastAPI simple

**Ejemplos**:
- **512MB RAM**: 1-2 workers máximo
- **1GB RAM**: 3-4 workers
- **2GB RAM**: 6-8 workers

### Gunicorn Options

```bash
# Producción standard
gunicorn -w 4 \
  -k uvicorn.workers.UvicornWorker \
  api.api:app \
  --bind 0.0.0.0:$PORT \
  --timeout 60 \
  --graceful-timeout 30 \
  --keep-alive 5 \
  --log-level info
```

**Opciones explicadas**:
- `-w 4`: 4 workers (ajustar según RAM)
- `-k uvicorn.workers.UvicornWorker`: Worker class para ASGI
- `--timeout 60`: Request timeout (60s)
- `--graceful-timeout 30`: Tiempo para terminar requests al shutdown
- `--keep-alive 5`: Keep-alive connections por 5s
- `--log-level info`: Nivel de logging

---

## Troubleshooting

### App no inicia

**Síntoma**: Railway/Render muestra "Crashed"

**Solución**:
1. Verificar logs: `railway logs` o Render Dashboard
2. Buscar errores de environment variables
3. Verificar que `Procfile` existe y es correcto
4. Verificar que `requirements.txt` incluye `gunicorn`

### Out of Memory (OOM)

**Síntoma**: App se reinicia aleatoriamente

**Solución**:
1. Reducir número de workers en Procfile
2. Verificar memory usage en Railway/Render dashboard
3. Considerar upgrade de plan

### Cold Starts (Free Tier)

**Síntoma**: Primera request tarda 30-60s

**Solución**:
- **Railway**: No tiene cold starts significativos
- **Render Free**: Cold start después de 15min inactividad (inevitable en free tier)
- **Solución**: Upgrade a paid tier ($7/month = 0 cold starts)

---

## Security Checklist

- [ ] JWT_SECRET generado con `openssl rand -hex 32`
- [ ] CORS configurado con URL específica (no wildcard)
- [ ] Secrets en environment variables (no hardcoded)
- [ ] MODE=production configurado
- [ ] HTTPS activado (Railway/Render lo hacen automáticamente)
- [ ] No logs de passwords/tokens
- [ ] Dependencies actualizadas (`pip list --outdated`)

---

## Resources

- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Uvicorn Workers](https://www.uvicorn.org/deployment/)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
