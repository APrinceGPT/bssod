"""
AI Prompt Engineering Module

Formats prompts for the AI analysis service.
"""

from ..models.schemas import AnalysisDataModel


# System prompt for the AI - requests structured JSON output
SYSTEM_PROMPT = """You are an expert Windows crash dump analyst with deep knowledge of:
- Windows kernel internals and memory management
- Common BSOD (Blue Screen of Death) error codes and their causes
- Driver development and compatibility issues
- Hardware and software troubleshooting

Your task is to analyze Windows memory dump data and provide a structured analysis.

CRITICAL: You MUST respond with ONLY valid JSON. No markdown, no explanations outside the JSON structure.

The JSON structure must be exactly:
{
  "severity": "critical" | "high" | "medium" | "low",
  "confidence": <number 0-100>,
  "executive_summary": "<1-2 sentence explanation for non-technical users>",
  "root_cause": {
    "title": "<short title summarizing root cause>",
    "explanation": "<detailed explanation of what caused the crash>",
    "affected_component": "<driver, process, or component that caused the issue>",
    "technical_details": "<low-level technical details for advanced users>"
  },
  "fix_steps": [
    {
      "step": <number>,
      "priority": "high" | "medium" | "low",
      "action": "<short action title>",
      "details": "<detailed instructions>"
    }
  ],
  "prevention_tips": ["<tip1>", "<tip2>", ...],
  "additional_notes": "<any other relevant information or warnings>",
  "related_bugchecks": ["<related bugcheck code 1>", ...]
}

Severity levels:
- critical: System cannot boot, data loss risk, hardware failure suspected
- high: Frequent crashes, driver issues, significant system instability
- medium: Occasional crashes, known software conflicts, manageable issues
- low: Rare occurrence, minor issues, easily fixable

Confidence levels:
- 90-100: Clear evidence, known issue pattern, high certainty
- 70-89: Strong indicators, likely cause identified
- 50-69: Multiple possible causes, needs further investigation
- 0-49: Limited data, speculative analysis

Be concise but thorough. Provide actionable fix steps ordered by priority."""


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

Analyze this Windows crash dump data and respond with a JSON object containing:

1. **severity**: Rate the severity (critical/high/medium/low) based on crash impact
2. **confidence**: Your confidence percentage (0-100) in the analysis
3. **executive_summary**: A simple 1-2 sentence summary for non-technical users
4. **root_cause**: Object with title, explanation, affected_component, and technical_details
5. **fix_steps**: Array of steps with step number, priority, action, and details
6. **prevention_tips**: Array of prevention recommendations
7. **additional_notes**: Any warnings or additional context
8. **related_bugchecks**: Array of related bugcheck codes (optional)

REMEMBER: Respond with ONLY valid JSON. No markdown formatting, no text outside the JSON."""


def get_system_prompt() -> str:
    """Get the system prompt for the AI."""
    return SYSTEM_PROMPT
