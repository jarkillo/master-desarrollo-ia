"""FastAPI main application for AI Dev Academy game."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, engine
from app.models import Player, Progress, Achievement, PlayerStats, UnlockedTool

# Import routes (will create next)
# from app.routes import player, progress, achievements, minigames

# Create FastAPI app
app = FastAPI(
    title="AI Dev Academy API",
    description="Backend API for AI Dev Academy gamified learning platform",
    version="1.0.0"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("🚀 Starting AI Dev Academy API...")
    print("📊 Initializing database...")
    init_db()
    print("✅ Database initialized!")


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "AI Dev Academy API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers (will uncomment after creating route files)
# app.include_router(player.router, prefix="/api/player", tags=["player"])
# app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
# app.include_router(achievements.router, prefix="/api/achievements", tags=["achievements"])
# app.include_router(minigames.router, prefix="/api/minigames", tags=["minigames"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
