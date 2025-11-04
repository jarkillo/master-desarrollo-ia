#!/bin/bash
#
# AI Dev Academy Game - VPS Deployment Script
# Este script garantiza que TODOS los cambios se aplican correctamente
#

set -e  # Exit on error

echo "🚀 AI Dev Academy - VPS Deployment"
echo "=================================="
echo ""

# Step 1: Pull latest code
echo "📥 Step 1/6: Pulling latest code from main..."
git fetch origin main
git reset --hard origin/main
echo "✅ Code updated to latest main branch"
echo ""

# Step 2: Stop containers
echo "🛑 Step 2/6: Stopping running containers..."
docker compose down
echo "✅ Containers stopped"
echo ""

# Step 3: Remove old images (force rebuild)
echo "🗑️  Step 3/6: Removing old images to force rebuild..."
docker compose rm -f
docker rmi ai-dev-academy-game-backend:latest 2>/dev/null || true
docker rmi ai-dev-academy-game-frontend:latest 2>/dev/null || true
echo "✅ Old images removed"
echo ""

# Step 4: Build new images (no cache)
echo "🔨 Step 4/6: Building new images (this may take 2-3 minutes)..."
docker compose build --no-cache
echo "✅ New images built"
echo ""

# Step 5: Start containers
echo "▶️  Step 5/6: Starting containers..."
docker compose up -d
echo "✅ Containers started"
echo ""

# Step 6: Wait for backend to be ready
echo "⏳ Step 6/6: Waiting for backend to initialize..."
sleep 10

# Check backend health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend health check failed, but it might still be starting..."
fi
echo ""

# Show logs to verify seed data
echo "📋 Backend startup logs (checking seed data):"
echo "--------------------------------------------"
docker compose logs backend | tail -20
echo ""

echo "✅ DEPLOYMENT COMPLETE"
echo "====================="
echo ""
echo "🌐 Game should be available at: http://your-vps-ip"
echo ""
echo "📊 To check status:"
echo "   docker compose ps"
echo ""
echo "📝 To view logs:"
echo "   docker compose logs -f backend"
echo "   docker compose logs -f frontend"
echo ""
echo "🔍 To verify player was created:"
echo "   curl http://localhost:8000/api/player/1"
echo ""
