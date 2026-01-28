"""
Test script to verify dump file parsing works with the sample dump files.
"""

import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser.dump_reader import DumpFileReader
from parser.header import parse_dump_header
from parser.bugcheck import analyze_bugcheck
from parser.stack_trace import parse_stack_trace
from parser.drivers import extract_drivers
from parser.analyzer import analyze_dump
from utils.constants import get_bugcheck_name, format_bugcheck_code


def test_dump_reader():
    """Test the DumpFileReader with the sample dump file."""
    dump_path = r"d:\AI Project\MemoryDumper\MEMORY.DMP"
    
    if not os.path.exists(dump_path):
        print(f"ERROR: Dump file not found at {dump_path}")
        return False
    
    print(f"Testing DumpFileReader with: {dump_path}")
    print(f"File size: {os.path.getsize(dump_path) / (1024**3):.2f} GB")
    
    try:
        with DumpFileReader(dump_path) as reader:
            print("\nParsing dump header...")
            header = reader.parse_header()
            
            print("\n" + "=" * 60)
            print("DUMP FILE INFORMATION")
            print("=" * 60)
            print(f"Signature:       {header.signature}{header.valid_dump}")
            print(f"Is 64-bit:       {header.is_64bit}")
            print(f"Dump Type:       {header.get_dump_type_name()}")
            print(f"Architecture:    {header.get_machine_type_name()}")
            print(f"Processors:      {header.number_processors}")
            print(f"Windows Version: {header.major_version}.{header.minor_version}")
            
            print("\n" + "-" * 60)
            print("BUGCHECK INFORMATION")
            print("-" * 60)
            bugcheck_name = get_bugcheck_name(header.bugcheck_code)
            bugcheck_hex = format_bugcheck_code(header.bugcheck_code)
            print(f"Bugcheck Code:   {bugcheck_hex}")
            print(f"Bugcheck Name:   {bugcheck_name}")
            print(f"Parameter 1:     0x{header.bugcheck_param1:016X}")
            print(f"Parameter 2:     0x{header.bugcheck_param2:016X}")
            print(f"Parameter 3:     0x{header.bugcheck_param3:016X}")
            print(f"Parameter 4:     0x{header.bugcheck_param4:016X}")
            
            print("\n" + "=" * 60)
            print("✅ Dump file parsed successfully!")
            print("=" * 60)
            return True
            
    except Exception as e:
        print(f"\n❌ Error parsing dump file: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_header_parser():
    """Test the high-level HeaderParser."""
    dump_path = r"d:\AI Project\MemoryDumper\MEMORY.DMP"
    
    print("\n" + "=" * 60)
    print("TESTING HeaderParser")
    print("=" * 60)
    
    system_info, crash_summary = parse_dump_header(dump_path)
    
    if system_info and crash_summary:
        print("\nSystem Info (JSON):")
        print(json.dumps(system_info.to_dict(), indent=2))
        
        print("\nCrash Summary (JSON):")
        print(json.dumps(crash_summary.to_dict(), indent=2))
        
        print("\n✅ HeaderParser test successful!")
        return True, crash_summary
    else:
        print("❌ HeaderParser test failed!")
        return False, None


def test_bugcheck_analyzer(crash_summary):
    """Test the BugcheckAnalyzer with data from the dump."""
    print("\n" + "=" * 60)
    print("TESTING BugcheckAnalyzer")
    print("=" * 60)
    
    if not crash_summary:
        print("❌ No crash summary available!")
        return False
    
    # Get the bugcheck info from crash summary
    analysis = analyze_bugcheck(
        crash_summary.bugcheck_code_int,
        int(crash_summary.parameter1, 16),
        int(crash_summary.parameter2, 16),
        int(crash_summary.parameter3, 16),
        int(crash_summary.parameter4, 16),
    )
    
    print(f"\nBugcheck: {analysis.name} ({analysis.code_hex})")
    print(f"Category: {analysis.category}")
    print(f"Severity: {analysis.severity}")
    print(f"Description: {analysis.description}")
    
    print("\nParameter Analysis:")
    for p in analysis.parameters:
        print(f"  Parameter {p.parameter_number}: {p.hex_value}")
        print(f"    Description: {p.description}")
        if p.interpretation:
            print(f"    Interpretation: {p.interpretation}")
    
    print("\nLikely Causes:")
    for cause in analysis.likely_causes:
        print(f"  • {cause}")
    
    print("\nRecommendations:")
    for rec in analysis.recommendations:
        print(f"  → {rec}")
    
    print("\nFull Analysis (JSON):")
    print(json.dumps(analysis.to_dict(), indent=2))
    
    print("\n✅ BugcheckAnalyzer test successful!")
    return True


def test_stack_trace_parser():
    """Test the StackTraceParser."""
    dump_path = r"d:\AI Project\MemoryDumper\MEMORY.DMP"
    
    print("\n" + "=" * 60)
    print("TESTING StackTraceParser")
    print("=" * 60)
    
    stack = parse_stack_trace(dump_path)
    
    print(f"\nHas Context: {stack.has_context}")
    print(f"Has Exception: {stack.has_exception}")
    
    if stack.instruction_pointer:
        print(f"Instruction Pointer (RIP): 0x{stack.instruction_pointer:016X}")
    if stack.stack_pointer:
        print(f"Stack Pointer (RSP): 0x{stack.stack_pointer:016X}")
    
    if stack.registers:
        print("\nKey Registers:")
        print(f"  RAX: 0x{stack.registers.rax:016X}")
        print(f"  RBX: 0x{stack.registers.rbx:016X}")
        print(f"  RCX: 0x{stack.registers.rcx:016X}")
        print(f"  RDX: 0x{stack.registers.rdx:016X}")
        print(f"  RSP: 0x{stack.registers.rsp:016X}")
        print(f"  RBP: 0x{stack.registers.rbp:016X}")
        print(f"  RIP: 0x{stack.registers.rip:016X}")
    
    if stack.exception:
        print(f"\nException: {stack.exception.get_exception_name()}")
        print(f"  Code: 0x{stack.exception.exception_code:08X}")
        print(f"  Address: 0x{stack.exception.exception_address:016X}")
    
    if stack.note:
        print(f"\nNote: {stack.note}")
    
    print("\nFull Stack Trace (JSON):")
    print(json.dumps(stack.to_dict(), indent=2))
    
    print("\n✅ StackTraceParser test successful!")
    return True


def test_driver_extractor():
    """Test the DriverListExtractor."""
    dump_path = r"d:\AI Project\MemoryDumper\MEMORY.DMP"
    
    print("\n" + "=" * 60)
    print("TESTING DriverListExtractor")
    print("=" * 60)
    
    result = extract_drivers(dump_path)
    
    print(f"\nTotal drivers found: {result.total_count}")
    print(f"Microsoft drivers: {result.microsoft_count}")
    print(f"Third-party drivers: {result.third_party_count}")
    print(f"Potentially problematic: {result.problematic_count}")
    print(f"Extraction method: {result.extraction_method}")
    
    if result.note:
        print(f"\nNote: {result.note}")
    
    if result.drivers:
        print("\nDrivers found:")
        for driver in result.drivers[:20]:  # Show first 20
            status = ""
            if driver.is_problematic:
                status = " ⚠️ PROBLEMATIC"
            elif driver.is_microsoft:
                status = " (Microsoft)"
            print(f"  {driver.name}{status}")
        
        if len(result.drivers) > 20:
            print(f"  ... and {len(result.drivers) - 20} more")
    
    if result.problematic_drivers:
        print("\n⚠️ Potentially Problematic Drivers:")
        for driver in result.problematic_drivers:
            print(f"  • {driver.name}: {driver.problematic_reason}")
    
    print("\nDriver Result (JSON - summary):")
    summary = {
        "total_count": result.total_count,
        "microsoft_count": result.microsoft_count,
        "third_party_count": result.third_party_count,
        "problematic_count": result.problematic_count,
        "extraction_method": result.extraction_method,
        "note": result.note,
    }
    print(json.dumps(summary, indent=2))
    
    print("\n✅ DriverListExtractor test successful!")
    return True


def test_complete_analyzer():
    """Test the complete DumpAnalyzer with ZIP export."""
    dump_path = r"d:\AI Project\MemoryDumper\MEMORY.DMP"
    output_dir = r"d:\AI Project\MemoryDumper\parser-tool\output"
    
    print("\n" + "=" * 60)
    print("TESTING Complete DumpAnalyzer with ZIP Export")
    print("=" * 60)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Run the complete analysis
    analysis, zip_path = analyze_dump(dump_path, create_zip=True, output_dir=output_dir)
    
    print(f"\nAnalysis completed: {analysis.success}")
    print(f"Duration: {analysis.metadata.analysis_duration_seconds:.2f} seconds")
    
    if analysis.metadata.parser_notes:
        print("\nParser Notes:")
        for note in analysis.metadata.parser_notes:
            print(f"  • {note}")
    
    if zip_path:
        print(f"\n📦 ZIP file created: {zip_path}")
        print(f"   Size: {os.path.getsize(zip_path) / 1024:.2f} KB")
        
        # Show ZIP contents
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zf:
            print("\n   ZIP Contents:")
            for name in zf.namelist():
                info = zf.getinfo(name)
                print(f"     - {name} ({info.file_size / 1024:.2f} KB)")
    
    # Show summary
    print("\n" + "-" * 60)
    print("ANALYSIS SUMMARY")
    print("-" * 60)
    
    if analysis.system_info:
        print(f"System: {analysis.system_info.os_version} ({analysis.system_info.architecture})")
    
    if analysis.crash_summary:
        print(f"Crash: {analysis.crash_summary.bugcheck_name} ({analysis.crash_summary.bugcheck_code})")
    
    if analysis.bugcheck_analysis:
        print(f"Category: {analysis.bugcheck_analysis.category}")
        print(f"Severity: {analysis.bugcheck_analysis.severity}")
    
    print("\n✅ Complete DumpAnalyzer test successful!")
    return True


if __name__ == "__main__":
    success1 = test_dump_reader()
    success2, crash_summary = test_header_parser()
    success3 = test_bugcheck_analyzer(crash_summary)
    success4 = test_stack_trace_parser()
    success5 = test_driver_extractor()
    success6 = test_complete_analyzer()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    tests = [
        ("DumpFileReader", success1),
        ("HeaderParser", success2),
        ("BugcheckAnalyzer", success3),
        ("StackTraceParser", success4),
        ("DriverListExtractor", success5),
        ("Complete Analyzer + ZIP", success6),
    ]
    for name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {name}: {status}")
    
    all_success = all(s for _, s in tests)
    print("\n" + ("✅ All tests passed!" if all_success else "❌ Some tests failed!"))
    sys.exit(0 if all_success else 1)
