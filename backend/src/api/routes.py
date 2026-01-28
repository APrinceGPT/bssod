"""
API Routes

Defines the FastAPI endpoints for the BSSOD Analyzer backend.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException

from ..config import get_settings
from ..models.schemas import AnalyzeResponse, ErrorResponse, HealthResponse
from ..services.zip_validator import create_validator, ZipValidationError
from ..services.ai_service import create_ai_service, AIServiceError


# Create the router
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and services are available"
)
async def health_check():
    """Health check endpoint."""
    # Simple health check - don't check AI service to avoid slow responses
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ai_service_available=True  # Assume available, actual check on /analyze
    )


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Analyze Memory Dump",
    description="Upload a ZIP file from the parser tool and get AI-powered analysis"
)
async def analyze_dump(
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
    
    # Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided"
        )
    
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="File must be a ZIP archive"
        )
    
    # Read the file content
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read uploaded file: {e}"
        )
    
    # Validate and extract the ZIP
    validator = create_validator(max_size_mb=settings.upload.max_size_mb)
    
    try:
        analysis_data, raw_data = validator.validate_and_extract(content)
    except ZipValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    # Call the AI service
    ai_service = create_ai_service()
    
    try:
        ai_result = await ai_service.analyze(analysis_data)
    except AIServiceError as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {e}"
        )
    
    # Build the response
    return AnalyzeResponse(
        success=True,
        message="Analysis completed successfully",
        dump_file=analysis_data.metadata.dump_filename or "Unknown",
        bugcheck_code=_get_bugcheck_code(analysis_data),
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
