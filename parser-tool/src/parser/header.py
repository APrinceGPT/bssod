"""
Header Parser Module

This module provides high-level functions for parsing and extracting
header information from Windows memory dump files.
"""

import os
import sys
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict

# Handle both relative and absolute imports
try:
    from .dump_reader import DumpFileReader, DumpHeader
    from ..utils.constants import get_bugcheck_name, format_bugcheck_code
except ImportError:
    from parser.dump_reader import DumpFileReader, DumpHeader
    from utils.constants import get_bugcheck_name, format_bugcheck_code


@dataclass
class SystemInfo:
    """System information extracted from dump header."""
    os_version: str
    architecture: str
    processor_count: int
    dump_type: str
    dump_size_bytes: int
    dump_size_human: str
    is_64bit: bool
    crash_time_raw: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass  
class CrashSummary:
    """Summary of crash information from dump file."""
    bugcheck_code: str
    bugcheck_code_int: int
    bugcheck_name: str
    parameter1: str
    parameter2: str
    parameter3: str
    parameter4: str
    file_path: str
    file_name: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class HeaderParser:
    """
    High-level parser for extracting header information from dump files.
    
    This class wraps DumpFileReader and provides convenient methods
    for extracting system info and crash summary in formats suitable
    for JSON export and AI analysis.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the header parser.
        
        Args:
            file_path: Path to the .DMP file
        """
        self.file_path = file_path
        self._reader: Optional[DumpFileReader] = None
        self._header: Optional[DumpHeader] = None
        self._system_info: Optional[SystemInfo] = None
        self._crash_summary: Optional[CrashSummary] = None
    
    def parse(self) -> bool:
        """
        Parse the dump file header.
        
        Returns:
            True if parsing was successful, False otherwise
        """
        try:
            self._reader = DumpFileReader(self.file_path)
            with self._reader:
                self._header = self._reader.parse_header()
            return True
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            print(f"Error parsing dump file: {e}")
            return False
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes >= 1024 ** 3:
            return f"{size_bytes / (1024 ** 3):.2f} GB"
        elif size_bytes >= 1024 ** 2:
            return f"{size_bytes / (1024 ** 2):.2f} MB"
        elif size_bytes >= 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes} bytes"
    
    def get_system_info(self) -> Optional[SystemInfo]:
        """
        Get system information from the dump header.
        
        Returns:
            SystemInfo object or None if not parsed
        """
        if not self._header:
            return None
        
        if self._system_info:
            return self._system_info
        
        file_size = os.path.getsize(self.file_path)
        
        self._system_info = SystemInfo(
            os_version=f"Windows {self._header.major_version}.{self._header.minor_version}",
            architecture=self._header.get_machine_type_name(),
            processor_count=self._header.number_processors,
            dump_type=self._header.get_dump_type_name(),
            dump_size_bytes=file_size,
            dump_size_human=self._format_size(file_size),
            is_64bit=self._header.is_64bit,
            crash_time_raw=self._header.system_time,
        )
        
        return self._system_info
    
    def get_crash_summary(self) -> Optional[CrashSummary]:
        """
        Get crash summary from the dump header.
        
        Returns:
            CrashSummary object or None if not parsed
        """
        if not self._header:
            return None
        
        if self._crash_summary:
            return self._crash_summary
        
        bugcheck_code = self._header.bugcheck_code
        
        self._crash_summary = CrashSummary(
            bugcheck_code=format_bugcheck_code(bugcheck_code),
            bugcheck_code_int=bugcheck_code,
            bugcheck_name=get_bugcheck_name(bugcheck_code),
            parameter1=f"0x{self._header.bugcheck_param1:016X}",
            parameter2=f"0x{self._header.bugcheck_param2:016X}",
            parameter3=f"0x{self._header.bugcheck_param3:016X}",
            parameter4=f"0x{self._header.bugcheck_param4:016X}",
            file_path=self.file_path,
            file_name=os.path.basename(self.file_path),
        )
        
        return self._crash_summary
    
    @property
    def header(self) -> Optional[DumpHeader]:
        """Get the raw dump header."""
        return self._header


def parse_dump_header(file_path: str) -> tuple[Optional[SystemInfo], Optional[CrashSummary]]:
    """
    Convenience function to parse a dump file and return system info and crash summary.
    
    Args:
        file_path: Path to the .DMP file
        
    Returns:
        Tuple of (SystemInfo, CrashSummary) or (None, None) if parsing failed
    """
    parser = HeaderParser(file_path)
    if parser.parse():
        return parser.get_system_info(), parser.get_crash_summary()
    return None, None
