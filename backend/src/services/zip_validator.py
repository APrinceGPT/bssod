"""
ZIP Validation Service

Validates and extracts analysis data from uploaded ZIP files.
"""

import json
import zipfile
from io import BytesIO
from typing import Tuple

from ..models.schemas import AnalysisDataModel


# Required files in the ZIP
REQUIRED_FILES = ["analysis.json"]

# Optional files that may be present
OPTIONAL_FILES = [
    "system_info.json",
    "crash_summary.json",
    "bugcheck_analysis.json",
    "stack_trace.json",
    "drivers.json",
    "summary.txt",
    "README.txt",
]


class ZipValidationError(Exception):
    """Raised when ZIP validation fails."""
    pass


class ZipValidator:
    """Validates and extracts data from uploaded ZIP files."""
    
    def __init__(self, max_size_bytes: int):
        """
        Initialize the ZIP validator.
        
        Args:
            max_size_bytes: Maximum allowed ZIP file size in bytes
        """
        self.max_size_bytes = max_size_bytes
    
    def validate_and_extract(self, file_content: bytes) -> Tuple[AnalysisDataModel, dict]:
        """
        Validate a ZIP file and extract the analysis data.
        
        Args:
            file_content: Raw bytes of the uploaded ZIP file
        
        Returns:
            Tuple of (AnalysisDataModel, raw_data_dict)
        
        Raises:
            ZipValidationError: If validation fails
        """
        # Check file size
        if len(file_content) > self.max_size_bytes:
            size_mb = len(file_content) / (1024 * 1024)
            max_mb = self.max_size_bytes / (1024 * 1024)
            raise ZipValidationError(
                f"File too large: {size_mb:.2f} MB (max: {max_mb:.2f} MB)"
            )
        
        # Check if it's a valid ZIP file
        if not self._is_valid_zip(file_content):
            raise ZipValidationError("Invalid ZIP file format")
        
        # Extract and validate contents
        try:
            return self._extract_analysis_data(file_content)
        except json.JSONDecodeError as e:
            raise ZipValidationError(f"Invalid JSON in analysis.json: {e}")
        except Exception as e:
            raise ZipValidationError(f"Failed to extract data: {e}")
    
    def _is_valid_zip(self, file_content: bytes) -> bool:
        """Check if the content is a valid ZIP file."""
        try:
            with zipfile.ZipFile(BytesIO(file_content), 'r') as zf:
                # Try to read the file list
                zf.namelist()
                return True
        except zipfile.BadZipFile:
            return False
        except Exception:
            return False
    
    def _extract_analysis_data(self, file_content: bytes) -> Tuple[AnalysisDataModel, dict]:
        """Extract and parse the analysis data from the ZIP."""
        with zipfile.ZipFile(BytesIO(file_content), 'r') as zf:
            file_list = zf.namelist()
            
            # Check for required files
            for required_file in REQUIRED_FILES:
                if required_file not in file_list:
                    raise ZipValidationError(
                        f"Missing required file: {required_file}"
                    )
            
            # Read and parse analysis.json
            analysis_json = zf.read("analysis.json").decode("utf-8")
            raw_data = json.loads(analysis_json)
            
            # Validate the structure
            self._validate_analysis_structure(raw_data)
            
            # Parse into Pydantic model
            analysis_data = AnalysisDataModel(**raw_data)
            
            return analysis_data, raw_data
    
    def _validate_analysis_structure(self, data: dict) -> None:
        """Validate the structure of the analysis data."""
        # Check for required top-level fields
        required_fields = ["metadata", "success"]
        for field in required_fields:
            if field not in data:
                raise ZipValidationError(f"Missing required field: {field}")
        
        # Check metadata structure
        metadata = data.get("metadata", {})
        if not metadata.get("tool_name"):
            raise ZipValidationError("Missing tool_name in metadata")
        
        # Check for crash data
        if not data.get("crash_summary") and not data.get("bugcheck_analysis"):
            raise ZipValidationError(
                "No crash data found. Both crash_summary and bugcheck_analysis are missing."
            )


def create_validator(max_size_mb: int = 50) -> ZipValidator:
    """
    Create a ZipValidator instance.
    
    Args:
        max_size_mb: Maximum file size in megabytes
    
    Returns:
        Configured ZipValidator instance
    """
    return ZipValidator(max_size_bytes=max_size_mb * 1024 * 1024)
