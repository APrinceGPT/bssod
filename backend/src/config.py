"""
Configuration Module

Loads environment variables and provides application configuration.
"""

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel


# Load .env file from backend directory or parent directory
env_path = Path(__file__).parent.parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(env_path)


class AIConfig(BaseModel):
    """AI API configuration."""
    base_url: str
    api_key: str
    model: str
    timeout: float = 120.0


class ServerConfig(BaseModel):
    """Server configuration."""
    host: str
    port: int
    debug: bool


class CORSConfig(BaseModel):
    """CORS configuration."""
    origins: List[str]


class UploadConfig(BaseModel):
    """File upload configuration."""
    max_size_mb: int
    max_size_bytes: int


class Settings:
    """Application settings loaded from environment."""
    
    def __init__(self):
        # AI Configuration
        self.ai = AIConfig(
            base_url=os.getenv("OPENAI_BASE_URL", ""),
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "claude-4-sonnet"),
            timeout=float(os.getenv("AI_TIMEOUT", "120.0")),
        )
        
        # Server Configuration
        self.server = ServerConfig(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            debug=os.getenv("DEBUG", "false").lower() == "true",
        )
        
        # CORS Configuration
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        self.cors = CORSConfig(
            origins=[origin.strip() for origin in cors_origins.split(",")],
        )
        
        # Upload Configuration
        max_size_mb = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
        self.upload = UploadConfig(
            max_size_mb=max_size_mb,
            max_size_bytes=max_size_mb * 1024 * 1024,
        )
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate that required configuration is present.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.ai.base_url:
            return False, "OPENAI_BASE_URL is not configured"
        if not self.ai.api_key:
            return False, "OPENAI_API_KEY is not configured"
        if not self.ai.model:
            return False, "OPENAI_MODEL is not configured"
        return True, ""


# Global settings instance
_settings: Settings = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
