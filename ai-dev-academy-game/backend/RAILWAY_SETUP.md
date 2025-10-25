# Railway Deployment Setup

## Prerequisites
- Railway account (https://railway.app)
- Railway CLI (optional, but recommended)

## Deployment Steps

### 1. Create a New Project on Railway

```bash
# Install Railway CLI (if not already installed)
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init
```

Or use the web interface:
1. Go to https://railway.app
2. Click "New Project"
3. Choose "Deploy from GitHub repo" or "Empty Project"

### 2. Configure Environment Variables

Set these environment variables in Railway dashboard:

```
ENVIRONMENT=production
DATABASE_URL=sqlite:///./ai_dev_academy.db
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://www.your-domain.com
SECRET_KEY=your-secure-random-secret-key-here
API_TITLE=AI Dev Academy API
API_VERSION=1.0.0
```

**Important CORS Setup:**
- After deploying frontend to Vercel, update `ALLOWED_ORIGINS` with the Vercel URL
- Format: comma-separated list with no spaces
- Example: `https://ai-dev-academy.vercel.app,https://custom-domain.com`

### 3. Deploy

#### Option A: Using Railway CLI
```bash
cd backend
railway up
```

#### Option B: Using GitHub Integration
1. Push code to GitHub
2. Connect repository in Railway dashboard
3. Railway will auto-detect the Dockerfile and deploy

### 4. Verify Deployment

After deployment, test the endpoints:

```bash
# Health check
curl https://your-app.railway.app/health

# Root endpoint
curl https://your-app.railway.app/

# API docs
# Open in browser: https://your-app.railway.app/docs
```

### 5. Database Persistence (Important!)

**SQLite Limitation on Railway:**
Railway uses ephemeral storage, so SQLite databases will be lost on redeploy.

**Solutions:**
1. **Short-term (for testing)**: Accept data loss on redeploy
2. **Production (recommended)**: Migrate to PostgreSQL

To migrate to PostgreSQL:
```bash
# Add PostgreSQL service in Railway dashboard
# Railway will auto-create DATABASE_URL

# Update requirements.txt
echo "psycopg2-binary==2.9.9" >> requirements.txt

# Update database.py to handle PostgreSQL URLs
# (No code change needed - SQLAlchemy handles it)
```

### 6. Custom Domain (Optional)

1. Go to Railway project settings
2. Add custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_ORIGINS` environment variable

## Monitoring

Railway provides:
- **Logs**: Real-time logs in dashboard
- **Metrics**: CPU, Memory, Network usage
- **Health checks**: Automatic monitoring of `/health` endpoint

## Troubleshooting

### Deployment fails
- Check Railway logs
- Verify Dockerfile builds locally: `docker build -t test .`
- Ensure all dependencies are in requirements.txt

### CORS errors
- Verify `ALLOWED_ORIGINS` includes your frontend URL
- Check frontend is using correct API URL
- Ensure no trailing slashes in origins

### Database issues
- Check `DATABASE_URL` is set correctly
- For production, migrate to PostgreSQL
- Verify database initialization in logs

## Rolling Back

```bash
# Using CLI
railway rollback

# Or use dashboard to redeploy previous version
```

## Cost Estimation

Railway free tier includes:
- $5 credit per month
- ~500 hours of execution time
- Should be sufficient for development/testing

For production:
- Estimated cost: $5-10/month for small apps
- Scales based on usage
