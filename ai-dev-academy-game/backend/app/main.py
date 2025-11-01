"""FastAPI main application for AI Dev Academy game."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routes import minigames, player, progress, achievements

# Load settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="Backend API for AI Dev Academy gamified learning platform",
    version=settings.API_VERSION
)

# Configure CORS - supports both development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("Starting AI Dev Academy API...")
    print("Initializing database...")
    init_db()
    print("Database initialized!")


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


# Include routers
app.include_router(minigames.router, prefix="/api/minigames", tags=["minigames"])
app.include_router(player.router, prefix="/api/player", tags=["player"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["achievements"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
