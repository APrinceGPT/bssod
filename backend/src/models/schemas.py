"""
Request/Response Models for the BSSOD Analyzer API.

These Pydantic models define the structure of data flowing through the API.
All models use Optional fields with defaults to handle varying parser output.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Analysis Data Models (from Parser Tool output)
# These models match the JSON structure from analyzer.py's to_dict() methods
# ============================================================================

class SystemInfoModel(BaseModel):
    """System information from the dump file."""
    model_config = ConfigDict(extra="allow")
    
    os_version: Optional[str] = None
    architecture: Optional[str] = None
    processor_count: Optional[int] = None
    dump_type: Optional[str] = None
    dump_size_bytes: Optional[int] = None
    dump_size_human: Optional[str] = None
    is_64bit: Optional[bool] = None
    crash_time_raw: Optional[int] = None


class CrashSummaryModel(BaseModel):
    """Crash summary from the dump file."""
    model_config = ConfigDict(extra="allow")
    
    bugcheck_code: Optional[str] = None
    bugcheck_code_int: Optional[int] = None
    bugcheck_name: Optional[str] = None
    parameter1: Optional[str] = None
    parameter2: Optional[str] = None
    parameter3: Optional[str] = None
    parameter4: Optional[str] = None
    file_path: Optional[str] = None
    file_name: Optional[str] = None


class ParameterModel(BaseModel):
    """Bugcheck parameter analysis."""
    model_config = ConfigDict(extra="allow")
    
    parameter_number: Optional[int] = None
    raw_value: Optional[int] = None
    hex_value: Optional[str] = None
    description: Optional[str] = None
    interpretation: Optional[str] = None


class BugcheckAnalysisModel(BaseModel):
    """Detailed bugcheck analysis."""
    model_config = ConfigDict(extra="allow")
    
    code: Optional[int] = None
    code_hex: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = []
    recommendations: Optional[List[str]] = []
    likely_causes: Optional[List[str]] = []
    severity: Optional[str] = None


class StackTraceModel(BaseModel):
    """Stack trace information."""
    model_config = ConfigDict(extra="allow")
    
    has_context: Optional[bool] = False
    has_exception: Optional[bool] = False
    stack_pointer: Optional[str] = None
    instruction_pointer: Optional[str] = None
    registers: Optional[Dict[str, Any]] = None
    exception: Optional[Dict[str, Any]] = None
    raw_frames: Optional[List[Dict[str, Any]]] = []
    raw_frame_count: Optional[int] = 0
    note: Optional[str] = ""


class DriverModel(BaseModel):
    """Individual driver information."""
    model_config = ConfigDict(extra="allow")
    
    name: Optional[str] = None
    base_address: Optional[str] = None
    size: Optional[int] = None
    size_human: Optional[str] = None
    path: Optional[str] = None
    timestamp: Optional[int] = None
    timestamp_human: Optional[str] = None
    version: Optional[str] = None
    is_microsoft: Optional[bool] = False
    is_problematic: Optional[bool] = False
    problematic_reason: Optional[str] = None


class DriversModel(BaseModel):
    """Driver list information."""
    model_config = ConfigDict(extra="allow")
    
    total_count: Optional[int] = 0
    microsoft_count: Optional[int] = 0
    third_party_count: Optional[int] = 0
    problematic_count: Optional[int] = 0
    extraction_method: Optional[str] = None
    note: Optional[str] = ""
    drivers: Optional[List[Dict[str, Any]]] = []
    problematic_drivers: Optional[List[Dict[str, Any]]] = []


class DumpFileModel(BaseModel):
    """Dump file information in metadata."""
    model_config = ConfigDict(extra="allow")
    
    path: Optional[str] = None
    name: Optional[str] = None
    size_bytes: Optional[int] = None
    size_human: Optional[str] = None


class MetadataModel(BaseModel):
    """Analysis metadata."""
    model_config = ConfigDict(extra="allow")
    
    tool_name: str
    tool_version: Optional[str] = None
    analysis_timestamp: Optional[str] = None
    analysis_duration_seconds: Optional[float] = None
    dump_file: Optional[Dict[str, Any]] = None
    dump_filename: Optional[str] = None  # Alternate field name
    parser_notes: Optional[List[str]] = []


class AnalysisDataModel(BaseModel):
    """Complete analysis data from the parser tool."""
    model_config = ConfigDict(extra="allow")
    
    metadata: MetadataModel
    success: bool
    error: Optional[str] = None
    system_info: Optional[SystemInfoModel] = None
    crash_summary: Optional[CrashSummaryModel] = None
    bugcheck_analysis: Optional[BugcheckAnalysisModel] = None
    stack_trace: Optional[StackTraceModel] = None
    drivers: Optional[DriversModel] = None


# ============================================================================
# API Response Models
# ============================================================================

# Import structured analysis models for the response
from .structured_analysis import StructuredAIAnalysisResult


class AnalyzeResponse(BaseModel):
    """Response from the /analyze endpoint with structured AI analysis."""
    success: bool
    message: str
    dump_file: Optional[str] = None
    bugcheck_code: Optional[str] = None
    bugcheck_name: Optional[str] = None
    ai_analysis: Optional[StructuredAIAnalysisResult] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    details: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    message: Optional[str] = None
    ai_service_available: bool
    request_id: Optional[str] = None
