"""
Request ID Middleware

Generates unique request IDs for tracking and debugging.
"""

import time
import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..logging_config import Loggers, log_request, log_response


# Context variable to store request ID across async boundaries
request_id_var: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    """
    Get the current request ID from context.
    
    Returns:
        Current request ID or empty string if not set
    """
    return request_id_var.get()


def generate_request_id() -> str:
    """
    Generate a unique request ID.
    
    Format: 8-character hex string from UUID4
    
    Returns:
        Unique request ID
    """
    return uuid.uuid4().hex[:8]


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds request ID to each request.
    
    - Generates a unique ID for each request
    - Stores it in context for access across the request lifecycle
    - Adds X-Request-ID header to response
    - Logs request/response with timing
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with ID tracking and logging."""
        # Generate request ID
        request_id = generate_request_id()
        request_id_var.set(request_id)
        
        # Store in request state for access in route handlers
        request.state.request_id = request_id
        
        # Log request
        logger = Loggers.api()
        log_request(
            logger,
            request_id,
            request.method,
            request.url.path
        )
        
        # Track timing
        start_time = time.perf_counter()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        # Log response
        log_response(logger, request_id, response.status_code, duration_ms)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
