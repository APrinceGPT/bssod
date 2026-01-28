"""
AI Prompt Engineering Module

Formats prompts for the AI analysis service.
"""

from ..models.schemas import AnalysisDataModel


# System prompt for the AI
SYSTEM_PROMPT = """You are an expert Windows crash dump analyst with deep knowledge of:
- Windows kernel internals and memory management
- Common BSOD (Blue Screen of Death) error codes and their causes
- Driver development and compatibility issues
- Hardware and software troubleshooting

Your task is to analyze Windows memory dump data and provide:
1. A clear explanation of what caused the crash
2. The most likely root cause
3. Specific actionable steps to fix the issue
4. Prevention recommendations

Be concise but thorough. Use technical terms when appropriate but explain them for users who may not be experts.
Format your response in clear sections with headers."""


def format_analysis_prompt(data: AnalysisDataModel) -> str:
    """
    Format the analysis data into a prompt for the AI.
    
    Args:
        data: The parsed analysis data from the memory dump
    
    Returns:
        Formatted prompt string
    """
    sections = []
    
    # Header
    sections.append("# Windows Memory Dump Analysis Request\n")
    
    # System Information
    if data.system_info:
        sections.append(_format_system_info(data))
    
    # Crash Summary
    if data.crash_summary:
        sections.append(_format_crash_summary(data))
    
    # Bugcheck Analysis
    if data.bugcheck_analysis:
        sections.append(_format_bugcheck_analysis(data))
    
    # Stack Trace
    if data.stack_trace:
        sections.append(_format_stack_trace(data))
    
    # Drivers
    if data.drivers:
        sections.append(_format_drivers(data))
    
    # Analysis Request
    sections.append(_format_request())
    
    return "\n".join(sections)


def _format_system_info(data: AnalysisDataModel) -> str:
    """Format system information section."""
    info = data.system_info
    lines = ["## System Information"]
    
    if info.dump_type:
        lines.append(f"- Dump Type: {info.dump_type}")
    
    if info.os_version:
        lines.append(f"- OS Version: {info.os_version}")
    
    if info.architecture:
        lines.append(f"- Architecture: {info.architecture}")
    
    if info.processor_count:
        lines.append(f"- Processors: {info.processor_count}")
    
    if info.dump_size_human:
        lines.append(f"- Dump Size: {info.dump_size_human}")
    elif info.dump_size_bytes:
        size_gb = info.dump_size_bytes / (1024 * 1024 * 1024)
        lines.append(f"- Dump Size: {size_gb:.2f} GB")
    
    lines.append("")
    return "\n".join(lines)


def _format_crash_summary(data: AnalysisDataModel) -> str:
    """Format crash summary section."""
    summary = data.crash_summary
    lines = [
        "## Crash Summary",
        f"- Bug Check Code: {summary.bugcheck_code}",
        f"- Bug Check Name: {summary.bugcheck_name}",
    ]
    
    # Include parameters
    params = [
        summary.parameter1,
        summary.parameter2,
        summary.parameter3,
        summary.parameter4,
    ]
    params_str = ", ".join([p for p in params if p and p != "0x0"])
    if params_str:
        lines.append(f"- Parameters: {params_str}")
    
    if summary.file_name:
        lines.append(f"- Dump File: {summary.file_name}")
    
    lines.append("")
    return "\n".join(lines)


def _format_bugcheck_analysis(data: AnalysisDataModel) -> str:
    """Format bugcheck analysis section."""
    analysis = data.bugcheck_analysis
    lines = ["## Bugcheck Analysis"]
    
    if analysis.code_hex:
        lines.append(f"- Code: {analysis.code_hex}")
    elif analysis.code:
        lines.append(f"- Code: 0x{analysis.code:X}")
    
    if analysis.name:
        lines.append(f"- Name: {analysis.name}")
    
    if analysis.description:
        lines.append(f"- Description: {analysis.description}")
    
    if analysis.category:
        lines.append(f"- Category: {analysis.category}")
    
    if analysis.severity:
        lines.append(f"- Severity: {analysis.severity}")
    
    if analysis.likely_causes:
        lines.append("- Likely Causes:")
        for cause in analysis.likely_causes[:5]:  # Limit to 5
            lines.append(f"  - {cause}")
    
    if analysis.recommendations:
        lines.append("- Recommendations:")
        for rec in analysis.recommendations[:5]:
            lines.append(f"  - {rec}")
    
    lines.append("")
    return "\n".join(lines)


def _format_stack_trace(data: AnalysisDataModel) -> str:
    """Format stack trace section."""
    stack = data.stack_trace
    lines = ["## Stack Trace"]
    
    if stack.note:
        lines.append(f"Note: {stack.note}")
    
    if stack.instruction_pointer:
        lines.append(f"- Instruction Pointer: {stack.instruction_pointer}")
    
    if stack.stack_pointer:
        lines.append(f"- Stack Pointer: {stack.stack_pointer}")
    
    if stack.exception:
        lines.append("### Exception Info:")
        exc = stack.exception
        if isinstance(exc, dict):
            for key, value in exc.items():
                lines.append(f"  - {key}: {value}")
    
    if stack.raw_frames:
        lines.append(f"### Stack Frames ({stack.raw_frame_count or len(stack.raw_frames)} frames):")
        for i, frame in enumerate(stack.raw_frames[:10], 1):  # Limit to top 10
            if isinstance(frame, dict):
                addr = frame.get("address", "Unknown")
                data_val = frame.get("data", "")
                lines.append(f"{i}. {addr}: {data_val}")
            else:
                lines.append(f"{i}. {frame}")
    
    lines.append("")
    return "\n".join(lines)


def _format_drivers(data: AnalysisDataModel) -> str:
    """Format drivers section."""
    drivers = data.drivers
    lines = ["## Driver Information"]
    
    if drivers.total_count:
        lines.append(f"- Total Drivers: {drivers.total_count}")
    
    if drivers.microsoft_count is not None:
        lines.append(f"- Microsoft Drivers: {drivers.microsoft_count}")
    
    if drivers.third_party_count is not None:
        lines.append(f"- Third-Party Drivers: {drivers.third_party_count}")
    
    if drivers.problematic_count:
        lines.append(f"- Problematic Drivers: {drivers.problematic_count}")
    
    if drivers.extraction_method:
        lines.append(f"- Extraction Method: {drivers.extraction_method}")
    
    if drivers.problematic_drivers:
        lines.append("### Problematic Drivers (Potential Issues):")
        for driver in drivers.problematic_drivers[:10]:  # Limit to 10
            if isinstance(driver, dict):
                name = driver.get("name", "Unknown")
                reason = driver.get("problematic_reason", "")
                if reason:
                    lines.append(f"- {name}: {reason}")
                else:
                    lines.append(f"- {name}")
            else:
                lines.append(f"- {driver}")
    
    if drivers.note:
        lines.append(f"\nNote: {drivers.note}")
    
    lines.append("")
    return "\n".join(lines)


def _format_request() -> str:
    """Format the analysis request section."""
    return """## Analysis Request

Please analyze this Windows crash dump data and provide:

1. **Root Cause Analysis**: What caused this crash? Explain the bugcheck code and its implications.

2. **Detailed Explanation**: Provide context about what was happening when the crash occurred based on the stack trace and driver information.

3. **Fix Recommendations**: List specific steps the user should take to resolve this issue, ordered by likelihood of success.

4. **Prevention Tips**: How can the user prevent this type of crash in the future?

5. **Additional Notes**: Any other relevant information or warnings the user should be aware of."""


def get_system_prompt() -> str:
    """Get the system prompt for the AI."""
    return SYSTEM_PROMPT
