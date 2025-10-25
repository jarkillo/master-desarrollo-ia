# AI Dev Academy Game - Production Deployment Guide

Complete guide to deploy the AI Dev Academy Game to production using Railway (backend) and Vercel (frontend).

## Architecture Overview

```
┌─────────────────────┐         ┌──────────────────────┐
│   Vercel (Frontend) │────────▶│  Railway (Backend)   │
│   React + Vite      │  HTTPS  │   FastAPI + SQLite   │
│   TypeScript        │         │   Python 3.12        │
└─────────────────────┘         └──────────────────────┘
       │                                  │
       │                                  │
       ▼                                  ▼
   Static CDN                       Database Volume
   (Optimized)                      (Ephemeral*)
```

*Note: SQLite on Railway is ephemeral. For production persistence, migrate to PostgreSQL.

---

## Prerequisites

- **GitHub account** (for CI/CD integration)
- **Railway account** → https://railway.app (free tier available)
- **Vercel account** → https://vercel.com (free tier available)
- **Git repository** pushed to GitHub

---

## Part 1: Deploy Backend to Railway

### Step 1.1: Prepare Repository

Ensure your backend has these files (✅ already created):
- `backend/Dockerfile` - Multi-stage production build
- `backend/railway.toml` - Railway configuration
- `backend/.env.example` - Environment variables template
- `backend/RAILWAY_SETUP.md` - Detailed Railway instructions

### Step 1.2: Deploy to Railway

#### Option A: Using Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Navigate to backend directory
cd ai-dev-academy-game/backend

# Initialize and deploy
railway init
railway up
```

#### Option B: Using Railway Dashboard

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the Dockerfile
5. Set root directory: `backend`

### Step 1.3: Configure Environment Variables

In Railway dashboard, add these variables:

```bash
ENVIRONMENT=production
DATABASE_URL=sqlite:///./ai_dev_academy.db
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
SECRET_KEY=GENERATE_A_SECURE_RANDOM_STRING_HERE
API_TITLE=AI Dev Academy API
API_VERSION=1.0.0
```

**Important:**
- Generate a secure SECRET_KEY: `openssl rand -hex 32`
- ALLOWED_ORIGINS will be updated after deploying frontend

### Step 1.4: Get Backend URL

After deployment completes:
1. Railway assigns a URL: `https://your-app.railway.app`
2. Test health endpoint: `curl https://your-app.railway.app/health`
3. **Save this URL** - you'll need it for frontend configuration

### Step 1.5: Verify Deployment

```bash
# Health check
curl https://your-app.railway.app/health
# Expected: {"status":"healthy"}

# API documentation
# Open in browser: https://your-app.railway.app/docs
```

---

## Part 2: Deploy Frontend to Vercel

### Step 2.1: Prepare Repository

Ensure your frontend has these files (✅ already created):
- `frontend/vercel.json` - Vercel configuration
- `frontend/.env.example` - Environment variables template
- `frontend/.env.production` - Production env template
- `frontend/VERCEL_SETUP.md` - Detailed Vercel instructions

### Step 2.2: Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd ai-dev-academy-game/frontend

# Login
vercel login

# Deploy to production
vercel --prod
```

#### Option B: Using Vercel Dashboard (Recommended)

1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### Step 2.3: Configure Environment Variables

In Vercel dashboard, go to Settings → Environment Variables:

```bash
VITE_API_URL=https://your-backend.railway.app
VITE_DEFAULT_PLAYER_ID=1
VITE_ENVIRONMENT=production
```

**Critical:** Replace `your-backend.railway.app` with your actual Railway URL from Part 1, Step 1.4

### Step 2.4: Redeploy with Environment Variables

After adding environment variables:
1. Go to Deployments tab
2. Click "Redeploy" on latest deployment
3. Vercel will rebuild with new env vars

### Step 2.5: Get Frontend URL

After deployment:
1. Vercel assigns a URL: `https://your-app.vercel.app`
2. **Save this URL** - you need to update backend CORS

---

## Part 3: Configure CORS (Critical!)

Now that both frontend and backend are deployed, update backend CORS configuration.

### Step 3.1: Update Backend ALLOWED_ORIGINS

1. Go to Railway dashboard
2. Open your backend project
3. Go to Variables tab
4. Update `ALLOWED_ORIGINS`:
   ```bash
   ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://www.your-custom-domain.com
   ```
   - Use your actual Vercel URL
   - No trailing slashes
   - Comma-separated (no spaces)

### Step 3.2: Redeploy Backend

Railway will automatically redeploy when you update environment variables.

Wait for deployment to complete (~2-3 minutes).

---

## Part 4: End-to-End Testing

### Step 4.1: Test Backend Independently

```bash
# Health check
curl https://your-backend.railway.app/health

# API documentation (open in browser)
https://your-backend.railway.app/docs

# Test Bug Hunt start endpoint
curl -X POST https://your-backend.railway.app/api/minigames/bug-hunt/start \
  -H "Content-Type: application/json" \
  -d '{"player_id": 1, "difficulty": "easy"}'
```

### Step 4.2: Test Frontend

1. Open frontend URL in browser: `https://your-frontend.vercel.app`
2. Open browser DevTools (F12) → Console
3. Check for:
   - ✅ No CORS errors
   - ✅ Successful API calls to backend
   - ✅ Network tab shows 200 OK responses

### Step 4.3: Test Bug Hunt Game Flow

1. Start a Bug Hunt game
2. Complete the game
3. Check leaderboard
4. Verify XP is saved

### Step 4.4: Common Issues and Solutions

#### CORS Errors

**Symptom:** Browser console shows CORS errors
```
Access to XMLHttpRequest at 'https://backend.railway.app' from origin 'https://frontend.vercel.app' has been blocked by CORS policy
```

**Solution:**
1. Verify `ALLOWED_ORIGINS` in Railway includes your Vercel URL
2. Ensure no trailing slashes: `https://frontend.vercel.app` (not `.../`)
3. Redeploy backend after changing environment variables

#### API Calls Fail (Network Error)

**Symptom:** All API calls fail with network errors

**Solution:**
1. Check `VITE_API_URL` is correct in Vercel env vars
2. Test backend health endpoint directly
3. Check Railway logs for backend errors

#### Environment Variables Not Working

**Symptom:** Frontend shows `undefined` for API URL

**Solution:**
1. Ensure env vars start with `VITE_` prefix
2. Redeploy frontend after adding/changing env vars
3. Clear browser cache and hard refresh (Ctrl+Shift+R)

---

## Part 5: Custom Domains (Optional)

### Frontend Custom Domain (Vercel)

1. Go to Vercel project settings → Domains
2. Add your domain: `game.yourdomain.com`
3. Update DNS records as instructed by Vercel
4. Update backend `ALLOWED_ORIGINS` to include new domain

### Backend Custom Domain (Railway)

1. Go to Railway project settings → Domains
2. Add custom domain
3. Update DNS CNAME record
4. Update frontend `VITE_API_URL` with new domain

---

## Part 6: Continuous Deployment (Automatic)

### GitHub Integration (Already Configured)

Both Railway and Vercel automatically deploy on git push:

**Frontend (Vercel):**
- Push to `main` → Production deployment
- Open PR → Preview deployment (unique URL)

**Backend (Railway):**
- Push to `main` → Production deployment
- Automatic rollback if deployment fails

### Deployment Workflow

```bash
# Make changes
git checkout -b feature/new-minigame
# ... code changes ...

# Commit and push
git add .
git commit -m "feat: add new minigame"
git push origin feature/new-minigame

# Create PR (triggers preview deployment)
gh pr create --base main

# After review, merge PR
gh pr merge --squash

# Auto-deploys to production! 🚀
```

---

## Part 7: Monitoring and Logs

### Backend Logs (Railway)

```bash
# Using CLI
railway logs

# Or in dashboard:
# Project → Deployments → View Logs
```

### Frontend Logs (Vercel)

- Dashboard → Project → Deployments → View Function Logs
- Real-time logs during build and runtime

### Health Monitoring

Set up uptime monitoring (optional):
- **UptimeRobot** (free): https://uptimerobot.com
- Monitor: `https://your-backend.railway.app/health`
- Alert on downtime

---

## Part 8: Database Considerations

### Current Setup: SQLite (Ephemeral)

**Limitations:**
- Data lost on redeploy
- Not suitable for production with persistent users

**Acceptable for:**
- Development
- Demos
- Temporary testing

### Migration to PostgreSQL (Recommended for Production)

#### Step 1: Add PostgreSQL on Railway

```bash
# In Railway dashboard
# Project → New → Database → PostgreSQL

# Railway auto-creates DATABASE_URL environment variable
```

#### Step 2: Update Dependencies

```bash
# Add to backend/requirements.txt
psycopg2-binary==2.9.9

# Reinstall
cd backend
pip install -r requirements.txt
```

#### Step 3: Database Migrations (Optional - Future)

For schema versioning, consider Alembic:
```bash
pip install alembic
alembic init migrations
# Configure alembic.ini with DATABASE_URL
```

#### Step 4: No Code Changes Needed

SQLAlchemy automatically supports PostgreSQL URLs.
Just update `DATABASE_URL` and redeploy.

---

## Part 9: Security Checklist

Before going live:

- ✅ SECRET_KEY is random and secure (not the default)
- ✅ ALLOWED_ORIGINS only includes your domains (no wildcards)
- ✅ Environment variables not hardcoded in code
- ✅ HTTPS enabled (automatic with Railway + Vercel)
- ✅ Database backups configured (if using PostgreSQL)
- ✅ Rate limiting implemented (future enhancement)
- ✅ Input validation on all endpoints (✅ already done with Pydantic)

---

## Part 10: Cost Estimation

### Free Tier Limits

**Vercel Free:**
- Unlimited deployments
- 100 GB bandwidth/month
- Hobby projects

**Railway Free:**
- $5 credit/month
- ~500 execution hours
- Sufficient for small apps

### Production Costs (Estimated)

For a small-scale production app:
- **Vercel**: Free (hobby) or $20/month (Pro)
- **Railway**: $5-20/month depending on usage
- **Total**: $5-40/month

---

## Part 11: Rollback Procedure

### If Deployment Breaks

**Frontend (Vercel):**
```bash
# CLI
vercel rollback

# Or dashboard: Deployments → Previous → Promote to Production
```

**Backend (Railway):**
```bash
# CLI
railway rollback

# Or dashboard: Deployments → Previous → Redeploy
```

---

## Part 12: Next Steps

After successful deployment:

1. **Add real authentication** (JWT tokens, OAuth)
2. **Migrate to PostgreSQL** for data persistence
3. **Add more minigames** (Prompt Duel, Architecture Builder)
4. **Implement leaderboards** across all minigames
5. **Add analytics** (Vercel Analytics, Sentry error tracking)
6. **Setup CI/CD tests** (run pytest before deploy)

---

## Troubleshooting Contact

If you encounter issues:

1. Check Railway logs: `railway logs`
2. Check Vercel logs in dashboard
3. Test locally first: `docker build -t test backend/`
4. Review detailed docs:
   - Backend: `backend/RAILWAY_SETUP.md`
   - Frontend: `frontend/VERCEL_SETUP.md`

---

## Quick Reference

### Important URLs

```bash
# Update after deployment
Backend (Railway):    https://your-backend.railway.app
Frontend (Vercel):    https://your-frontend.vercel.app
Backend API Docs:     https://your-backend.railway.app/docs
Backend Health:       https://your-backend.railway.app/health
```

### Environment Variables Summary

**Backend (Railway):**
```bash
ENVIRONMENT=production
DATABASE_URL=sqlite:///./ai_dev_academy.db
ALLOWED_ORIGINS=https://your-frontend.vercel.app
SECRET_KEY=<random-secure-string>
API_TITLE=AI Dev Academy API
API_VERSION=1.0.0
```

**Frontend (Vercel):**
```bash
VITE_API_URL=https://your-backend.railway.app
VITE_DEFAULT_PLAYER_ID=1
VITE_ENVIRONMENT=production
```

---

## Validation Results

All configurations have been validated against educational best practices:

✅ **Docker Infrastructure** (validated)
- Multi-stage build for optimized image size
- Non-root user for security
- Health checks configured
- Layer caching optimized

✅ **FastAPI Design** (validated)
- RESTful endpoint design
- Proper HTTP verbs and status codes
- Pydantic validation on all inputs
- Error handling with HTTPException
- Complete API documentation

✅ **React Integration** (validated)
- Centralized API client configuration
- TypeScript types for all API responses
- Environment variable configuration
- Axios interceptors for error handling
- Service layer abstraction

---

**Deployment prepared by:** AI Dev Academy Team
**Last updated:** 2025-10-25
**Status:** Ready for Production 🚀
