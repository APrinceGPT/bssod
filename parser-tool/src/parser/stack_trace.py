"""
Stack Trace Parser Module

This module provides parsing of stack trace information from Windows memory dumps.
For full symbol resolution, external tools like WinDbg are needed.
This module extracts raw stack/context data that can be sent for AI analysis.
"""

import struct
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict

# Handle both relative and absolute imports
try:
    from .dump_reader import DumpFileReader, DumpHeader
except ImportError:
    from parser.dump_reader import DumpFileReader, DumpHeader


# Context record offsets (for x64 CONTEXT structure)
# The CONTEXT structure contains CPU register state at time of crash
CONTEXT_X64_SIZE = 1232  # Size of x64 CONTEXT structure

# Key register offsets within x64 CONTEXT (relative to context record start)
CONTEXT_FLAGS_OFFSET = 0x30
CONTEXT_RAX_OFFSET = 0x78
CONTEXT_RCX_OFFSET = 0x80
CONTEXT_RDX_OFFSET = 0x88
CONTEXT_RBX_OFFSET = 0x90
CONTEXT_RSP_OFFSET = 0x98
CONTEXT_RBP_OFFSET = 0xA0
CONTEXT_RSI_OFFSET = 0xA8
CONTEXT_RDI_OFFSET = 0xB0
CONTEXT_R8_OFFSET = 0xB8
CONTEXT_R9_OFFSET = 0xC0
CONTEXT_R10_OFFSET = 0xC8
CONTEXT_R11_OFFSET = 0xD0
CONTEXT_R12_OFFSET = 0xD8
CONTEXT_R13_OFFSET = 0xE0
CONTEXT_R14_OFFSET = 0xE8
CONTEXT_R15_OFFSET = 0xF0
CONTEXT_RIP_OFFSET = 0xF8

# Exception record offsets (for x64 EXCEPTION_RECORD structure)
EXCEPTION_CODE_OFFSET = 0x00
EXCEPTION_FLAGS_OFFSET = 0x04
EXCEPTION_RECORD_OFFSET = 0x08
EXCEPTION_ADDRESS_OFFSET = 0x10
EXCEPTION_NUM_PARAMS_OFFSET = 0x18
EXCEPTION_PARAMS_OFFSET = 0x20


@dataclass
class RegisterState:
    """CPU register state at time of crash."""
    rax: int = 0
    rbx: int = 0
    rcx: int = 0
    rdx: int = 0
    rsi: int = 0
    rdi: int = 0
    rsp: int = 0  # Stack pointer
    rbp: int = 0  # Base pointer
    rip: int = 0  # Instruction pointer
    r8: int = 0
    r9: int = 0
    r10: int = 0
    r11: int = 0
    r12: int = 0
    r13: int = 0
    r14: int = 0
    r15: int = 0
    context_flags: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary with hex values for JSON serialization."""
        return {
            "rax": f"0x{self.rax:016X}",
            "rbx": f"0x{self.rbx:016X}",
            "rcx": f"0x{self.rcx:016X}",
            "rdx": f"0x{self.rdx:016X}",
            "rsi": f"0x{self.rsi:016X}",
            "rdi": f"0x{self.rdi:016X}",
            "rsp": f"0x{self.rsp:016X}",
            "rbp": f"0x{self.rbp:016X}",
            "rip": f"0x{self.rip:016X}",
            "r8": f"0x{self.r8:016X}",
            "r9": f"0x{self.r9:016X}",
            "r10": f"0x{self.r10:016X}",
            "r11": f"0x{self.r11:016X}",
            "r12": f"0x{self.r12:016X}",
            "r13": f"0x{self.r13:016X}",
            "r14": f"0x{self.r14:016X}",
            "r15": f"0x{self.r15:016X}",
            "context_flags": f"0x{self.context_flags:08X}",
        }


@dataclass
class ExceptionInfo:
    """Exception information from the dump."""
    exception_code: int = 0
    exception_flags: int = 0
    exception_address: int = 0
    num_parameters: int = 0
    parameters: List[int] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []
    
    def get_exception_name(self) -> str:
        """Get a human-readable name for the exception code."""
        exceptions = {
            0xC0000005: "ACCESS_VIOLATION",
            0xC000001D: "ILLEGAL_INSTRUCTION",
            0xC0000025: "NONCONTINUABLE_EXCEPTION",
            0xC0000026: "INVALID_DISPOSITION",
            0xC000008C: "ARRAY_BOUNDS_EXCEEDED",
            0xC000008D: "FLOAT_DENORMAL_OPERAND",
            0xC000008E: "FLOAT_DIVIDE_BY_ZERO",
            0xC000008F: "FLOAT_INEXACT_RESULT",
            0xC0000090: "FLOAT_INVALID_OPERATION",
            0xC0000091: "FLOAT_OVERFLOW",
            0xC0000092: "FLOAT_STACK_CHECK",
            0xC0000093: "FLOAT_UNDERFLOW",
            0xC0000094: "INTEGER_DIVIDE_BY_ZERO",
            0xC0000095: "INTEGER_OVERFLOW",
            0xC0000096: "PRIVILEGED_INSTRUCTION",
            0xC00000FD: "STACK_OVERFLOW",
            0xC0000409: "STACK_BUFFER_OVERRUN",
            0xC0000420: "ASSERTION_FAILURE",
            0x80000003: "BREAKPOINT",
            0x80000004: "SINGLE_STEP",
        }
        return exceptions.get(self.exception_code, f"UNKNOWN_0x{self.exception_code:08X}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "exception_code": f"0x{self.exception_code:08X}",
            "exception_code_int": self.exception_code,
            "exception_name": self.get_exception_name(),
            "exception_flags": f"0x{self.exception_flags:08X}",
            "exception_address": f"0x{self.exception_address:016X}",
            "num_parameters": self.num_parameters,
            "parameters": [f"0x{p:016X}" for p in self.parameters],
        }


@dataclass
class RawStackFrame:
    """A raw stack frame (without symbol resolution)."""
    address: int
    return_address: int = 0
    offset: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "address": f"0x{self.address:016X}",
            "return_address": f"0x{self.return_address:016X}" if self.return_address else None,
            "offset": self.offset,
        }


@dataclass
class StackTrace:
    """Stack trace information from the dump."""
    registers: Optional[RegisterState] = None
    exception: Optional[ExceptionInfo] = None
    raw_frames: List[RawStackFrame] = None
    stack_pointer: int = 0
    instruction_pointer: int = 0
    has_context: bool = False
    has_exception: bool = False
    note: str = ""
    
    def __post_init__(self):
        if self.raw_frames is None:
            self.raw_frames = []
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "has_context": self.has_context,
            "has_exception": self.has_exception,
            "stack_pointer": f"0x{self.stack_pointer:016X}" if self.stack_pointer else None,
            "instruction_pointer": f"0x{self.instruction_pointer:016X}" if self.instruction_pointer else None,
            "registers": self.registers.to_dict() if self.registers else None,
            "exception": self.exception.to_dict() if self.exception else None,
            "raw_frames": [f.to_dict() for f in self.raw_frames],
            "raw_frame_count": len(self.raw_frames),
            "note": self.note,
        }


class StackTraceParser:
    """Parser for stack trace information from dump files."""
    
    # Exception record offset in DUMP_HEADER64 (after standard headers)
    # This is at offset 0x348 in the DUMP_HEADER64 structure
    EXCEPTION_RECORD_OFFSET_IN_HEADER = 0x348
    CONTEXT_RECORD_OFFSET_IN_HEADER = 0x408
    
    def __init__(self, dump_path: str):
        """
        Initialize the stack trace parser.
        
        Args:
            dump_path: Path to the dump file
        """
        self.dump_path = dump_path
        self._file = None
        self._header = None
    
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
    
    def parse_registers(self) -> Optional[RegisterState]:
        """
        Parse CPU register state from context record.
        
        Returns:
            RegisterState with CPU registers, or None if not available
        """
        if not self._file:
            return None
        
        try:
            # The context record is embedded in the dump header
            ctx_base = self.CONTEXT_RECORD_OFFSET_IN_HEADER
            
            registers = RegisterState(
                context_flags=self._read_uint32(ctx_base + CONTEXT_FLAGS_OFFSET),
                rax=self._read_uint64(ctx_base + CONTEXT_RAX_OFFSET),
                rcx=self._read_uint64(ctx_base + CONTEXT_RCX_OFFSET),
                rdx=self._read_uint64(ctx_base + CONTEXT_RDX_OFFSET),
                rbx=self._read_uint64(ctx_base + CONTEXT_RBX_OFFSET),
                rsp=self._read_uint64(ctx_base + CONTEXT_RSP_OFFSET),
                rbp=self._read_uint64(ctx_base + CONTEXT_RBP_OFFSET),
                rsi=self._read_uint64(ctx_base + CONTEXT_RSI_OFFSET),
                rdi=self._read_uint64(ctx_base + CONTEXT_RDI_OFFSET),
                r8=self._read_uint64(ctx_base + CONTEXT_R8_OFFSET),
                r9=self._read_uint64(ctx_base + CONTEXT_R9_OFFSET),
                r10=self._read_uint64(ctx_base + CONTEXT_R10_OFFSET),
                r11=self._read_uint64(ctx_base + CONTEXT_R11_OFFSET),
                r12=self._read_uint64(ctx_base + CONTEXT_R12_OFFSET),
                r13=self._read_uint64(ctx_base + CONTEXT_R13_OFFSET),
                r14=self._read_uint64(ctx_base + CONTEXT_R14_OFFSET),
                r15=self._read_uint64(ctx_base + CONTEXT_R15_OFFSET),
                rip=self._read_uint64(ctx_base + CONTEXT_RIP_OFFSET),
            )
            
            return registers
            
        except Exception as e:
            print(f"Error parsing registers: {e}")
            return None
    
    def parse_exception(self) -> Optional[ExceptionInfo]:
        """
        Parse exception record from dump header.
        
        Returns:
            ExceptionInfo with exception details, or None if not available
        """
        if not self._file:
            return None
        
        try:
            exc_base = self.EXCEPTION_RECORD_OFFSET_IN_HEADER
            
            exception_code = self._read_uint32(exc_base + EXCEPTION_CODE_OFFSET)
            exception_flags = self._read_uint32(exc_base + EXCEPTION_FLAGS_OFFSET)
            exception_address = self._read_uint64(exc_base + EXCEPTION_ADDRESS_OFFSET)
            num_params = self._read_uint32(exc_base + EXCEPTION_NUM_PARAMS_OFFSET)
            
            # Read exception parameters (up to 15 parameters, each 8 bytes)
            params = []
            if num_params > 0 and num_params <= 15:
                for i in range(num_params):
                    param = self._read_uint64(exc_base + EXCEPTION_PARAMS_OFFSET + (i * 8))
                    params.append(param)
            
            return ExceptionInfo(
                exception_code=exception_code,
                exception_flags=exception_flags,
                exception_address=exception_address,
                num_parameters=num_params,
                parameters=params,
            )
            
        except Exception as e:
            print(f"Error parsing exception: {e}")
            return None
    
    def parse_stack_trace(self) -> StackTrace:
        """
        Parse stack trace from dump file.
        
        Note: Full stack walking requires symbol resolution which needs
        debug symbols (PDB files) and is beyond the scope of this tool.
        We extract the raw context and any available stack frames.
        
        Returns:
            StackTrace with available information
        """
        registers = self.parse_registers()
        exception = self.parse_exception()
        
        # Check if we got valid data
        has_context = registers is not None and registers.context_flags != 0
        has_exception = exception is not None and exception.exception_code != 0
        
        stack_ptr = registers.rsp if registers else 0
        instr_ptr = registers.rip if registers else 0
        
        # For raw stack frames, we would need to walk the stack
        # This requires knowing the stack base and reading memory
        # For MVP, we'll note that full stack walking needs symbols
        raw_frames = []
        
        note = ""
        if not has_context:
            note = "Context record not found or invalid. "
        if not has_exception:
            note += "No exception record. This may be a live dump or the exception was not captured."
        else:
            note = "Full stack trace requires debug symbols (PDBs). Raw register state captured."
        
        return StackTrace(
            registers=registers if has_context else None,
            exception=exception if has_exception else None,
            raw_frames=raw_frames,
            stack_pointer=stack_ptr,
            instruction_pointer=instr_ptr,
            has_context=has_context,
            has_exception=has_exception,
            note=note,
        )


def parse_stack_trace(dump_path: str) -> StackTrace:
    """
    Convenience function to parse stack trace from a dump file.
    
    Args:
        dump_path: Path to the dump file
    
    Returns:
        StackTrace with parsed information
    """
    with StackTraceParser(dump_path) as parser:
        return parser.parse_stack_trace()
