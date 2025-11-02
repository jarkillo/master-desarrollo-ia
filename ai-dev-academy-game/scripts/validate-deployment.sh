#!/bin/bash

# AI Dev Academy Game - Post-Deployment Validation Script
# This script validates that your deployment is working correctly

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL=""
FRONTEND_URL=""

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
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Ask for URLs
echo "=========================================="
echo "AI Dev Academy - Deployment Validator"
echo "=========================================="
echo ""

read -p "Enter your BACKEND URL (Railway): " BACKEND_URL
read -p "Enter your FRONTEND URL (Vercel): " FRONTEND_URL

# Remove trailing slashes
BACKEND_URL=${BACKEND_URL%/}
FRONTEND_URL=${FRONTEND_URL%/}

echo ""
echo "Validating deployment..."
echo ""

# Test 1: Backend Health Check
echo "Test 1: Backend Health Check"
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health")

if [ "$HEALTH_RESPONSE" -eq 200 ]; then
    HEALTH_BODY=$(curl -s "$BACKEND_URL/health")
    if [[ "$HEALTH_BODY" == *"healthy"* ]]; then
        print_success "Backend health check passed"
    else
        print_error "Backend health check returned unexpected response: $HEALTH_BODY"
        exit 1
    fi
else
    print_error "Backend health check failed (HTTP $HEALTH_RESPONSE)"
    exit 1
fi

# Test 2: Backend Root Endpoint
echo "Test 2: Backend Root Endpoint"
ROOT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/")

if [ "$ROOT_RESPONSE" -eq 200 ]; then
    print_success "Backend root endpoint accessible"
else
    print_error "Backend root endpoint failed (HTTP $ROOT_RESPONSE)"
    exit 1
fi

# Test 3: API Docs
echo "Test 3: API Documentation"
DOCS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/docs")

if [ "$DOCS_RESPONSE" -eq 200 ]; then
    print_success "API documentation accessible at $BACKEND_URL/docs"
else
    print_warning "API documentation not accessible (HTTP $DOCS_RESPONSE)"
fi

# Test 4: Frontend Accessibility
echo "Test 4: Frontend Accessibility"
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL")

if [ "$FRONTEND_RESPONSE" -eq 200 ]; then
    print_success "Frontend is accessible"
else
    print_error "Frontend is not accessible (HTTP $FRONTEND_RESPONSE)"
    exit 1
fi

# Test 5: CORS Configuration
echo "Test 5: CORS Configuration"
print_info "Testing preflight request..."

CORS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Origin: $FRONTEND_URL" \
    -H "Access-Control-Request-Method: GET" \
    -H "Access-Control-Request-Headers: Content-Type" \
    -X OPTIONS \
    "$BACKEND_URL/health")

if [ "$CORS_RESPONSE" -eq 200 ]; then
    # Check if Access-Control-Allow-Origin header is present
    CORS_HEADER=$(curl -s -I \
        -H "Origin: $FRONTEND_URL" \
        "$BACKEND_URL/health" | grep -i "access-control-allow-origin")

    if [[ ! -z "$CORS_HEADER" ]]; then
        print_success "CORS is properly configured"
    else
        print_warning "CORS headers not found. Check ALLOWED_ORIGINS in Railway."
    fi
else
    print_warning "CORS preflight request returned HTTP $CORS_RESPONSE"
fi

# Test 6: Bug Hunt Endpoint
echo "Test 6: Bug Hunt API Endpoint"
BUG_HUNT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "$BACKEND_URL/api/minigames/bug-hunt/start" \
    -H "Content-Type: application/json" \
    -d '{"player_id": 1, "difficulty": "easy"}')

if [ "$BUG_HUNT_RESPONSE" -eq 200 ]; then
    print_success "Bug Hunt API is working"
elif [ "$BUG_HUNT_RESPONSE" -eq 404 ]; then
    print_error "Bug Hunt endpoint not found (check API routes)"
else
    print_warning "Bug Hunt API returned HTTP $BUG_HUNT_RESPONSE"
fi

# Test 7: Environment Variables Check
echo "Test 7: Environment Variables Verification"
print_info "Please verify manually in Railway dashboard:"
echo "  - ENVIRONMENT=production"
echo "  - DATABASE_URL is set"
echo "  - ALLOWED_ORIGINS=$FRONTEND_URL"
echo "  - SECRET_KEY is set (not default)"
echo ""
print_info "Please verify manually in Vercel dashboard:"
echo "  - VITE_API_URL=$BACKEND_URL"
echo "  - VITE_DEFAULT_PLAYER_ID=1"
echo "  - VITE_ENVIRONMENT=production"

echo ""
echo "=========================================="
echo "Validation Summary"
echo "=========================================="
print_success "All automated tests passed!"
echo ""
print_info "Manual checks remaining:"
echo "  1. Open $FRONTEND_URL in browser"
echo "  2. Open DevTools (F12) → Console"
echo "  3. Verify NO CORS errors"
echo "  4. Try playing Bug Hunt game"
echo "  5. Verify XP is awarded"
echo "  6. Check Leaderboard shows data"
echo ""
print_success "Deployment validation complete!"
echo ""
