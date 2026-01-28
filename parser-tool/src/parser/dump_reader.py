"""
Windows Memory Dump File Reader

This module provides low-level reading capabilities for Windows memory dump files (.DMP).
It uses Python's built-in struct module to parse the binary format.

Windows Dump File Format Reference:
- Full Memory Dump: Contains complete physical memory contents
- Kernel Memory Dump: Contains kernel and driver memory only
- Small Memory Dump (Minidump): Contains minimal crash information

The dump file starts with a header that contains:
- Signature identifying the dump type
- System information (version, architecture)
- Bugcheck code and parameters
- Physical memory descriptor
"""

import struct
import os
from dataclasses import dataclass
from typing import Optional
from enum import IntEnum


class DumpType(IntEnum):
    """Windows dump file types."""
    UNKNOWN = 0
    FULL_DUMP = 1
    KERNEL_DUMP = 2
    BMP_DUMP = 3  # Bitmap dump (Windows 8+)
    MINIDUMP = 4
    LIVEDUMP = 5


class MachineType(IntEnum):
    """Processor architecture types."""
    UNKNOWN = 0
    I386 = 0x014c      # x86
    AMD64 = 0x8664     # x64
    ARM = 0x01c0       # ARM
    ARM64 = 0xAA64     # ARM64


# Dump file signatures
DUMP_SIGNATURE_32 = b'PAGEDUMP'  # 32-bit dump
DUMP_SIGNATURE_64 = b'PAGEDU64'  # 64-bit dump
DUMP_VALID_SIGNATURE = b'DUMP'   # Valid dump marker


@dataclass
class DumpHeader:
    """Represents the parsed dump file header."""
    signature: str
    valid_dump: str
    major_version: int
    minor_version: int
    machine_type: MachineType
    number_processors: int
    bugcheck_code: int
    bugcheck_param1: int
    bugcheck_param2: int
    bugcheck_param3: int
    bugcheck_param4: int
    dump_type: DumpType
    required_dump_space: int
    system_time: int
    is_64bit: bool
    physical_memory_block_offset: int
    exception_record_offset: int
    
    def get_machine_type_name(self) -> str:
        """Get human-readable machine type name."""
        names = {
            MachineType.I386: "x86 (32-bit)",
            MachineType.AMD64: "x64 (64-bit)",
            MachineType.ARM: "ARM (32-bit)",
            MachineType.ARM64: "ARM64 (64-bit)",
        }
        return names.get(self.machine_type, f"Unknown ({self.machine_type})")
    
    def get_dump_type_name(self) -> str:
        """Get human-readable dump type name."""
        names = {
            DumpType.FULL_DUMP: "Full Memory Dump",
            DumpType.KERNEL_DUMP: "Kernel Memory Dump",
            DumpType.BMP_DUMP: "Bitmap Dump",
            DumpType.MINIDUMP: "Small Memory Dump (Minidump)",
            DumpType.LIVEDUMP: "Live Dump",
        }
        return names.get(self.dump_type, f"Unknown ({self.dump_type})")


class DumpFileReader:
    """
    Reader for Windows memory dump files.
    
    This class handles opening and reading the dump file header
    without loading the entire file into memory.
    """
    
    # Header structure offsets for 64-bit dumps (PAGEDU64)
    # Based on _DUMP_HEADER64 structure from Windows SDK
    OFFSET_SIGNATURE = 0x0000          # 4 bytes: "PAGE"
    OFFSET_VALID_DUMP = 0x0004         # 4 bytes: "DU64" or "DUMP"
    OFFSET_MAJOR_VERSION = 0x0008      # 4 bytes
    OFFSET_MINOR_VERSION = 0x000C      # 4 bytes
    OFFSET_DIRECTORY_TABLE_BASE = 0x0010  # 8 bytes
    OFFSET_PFN_DATABASE = 0x0018       # 8 bytes
    OFFSET_PS_LOADED_MODULE_LIST = 0x0020  # 8 bytes
    OFFSET_PS_ACTIVE_PROCESS_HEAD = 0x0028  # 8 bytes
    OFFSET_MACHINE_IMAGE_TYPE = 0x0030  # 4 bytes
    OFFSET_NUMBER_PROCESSORS = 0x0034  # 4 bytes
    OFFSET_BUGCHECK_CODE = 0x0038      # 4 bytes
    OFFSET_BUGCHECK_PARAM1 = 0x0040    # 8 bytes (64-bit)
    OFFSET_BUGCHECK_PARAM2 = 0x0048    # 8 bytes
    OFFSET_BUGCHECK_PARAM3 = 0x0050    # 8 bytes
    OFFSET_BUGCHECK_PARAM4 = 0x0058    # 8 bytes
    OFFSET_DUMP_TYPE = 0x0F98          # 4 bytes
    OFFSET_SYSTEM_TIME = 0x0FA0        # 8 bytes
    OFFSET_REQUIRED_DUMP_SPACE = 0x1028  # 8 bytes
    
    def __init__(self, file_path: str):
        """
        Initialize the dump file reader.
        
        Args:
            file_path: Path to the .DMP file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a valid Windows dump file
        """
        self.file_path = file_path
        self._file_handle: Optional[object] = None
        self._header: Optional[DumpHeader] = None
        self._is_64bit: bool = False
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dump file not found: {file_path}")
        
        self.file_size = os.path.getsize(file_path)
    
    def open(self) -> None:
        """Open the dump file for reading."""
        self._file_handle = open(self.file_path, 'rb')
    
    def close(self) -> None:
        """Close the dump file."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def _read_at(self, offset: int, size: int) -> bytes:
        """
        Read bytes at a specific offset.
        
        Args:
            offset: File offset to read from
            size: Number of bytes to read
            
        Returns:
            The bytes read from the file
        """
        if not self._file_handle:
            raise RuntimeError("File not opened. Call open() first.")
        
        self._file_handle.seek(offset)
        return self._file_handle.read(size)
    
    def _read_uint32(self, offset: int) -> int:
        """Read unsigned 32-bit integer at offset."""
        data = self._read_at(offset, 4)
        return struct.unpack('<I', data)[0]
    
    def _read_uint64(self, offset: int) -> int:
        """Read unsigned 64-bit integer at offset."""
        data = self._read_at(offset, 8)
        return struct.unpack('<Q', data)[0]
    
    def _read_uint16(self, offset: int) -> int:
        """Read unsigned 16-bit integer at offset."""
        data = self._read_at(offset, 2)
        return struct.unpack('<H', data)[0]
    
    def _read_string(self, offset: int, max_length: int) -> str:
        """Read null-terminated string at offset."""
        data = self._read_at(offset, max_length)
        try:
            # Find null terminator
            null_pos = data.find(b'\x00')
            if null_pos != -1:
                data = data[:null_pos]
            return data.decode('utf-8', errors='replace')
        except (UnicodeDecodeError, AttributeError):
            return ""
    
    def validate_signature(self) -> bool:
        """
        Validate that the file is a Windows dump file.
        
        Returns:
            True if the file has a valid dump signature
        """
        # Read first 8 bytes
        sig_data = self._read_at(0, 8)
        
        # Check for 64-bit dump
        if sig_data == DUMP_SIGNATURE_64:
            self._is_64bit = True
            return True
        
        # Check for 32-bit dump
        if sig_data == DUMP_SIGNATURE_32:
            self._is_64bit = False
            return True
        
        return False
    
    def parse_header(self) -> DumpHeader:
        """
        Parse the dump file header.
        
        Returns:
            DumpHeader object containing parsed header data
            
        Raises:
            ValueError: If the file is not a valid dump file
        """
        if not self._file_handle:
            raise RuntimeError("File not opened. Call open() first.")
        
        if not self.validate_signature():
            raise ValueError("Invalid dump file signature")
        
        # Read signature and valid dump marker
        signature = self._read_at(0, 4).decode('ascii', errors='replace')
        valid_dump = self._read_at(4, 4).decode('ascii', errors='replace')
        
        # Read version info
        major_version = self._read_uint32(self.OFFSET_MAJOR_VERSION)
        minor_version = self._read_uint32(self.OFFSET_MINOR_VERSION)
        
        # Read machine image type (at offset 0x30 for 64-bit dumps)
        machine_type_raw = self._read_uint32(self.OFFSET_MACHINE_IMAGE_TYPE)
        try:
            machine_type = MachineType(machine_type_raw)
        except ValueError:
            machine_type = MachineType.UNKNOWN
        
        # Read number of processors
        number_processors = self._read_uint32(self.OFFSET_NUMBER_PROCESSORS)
        
        # Read bugcheck code and parameters
        bugcheck_code = self._read_uint32(self.OFFSET_BUGCHECK_CODE)
        
        if self._is_64bit:
            bugcheck_param1 = self._read_uint64(self.OFFSET_BUGCHECK_PARAM1)
            bugcheck_param2 = self._read_uint64(self.OFFSET_BUGCHECK_PARAM2)
            bugcheck_param3 = self._read_uint64(self.OFFSET_BUGCHECK_PARAM3)
            bugcheck_param4 = self._read_uint64(self.OFFSET_BUGCHECK_PARAM4)
        else:
            # 32-bit dumps have 32-bit parameters at different offsets
            bugcheck_param1 = self._read_uint32(0x001C)
            bugcheck_param2 = self._read_uint32(0x0020)
            bugcheck_param3 = self._read_uint32(0x0024)
            bugcheck_param4 = self._read_uint32(0x0028)
        
        # Read dump type
        dump_type_raw = self._read_uint32(self.OFFSET_DUMP_TYPE)
        try:
            dump_type = DumpType(dump_type_raw)
        except ValueError:
            dump_type = DumpType.UNKNOWN
        
        # Read system time
        system_time = self._read_uint64(self.OFFSET_SYSTEM_TIME)
        
        # Read required dump space
        try:
            required_dump_space = self._read_uint64(self.OFFSET_REQUIRED_DUMP_SPACE)
        except (struct.error, IndexError):
            required_dump_space = self.file_size
        
        self._header = DumpHeader(
            signature=signature,
            valid_dump=valid_dump,
            major_version=major_version,
            minor_version=minor_version,
            machine_type=machine_type,
            number_processors=number_processors,
            bugcheck_code=bugcheck_code,
            bugcheck_param1=bugcheck_param1,
            bugcheck_param2=bugcheck_param2,
            bugcheck_param3=bugcheck_param3,
            bugcheck_param4=bugcheck_param4,
            dump_type=dump_type,
            required_dump_space=required_dump_space,
            system_time=system_time,
            is_64bit=self._is_64bit,
            physical_memory_block_offset=0x0088 if self._is_64bit else 0x0064,
            exception_record_offset=0x0F00 if self._is_64bit else 0x07D0,
        )
        
        return self._header
    
    @property
    def header(self) -> Optional[DumpHeader]:
        """Get the parsed header."""
        return self._header
    
    @property
    def is_64bit(self) -> bool:
        """Check if this is a 64-bit dump."""
        return self._is_64bit
