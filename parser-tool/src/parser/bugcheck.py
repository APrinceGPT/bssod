"""
Bugcheck Analyzer Module

This module provides detailed analysis and interpretation of Windows
bugcheck (BSOD) codes and their parameters.
"""

import sys
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

# Handle both relative and absolute imports
try:
    from ..utils.constants import get_bugcheck_name, format_bugcheck_code, BUGCHECK_CODES
except ImportError:
    from utils.constants import get_bugcheck_name, format_bugcheck_code, BUGCHECK_CODES


# Parameter descriptions for common bugcheck codes
# Format: {bugcheck_code: {param_num: description}}
BUGCHECK_PARAM_DESCRIPTIONS: Dict[int, Dict[int, str]] = {
    0x0000001A: {  # MEMORY_MANAGEMENT
        1: "Memory management subtype code",
        2: "Address that caused the problem",
        3: "PFN of the corrupted page (if applicable)",
        4: "Reserved / Additional context",
    },
    0x0000001E: {  # KMODE_EXCEPTION_NOT_HANDLED
        1: "Exception code (NTSTATUS)",
        2: "Address where exception occurred",
        3: "First exception parameter",
        4: "Second exception parameter",
    },
    0x00000050: {  # PAGE_FAULT_IN_NONPAGED_AREA
        1: "Address referenced causing the fault",
        2: "0 = read, 1 = write, 2 = execute, 8 = execute",
        3: "Address that referenced the bad memory",
        4: "Type of read: 0 = read, 2 = execute",
    },
    0x0000007E: {  # SYSTEM_THREAD_EXCEPTION_NOT_HANDLED
        1: "Exception code (NTSTATUS)",
        2: "Address where exception occurred",
        3: "Exception record address",
        4: "Context record address",
    },
    0x0000007F: {  # UNEXPECTED_KERNEL_MODE_TRAP
        1: "Trap number (x86/x64 processor exception)",
        2: "Reserved",
        3: "Reserved",
        4: "Reserved",
    },
    0x0000009F: {  # DRIVER_POWER_STATE_FAILURE
        1: "Subtype of power failure",
        2: "Address of the device object",
        3: "Address of the driver object",
        4: "Reserved (depends on subtype)",
    },
    0x000000A0: {  # INTERNAL_POWER_ERROR
        1: "Subtype of internal power error",
        2: "Additional info (subtype-dependent)",
        3: "Additional info (subtype-dependent)",
        4: "Additional info (subtype-dependent)",
    },
    0x000000D1: {  # DRIVER_IRQL_NOT_LESS_OR_EQUAL
        1: "Memory address referenced",
        2: "IRQL at time of reference",
        3: "0 = read, 1 = write",
        4: "Address of instruction that referenced memory",
    },
    0x000000EF: {  # CRITICAL_PROCESS_DIED
        1: "Process object address",
        2: "If 0 = process terminated, if 1 = thread terminated",
        3: "Reserved",
        4: "Reserved",
    },
    0x00000116: {  # VIDEO_TDR_FAILURE
        1: "Pointer to internal TDR recovery context",
        2: "Pointer to responsible device driver module",
        3: "Error code of last failed operation",
        4: "Internal context dependent data",
    },
    0x00000139: {  # KERNEL_SECURITY_CHECK_FAILURE
        1: "Security cookie failure type",
        2: "Address of trap frame / exception record",
        3: "Address of context record",
        4: "Reserved",
    },
    0x000001CA: {  # SYNTHETIC_WATCHDOG_TIMEOUT
        1: "Timeout count",
        2: "Process object (if applicable)",
        3: "Thread object (if applicable)",
        4: "Additional context",
    },
    0x00000154: {  # UNEXPECTED_STORE_EXCEPTION
        1: "Exception record address",
        2: "Context record address",
        3: "Exception code",
        4: "Reserved",
    },
    0x000000C2: {  # BAD_POOL_CALLER
        1: "Type of pool corruption",
        2: "Depends on parameter 1",
        3: "Depends on parameter 1",
        4: "Depends on parameter 1",
    },
    0x000000C4: {  # DRIVER_VERIFIER_DETECTED_VIOLATION
        1: "Subtype of driver verifier violation",
        2: "Address of driver with the violation",
        3: "Violation-specific parameter",
        4: "Violation-specific parameter",
    },
    0x000000FC: {  # ATTEMPTED_EXECUTE_OF_NOEXECUTE_MEMORY
        1: "Address being executed",
        2: "PTE contents",
        3: "Reserved",
        4: "Reserved",
    },
}

# MEMORY_MANAGEMENT subtypes (param1)
MEMORY_MANAGEMENT_SUBTYPES: Dict[int, str] = {
    0x00041284: "A page that should have been filled with zeros was not.",
    0x00041285: "A PTE has been corrupted.",
    0x00041286: "A page table page has been corrupted.",
    0x00041287: "A PFN list head has been corrupted.",
    0x00041790: "The page frame number list is corrupt.",
    0x00041792: "A PTE or the PFN is corrupted.",
    0x00041793: "A page table has been corrupted.",
    0x00041794: "An illegal PFN was used.",
    0x00061940: "An allocation that should have been pageable was not.",
    0x00061941: "A free happened on bad pool.",
    0x00061946: "A corrupted page table was detected.",
}

# x86/x64 trap numbers for UNEXPECTED_KERNEL_MODE_TRAP
TRAP_NUMBERS: Dict[int, str] = {
    0x00: "Divide Error",
    0x01: "Debug Exception",
    0x02: "NMI Interrupt",
    0x03: "Breakpoint",
    0x04: "Overflow",
    0x05: "Bound Range Exceeded",
    0x06: "Invalid Opcode",
    0x07: "Device Not Available (No Math Coprocessor)",
    0x08: "Double Fault",
    0x09: "Coprocessor Segment Overrun",
    0x0A: "Invalid TSS",
    0x0B: "Segment Not Present",
    0x0C: "Stack Segment Fault",
    0x0D: "General Protection Fault",
    0x0E: "Page Fault",
    0x10: "x87 Floating-Point Error",
    0x11: "Alignment Check",
    0x12: "Machine Check",
    0x13: "SIMD Floating-Point Exception",
}


@dataclass
class ParameterAnalysis:
    """Analysis of a single bugcheck parameter."""
    parameter_number: int
    raw_value: int
    hex_value: str
    description: str
    interpretation: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class BugcheckAnalysis:
    """Complete analysis of a bugcheck."""
    code: int
    code_hex: str
    name: str
    category: str
    description: str
    parameters: List[ParameterAnalysis]
    recommendations: List[str]
    likely_causes: List[str]
    severity: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "code": self.code,
            "code_hex": self.code_hex,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "parameters": [p.to_dict() for p in self.parameters],
            "recommendations": self.recommendations,
            "likely_causes": self.likely_causes,
            "severity": self.severity,
        }
        return result


# Bugcheck categories and their descriptions
BUGCHECK_CATEGORIES: Dict[str, List[int]] = {
    "Memory Corruption": [0x1A, 0x50, 0x7A, 0xC2, 0xC5, 0xFC],
    "Driver Issues": [0xD1, 0xD3, 0xD8, 0xC4, 0x9F, 0x116],
    "Hardware Failure": [0x7F, 0x124, 0x9C],
    "Process/Thread": [0xEF, 0x139, 0xF4],
    "File System": [0x24, 0x77],
    "Power Management": [0x9F, 0xA0],
    "Security": [0x139],
    "Graphics/Display": [0x116, 0x119],
    "General Exception": [0x1E, 0x7E, 0x8E],
}


def get_category(bugcheck_code: int) -> str:
    """Get the category for a bugcheck code."""
    for category, codes in BUGCHECK_CATEGORIES.items():
        if bugcheck_code in codes:
            return category
    return "Other"


def get_severity(bugcheck_code: int) -> str:
    """Estimate severity based on bugcheck code."""
    critical = [0xEF, 0x139, 0x7F, 0x124, 0x50]
    high = [0xD1, 0x1A, 0x7E, 0x1E, 0xC4]
    
    if bugcheck_code in critical:
        return "Critical"
    elif bugcheck_code in high:
        return "High"
    else:
        return "Medium"


def get_likely_causes(bugcheck_code: int) -> List[str]:
    """Get likely causes for a bugcheck code."""
    causes = {
        0x0000001A: [
            "Faulty RAM or memory hardware",
            "Corrupted memory due to driver bug",
            "Overclocked memory causing instability",
            "Damaged system files",
        ],
        0x0000001E: [
            "Incompatible or buggy driver",
            "Faulty hardware",
            "Software conflict",
        ],
        0x00000050: [
            "Faulty driver accessing invalid memory",
            "Defective RAM",
            "Antivirus software conflict",
            "Corrupted system files",
        ],
        0x0000007E: [
            "System thread generated an unhandled exception",
            "Driver compatibility issue",
            "Corrupted system files",
        ],
        0x0000007F: [
            "Hardware failure (memory, CPU)",
            "Kernel stack overflow",
            "Driver bug",
        ],
        0x0000009F: [
            "Driver failed to complete a power IRP",
            "Incompatible power management driver",
            "Hardware device not responding",
        ],
        0x000000D1: [
            "Driver accessing pageable memory at high IRQL",
            "Driver bug (most common)",
            "Faulty driver installation",
        ],
        0x000000EF: [
            "Critical system process terminated unexpectedly",
            "Corrupted system files",
            "Failed system update",
            "Hardware failure",
        ],
        0x00000116: [
            "Graphics driver failed to respond",
            "Overheating GPU",
            "Outdated graphics drivers",
            "Faulty graphics card",
        ],
        0x00000139: [
            "Buffer overflow detected in kernel",
            "Stack corruption",
            "Malware or security compromise",
        ],
    }
    return causes.get(bugcheck_code, [
        "Driver compatibility issue",
        "Hardware malfunction",
        "Corrupted system files",
    ])


def get_recommendations(bugcheck_code: int) -> List[str]:
    """Get recommendations for resolving a bugcheck."""
    recs = {
        0x0000001A: [
            "Run Windows Memory Diagnostic (mdsched.exe)",
            "Check for driver updates",
            "Run System File Checker (sfc /scannow)",
            "Check for overclocking and reset to defaults",
        ],
        0x00000050: [
            "Run Windows Memory Diagnostic",
            "Update all drivers especially graphics and storage",
            "Temporarily disable antivirus to test",
            "Run chkdsk to check disk health",
        ],
        0x000000D1: [
            "Update the driver mentioned in the crash",
            "Use Driver Verifier to identify problematic driver",
            "Roll back recent driver updates",
        ],
        0x000000EF: [
            "Run System File Checker (sfc /scannow)",
            "Run DISM /Online /Cleanup-Image /RestoreHealth",
            "Check disk health with chkdsk",
            "Consider system restore to earlier point",
        ],
        0x00000116: [
            "Update graphics drivers",
            "Check GPU temperature and cooling",
            "Reduce graphics settings in games/apps",
            "Clean GPU and improve ventilation",
        ],
        0x00000139: [
            "Scan for malware with Windows Defender",
            "Run System File Checker",
            "Update Windows to latest version",
        ],
    }
    return recs.get(bugcheck_code, [
        "Update all drivers to latest versions",
        "Run System File Checker (sfc /scannow)",
        "Check Windows Event Viewer for more details",
        "Run Windows Memory Diagnostic",
    ])


def interpret_parameter(bugcheck_code: int, param_num: int, value: int) -> Optional[str]:
    """Provide specific interpretation for known parameter values."""
    if bugcheck_code == 0x1A and param_num == 1:
        # MEMORY_MANAGEMENT subtype
        return MEMORY_MANAGEMENT_SUBTYPES.get(value)
    
    if bugcheck_code == 0x7F and param_num == 1:
        # UNEXPECTED_KERNEL_MODE_TRAP trap number
        return TRAP_NUMBERS.get(value)
    
    if bugcheck_code == 0x50 and param_num == 2:
        # PAGE_FAULT operation type
        ops = {0: "Read operation", 1: "Write operation", 2: "Execute operation", 8: "Execute operation"}
        return ops.get(value)
    
    if bugcheck_code == 0xD1 and param_num == 3:
        # DRIVER_IRQL operation type
        ops = {0: "Read operation", 1: "Write operation"}
        return ops.get(value)
    
    return None


class BugcheckAnalyzer:
    """Analyzer for Windows bugcheck codes."""
    
    def __init__(self, bugcheck_code: int, param1: int = 0, param2: int = 0,
                 param3: int = 0, param4: int = 0):
        """
        Initialize the bugcheck analyzer.
        
        Args:
            bugcheck_code: The bugcheck code (BSOD stop code)
            param1-4: The four bugcheck parameters
        """
        self.code = bugcheck_code
        self.params = [param1, param2, param3, param4]
    
    def analyze(self) -> BugcheckAnalysis:
        """Perform complete analysis of the bugcheck."""
        # Get basic info
        name = get_bugcheck_name(self.code)
        code_hex = format_bugcheck_code(self.code)
        category = get_category(self.code)
        
        # Get bugcheck description
        description = self._get_description()
        
        # Analyze parameters
        parameters = self._analyze_parameters()
        
        # Get causes and recommendations
        likely_causes = get_likely_causes(self.code)
        recommendations = get_recommendations(self.code)
        severity = get_severity(self.code)
        
        return BugcheckAnalysis(
            code=self.code,
            code_hex=code_hex,
            name=name,
            category=category,
            description=description,
            parameters=parameters,
            recommendations=recommendations,
            likely_causes=likely_causes,
            severity=severity,
        )
    
    def _get_description(self) -> str:
        """Get a description of the bugcheck code."""
        descriptions = {
            0x1A: "The memory manager has detected a memory corruption issue.",
            0x1E: "A kernel-mode program generated an exception that wasn't caught.",
            0x50: "The system tried to access invalid memory (page fault).",
            0x7E: "A system thread generated an exception that wasn't handled.",
            0x7F: "The CPU generated an unexpected trap (processor exception).",
            0x9F: "A driver is in an inconsistent or invalid power state.",
            0xA0: "The power policy manager experienced a fatal error.",
            0xD1: "A driver accessed paged memory at an improper IRQL level.",
            0xEF: "A critical system process died unexpectedly.",
            0x116: "The display driver failed to respond in the allowed time.",
            0x139: "The kernel detected security violations (buffer overflow/stack corruption).",
            0x154: "An unexpected store exception occurred.",
            0xC2: "A caller with pool responsibility passed bad parameters.",
            0xC4: "Driver Verifier detected a driver violation.",
            0xFC: "Attempt to execute non-executable memory.",
        }
        return descriptions.get(self.code, 
                               f"System stop error occurred with code {format_bugcheck_code(self.code)}")
    
    def _analyze_parameters(self) -> List[ParameterAnalysis]:
        """Analyze the bugcheck parameters."""
        parameters = []
        param_descs = BUGCHECK_PARAM_DESCRIPTIONS.get(self.code, {})
        
        for i, value in enumerate(self.params, 1):
            desc = param_descs.get(i, f"Bugcheck parameter {i}")
            interpretation = interpret_parameter(self.code, i, value)
            
            param = ParameterAnalysis(
                parameter_number=i,
                raw_value=value,
                hex_value=f"0x{value:016X}",
                description=desc,
                interpretation=interpretation,
            )
            parameters.append(param)
        
        return parameters


def analyze_bugcheck(bugcheck_code: int, param1: int = 0, param2: int = 0,
                     param3: int = 0, param4: int = 0) -> BugcheckAnalysis:
    """
    Convenience function to analyze a bugcheck.
    
    Args:
        bugcheck_code: The bugcheck code (BSOD stop code)
        param1-4: The four bugcheck parameters
    
    Returns:
        BugcheckAnalysis with complete analysis
    """
    analyzer = BugcheckAnalyzer(bugcheck_code, param1, param2, param3, param4)
    return analyzer.analyze()
