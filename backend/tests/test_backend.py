"""
Tests for the BSSOD Analyzer Backend

Run with: python -m pytest backend/tests/ -v
"""

import json
import zipfile
from io import BytesIO

import pytest

from src.services.zip_validator import ZipValidator, ZipValidationError, create_validator
from src.services.prompt_engineering import format_analysis_prompt, get_system_prompt
from src.models.schemas import AnalysisDataModel


# Sample valid analysis data (matching actual parser output structure)
SAMPLE_ANALYSIS_DATA = {
    "metadata": {
        "tool_name": "BSSOD Analyzer Parser Tool",
        "tool_version": "1.0.0",
        "analysis_timestamp": "2025-01-01T12:00:00",
        "analysis_duration_seconds": 1.5,
        "dump_file": {
            "path": "C:\\MEMORY.DMP",
            "name": "MEMORY.DMP",
            "size_bytes": 16895483904,
            "size_human": "15.74 GB"
        },
        "parser_notes": []
    },
    "success": True,
    "error": None,
    "system_info": {
        "os_version": "Windows 10.0",
        "architecture": "x64",
        "processor_count": 8,
        "dump_type": "Full Memory Dump",
        "dump_size_bytes": 16895483904,
        "dump_size_human": "15.74 GB",
        "is_64bit": True,
        "crash_time_raw": 0
    },
    "crash_summary": {
        "bugcheck_code": "0x0000001A",
        "bugcheck_code_int": 26,
        "bugcheck_name": "MEMORY_MANAGEMENT",
        "parameter1": "0x41790",
        "parameter2": "0x0",
        "parameter3": "0x0",
        "parameter4": "0x0",
        "file_path": "C:\\MEMORY.DMP",
        "file_name": "MEMORY.DMP"
    },
    "bugcheck_analysis": {
        "code": 26,
        "code_hex": "0x0000001A",
        "name": "MEMORY_MANAGEMENT",
        "category": "Memory Corruption",
        "description": "The memory manager has detected a problem.",
        "parameters": [
            {"parameter_number": 1, "raw_value": 268176, "hex_value": "0x41790", "description": "Memory management subtype code"}
        ],
        "recommendations": ["Run Windows Memory Diagnostic", "Check for driver updates"],
        "likely_causes": ["Faulty RAM", "Driver issues", "Corrupted system files"],
        "severity": "High"
    },
    "stack_trace": {
        "has_context": True,
        "has_exception": False,
        "stack_pointer": "0xFFFFF80012340000",
        "instruction_pointer": "0xFFFFF80012345678",
        "registers": None,
        "exception": None,
        "raw_frames": [
            {"address": "0xFFFFF80012345678", "data": "0x1234567890ABCDEF"}
        ],
        "raw_frame_count": 1,
        "note": "Stack trace captured from memory dump"
    },
    "drivers": {
        "total_count": 150,
        "microsoft_count": 140,
        "third_party_count": 10,
        "problematic_count": 1,
        "extraction_method": "header_scan",
        "note": "",
        "drivers": [],
        "problematic_drivers": [
            {"name": "problematic.sys", "is_problematic": True, "problematic_reason": "Third-party driver"}
        ]
    }
}


def create_test_zip(analysis_data: dict) -> bytes:
    """Create a test ZIP file with the given analysis data."""
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("analysis.json", json.dumps(analysis_data))
    return buffer.getvalue()


class TestZipValidator:
    """Tests for ZipValidator class."""
    
    def test_valid_zip(self):
        """Test validation of a valid ZIP file."""
        zip_content = create_test_zip(SAMPLE_ANALYSIS_DATA)
        validator = create_validator(max_size_mb=50)
        
        analysis_data, raw_data = validator.validate_and_extract(zip_content)
        
        assert analysis_data.success is True
        assert analysis_data.metadata.tool_name == "BSSOD Analyzer Parser Tool"
        assert analysis_data.crash_summary.bugcheck_code == "0x0000001A"
    
    def test_invalid_zip_format(self):
        """Test rejection of invalid ZIP format."""
        validator = create_validator(max_size_mb=50)
        
        with pytest.raises(ZipValidationError, match="Invalid ZIP file format"):
            validator.validate_and_extract(b"not a zip file")
    
    def test_missing_analysis_json(self):
        """Test rejection when analysis.json is missing."""
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("other.json", "{}")
        
        validator = create_validator(max_size_mb=50)
        
        with pytest.raises(ZipValidationError, match="Missing required file"):
            validator.validate_and_extract(buffer.getvalue())
    
    def test_file_too_large(self):
        """Test rejection of files exceeding size limit."""
        zip_content = create_test_zip(SAMPLE_ANALYSIS_DATA)
        validator = ZipValidator(max_size_bytes=100)  # Very small limit
        
        with pytest.raises(ZipValidationError, match="File too large"):
            validator.validate_and_extract(zip_content)
    
    def test_invalid_json(self):
        """Test rejection of invalid JSON in analysis.json."""
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("analysis.json", "not valid json")
        
        validator = create_validator(max_size_mb=50)
        
        with pytest.raises(ZipValidationError, match="Invalid JSON"):
            validator.validate_and_extract(buffer.getvalue())
    
    def test_missing_metadata(self):
        """Test rejection when metadata is missing."""
        invalid_data = {"success": True}
        zip_content = create_test_zip(invalid_data)
        validator = create_validator(max_size_mb=50)
        
        with pytest.raises(ZipValidationError, match="Missing required field"):
            validator.validate_and_extract(zip_content)


class TestPromptEngineering:
    """Tests for prompt engineering functions."""
    
    def test_format_analysis_prompt(self):
        """Test prompt formatting with sample data."""
        analysis_data = AnalysisDataModel(**SAMPLE_ANALYSIS_DATA)
        prompt = format_analysis_prompt(analysis_data)
        
        # Check that key sections are present
        assert "# Windows Memory Dump Analysis Request" in prompt
        assert "## System Information" in prompt
        assert "## Crash Summary" in prompt
        assert "MEMORY_MANAGEMENT" in prompt
        assert "0x0000001A" in prompt
    
    def test_system_prompt_not_empty(self):
        """Test that system prompt is defined."""
        system_prompt = get_system_prompt()
        
        assert len(system_prompt) > 100
        assert "Windows" in system_prompt
        assert "crash" in system_prompt.lower()


class TestSchemas:
    """Tests for Pydantic schemas."""
    
    def test_analysis_data_model_parsing(self):
        """Test that AnalysisDataModel parses correctly."""
        model = AnalysisDataModel(**SAMPLE_ANALYSIS_DATA)
        
        assert model.success is True
        assert model.metadata.tool_name == "BSSOD Analyzer Parser Tool"
        assert model.system_info.dump_type == "Full Memory Dump"
        assert model.crash_summary.bugcheck_code == "0x0000001A"
        assert model.bugcheck_analysis.name == "MEMORY_MANAGEMENT"
        assert len(model.drivers.problematic_drivers) == 1
    
    def test_minimal_analysis_data(self):
        """Test parsing with minimal required fields."""
        minimal_data = {
            "metadata": {
                "tool_name": "BSSOD Analyzer Parser"
            },
            "success": True
        }
        
        model = AnalysisDataModel(**minimal_data)
        assert model.success is True
        assert model.system_info is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
