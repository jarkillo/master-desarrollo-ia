# Deployment Checklist - AI Dev Academy Game

## ✅ Pre-Deployment (Completed)

- [x] Backend Dockerfile created (multi-stage, optimized)
- [x] Backend `.dockerignore` configured
- [x] Backend `railway.toml` configured
- [x] Backend `.env.example` created
- [x] Backend `app/config.py` for environment management
- [x] Frontend `vercel.json` configured
- [x] Frontend `.env.production` created
- [x] CORS configuration updated (dynamic via env vars)
- [x] Health check endpoint verified
- [x] Documentation complete (DEPLOY.md, RAILWAY_SETUP.md, VERCEL_SETUP.md)
- [x] Code validated against best practices

## 📋 Deployment Steps (To Execute)

### Phase 1: Backend Deployment (Railway)

- [ ] Go to https://railway.app
- [ ] Create new project
- [ ] Connect GitHub repository
- [ ] Set root directory: `ai-dev-academy-game/backend`
- [ ] Add environment variables:
  ```
  ENVIRONMENT=production
  DATABASE_URL=sqlite:///./ai_dev_academy.db
  ALLOWED_ORIGINS=https://your-frontend.vercel.app
  SECRET_KEY=<generate with: openssl rand -hex 32>
  API_TITLE=AI Dev Academy API
  API_VERSION=1.0.0
  ```
- [ ] Deploy and wait for completion
- [ ] Copy Railway URL: `https://__________.railway.app`
- [ ] Test health endpoint: `curl https://__________.railway.app/health`

### Phase 2: Frontend Deployment (Vercel)

- [ ] Go to https://vercel.com
- [ ] Import GitHub repository
- [ ] Configure:
  - Framework: Vite
  - Root Directory: `ai-dev-academy-game/frontend`
  - Build Command: `npm run build`
  - Output Directory: `dist`
- [ ] Add environment variables:
  ```
  VITE_API_URL=https://__________.railway.app
  VITE_DEFAULT_PLAYER_ID=1
  VITE_ENVIRONMENT=production
  ```
- [ ] Deploy and wait for completion
- [ ] Copy Vercel URL: `https://__________.vercel.app`

### Phase 3: CORS Configuration

- [ ] Go back to Railway dashboard
- [ ] Update `ALLOWED_ORIGINS` variable:
  ```
  ALLOWED_ORIGINS=https://__________.vercel.app
  ```
- [ ] Wait for Railway to redeploy (~2-3 minutes)

### Phase 4: Testing

- [ ] Open frontend URL in browser
- [ ] Open browser DevTools (F12) → Console
- [ ] Verify no CORS errors
- [ ] Start a Bug Hunt game
- [ ] Complete the game
- [ ] Check leaderboard
- [ ] Verify XP is saved

### Phase 5: Post-Deployment (Optional)

- [ ] Add custom domain to Vercel
- [ ] Update `ALLOWED_ORIGINS` with custom domain
- [ ] Add custom domain to Railway (if needed)
- [ ] Set up monitoring (UptimeRobot, etc.)
- [ ] Configure PostgreSQL (for data persistence)

## 🔍 Verification Commands

```bash
# Backend health
curl https://__________.railway.app/health

# Backend API docs
# Open in browser: https://__________.railway.app/docs

# Test Bug Hunt start
curl -X POST https://__________.railway.app/api/minigames/bug-hunt/start \
  -H "Content-Type: application/json" \
  -d '{"player_id": 1, "difficulty": "easy"}'
```

## 🚨 Common Issues

### CORS Errors
**Symptom:** Browser shows CORS policy errors
**Solution:**
1. Verify `ALLOWED_ORIGINS` in Railway matches Vercel URL exactly
2. No trailing slashes
3. Redeploy backend

### 404 on API Calls
**Symptom:** All API calls return 404
**Solution:**
1. Verify `VITE_API_URL` in Vercel is correct
2. Check Railway logs for errors
3. Test backend health endpoint directly

### Environment Variables Not Working
**Symptom:** Frontend shows undefined values
**Solution:**
1. Redeploy frontend after adding env vars
2. Clear browser cache (Ctrl+Shift+R)
3. Verify variables start with `VITE_` prefix

## 📊 Success Metrics

Deployment is successful when:
- ✅ Backend health endpoint returns `{"status":"healthy"}`
- ✅ Frontend loads without errors
- ✅ No CORS errors in browser console
- ✅ Can start and complete a Bug Hunt game
- ✅ Leaderboard shows scores
- ✅ XP is persisted

## 📚 Documentation Reference

- **Complete Guide**: `DEPLOY.md` (step-by-step, 12 sections)
- **Railway Details**: `backend/RAILWAY_SETUP.md`
- **Vercel Details**: `frontend/VERCEL_SETUP.md`
- **Local Development**: `SETUP.md`

## 🎯 Estimated Time

- Backend deployment: 10-15 minutes
- Frontend deployment: 10-15 minutes
- CORS configuration: 5 minutes
- Testing: 10 minutes
- **Total: ~40-50 minutes**

## 🔐 Security Notes

- Generate a secure `SECRET_KEY` (don't use default)
- Only include necessary origins in `ALLOWED_ORIGINS`
- For production with real users, migrate to PostgreSQL
- Consider adding rate limiting (future enhancement)

---

**Last Updated:** 2025-10-25
**Issue:** JAR-239
**Status:** Ready to Deploy 🚀
