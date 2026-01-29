"""
Logging Module

Configures structured logging for the BSSOD Analyzer API.
Replaces print statements with proper logging infrastructure.
"""

import logging
import sys
from typing import Optional

from .config import get_settings


# Log format with timestamp, level, and message
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Configure and return the root logger for the application.
    
    Args:
        level: Optional log level override (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured root logger
    """
    settings = get_settings()
    
    # Determine log level
    if level:
        log_level = getattr(logging, level.upper(), logging.INFO)
    elif settings.server.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Get the root logger
    root_logger = logging.getLogger("bssod")
    root_logger.setLevel(log_level)
    
    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Module name (typically __name__)
    
    Returns:
        Logger instance for the module
    """
    return logging.getLogger(f"bssod.{name}")


# Pre-configured loggers for common modules
class Loggers:
    """Container for pre-configured loggers."""
    
    @staticmethod
    def api() -> logging.Logger:
        """Logger for API routes."""
        return get_logger("api")
    
    @staticmethod
    def ai_service() -> logging.Logger:
        """Logger for AI service."""
        return get_logger("ai_service")
    
    @staticmethod
    def validator() -> logging.Logger:
        """Logger for ZIP validator."""
        return get_logger("validator")
    
    @staticmethod
    def app() -> logging.Logger:
        """Logger for main application."""
        return get_logger("app")


def log_request(
    logger: logging.Logger,
    request_id: str,
    method: str,
    path: str,
    extra: Optional[dict] = None
) -> None:
    """
    Log an incoming request.
    
    Args:
        logger: Logger to use
        request_id: Unique request ID
        method: HTTP method
        path: Request path
        extra: Optional extra data to log
    """
    msg = f"[{request_id}] {method} {path}"
    if extra:
        extra_str = " | ".join(f"{k}={v}" for k, v in extra.items())
        msg = f"{msg} | {extra_str}"
    logger.info(msg)


def log_response(
    logger: logging.Logger,
    request_id: str,
    status_code: int,
    duration_ms: float
) -> None:
    """
    Log a response.
    
    Args:
        logger: Logger to use
        request_id: Unique request ID
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
    """
    logger.info(f"[{request_id}] Response: {status_code} | {duration_ms:.2f}ms")


def log_error(
    logger: logging.Logger,
    request_id: str,
    error_code: str,
    message: str,
    details: Optional[str] = None
) -> None:
    """
    Log an error.
    
    Args:
        logger: Logger to use
        request_id: Unique request ID
        error_code: Error code from ErrorCode enum
        message: Error message
        details: Optional error details
    """
    msg = f"[{request_id}] Error: {error_code} - {message}"
    if details:
        msg = f"{msg} | Details: {details}"
    logger.error(msg)


def log_ai_request(
    logger: logging.Logger,
    request_id: str,
    model: str,
    bugcheck_code: Optional[str] = None
) -> None:
    """
    Log an AI service request (without sensitive content).
    
    Args:
        logger: Logger to use
        request_id: Unique request ID
        model: AI model name
        bugcheck_code: Optional bugcheck code being analyzed
    """
    msg = f"[{request_id}] AI Request: model={model}"
    if bugcheck_code:
        msg = f"{msg} | bugcheck={bugcheck_code}"
    logger.info(msg)


def log_ai_response(
    logger: logging.Logger,
    request_id: str,
    tokens_used: Optional[int] = None,
    duration_ms: Optional[float] = None
) -> None:
    """
    Log an AI service response (without content for privacy).
    
    Args:
        logger: Logger to use
        request_id: Unique request ID
        tokens_used: Optional token count
        duration_ms: Optional duration
    """
    parts = [f"[{request_id}] AI Response"]
    if tokens_used:
        parts.append(f"tokens={tokens_used}")
    if duration_ms:
        parts.append(f"duration={duration_ms:.2f}ms")
    logger.info(" | ".join(parts))
