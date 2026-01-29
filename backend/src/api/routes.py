"""
API Routes

Defines the FastAPI endpoints for the BSSOD Analyzer backend.
"""

from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse

from ..config import get_settings
from ..models.schemas import AnalyzeResponse, HealthResponse
from ..models.error_codes import (
    ErrorResponseModel,
    no_filename_error,
    invalid_file_type_error,
    file_read_error,
    zip_validation_error,
    ai_service_error,
)
from ..services.zip_validator import create_validator, ZipValidationError
from ..services.ai_service import create_ai_service, AIServiceError
from ..logging_config import Loggers, log_error, log_ai_request, log_ai_response
from ..middleware import get_request_id


# Create the router
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and services are available"
)
async def health_check(check_ai: bool = False):
    """
    Health check endpoint.
    
    Args:
        check_ai: If True, perform a connectivity check to the AI service.
                  This adds latency but confirms AI service availability.
    """
    request_id = get_request_id()
    logger = Loggers.api()
    
    ai_available = True
    message = "All systems operational"
    
    # Optionally check AI service connectivity
    if check_ai:
        logger.info(f"[{request_id}] Health check with AI verification")
        ai_service = create_ai_service()
        ai_available = await ai_service.health_check()
        if not ai_available:
            message = "AI service is not reachable"
            logger.warning(f"[{request_id}] AI service health check failed")
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message=message,
        ai_service_available=ai_available,
        request_id=request_id
    )


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        400: {"model": ErrorResponseModel, "description": "Invalid input"},
        500: {"model": ErrorResponseModel, "description": "Server error"}
    },
    summary="Analyze Memory Dump",
    description="Upload a ZIP file from the parser tool and get AI-powered analysis"
)
async def analyze_dump(
    request: Request,
    file: UploadFile = File(
        ...,
        description="ZIP file exported from the BSOD Parser Tool containing analysis.json"
    )
):
    """
    Analyze a memory dump ZIP file.
    
    Accepts a ZIP file exported from the BSOD Parser Tool,
    validates the contents, and returns AI-powered analysis.
    """
    settings = get_settings()
    logger = Loggers.api()
    request_id = get_request_id()
    
    # Validate filename
    if not file.filename:
        error = no_filename_error()
        log_error(logger, request_id, error.code.value, error.message)
        return JSONResponse(
            status_code=error.status_code,
            content={**error.to_dict(), "request_id": request_id}
        )
    
    # Validate file type
    if not file.filename.lower().endswith(".zip"):
        error = invalid_file_type_error(file.filename)
        log_error(logger, request_id, error.code.value, error.message, error.details)
        return JSONResponse(
            status_code=error.status_code,
            content={**error.to_dict(), "request_id": request_id}
        )
    
    # Read the file content
    try:
        content = await file.read()
    except Exception as e:
        error = file_read_error(str(e))
        log_error(logger, request_id, error.code.value, error.message, error.details)
        return JSONResponse(
            status_code=error.status_code,
            content={**error.to_dict(), "request_id": request_id}
        )
    
    # Log file info
    file_size_mb = len(content) / (1024 * 1024)
    logger.info(f"[{request_id}] Processing: {file.filename} ({file_size_mb:.2f} MB)")
    
    # Validate and extract the ZIP
    validator = create_validator(max_size_mb=settings.upload.max_size_mb)
    
    try:
        analysis_data, raw_data = validator.validate_and_extract(content)
    except ZipValidationError as e:
        error = zip_validation_error(str(e))
        log_error(logger, request_id, error.code.value, error.message)
        return JSONResponse(
            status_code=error.status_code,
            content={**error.to_dict(), "request_id": request_id}
        )
    
    # Get bugcheck info for logging
    bugcheck_code = _get_bugcheck_code(analysis_data)
    
    # Call the AI service
    ai_service = create_ai_service()
    log_ai_request(logger, request_id, settings.ai.model, bugcheck_code)
    
    try:
        ai_result = await ai_service.analyze(analysis_data)
        log_ai_response(logger, request_id, ai_result.tokens_used)
    except AIServiceError as e:
        error = ai_service_error(str(e))
        log_error(logger, request_id, error.code.value, error.message, error.details)
        return JSONResponse(
            status_code=error.status_code,
            content={**error.to_dict(), "request_id": request_id}
        )
    
    # Build the response
    logger.info(f"[{request_id}] Analysis completed successfully")
    return AnalyzeResponse(
        success=True,
        message="Analysis completed successfully",
        dump_file=analysis_data.metadata.dump_filename or "Unknown",
        bugcheck_code=bugcheck_code,
        bugcheck_name=_get_bugcheck_name(analysis_data),
        ai_analysis=ai_result
    )


def _get_bugcheck_code(data) -> str:
    """Extract bugcheck code from analysis data."""
    if data.crash_summary:
        return data.crash_summary.bugcheck_code
    if data.bugcheck_analysis:
        return data.bugcheck_analysis.code
    return "Unknown"


def _get_bugcheck_name(data) -> str:
    """Extract bugcheck name from analysis data."""
    if data.crash_summary:
        return data.crash_summary.bugcheck_name
    if data.bugcheck_analysis:
        return data.bugcheck_analysis.name
    return "Unknown"
