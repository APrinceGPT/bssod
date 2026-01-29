"""
Error Codes Module

Defines standardized error codes for the BSSOD Analyzer API.
These codes help the frontend display context-specific error messages.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ErrorCode(str, Enum):
    """Standardized error codes for API responses."""
    
    # File validation errors (400)
    NO_FILENAME = "NO_FILENAME"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    FILE_READ_ERROR = "FILE_READ_ERROR"
    INVALID_ZIP = "INVALID_ZIP"
    MISSING_ANALYSIS_JSON = "MISSING_ANALYSIS_JSON"
    INVALID_JSON = "INVALID_JSON"
    INVALID_STRUCTURE = "INVALID_STRUCTURE"
    
    # AI service errors (500)
    AI_TIMEOUT = "AI_TIMEOUT"
    AI_UNAVAILABLE = "AI_UNAVAILABLE"
    AI_RESPONSE_ERROR = "AI_RESPONSE_ERROR"
    
    # Server errors (500)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    CONFIG_ERROR = "CONFIG_ERROR"


class APIError(Exception):
    """
    Custom API exception with structured error information.
    
    Attributes:
        code: ErrorCode enum value
        message: Human-readable error message
        status_code: HTTP status code
        details: Optional additional details
    """
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = 400,
        details: Optional[str] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON response."""
        result = {
            "success": False,
            "error_code": self.code.value,
            "error": self.message,
        }
        if self.details:
            result["details"] = self.details
        return result


class ErrorResponseModel(BaseModel):
    """Pydantic model for error responses."""
    success: bool = False
    error_code: str
    error: str
    details: Optional[str] = None
    request_id: Optional[str] = None


# Pre-defined error factories for common errors
def no_filename_error() -> APIError:
    """Create error for missing filename."""
    return APIError(
        code=ErrorCode.NO_FILENAME,
        message="No filename provided",
        status_code=400
    )


def invalid_file_type_error(filename: str) -> APIError:
    """Create error for invalid file type."""
    return APIError(
        code=ErrorCode.INVALID_FILE_TYPE,
        message="File must be a ZIP archive",
        status_code=400,
        details=f"Received: {filename}"
    )


def file_too_large_error(size_mb: float, max_mb: int) -> APIError:
    """Create error for file exceeding size limit."""
    return APIError(
        code=ErrorCode.FILE_TOO_LARGE,
        message=f"File too large: {size_mb:.2f} MB (max: {max_mb} MB)",
        status_code=400
    )


def file_read_error(error: str) -> APIError:
    """Create error for file read failure."""
    return APIError(
        code=ErrorCode.FILE_READ_ERROR,
        message="Failed to read uploaded file",
        status_code=400,
        details=str(error)
    )


def zip_validation_error(error: str) -> APIError:
    """Create error for ZIP validation failure."""
    # Determine the specific error code based on the message
    error_lower = error.lower()
    
    if "missing required file" in error_lower:
        code = ErrorCode.MISSING_ANALYSIS_JSON
    elif "invalid zip" in error_lower:
        code = ErrorCode.INVALID_ZIP
    elif "invalid json" in error_lower:
        code = ErrorCode.INVALID_JSON
    elif "missing" in error_lower or "structure" in error_lower:
        code = ErrorCode.INVALID_STRUCTURE
    else:
        code = ErrorCode.INVALID_ZIP
    
    return APIError(
        code=code,
        message=error,
        status_code=400
    )


def ai_service_error(error: str) -> APIError:
    """Create error for AI service failure."""
    error_lower = error.lower()
    
    if "timeout" in error_lower or "timed out" in error_lower:
        code = ErrorCode.AI_TIMEOUT
        message = "AI analysis timed out"
    elif "connect" in error_lower or "unavailable" in error_lower:
        code = ErrorCode.AI_UNAVAILABLE
        message = "AI service is unavailable"
    else:
        code = ErrorCode.AI_RESPONSE_ERROR
        message = "AI analysis failed"
    
    return APIError(
        code=code,
        message=message,
        status_code=500,
        details=str(error)
    )


def internal_error(error: str) -> APIError:
    """Create error for internal server errors."""
    return APIError(
        code=ErrorCode.INTERNAL_ERROR,
        message="An internal error occurred",
        status_code=500,
        details=str(error)
    )
