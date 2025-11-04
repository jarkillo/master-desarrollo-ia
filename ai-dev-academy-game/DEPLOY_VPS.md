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
sudo apt-get install docker compose-plugin

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
docker compose ps

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
docker compose down
docker rmi $(docker images -q ai-dev-academy-game*)  # Remove all game images
docker compose build --no-cache
docker compose up -d
```

---

## Success Checklist

After deployment, verify:

- ✅ Containers are running: `docker compose ps`
- ✅ Backend health check passes: `curl http://localhost:8000/health`
- ✅ Player endpoint returns data: `curl http://localhost:8000/api/player/1`
- ✅ Modules endpoint returns array: `curl http://localhost:8000/api/progress/modules`
- ✅ Frontend loads in browser: `http://your-vps-ip:3000`
- ✅ Browser console has no 404/422 errors
- ✅ Favicon loads correctly (no 404)
- ✅ Game starts and shows Module 0

---

**Deployment Guide Version:** 1.0
**Last Updated:** 2025-11-04
**Status:** Ready for Deployment 🚀
