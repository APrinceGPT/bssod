"""
BSSOD Analyzer Backend API

Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import get_settings
from .api.routes import router
from .middleware import RequestIdMiddleware
from .logging_config import setup_logging, Loggers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger = Loggers.app()
    settings = get_settings()
    
    logger.info("Starting BSSOD Analyzer API v1.0.0")
    logger.info(f"AI Model: {settings.ai.model}")
    logger.info(f"Max upload size: {settings.upload.max_size_mb} MB")
    logger.info(f"Debug mode: {settings.server.debug}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down BSSOD Analyzer API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    # Setup logging first
    setup_logging()
    
    app = FastAPI(
        title="BSSOD Analyzer API",
        description="AI-powered Windows memory dump analysis backend",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Add request ID middleware (must be before CORS)
    app.add_middleware(RequestIdMiddleware)
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
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
