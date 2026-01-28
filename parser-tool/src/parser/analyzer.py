"""
Dump Analyzer Orchestrator

This module orchestrates all parsing modules and produces a complete
analysis report that can be exported as JSON and packaged into a ZIP file.
"""

import os
import json
import zipfile
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# Handle both relative and absolute imports
try:
    from .header import HeaderParser, parse_dump_header, SystemInfo, CrashSummary
    from .bugcheck import BugcheckAnalyzer, analyze_bugcheck, BugcheckAnalysis
    from .stack_trace import StackTraceParser, parse_stack_trace, StackTrace
    from .drivers import DriverListExtractor, extract_drivers, DriverListResult
except ImportError:
    from parser.header import HeaderParser, parse_dump_header, SystemInfo, CrashSummary
    from parser.bugcheck import BugcheckAnalyzer, analyze_bugcheck, BugcheckAnalysis
    from parser.stack_trace import StackTraceParser, parse_stack_trace, StackTrace
    from parser.drivers import DriverListExtractor, extract_drivers, DriverListResult


@dataclass
class AnalysisMetadata:
    """Metadata about the analysis itself."""
    tool_name: str = "BSSOD Analyzer Parser Tool"
    tool_version: str = "1.0.0"
    analysis_timestamp: str = ""
    analysis_duration_seconds: float = 0.0
    dump_file_path: str = ""
    dump_file_name: str = ""
    dump_file_size_bytes: int = 0
    parser_notes: list = None
    
    def __post_init__(self):
        if not self.analysis_timestamp:
            self.analysis_timestamp = datetime.now().isoformat()
        if self.parser_notes is None:
            self.parser_notes = []
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "tool_name": self.tool_name,
            "tool_version": self.tool_version,
            "analysis_timestamp": self.analysis_timestamp,
            "analysis_duration_seconds": self.analysis_duration_seconds,
            "dump_file": {
                "path": self.dump_file_path,
                "name": self.dump_file_name,
                "size_bytes": self.dump_file_size_bytes,
                "size_human": self._format_size(self.dump_file_size_bytes),
            },
            "parser_notes": self.parser_notes,
        }
    
    def _format_size(self, size: int) -> str:
        """Format size in human-readable format."""
        if size >= 1024 ** 3:
            return f"{size / (1024 ** 3):.2f} GB"
        elif size >= 1024 ** 2:
            return f"{size / (1024 ** 2):.2f} MB"
        elif size >= 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size} bytes"


@dataclass
class CompleteAnalysis:
    """Complete analysis result combining all parser outputs."""
    metadata: AnalysisMetadata
    system_info: Optional[SystemInfo]
    crash_summary: Optional[CrashSummary]
    bugcheck_analysis: Optional[BugcheckAnalysis]
    stack_trace: Optional[StackTrace]
    drivers: Optional[DriverListResult]
    success: bool = True
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "metadata": self.metadata.to_dict(),
            "success": self.success,
            "error": self.error,
            "system_info": self.system_info.to_dict() if self.system_info else None,
            "crash_summary": self.crash_summary.to_dict() if self.crash_summary else None,
            "bugcheck_analysis": self.bugcheck_analysis.to_dict() if self.bugcheck_analysis else None,
            "stack_trace": self.stack_trace.to_dict() if self.stack_trace else None,
            "drivers": self.drivers.to_dict() if self.drivers else None,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


class DumpAnalyzer:
    """
    Main orchestrator for dump file analysis.
    
    This class coordinates all parsing modules to produce a complete
    analysis of a Windows memory dump file.
    """
    
    def __init__(self, dump_path: str):
        """
        Initialize the dump analyzer.
        
        Args:
            dump_path: Path to the dump file to analyze
        """
        self.dump_path = dump_path
        self._start_time = None
    
    def analyze(self) -> CompleteAnalysis:
        """
        Perform complete analysis of the dump file.
        
        Returns:
            CompleteAnalysis with all parsed information
        """
        import time
        self._start_time = time.time()
        
        # Initialize metadata
        metadata = AnalysisMetadata(
            dump_file_path=self.dump_path,
            dump_file_name=os.path.basename(self.dump_path),
        )
        
        # Check if file exists
        if not os.path.exists(self.dump_path):
            return CompleteAnalysis(
                metadata=metadata,
                system_info=None,
                crash_summary=None,
                bugcheck_analysis=None,
                stack_trace=None,
                drivers=None,
                success=False,
                error=f"Dump file not found: {self.dump_path}"
            )
        
        # Get file size
        try:
            metadata.dump_file_size_bytes = os.path.getsize(self.dump_path)
        except Exception as e:
            metadata.parser_notes.append(f"Could not get file size: {e}")
        
        # Parse each component
        system_info = None
        crash_summary = None
        bugcheck_analysis = None
        stack_trace = None
        drivers = None
        
        # 1. Parse header (system info + crash summary)
        try:
            system_info, crash_summary = parse_dump_header(self.dump_path)
            if not system_info:
                metadata.parser_notes.append("Failed to parse system info from header")
        except Exception as e:
            metadata.parser_notes.append(f"Header parsing error: {e}")
        
        # 2. Analyze bugcheck
        if crash_summary:
            try:
                bugcheck_analysis = analyze_bugcheck(
                    crash_summary.bugcheck_code_int,
                    int(crash_summary.parameter1, 16),
                    int(crash_summary.parameter2, 16),
                    int(crash_summary.parameter3, 16),
                    int(crash_summary.parameter4, 16),
                )
            except Exception as e:
                metadata.parser_notes.append(f"Bugcheck analysis error: {e}")
        
        # 3. Parse stack trace
        try:
            stack_trace = parse_stack_trace(self.dump_path)
            if not stack_trace.has_context and not stack_trace.has_exception:
                metadata.parser_notes.append("Limited stack trace info available (Live Dump)")
        except Exception as e:
            metadata.parser_notes.append(f"Stack trace parsing error: {e}")
        
        # 4. Extract drivers
        try:
            drivers = extract_drivers(self.dump_path)
            if drivers.total_count == 0:
                metadata.parser_notes.append(
                    "Driver list requires virtual address translation. "
                    "Use WinDbg for complete driver list."
                )
        except Exception as e:
            metadata.parser_notes.append(f"Driver extraction error: {e}")
        
        # Calculate duration
        metadata.analysis_duration_seconds = time.time() - self._start_time
        
        return CompleteAnalysis(
            metadata=metadata,
            system_info=system_info,
            crash_summary=crash_summary,
            bugcheck_analysis=bugcheck_analysis,
            stack_trace=stack_trace,
            drivers=drivers,
            success=True,
        )


def create_analysis_zip(analysis: CompleteAnalysis, output_dir: str = None) -> str:
    """
    Create a ZIP file containing the analysis results.
    
    Args:
        analysis: CompleteAnalysis result from DumpAnalyzer
        output_dir: Directory to save the ZIP file (default: same as dump file)
    
    Returns:
        Path to the created ZIP file
    """
    if output_dir is None:
        output_dir = os.path.dirname(analysis.metadata.dump_file_path)
    
    # Create filename based on dump file name and timestamp
    dump_name = os.path.splitext(analysis.metadata.dump_file_name)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"BSOD_Analysis_{dump_name}_{timestamp}.zip"
    zip_path = os.path.join(output_dir, zip_name)
    
    # Create the ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Main analysis JSON
        analysis_json = analysis.to_json(indent=2)
        zf.writestr("analysis.json", analysis_json)
        
        # Create separate JSON files for each component
        if analysis.system_info:
            zf.writestr(
                "system_info.json",
                json.dumps(analysis.system_info.to_dict(), indent=2)
            )
        
        if analysis.crash_summary:
            zf.writestr(
                "crash_summary.json",
                json.dumps(analysis.crash_summary.to_dict(), indent=2)
            )
        
        if analysis.bugcheck_analysis:
            zf.writestr(
                "bugcheck_analysis.json",
                json.dumps(analysis.bugcheck_analysis.to_dict(), indent=2)
            )
        
        if analysis.stack_trace:
            zf.writestr(
                "stack_trace.json",
                json.dumps(analysis.stack_trace.to_dict(), indent=2)
            )
        
        if analysis.drivers:
            zf.writestr(
                "drivers.json",
                json.dumps(analysis.drivers.to_dict(), indent=2)
            )
        
        # Create a human-readable summary
        summary_text = generate_text_summary(analysis)
        zf.writestr("summary.txt", summary_text)
        
        # Create README
        readme = generate_readme()
        zf.writestr("README.txt", readme)
    
    return zip_path


def generate_text_summary(analysis: CompleteAnalysis) -> str:
    """Generate a human-readable text summary of the analysis."""
    lines = []
    lines.append("=" * 70)
    lines.append("BSOD ANALYSIS SUMMARY")
    lines.append("=" * 70)
    lines.append("")
    
    # Metadata
    lines.append(f"Generated: {analysis.metadata.analysis_timestamp}")
    lines.append(f"Dump File: {analysis.metadata.dump_file_name}")
    lines.append(f"File Size: {analysis.metadata._format_size(analysis.metadata.dump_file_size_bytes)}")
    lines.append(f"Analysis Duration: {analysis.metadata.analysis_duration_seconds:.2f} seconds")
    lines.append("")
    
    # System Info
    if analysis.system_info:
        lines.append("-" * 70)
        lines.append("SYSTEM INFORMATION")
        lines.append("-" * 70)
        lines.append(f"OS Version: {analysis.system_info.os_version}")
        lines.append(f"Architecture: {analysis.system_info.architecture}")
        lines.append(f"Processors: {analysis.system_info.processor_count}")
        lines.append(f"Dump Type: {analysis.system_info.dump_type}")
        lines.append("")
    
    # Crash Summary
    if analysis.crash_summary:
        lines.append("-" * 70)
        lines.append("CRASH INFORMATION")
        lines.append("-" * 70)
        lines.append(f"Bugcheck Code: {analysis.crash_summary.bugcheck_code}")
        lines.append(f"Bugcheck Name: {analysis.crash_summary.bugcheck_name}")
        lines.append(f"Parameter 1: {analysis.crash_summary.parameter1}")
        lines.append(f"Parameter 2: {analysis.crash_summary.parameter2}")
        lines.append(f"Parameter 3: {analysis.crash_summary.parameter3}")
        lines.append(f"Parameter 4: {analysis.crash_summary.parameter4}")
        lines.append("")
    
    # Bugcheck Analysis
    if analysis.bugcheck_analysis:
        lines.append("-" * 70)
        lines.append("BUGCHECK ANALYSIS")
        lines.append("-" * 70)
        lines.append(f"Category: {analysis.bugcheck_analysis.category}")
        lines.append(f"Severity: {analysis.bugcheck_analysis.severity}")
        lines.append(f"Description: {analysis.bugcheck_analysis.description}")
        lines.append("")
        
        lines.append("Parameter Analysis:")
        for p in analysis.bugcheck_analysis.parameters:
            lines.append(f"  Param {p.parameter_number}: {p.hex_value}")
            lines.append(f"    {p.description}")
            if p.interpretation:
                lines.append(f"    -> {p.interpretation}")
        lines.append("")
        
        lines.append("Likely Causes:")
        for cause in analysis.bugcheck_analysis.likely_causes:
            lines.append(f"  • {cause}")
        lines.append("")
        
        lines.append("Recommendations:")
        for rec in analysis.bugcheck_analysis.recommendations:
            lines.append(f"  → {rec}")
        lines.append("")
    
    # Notes
    if analysis.metadata.parser_notes:
        lines.append("-" * 70)
        lines.append("PARSER NOTES")
        lines.append("-" * 70)
        for note in analysis.metadata.parser_notes:
            lines.append(f"• {note}")
        lines.append("")
    
    lines.append("=" * 70)
    lines.append("END OF SUMMARY")
    lines.append("=" * 70)
    
    return "\n".join(lines)


def generate_readme() -> str:
    """Generate README content for the ZIP file."""
    return """BSSOD Analyzer - EXTRACTED DATA
==============================

This ZIP file contains extracted diagnostic data from a Windows memory dump file.
The data was extracted using the BSSOD Analyzer Parser Tool.

FILES INCLUDED:
---------------
- analysis.json      : Complete analysis in JSON format (for upload to BSSOD Analyzer website)
- summary.txt        : Human-readable summary of the crash
- system_info.json   : System information (OS version, architecture, etc.)
- crash_summary.json : Basic crash information (bugcheck code and parameters)
- bugcheck_analysis.json : Detailed bugcheck interpretation
- stack_trace.json   : CPU register state and exception info (if available)
- drivers.json       : List of loaded drivers (if extractable)

HOW TO USE:
-----------
1. Upload the 'analysis.json' file to the BSSOD Analyzer website for AI-powered analysis
2. The AI will provide detailed explanations and troubleshooting recommendations
3. Review the 'summary.txt' file for a quick human-readable overview

PRIVACY NOTE:
-------------
This extracted data contains ONLY diagnostic information.
- NO personal files or data are included
- NO passwords or credentials are included
- NO browsing history or personal content is included
- Only technical crash information is extracted

The original dump file is NOT included in this ZIP.

For questions or support, visit the BSSOD Analyzer website.
"""


def analyze_dump(dump_path: str, create_zip: bool = True, 
                 output_dir: str = None) -> Tuple[CompleteAnalysis, Optional[str]]:
    """
    Convenience function to analyze a dump file and optionally create ZIP.
    
    Args:
        dump_path: Path to the dump file
        create_zip: Whether to create a ZIP file with results
        output_dir: Directory for ZIP output (default: same as dump file)
    
    Returns:
        Tuple of (CompleteAnalysis, zip_path or None)
    """
    analyzer = DumpAnalyzer(dump_path)
    analysis = analyzer.analyze()
    
    zip_path = None
    if create_zip and analysis.success:
        zip_path = create_analysis_zip(analysis, output_dir)
    
    return analysis, zip_path
