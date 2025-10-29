# Vercel Deployment Setup

## Prerequisites
- Vercel account (https://vercel.com)
- Vercel CLI (optional, but recommended)
- Backend already deployed to Railway

## Deployment Steps

### 1. Install Vercel CLI (Optional)

```bash
npm i -g vercel
```

### 2. Deploy via Vercel CLI

```bash
cd frontend

# Login to Vercel
vercel login

# Deploy to production
vercel --prod
```

### 3. Deploy via GitHub Integration (Recommended)

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### 4. Configure Environment Variables

In Vercel dashboard, add these environment variables:

```
VITE_API_URL=https://your-backend.railway.app
VITE_DEFAULT_PLAYER_ID=1
VITE_ENVIRONMENT=production
```

**Important:**
- Replace `your-backend.railway.app` with your actual Railway backend URL
- Do NOT include trailing slashes in `VITE_API_URL`

### 5. Update Backend CORS

After frontend is deployed, update backend's `ALLOWED_ORIGINS`:

1. Go to Railway dashboard
2. Open your backend project
3. Update `ALLOWED_ORIGINS` environment variable:
   ```
   ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://www.your-custom-domain.com
   ```
4. Redeploy backend for changes to take effect

### 6. Verify Deployment

Test the deployed frontend:

1. Open your Vercel URL in browser
2. Check browser console for API connection
3. Test Bug Hunt game functionality
4. Verify no CORS errors in console

### 7. Custom Domain (Optional)

1. Go to Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed
5. Update backend's `ALLOWED_ORIGINS` with new domain

## Automatic Deployments

Vercel automatically deploys:
- **Production**: On push to `main` branch
- **Preview**: On pull requests

Configure branches in Vercel project settings.

## Monitoring

Vercel provides:
- **Analytics**: Page views, performance metrics
- **Logs**: Build and runtime logs
- **Insights**: Web Vitals and performance data

## Troubleshooting

### Build fails
```bash
# Test build locally
npm run build

# Check for TypeScript errors
npm run lint
```

### CORS errors
1. Verify backend `ALLOWED_ORIGINS` includes Vercel URL
2. Check `VITE_API_URL` is correct in Vercel env vars
3. Ensure no trailing slashes in URLs

### Environment variables not working
1. Ensure variables start with `VITE_`
2. Redeploy after adding/changing env vars
3. Clear cache: Vercel dashboard → Deployments → Redeploy

### API calls failing
1. Check backend is running: `curl https://your-backend.railway.app/health`
2. Verify `VITE_API_URL` in browser console
3. Check network tab in DevTools for actual request URLs

## Performance Optimization

Already configured in `vercel.json`:
- **Cache headers**: Static assets cached for 1 year
- **SPA routing**: All routes serve index.html
- **Build optimization**: Vite production build

Additional optimizations:
```bash
# Analyze bundle size
npm run build -- --report

# Add to package.json for bundle analysis
npm install --save-dev rollup-plugin-visualizer
```

## Rollback

```bash
# Using CLI
vercel rollback

# Or use dashboard:
# Deployments → Previous deployment → Promote to Production
```

## Cost

Vercel free tier includes:
- Unlimited deployments
- 100 GB bandwidth per month
- Automatic HTTPS
- Analytics

Should be sufficient for development and small-scale production.

## CI/CD Integration

Vercel automatically detects and deploys from Git.

Optional: Add preview deployment comments in PRs
1. Vercel dashboard → Project settings → Git
2. Enable "Comments on Pull Requests"

## Security

Already implemented:
- HTTPS by default
- Secure headers in `vercel.json`
- Environment variable encryption

Additional recommendations:
- Enable Vercel Authentication for staging deployments
- Use Vercel Firewall for DDoS protection (paid tier)
- Implement rate limiting in backend
