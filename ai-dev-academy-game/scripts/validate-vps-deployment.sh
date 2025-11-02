#!/bin/bash

# AI Dev Academy Game - VPS Deployment Validation Script
# This script validates that your Docker Compose deployment is working correctly

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${BLUE}=========================================="
    echo -e "$1"
    echo -e "==========================================${NC}\n"
}

# Main validation
print_header "AI Dev Academy - VPS Deployment Validator"

# Test 1: Docker Compose Status
echo "Test 1: Docker Compose Status"
if docker-compose ps | grep -q "Up"; then
    print_success "Docker Compose containers are running"
    docker-compose ps
else
    print_error "Docker Compose containers are not running"
    print_info "Run: docker-compose up -d"
    exit 1
fi

echo ""

# Test 2: Backend Container Health
echo "Test 2: Backend Container Health"
BACKEND_HEALTH=$(docker inspect --format='{{.State.Health.Status}}' ai-dev-academy-backend 2>/dev/null || echo "unknown")

if [ "$BACKEND_HEALTH" = "healthy" ]; then
    print_success "Backend container is healthy"
elif [ "$BACKEND_HEALTH" = "unknown" ]; then
    print_warning "Backend health status unknown (healthcheck may not be configured)"
else
    print_error "Backend container is $BACKEND_HEALTH"
    print_info "Check logs: docker-compose logs backend"
    exit 1
fi

echo ""

# Test 3: Backend Health Endpoint
echo "Test 3: Backend Health Endpoint"
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health" 2>/dev/null || echo "000")

if [ "$HEALTH_RESPONSE" -eq 200 ]; then
    HEALTH_BODY=$(curl -s "http://localhost:8000/health")
    if [[ "$HEALTH_BODY" == *"healthy"* ]]; then
        print_success "Backend health endpoint responding correctly"
    else
        print_error "Backend health check returned unexpected response: $HEALTH_BODY"
    fi
else
    print_error "Backend health check failed (HTTP $HEALTH_RESPONSE)"
    print_info "Verify backend container is running and port 8000 is exposed"
fi

echo ""

# Test 4: Frontend Container Status
echo "Test 4: Frontend Container Status"
if docker ps | grep -q "ai-dev-academy-frontend"; then
    print_success "Frontend container is running"
else
    print_error "Frontend container is not running"
    print_info "Check logs: docker-compose logs frontend"
fi

echo ""

# Test 5: Frontend Health
echo "Test 5: Frontend Accessibility"
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost/" 2>/dev/null || echo "000")

if [ "$FRONTEND_RESPONSE" -eq 200 ]; then
    print_success "Frontend is accessible on port 80"
else
    print_error "Frontend is not accessible (HTTP $FRONTEND_RESPONSE)"
    print_info "Check nginx logs: docker-compose logs frontend"
fi

echo ""

# Test 6: Database Volume
echo "Test 6: Database Volume"
if docker volume ls | grep -q "backend-data"; then
    VOLUME_SIZE=$(docker volume inspect backend-data --format '{{.Mountpoint}}' 2>/dev/null)
    if [ -n "$VOLUME_SIZE" ]; then
        print_success "Database volume exists: backend-data"
        print_info "Volume location: $VOLUME_SIZE"
    fi
else
    print_warning "Database volume not found. Data may not persist."
fi

echo ""

# Test 7: Container Restart Policy
echo "Test 7: Container Restart Policy"
BACKEND_RESTART=$(docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' ai-dev-academy-backend 2>/dev/null || echo "none")
FRONTEND_RESTART=$(docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' ai-dev-academy-frontend 2>/dev/null || echo "none")

if [ "$BACKEND_RESTART" = "unless-stopped" ]; then
    print_success "Backend has correct restart policy: $BACKEND_RESTART"
else
    print_warning "Backend restart policy is: $BACKEND_RESTART (recommended: unless-stopped)"
fi

if [ "$FRONTEND_RESTART" = "unless-stopped" ]; then
    print_success "Frontend has correct restart policy: $FRONTEND_RESTART"
else
    print_warning "Frontend restart policy is: $FRONTEND_RESTART (recommended: unless-stopped)"
fi

echo ""

# Test 8: Environment Variables
echo "Test 8: Environment Variables Check"
if [ -f .env ]; then
    print_success ".env file exists"

    # Check required variables (without exposing values)
    if grep -q "^SECRET_KEY=" .env && ! grep -q "^SECRET_KEY=change-me" .env; then
        print_success "SECRET_KEY is set (and not default)"
    else
        print_warning "SECRET_KEY is not set or using default value"
        print_info "Generate secure key: openssl rand -hex 32"
    fi

    if grep -q "^FRONTEND_URL=" .env; then
        FRONTEND_URL=$(grep "^FRONTEND_URL=" .env | cut -d'=' -f2)
        print_success "FRONTEND_URL is set: $FRONTEND_URL"
    else
        print_warning "FRONTEND_URL is not set in .env"
    fi

    if grep -q "^BACKEND_URL=" .env; then
        BACKEND_URL=$(grep "^BACKEND_URL=" .env | cut -d'=' -f2)
        print_success "BACKEND_URL is set: $BACKEND_URL"
    else
        print_warning "BACKEND_URL is not set in .env"
    fi
else
    print_error ".env file not found"
    print_info "Copy .env.production.example to .env and configure"
fi

echo ""

# Test 9: Bug Hunt API
echo "Test 9: Bug Hunt API Endpoint"
BUG_HUNT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "http://localhost:8000/api/minigames/bug-hunt/start" \
    -H "Content-Type: application/json" \
    -d '{"player_id": 1, "difficulty": "easy"}' 2>/dev/null || echo "000")

if [ "$BUG_HUNT_RESPONSE" -eq 200 ]; then
    print_success "Bug Hunt API is working"
elif [ "$BUG_HUNT_RESPONSE" -eq 404 ]; then
    print_error "Bug Hunt endpoint not found (check API routes)"
else
    print_warning "Bug Hunt API returned HTTP $BUG_HUNT_RESPONSE"
fi

echo ""

# Test 10: Resource Usage
echo "Test 10: Resource Usage"
print_info "Container resource usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" ai-dev-academy-backend ai-dev-academy-frontend

echo ""

# Summary
print_header "Validation Summary"
print_success "All automated tests completed!"

echo ""
print_info "Manual checks remaining:"
echo "  1. Open http://$(hostname -I | awk '{print $1}') in browser"
echo "  2. Open DevTools (F12) → Console"
echo "  3. Verify NO CORS errors"
echo "  4. Try playing Bug Hunt game"
echo "  5. Verify XP is awarded"
echo "  6. Check Leaderboard shows data"

echo ""
print_info "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Restart: docker-compose restart"
echo "  - Stop: docker-compose down"
echo "  - Update: git pull && docker-compose up -d --build"

echo ""
print_success "Deployment validation complete!"
echo ""
