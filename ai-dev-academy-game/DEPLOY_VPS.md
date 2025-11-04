# AI Dev Academy Game - VPS Deployment Guide

Complete guide to deploy the AI Dev Academy Game to a VPS using Docker.

## Architecture Overview

```
┌──────────────────────────────────────────────┐
│              VPS (Linux Server)              │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │     Docker Compose Environment         │ │
│  │                                        │ │
│  │  ┌──────────────┐   ┌──────────────┐ │ │
│  │  │   Frontend   │   │   Backend    │ │ │
│  │  │   (Nginx)    │──▶│  (FastAPI)   │ │ │
│  │  │   Port 3000  │   │  Port 8000   │ │ │
│  │  └──────────────┘   └──────────────┘ │ │
│  │         │                   │         │ │
│  │         │                   ▼         │ │
│  │         │            ┌──────────────┐ │ │
│  │         │            │   SQLite DB  │ │ │
│  │         │            │   (Volume)   │ │ │
│  │         │            └──────────────┘ │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  Port 80 (HTTP) → Frontend                  │
└──────────────────────────────────────────────┘
```

---

## Prerequisites

- **Linux VPS** (Ubuntu 20.04+, Debian 11+, or similar)
- **Docker** installed (version 20.10+)
- **Docker Compose** installed (version 2.0+)
- **Git** installed
- **Root or sudo access**
- **Public IP** or domain name

### Installation Commands (if needed)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Verify installations
docker --version
docker compose version

# Add current user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

---

## Quick Deployment (Automated)

### Step 1: Clone Repository

```bash
cd /home/your-user
git clone https://github.com/your-username/master-ia-manu.git
cd master-ia-manu/ai-dev-academy-game
```

### Step 2: Run Deployment Script

```bash
chmod +x deploy-vps.sh
./deploy-vps.sh
```

**What the script does:**
1. ✅ Pulls latest code from `main` branch
2. ✅ Stops running containers
3. ✅ Removes old Docker images (forces rebuild)
4. ✅ Builds new images with `--no-cache`
5. ✅ Starts containers in detached mode
6. ✅ Verifies backend health
7. ✅ Shows logs to confirm seed data was created

**Expected output:**
```
🚀 AI Dev Academy - VPS Deployment
==================================

📥 Step 1/6: Pulling latest code from main...
✅ Code updated to latest main branch

🛑 Step 2/6: Stopping running containers...
✅ Containers stopped

🗑️  Step 3/6: Removing old images to force rebuild...
✅ Old images removed

🔨 Step 4/6: Building new images (this may take 2-3 minutes)...
✅ New images built

▶️  Step 5/6: Starting containers...
✅ Containers started

⏳ Step 6/6: Waiting for backend to initialize...
✅ Backend is healthy

📋 Backend startup logs (checking seed data):
--------------------------------------------
Starting AI Dev Academy API...
Initializing database...
Database initialized!
Checking for seed data...
✅ Default player created successfully!
Seed data check complete!

✅ DEPLOYMENT COMPLETE
```

### Step 3: Verify Deployment

```bash
# Check containers are running
docker-compose ps

# Should show:
#   backend   Up
#   frontend  Up

# Test backend API
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test player endpoint
curl http://localhost:8000/api/player/1
# Expected: {"id":1,"username":"Demo Player",...}

# Test modules endpoint
curl http://localhost:8000/api/progress/modules
# Expected: Array of modules with classes
```

### Step 4: Access the Game

Open browser and go to:
- **Local**: `http://your-vps-ip:3000`
- **With domain**: `http://your-domain.com`

**Check browser console** (F12):
- ✅ No 404 errors on `/api/*` endpoints
- ✅ No 422 errors
- ✅ All API calls return 200 OK
- ✅ Favicon loads correctly

---

## Manual Deployment (Step-by-Step)

If the automated script fails or you want more control:

### Step 1: Update Code

```bash
cd /path/to/master-ia-manu/ai-dev-academy-game
git fetch origin main
git reset --hard origin/main
```

### Step 2: Stop Containers

```bash
docker-compose down
```

### Step 3: Remove Old Images

```bash
docker-compose rm -f
docker rmi ai-dev-academy-game-backend:latest
docker rmi ai-dev-academy-game-frontend:latest
```

### Step 4: Build New Images

```bash
# Build without cache (ensures all changes are applied)
docker-compose build --no-cache
```

### Step 5: Start Containers

```bash
docker-compose up -d
```

### Step 6: Verify

```bash
# Wait a few seconds for startup
sleep 10

# Check logs
docker-compose logs backend | tail -30
docker-compose logs frontend | tail -30

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/player/1
```

---

## Troubleshooting

### Problem 1: Same errors persist (404, 422)

**Symptoms:**
```
api/player/1:1  Failed to load resource: the server responded with a status of 404
api/progress/modules:1  Failed to load resource: the server responded with a status of 422
```

**Root cause:** Docker containers are using cached images with old code.

**Solution:**
```bash
# Force complete rebuild
cd ai-dev-academy-game
docker-compose down
docker rmi $(docker images -q ai-dev-academy-game*)  # Remove all game images
docker-compose build --no-cache
docker-compose up -d
```

### Problem 2: Backend not creating player

**Symptoms:**
```
curl http://localhost:8000/api/player/1
# Returns: {"detail":"Player not found"}
```

**Root cause:** Seed data not running or database volume issue.

**Solution:**
```bash
# Check backend logs for seed data confirmation
docker-compose logs backend | grep "Default player"

# If you don't see "✅ Default player created successfully!", the seed didn't run

# Option A: Restart backend
docker-compose restart backend

# Option B: Reset database (DELETES ALL DATA)
docker-compose down
docker volume rm ai-dev-academy-game_backend-data
docker-compose up -d
```

### Problem 3: Route order issue (422 on /modules)

**Symptoms:**
```
curl http://localhost:8000/api/progress/modules
# Returns: 422 Unprocessable Entity
```

**Root cause:** Old version of `backend/app/routes/progress.py` where `/{player_id}` route comes before `/modules`.

**Verification:**
```bash
# Check if latest code is deployed
docker-compose exec backend cat app/routes/progress.py | grep -A 5 "router = APIRouter"

# Should show /modules routes BEFORE /{player_id}
```

**Solution:**
```bash
# Force rebuild (see Problem 1 solution)
```

### Problem 4: Frontend shows "Network Error"

**Symptoms:**
- Browser console shows: `Network Error` or `ERR_CONNECTION_REFUSED`
- Frontend can't reach backend

**Verification:**
```bash
# Check backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend | tail -50

# Test from VPS directly
curl http://localhost:8000/health
```

**Solution:**
```bash
# If backend is down, restart it
docker-compose restart backend

# Check for port conflicts
sudo netstat -tulpn | grep 8000

# If another process is using port 8000, stop it or change docker-compose.yml port
```

### Problem 5: CORS errors

**Symptoms:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Root cause:** Backend `ALLOWED_ORIGINS` doesn't include frontend URL.

**Solution:**
```bash
# Edit backend/.env or docker-compose.yml
# Ensure ALLOWED_ORIGINS includes:
ALLOWED_ORIGINS=http://localhost:3000,http://your-vps-ip:3000

# Restart backend
docker-compose restart backend
```

### Problem 6: Docker Compose not found

**Symptoms:**
```bash
./deploy-vps.sh
# Error: docker-compose: command not found
```

**Solution:**
```bash
# Try with 'docker compose' (v2 syntax)
docker compose version

# If that works, edit deploy-vps.sh and replace:
#   docker-compose  →  docker compose
```

---

## Configuration

### Environment Variables

**Backend** (configured in `docker-compose.yml`):
```yaml
ENVIRONMENT: development
DATABASE_URL: sqlite:///./ai_dev_academy.db
ALLOWED_ORIGINS: http://localhost:3000
SECRET_KEY: dev-secret-key-change-in-production
```

**Frontend** (configured in `docker-compose.yml`):
```yaml
VITE_API_URL: http://localhost:8000
VITE_DEFAULT_PLAYER_ID: "1"
VITE_ENVIRONMENT: development
```

### Ports

- **Frontend**: 3000 (Nginx serving React app)
- **Backend**: 8000 (FastAPI)

To change ports, edit `docker-compose.yml`:
```yaml
services:
  frontend:
    ports:
      - "80:80"  # Change 3000 to 80 for production

  backend:
    ports:
      - "8000:8000"
```

---

## Monitoring

### Check Container Status

```bash
# List running containers
docker-compose ps

# View resource usage
docker stats

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Backend Health Check

```bash
# Health endpoint
curl http://localhost:8000/health

# API documentation
# Open in browser: http://your-vps-ip:8000/docs
```

### Database Inspection

```bash
# Enter backend container
docker-compose exec backend bash

# Inside container, open SQLite
sqlite3 ai_dev_academy.db

# Run queries
SELECT * FROM players;
SELECT * FROM progress;
.exit
```

---

## Backup and Restore

### Backup Database

```bash
# Copy database from container to host
docker-compose exec backend cat ai_dev_academy.db > backup_$(date +%Y%m%d).db
```

### Restore Database

```bash
# Stop containers
docker-compose down

# Replace database file
# (Database is in Docker volume, need to mount and copy)
docker-compose up -d backend
docker-compose cp backup_20250425.db backend:/app/ai_dev_academy.db
docker-compose restart backend
```

---

## Production Hardening

Before exposing to the internet:

### 1. Use HTTPS (Recommended: Caddy or Nginx Reverse Proxy)

```bash
# Install Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Create Caddyfile
sudo nano /etc/caddy/Caddyfile
```

**Caddyfile example:**
```
your-domain.com {
    reverse_proxy localhost:3000
}

api.your-domain.com {
    reverse_proxy localhost:8000
}
```

```bash
# Restart Caddy
sudo systemctl restart caddy
```

### 2. Change Secret Key

```bash
# Generate random secret
openssl rand -hex 32

# Update docker-compose.yml or create .env file
SECRET_KEY=<your-generated-secret>
```

### 3. Migrate to PostgreSQL

For persistent, production-grade database:

```yaml
# Add to docker-compose.yml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_dev_academy
      POSTGRES_USER: gameuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data

  backend:
    environment:
      DATABASE_URL: postgresql://gameuser:${DB_PASSWORD}@db:5432/ai_dev_academy

volumes:
  postgres-data:
```

### 4. Rate Limiting

Add to backend (future enhancement):
```bash
pip install slowapi
```

### 5. Firewall

```bash
# Allow only HTTP, HTTPS, SSH
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## CI/CD Integration

### GitHub Actions Deployment

Create `.github/workflows/deploy-vps.yml`:

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /path/to/ai-dev-academy-game
            ./deploy-vps.sh
```

**Setup:**
1. Generate SSH key: `ssh-keygen -t ed25519 -f vps_deploy`
2. Add public key to VPS: `~/.ssh/authorized_keys`
3. Add secrets to GitHub repo settings:
   - `VPS_HOST`: Your VPS IP
   - `VPS_USER`: SSH username
   - `VPS_SSH_KEY`: Private key content

---

## Common Commands Reference

```bash
# Deployment
./deploy-vps.sh                    # Automated deployment

# Container management
docker-compose up -d               # Start containers
docker-compose down                # Stop containers
docker-compose restart backend     # Restart backend only
docker-compose ps                  # List containers
docker-compose logs -f backend     # Follow backend logs

# Rebuild
docker-compose build --no-cache    # Rebuild without cache
docker-compose up -d --force-recreate  # Force recreate containers

# Database
docker-compose exec backend bash   # Enter backend container
sqlite3 ai_dev_academy.db          # Open database (inside container)

# Cleanup
docker system prune -a             # Remove all unused images/containers
docker volume prune                # Remove unused volumes (⚠️ DELETES DATA)

# Health checks
curl http://localhost:8000/health           # Backend health
curl http://localhost:8000/api/player/1     # Test player endpoint
curl http://localhost:8000/api/progress/modules  # Test modules endpoint
```

---

## Success Checklist

After deployment, verify:

- ✅ Containers are running: `docker-compose ps`
- ✅ Backend health check passes: `curl http://localhost:8000/health`
- ✅ Player endpoint returns data: `curl http://localhost:8000/api/player/1`
- ✅ Modules endpoint returns array: `curl http://localhost:8000/api/progress/modules`
- ✅ Frontend loads in browser: `http://your-vps-ip:3000`
- ✅ Browser console has no 404/422 errors
- ✅ Favicon loads correctly (no 404)
- ✅ Game starts and shows Module 0

---

## Validation Results

All fixes have been applied:

✅ **Seed Data** (`backend/app/seed_data.py`)
- Auto-creates demo player on startup
- Idempotent (checks if player exists)
- Integrated in `main.py` startup event

✅ **Route Ordering** (`backend/app/routes/progress.py`)
- `/modules` route comes BEFORE `/{player_id}`
- Prevents 422 error on `/api/progress/modules`

✅ **Favicon** (`frontend/public/favicon.svg`)
- AI-themed neural network icon created
- Linked in `frontend/index.html`

✅ **Curriculum Metadata** (`backend/app/services/content_service.py`)
- Added `difficulty`, `estimated_time_minutes`, `learning_objectives`
- Frontend guards added to prevent TypeErrors

✅ **Security Fix** (`requirements.txt`)
- Updated `python-jose` to 3.5.0 (CVE-2022-29217)

---

## Next Steps

1. **Run deployment script** on VPS: `./deploy-vps.sh`
2. **Verify all endpoints** return 200 OK
3. **Test game flow** in browser (Module 0 → exercises)
4. **Monitor logs** for any errors: `docker-compose logs -f`
5. **(Optional) Setup HTTPS** with Caddy or Nginx
6. **(Optional) Migrate to PostgreSQL** for production

---

**Deployment Guide Version:** 1.0
**Last Updated:** 2025-11-04
**Status:** Ready for Deployment 🚀
