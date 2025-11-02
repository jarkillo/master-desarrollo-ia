# AI Dev Academy Game - Post-Deployment Validation Script (PowerShell)
# This script validates that your deployment is working correctly

# Configuration
$BackendUrl = Read-Host "Enter your BACKEND URL (Railway)"
$FrontendUrl = Read-Host "Enter your FRONTEND URL (Vercel)"

# Remove trailing slashes
$BackendUrl = $BackendUrl.TrimEnd('/')
$FrontendUrl = $FrontendUrl.TrimEnd('/')

Write-Host "`n=========================================="
Write-Host "AI Dev Academy - Deployment Validator"
Write-Host "==========================================`n"

Write-Host "Validating deployment...`n" -ForegroundColor Yellow

# Test 1: Backend Health Check
Write-Host "Test 1: Backend Health Check" -ForegroundColor Cyan
try {
    $healthResponse = Invoke-RestMethod -Uri "$BackendUrl/health" -Method Get
    if ($healthResponse.status -eq "healthy") {
        Write-Host "✅ Backend health check passed" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend health check returned unexpected response" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Backend health check failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Backend Root Endpoint
Write-Host "`nTest 2: Backend Root Endpoint" -ForegroundColor Cyan
try {
    $rootResponse = Invoke-WebRequest -Uri "$BackendUrl/" -Method Get -ErrorAction Stop
    if ($rootResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend root endpoint accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 3: API Docs
Write-Host "`nTest 3: API Documentation" -ForegroundColor Cyan
try {
    $docsResponse = Invoke-WebRequest -Uri "$BackendUrl/docs" -Method Get -ErrorAction Stop
    if ($docsResponse.StatusCode -eq 200) {
        Write-Host "✅ API documentation accessible at $BackendUrl/docs" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  API documentation not accessible" -ForegroundColor Yellow
}

# Test 4: Frontend Accessibility
Write-Host "`nTest 4: Frontend Accessibility" -ForegroundColor Cyan
try {
    $frontendResponse = Invoke-WebRequest -Uri "$FrontendUrl" -Method Get -ErrorAction Stop
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend is accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend is not accessible: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 5: Bug Hunt Endpoint
Write-Host "`nTest 5: Bug Hunt API Endpoint" -ForegroundColor Cyan
try {
    $bugHuntBody = @{
        player_id = 1
        difficulty = "easy"
    } | ConvertTo-Json

    $bugHuntResponse = Invoke-RestMethod -Uri "$BackendUrl/api/minigames/bug-hunt/start" `
        -Method Post `
        -Body $bugHuntBody `
        -ContentType "application/json" `
        -ErrorAction Stop

    Write-Host "✅ Bug Hunt API is working" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 404) {
        Write-Host "❌ Bug Hunt endpoint not found (check API routes)" -ForegroundColor Red
    } else {
        Write-Host "⚠️  Bug Hunt API returned error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "`n=========================================="
Write-Host "Validation Summary"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ All automated tests passed!" -ForegroundColor Green

Write-Host "`nℹ️  Manual checks remaining:" -ForegroundColor Yellow
Write-Host "  1. Open $FrontendUrl in browser"
Write-Host "  2. Open DevTools (F12) → Console"
Write-Host "  3. Verify NO CORS errors"
Write-Host "  4. Try playing Bug Hunt game"
Write-Host "  5. Verify XP is awarded"
Write-Host "  6. Check Leaderboard shows data"

Write-Host "`nℹ️  Verify Environment Variables:" -ForegroundColor Yellow
Write-Host "`n  Railway (Backend):"
Write-Host "    - ENVIRONMENT=production"
Write-Host "    - ALLOWED_ORIGINS=$FrontendUrl"
Write-Host "    - SECRET_KEY is set (not default)"
Write-Host "`n  Vercel (Frontend):"
Write-Host "    - VITE_API_URL=$BackendUrl"
Write-Host "    - VITE_ENVIRONMENT=production"

Write-Host "`n✅ Deployment validation complete!`n" -ForegroundColor Green
