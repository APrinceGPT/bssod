"""
BSSOD Analyzer Backend API

Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import get_settings
from .api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    settings = get_settings()
    print("Starting BSSOD Analyzer API v1.0.0")
    print(f"AI Model: {settings.ai.model}")
    print(f"Max upload size: {settings.upload.max_size_mb} MB")
    
    yield
    
    # Shutdown
    print("Shutting down BSSOD Analyzer API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="BSSOD Analyzer API",
        description="AI-powered Windows memory dump analysis backend",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(router, prefix="/api/v1", tags=["Analysis"])
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "name": "BSSOD Analyzer API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    return app


# Create the app instance
app = create_app()
