"""
Driver List Extractor Module

This module extracts the list of loaded kernel drivers from Windows memory dumps.
Drivers are critical for BSOD analysis as they are often the cause of system crashes.
"""

import struct
import os
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Handle both relative and absolute imports
try:
    from .dump_reader import DumpFileReader, DumpHeader
except ImportError:
    from parser.dump_reader import DumpFileReader, DumpHeader


# Known problematic drivers database
# These are drivers commonly associated with system issues
KNOWN_PROBLEMATIC_DRIVERS: Dict[str, str] = {
    # Antivirus/Security (can cause conflicts)
    "aswsp.sys": "Avast Software - may cause memory issues",
    "aswsnx.sys": "Avast Software - file system filter",
    "avgsp.sys": "AVG Antivirus - may cause conflicts",
    "bdvedisk.sys": "Bitdefender - virtual disk driver",
    "klif.sys": "Kaspersky Lab - file system filter",
    "tmusa.sys": "Trend Micro - may cause performance issues",
    "tmcomm.sys": "Trend Micro - communication driver",
    
    # Graphics drivers
    "nvlddmkm.sys": "NVIDIA Display Driver - common crash source",
    "atikmpag.sys": "AMD Display Driver - may cause TDR failures",
    "igdkmd64.sys": "Intel Graphics - may conflict with dedicated GPU",
    "amdkmdag.sys": "AMD Graphics - kernel mode driver",
    
    # Network drivers
    "e1c62x64.sys": "Intel Ethernet - may cause network issues",
    "rt640x64.sys": "Realtek Ethernet - may cause BSODs",
    "nwifi.sys": "Windows WiFi driver - rarely causes issues",
    
    # Storage drivers
    "iaStorV.sys": "Intel Rapid Storage - may cause disk issues",
    "storahci.sys": "Standard AHCI driver - check for updates",
    "nvme.sys": "NVMe controller driver",
    "mrvldev0.sys": "Marvell storage - known for issues",
    
    # Third-party software
    "cpuz.sys": "CPU-Z driver - can cause issues",
    "rtcore64.sys": "MSI Afterburner - known vulnerability",
    "asmtxhci.sys": "ASMedia USB 3.0 - may cause USB issues",
    "asustp.sys": "ASUS driver - check for updates",
    "ene.sys": "MSI/RGB software - known issues",
    "wintap.sys": "VPN/Firewall software",
    
    # Virtualization
    "vboxdrv.sys": "VirtualBox - may conflict with Hyper-V",
    "vmci.sys": "VMware - virtualization driver",
    "vmx86.sys": "VMware Workstation driver",
    
    # Audio
    "nahimicservice.sys": "Nahimic audio - known for conflicts",
    "a2dpsrv.sys": "A-Volute - Sonic Studio, causes issues",
}

# Known Microsoft/Windows system drivers (typically safe)
KNOWN_SAFE_DRIVERS: set = {
    "ntoskrnl.exe", "hal.dll", "ci.dll", "clfs.sys", "tm.sys",
    "ntfs.sys", "fltmgr.sys", "wdf01000.sys", "ksecdd.sys",
    "ndis.sys", "tcpip.sys", "netio.sys", "fwpkclnt.sys",
    "storport.sys", "spaceport.sys", "volmgr.sys", "volmgrx.sys",
    "mountmgr.sys", "partmgr.sys", "disk.sys", "classpnp.sys",
    "acpi.sys", "wmilib.sys", "msrpc.sys", "cng.sys", "ksecpkg.sys",
}


@dataclass
class DriverInfo:
    """Information about a loaded kernel driver."""
    name: str
    base_address: int
    size: int
    path: Optional[str] = None
    timestamp: Optional[int] = None
    version: Optional[str] = None
    is_microsoft: bool = False
    is_problematic: bool = False
    problematic_reason: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "base_address": f"0x{self.base_address:016X}",
            "size": self.size,
            "size_human": self._format_size(self.size),
            "path": self.path,
            "timestamp": self.timestamp,
            "timestamp_human": self._format_timestamp() if self.timestamp else None,
            "version": self.version,
            "is_microsoft": self.is_microsoft,
            "is_problematic": self.is_problematic,
            "problematic_reason": self.problematic_reason,
        }
    
    def _format_size(self, size: int) -> str:
        """Format size in human-readable format."""
        if size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.2f} MB"
        elif size >= 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size} bytes"
    
    def _format_timestamp(self) -> Optional[str]:
        """Format timestamp as human-readable date."""
        if self.timestamp:
            try:
                dt = datetime.fromtimestamp(self.timestamp)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, OSError):
                return None
        return None


@dataclass
class DriverListResult:
    """Result of driver list extraction."""
    drivers: List[DriverInfo]
    total_count: int
    microsoft_count: int
    third_party_count: int
    problematic_count: int
    problematic_drivers: List[DriverInfo]
    extraction_method: str
    note: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_count": self.total_count,
            "microsoft_count": self.microsoft_count,
            "third_party_count": self.third_party_count,
            "problematic_count": self.problematic_count,
            "extraction_method": self.extraction_method,
            "note": self.note,
            "drivers": [d.to_dict() for d in self.drivers],
            "problematic_drivers": [d.to_dict() for d in self.problematic_drivers],
        }


class DriverListExtractor:
    """
    Extracts the list of loaded kernel drivers from a memory dump.
    
    This uses the DUMP_HEADER64's module list information to enumerate drivers.
    The driver list in full kernel dumps starts at the ModuleListOffset pointer.
    """
    
    # Offsets in DUMP_HEADER64 for module list
    # These offsets point to the loaded module database
    MODULE_LIST_OFFSET_FIELD = 0x0060  # Offset to PsLoadedModuleList in header
    
    # Offsets within KLDR_DATA_TABLE_ENTRY structure (loaded module entry)
    KLDR_ENTRY_SIZE = 0xE0  # Approximate size of entry
    KLDR_FLINK_OFFSET = 0x00  # Forward link to next entry
    KLDR_BLINK_OFFSET = 0x08  # Back link to previous entry
    KLDR_BASE_ADDRESS_OFFSET = 0x30  # DllBase
    KLDR_ENTRY_POINT_OFFSET = 0x38  # EntryPoint
    KLDR_SIZE_OF_IMAGE_OFFSET = 0x40  # SizeOfImage
    KLDR_FULL_DLL_NAME_OFFSET = 0x48  # UNICODE_STRING FullDllName
    KLDR_BASE_DLL_NAME_OFFSET = 0x58  # UNICODE_STRING BaseDllName
    
    def __init__(self, dump_path: str):
        """
        Initialize the driver list extractor.
        
        Args:
            dump_path: Path to the dump file
        """
        self.dump_path = dump_path
        self._file = None
        self._drivers: List[DriverInfo] = []
    
    def __enter__(self):
        self._file = open(self.dump_path, 'rb')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
    
    def _read_uint64(self, offset: int) -> int:
        """Read an unsigned 64-bit integer at offset."""
        self._file.seek(offset)
        data = self._file.read(8)
        if len(data) < 8:
            return 0
        return struct.unpack('<Q', data)[0]
    
    def _read_uint32(self, offset: int) -> int:
        """Read an unsigned 32-bit integer at offset."""
        self._file.seek(offset)
        data = self._file.read(4)
        if len(data) < 4:
            return 0
        return struct.unpack('<I', data)[0]
    
    def _read_uint16(self, offset: int) -> int:
        """Read an unsigned 16-bit integer at offset."""
        self._file.seek(offset)
        data = self._file.read(2)
        if len(data) < 2:
            return 0
        return struct.unpack('<H', data)[0]
    
    def _read_unicode_string(self, offset: int, max_length: int = 512) -> str:
        """
        Read a UNICODE_STRING structure and return the string.
        UNICODE_STRING: { Length (2), MaxLength (2), Padding (4), Buffer (8) }
        """
        try:
            length = self._read_uint16(offset)
            if length == 0 or length > max_length:
                return ""
            
            # Buffer pointer is at offset + 8
            buffer_ptr = self._read_uint64(offset + 8)
            if buffer_ptr == 0:
                return ""
            
            # For kernel dumps, we can't directly read from virtual addresses
            # This would require address translation using PFN database
            # For MVP, return empty string and use alternative extraction
            return ""
            
        except Exception:
            return ""
    
    def _classify_driver(self, name: str, path: str = "") -> Tuple[bool, bool, Optional[str]]:
        """
        Classify a driver as Microsoft or third-party, and check if problematic.
        
        Returns:
            (is_microsoft, is_problematic, problematic_reason)
        """
        name_lower = name.lower()
        
        # Check if it's a known safe Microsoft driver
        is_microsoft = name_lower in KNOWN_SAFE_DRIVERS
        
        # Check path for Microsoft indicators
        if path:
            path_lower = path.lower()
            if "\\windows\\system32\\drivers\\" in path_lower:
                is_microsoft = True
            elif "\\windows\\system32\\" in path_lower:
                is_microsoft = True
        
        # Check against known problematic drivers
        is_problematic = name_lower in KNOWN_PROBLEMATIC_DRIVERS
        reason = KNOWN_PROBLEMATIC_DRIVERS.get(name_lower)
        
        return is_microsoft, is_problematic, reason
    
    def _extract_drivers_from_strings(self) -> List[DriverInfo]:
        """
        Alternative extraction method: scan dump file for driver name patterns.
        This is a fallback method that looks for .sys strings in the dump.
        """
        drivers = []
        seen_names = set()
        
        # Read header section (first 8KB which contains module info in some dumps)
        self._file.seek(0)
        header_data = self._file.read(8192)
        
        # Scan for PE headers and module references
        # Look for common driver name patterns
        i = 0
        while i < len(header_data) - 100:
            # Look for patterns that might indicate driver names
            # In kernel dumps, driver info is sometimes stored as wide strings
            
            # Check for .sys in ASCII
            if header_data[i:i+4] == b'.sys':
                # Try to extract the name before .sys
                start = i - 1
                while start > 0 and header_data[start] >= 0x20 and header_data[start] < 0x7F:
                    start -= 1
                start += 1
                
                if i - start >= 3:  # At least 3 chars before .sys
                    try:
                        name = header_data[start:i+4].decode('ascii')
                        if name and name not in seen_names and not name.startswith('.'):
                            seen_names.add(name)
                            is_ms, is_prob, reason = self._classify_driver(name)
                            drivers.append(DriverInfo(
                                name=name,
                                base_address=0,
                                size=0,
                                is_microsoft=is_ms,
                                is_problematic=is_prob,
                                problematic_reason=reason,
                            ))
                    except Exception:
                        pass
            i += 1
        
        return drivers
    
    def _scan_for_pe_signatures(self) -> List[DriverInfo]:
        """
        Scan the dump for PE signatures to find loaded modules.
        This method reads chunks of the dump to find PE headers.
        """
        drivers = []
        seen = set()
        
        # For very large dumps, we only scan the first portion
        # The loaded module list is typically in the first few MB
        scan_size = min(50 * 1024 * 1024, os.path.getsize(self.dump_path))  # Max 50MB scan
        
        self._file.seek(0)
        chunk_size = 4096
        offset = 0
        
        while offset < scan_size:
            self._file.seek(offset)
            chunk = self._file.read(chunk_size)
            
            if len(chunk) < 64:
                break
            
            # Look for MZ signature (PE header)
            i = 0
            while i < len(chunk) - 64:
                if chunk[i:i+2] == b'MZ':
                    # Found potential PE header
                    try:
                        # Read PE offset at 0x3C
                        pe_offset = struct.unpack('<I', chunk[i+0x3C:i+0x40])[0]
                        if pe_offset < 0x400:
                            # Verify PE signature
                            if i + pe_offset + 4 < len(chunk):
                                if chunk[i+pe_offset:i+pe_offset+4] == b'PE\x00\x00':
                                    # Valid PE found at this offset
                                    # We'd need more logic to extract the name
                                    pass
                    except Exception:
                        pass
                i += 1
            
            offset += chunk_size - 64  # Overlap to catch signatures at boundaries
        
        return drivers
    
    def extract_drivers(self) -> DriverListResult:
        """
        Extract the list of loaded kernel drivers from the dump.
        
        Returns:
            DriverListResult with list of drivers
        """
        if not self._file:
            return DriverListResult(
                drivers=[],
                total_count=0,
                microsoft_count=0,
                third_party_count=0,
                problematic_count=0,
                problematic_drivers=[],
                extraction_method="none",
                note="File not opened"
            )
        
        # Try string-based extraction first
        drivers = self._extract_drivers_from_strings()
        
        if not drivers:
            # If string extraction found nothing, report that
            return DriverListResult(
                drivers=[],
                total_count=0,
                microsoft_count=0,
                third_party_count=0,
                problematic_count=0,
                problematic_drivers=[],
                extraction_method="string_scan",
                note="No drivers found in header. Full driver list requires loading module database from dump which needs virtual address translation. For complete driver info, use 'lm' command in WinDbg."
            )
        
        # Count and classify
        microsoft_count = sum(1 for d in drivers if d.is_microsoft)
        third_party = [d for d in drivers if not d.is_microsoft]
        problematic = [d for d in drivers if d.is_problematic]
        
        return DriverListResult(
            drivers=drivers,
            total_count=len(drivers),
            microsoft_count=microsoft_count,
            third_party_count=len(third_party),
            problematic_count=len(problematic),
            problematic_drivers=problematic,
            extraction_method="string_scan",
            note=f"Found {len(drivers)} driver references. For complete driver listing with addresses and versions, analyze with WinDbg."
        )


def get_common_drivers_analysis() -> Dict[str, Any]:
    """
    Return analysis template for common drivers.
    This can be used when dump parsing doesn't yield driver list.
    """
    return {
        "note": "To get a complete driver list, the dump file needs to be analyzed with WinDbg or similar tools that can translate virtual addresses.",
        "common_problematic_drivers": {
            name: desc for name, desc in KNOWN_PROBLEMATIC_DRIVERS.items()
        },
        "recommendation": "If you know which drivers are installed, you can manually check against the problematic drivers list above."
    }


def extract_drivers(dump_path: str) -> DriverListResult:
    """
    Convenience function to extract drivers from a dump file.
    
    Args:
        dump_path: Path to the dump file
    
    Returns:
        DriverListResult with extracted drivers
    """
    with DriverListExtractor(dump_path) as extractor:
        return extractor.extract_drivers()
