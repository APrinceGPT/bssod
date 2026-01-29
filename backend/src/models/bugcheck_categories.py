"""
Bugcheck Categories Module

Maps Windows bugcheck codes to categories for specialized AI prompt generation.
Each category has specific analysis focus areas and recommendations.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


class BugcheckCategory(str, Enum):
    """Categories of Windows bugcheck codes for specialized analysis."""
    DRIVER = "driver"
    MEMORY = "memory"
    HARDWARE = "hardware"
    SYSTEM = "system"
    VIDEO = "video"
    STORAGE = "storage"
    UNKNOWN = "unknown"


@dataclass
class CategoryConfig:
    """Configuration for a bugcheck category."""
    name: str
    description: str
    focus_areas: List[str]
    key_questions: List[str]
    common_fixes: List[str]


# Category configurations with specialized analysis guidance
CATEGORY_CONFIGS: Dict[BugcheckCategory, CategoryConfig] = {
    BugcheckCategory.DRIVER: CategoryConfig(
        name="Driver-Related Crash",
        description="Crash caused by a device driver issue, often due to bugs, incompatibility, or corruption.",
        focus_areas=[
            "Identify the specific driver that caused the crash",
            "Check driver version and whether updates are available",
            "Look for patterns indicating driver bugs vs hardware issues",
            "Analyze IRQL levels and improper memory access",
        ],
        key_questions=[
            "Which driver is directly responsible for this crash?",
            "Is this a known issue with this driver version?",
            "Is the driver accessing memory it shouldn't?",
            "Could this be a driver compatibility issue with the Windows version?",
        ],
        common_fixes=[
            "Update the problematic driver to the latest version",
            "Roll back to a previous stable driver version",
            "Disable or uninstall the problematic driver",
            "Run Driver Verifier to identify additional driver issues",
            "Check Windows Update for driver updates",
        ],
    ),
    BugcheckCategory.MEMORY: CategoryConfig(
        name="Memory-Related Crash",
        description="Crash related to RAM, page file, or memory management issues.",
        focus_areas=[
            "Determine if this is a hardware (RAM) or software issue",
            "Check for memory corruption patterns",
            "Analyze page fault context and memory pressure",
            "Look for pool corruption or heap issues",
        ],
        key_questions=[
            "Is this likely a faulty RAM stick or software bug?",
            "Are there signs of memory corruption?",
            "Is the system under memory pressure?",
            "Could page file configuration be contributing?",
        ],
        common_fixes=[
            "Run Windows Memory Diagnostic (mdsched.exe)",
            "Test RAM with MemTest86+",
            "Check and adjust page file settings",
            "Update Windows to latest version for memory management fixes",
            "Check for memory-hungry applications",
        ],
    ),
    BugcheckCategory.HARDWARE: CategoryConfig(
        name="Hardware-Related Crash",
        description="Crash indicating possible hardware failure or firmware issues.",
        focus_areas=[
            "Identify the specific hardware component involved",
            "Determine if this is a WHEA (Windows Hardware Error Architecture) event",
            "Check for thermal or power-related issues",
            "Analyze machine check exception details",
        ],
        key_questions=[
            "Which hardware component is failing?",
            "Is this a CPU, motherboard, or peripheral issue?",
            "Are there signs of overheating or power issues?",
            "Is the BIOS/UEFI firmware up to date?",
        ],
        common_fixes=[
            "Update BIOS/UEFI firmware to latest version",
            "Check CPU and system temperatures",
            "Test with minimal hardware configuration",
            "Run manufacturer hardware diagnostics",
            "Check power supply stability and connections",
            "Reseat RAM and expansion cards",
        ],
    ),
    BugcheckCategory.SYSTEM: CategoryConfig(
        name="System/Kernel Crash",
        description="Crash in core Windows kernel or critical system processes.",
        focus_areas=[
            "Identify if this is a kernel integrity issue",
            "Check for security-related crashes",
            "Analyze critical process termination",
            "Look for system file corruption",
        ],
        key_questions=[
            "Is a critical Windows process crashing?",
            "Are there signs of system file corruption?",
            "Could this be a security or antivirus issue?",
            "Is the Windows installation healthy?",
        ],
        common_fixes=[
            "Run System File Checker (sfc /scannow)",
            "Run DISM to repair Windows image",
            "Check for Windows Update issues",
            "Temporarily disable antivirus/security software",
            "Consider Windows repair installation",
            "Check for malware with offline scanner",
        ],
    ),
    BugcheckCategory.VIDEO: CategoryConfig(
        name="Video/Display Crash",
        description="Crash related to graphics drivers or display subsystem.",
        focus_areas=[
            "Identify the graphics driver involved",
            "Check for TDR (Timeout Detection and Recovery) issues",
            "Analyze GPU timeout or scheduler problems",
            "Look for display driver memory issues",
        ],
        key_questions=[
            "Which graphics driver is responsible?",
            "Is this a GPU hardware or driver software issue?",
            "Are there signs of GPU overheating or power issues?",
            "Is the GPU overclocked or running demanding workloads?",
        ],
        common_fixes=[
            "Update graphics driver using DDU for clean install",
            "Roll back to previous stable graphics driver",
            "Check GPU temperatures and cooling",
            "Reduce GPU overclock settings",
            "Increase TDR timeout via registry (advanced)",
            "Test with basic display adapter",
        ],
    ),
    BugcheckCategory.STORAGE: CategoryConfig(
        name="Storage/Disk Crash",
        description="Crash related to storage drivers, file systems, or disk hardware.",
        focus_areas=[
            "Identify the storage driver or controller involved",
            "Check for file system corruption",
            "Analyze disk I/O errors or timeouts",
            "Look for storage controller issues",
        ],
        key_questions=[
            "Is this a disk hardware or driver issue?",
            "Are there signs of file system corruption?",
            "Is the storage controller firmware up to date?",
            "Could this be a cable or connection issue?",
        ],
        common_fixes=[
            "Run CHKDSK on affected drives",
            "Update storage controller drivers",
            "Check disk health with manufacturer tools",
            "Check and replace SATA/power cables",
            "Update storage controller firmware",
            "Check for SSD firmware updates",
        ],
    ),
    BugcheckCategory.UNKNOWN: CategoryConfig(
        name="Unknown Crash Type",
        description="Crash type could not be categorized; requires general analysis.",
        focus_areas=[
            "Perform general crash analysis",
            "Look for patterns in crash data",
            "Identify any obvious issues from stack trace",
            "Check for recently installed software or drivers",
        ],
        key_questions=[
            "What was the system doing when it crashed?",
            "Are there any patterns in recent crashes?",
            "Were any changes made before the crash started?",
            "What software was running at the time?",
        ],
        common_fixes=[
            "Check Event Viewer for related errors",
            "Review recently installed software and drivers",
            "Run Windows Update",
            "Perform clean boot to isolate issues",
            "Check system temperatures",
        ],
    ),
}

# Bugcheck code to category mapping
# Based on Windows bugcheck documentation and common patterns
BUGCHECK_CATEGORY_MAP: Dict[int, BugcheckCategory] = {
    # Driver-related
    0x0000000A: BugcheckCategory.DRIVER,  # IRQL_NOT_LESS_OR_EQUAL
    0x0000001E: BugcheckCategory.DRIVER,  # KMODE_EXCEPTION_NOT_HANDLED
    0x0000003B: BugcheckCategory.DRIVER,  # SYSTEM_SERVICE_EXCEPTION
    0x0000007E: BugcheckCategory.DRIVER,  # SYSTEM_THREAD_EXCEPTION_NOT_HANDLED
    0x0000008E: BugcheckCategory.DRIVER,  # KERNEL_MODE_EXCEPTION_NOT_HANDLED
    0x0000009F: BugcheckCategory.DRIVER,  # DRIVER_POWER_STATE_FAILURE
    0x000000BE: BugcheckCategory.DRIVER,  # ATTEMPTED_WRITE_TO_READONLY_MEMORY
    0x000000C2: BugcheckCategory.DRIVER,  # BAD_POOL_CALLER
    0x000000C4: BugcheckCategory.DRIVER,  # DRIVER_VERIFIER_DETECTED_VIOLATION
    0x000000C5: BugcheckCategory.DRIVER,  # DRIVER_CORRUPTED_EXPOOL
    0x000000D1: BugcheckCategory.DRIVER,  # DRIVER_IRQL_NOT_LESS_OR_EQUAL
    0x000000D8: BugcheckCategory.DRIVER,  # DRIVER_USED_EXCESSIVE_PTES
    0x000000EA: BugcheckCategory.DRIVER,  # THREAD_STUCK_IN_DEVICE_DRIVER
    0x000000FC: BugcheckCategory.DRIVER,  # ATTEMPTED_EXECUTE_OF_NOEXECUTE_MEMORY
    0x000000FE: BugcheckCategory.DRIVER,  # BUGCODE_USB_DRIVER
    0x0000011B: BugcheckCategory.DRIVER,  # DRIVER_RETURNED_HOLDING_CANCEL_LOCK
    0x000001C4: BugcheckCategory.DRIVER,  # DRIVER_VERIFIER_DETECTED_VIOLATION_LIVEDUMP
    0x000001D5: BugcheckCategory.DRIVER,  # DRIVER_PNP_WATCHDOG
    
    # Memory-related
    0x0000001A: BugcheckCategory.MEMORY,  # MEMORY_MANAGEMENT
    0x0000003F: BugcheckCategory.MEMORY,  # NO_MORE_SYSTEM_PTES
    0x00000050: BugcheckCategory.MEMORY,  # PAGE_FAULT_IN_NONPAGED_AREA
    0x0000007A: BugcheckCategory.MEMORY,  # KERNEL_DATA_INPAGE_ERROR
    0x0000013A: BugcheckCategory.MEMORY,  # KERNEL_MODE_HEAP_CORRUPTION
    0x00000189: BugcheckCategory.MEMORY,  # BAD_OBJECT_HEADER
    0x000001C7: BugcheckCategory.MEMORY,  # STORE_DATA_STRUCTURE_CORRUPTION
    
    # Hardware-related
    0x0000002E: BugcheckCategory.HARDWARE,  # DATA_BUS_ERROR
    0x0000007F: BugcheckCategory.HARDWARE,  # UNEXPECTED_KERNEL_MODE_TRAP
    0x0000009C: BugcheckCategory.HARDWARE,  # MACHINE_CHECK_EXCEPTION
    0x00000101: BugcheckCategory.HARDWARE,  # CLOCK_WATCHDOG_TIMEOUT
    0x00000124: BugcheckCategory.HARDWARE,  # WHEA_UNCORRECTABLE_ERROR
    0x00000133: BugcheckCategory.HARDWARE,  # DPC_WATCHDOG_TIMEOUT
    0x0000015F: BugcheckCategory.HARDWARE,  # CONNECTED_STANDBY_WATCHDOG_TIMEOUT
    0x000001CF: BugcheckCategory.HARDWARE,  # HARDWARE_WATCHDOG_TIMEOUT
    0x000001D0: BugcheckCategory.HARDWARE,  # CPI_FIRMWARE_WATCHDOG_TIMEOUT
    0x000001DB: BugcheckCategory.HARDWARE,  # IPI_WATCHDOG_TIMEOUT
    
    # System/Kernel-related
    0x00000001: BugcheckCategory.SYSTEM,  # APC_INDEX_MISMATCH
    0x000000F4: BugcheckCategory.SYSTEM,  # CRITICAL_OBJECT_TERMINATION
    0x00000109: BugcheckCategory.SYSTEM,  # CRITICAL_STRUCTURE_CORRUPTION
    0x00000139: BugcheckCategory.SYSTEM,  # KERNEL_SECURITY_CHECK_FAILURE
    0x00000154: BugcheckCategory.SYSTEM,  # UNEXPECTED_STORE_EXCEPTION
    0x0000018B: BugcheckCategory.SYSTEM,  # SECURE_FAULT_UNHANDLED
    0x0000018E: BugcheckCategory.SYSTEM,  # KERNEL_PARTITION_REFERENCE_VIOLATION
    0x000001C6: BugcheckCategory.SYSTEM,  # FAST_ERESOURCE_PRECONDITION_VIOLATION
    0x000001D2: BugcheckCategory.SYSTEM,  # WORKER_THREAD_INVALID_STATE
    
    # Video/Display-related
    0x00000116: BugcheckCategory.VIDEO,  # VIDEO_TDR_FAILURE
    0x00000119: BugcheckCategory.VIDEO,  # VIDEO_SCHEDULER_INTERNAL_ERROR
    0x0000011A: BugcheckCategory.VIDEO,  # VIDEO_SHADOW_DRIVER_FATAL_ERROR
    0x00000187: BugcheckCategory.VIDEO,  # VIDEO_DWMINIT_TIMEOUT_FALLBACK_BDD
    
    # Storage-related
    0x00000024: BugcheckCategory.STORAGE,  # NTFS_FILE_SYSTEM
    0x000000ED: BugcheckCategory.STORAGE,  # UNMOUNTABLE_BOOT_VOLUME
}


def get_bugcheck_category(bugcheck_code: int) -> BugcheckCategory:
    """
    Get the category for a bugcheck code.
    
    Args:
        bugcheck_code: The bugcheck code as an integer
        
    Returns:
        The BugcheckCategory for the code
    """
    return BUGCHECK_CATEGORY_MAP.get(bugcheck_code, BugcheckCategory.UNKNOWN)


def get_category_config(category: BugcheckCategory) -> CategoryConfig:
    """
    Get the configuration for a category.
    
    Args:
        category: The BugcheckCategory
        
    Returns:
        CategoryConfig with focus areas, questions, and fixes
    """
    return CATEGORY_CONFIGS[category]


def parse_bugcheck_code(code_str: Optional[str]) -> Optional[int]:
    """
    Parse a bugcheck code string to an integer.
    
    Args:
        code_str: Bugcheck code as string (e.g., "0x0000001A" or "26")
        
    Returns:
        Integer bugcheck code or None if parsing fails
    """
    if not code_str:
        return None
    
    try:
        # Handle hex format (0x...) or decimal
        code_str = code_str.strip()
        if code_str.lower().startswith("0x"):
            return int(code_str, 16)
        return int(code_str)
    except (ValueError, TypeError):
        return None
