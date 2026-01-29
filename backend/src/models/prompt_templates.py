"""
Specialized Prompt Templates Module

Provides category-specific system prompts and analysis guidance for AI.
Extends the base system prompt with specialized focus areas.
"""

from .bugcheck_categories import BugcheckCategory, CategoryConfig, get_category_config


# Base JSON structure requirement (shared across all categories)
BASE_JSON_STRUCTURE = """
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
"""


def _build_category_prompt(category: BugcheckCategory) -> str:
    """
    Build the specialized system prompt for a bugcheck category.
    
    Args:
        category: The BugcheckCategory to build prompt for
        
    Returns:
        Complete system prompt with category-specific guidance
    """
    config = get_category_config(category)
    
    # Build focus areas section
    focus_areas = "\n".join(f"  - {area}" for area in config.focus_areas)
    
    # Build key questions section
    key_questions = "\n".join(f"  - {q}" for q in config.key_questions)
    
    # Build common fixes section
    common_fixes = "\n".join(f"  - {fix}" for fix in config.common_fixes)
    
    prompt = f"""You are an expert Windows crash dump analyst specializing in {config.name}.

**Crash Category:** {config.name}
**Description:** {config.description}

Your deep expertise includes:
- Windows kernel internals and memory management
- Device driver development and debugging
- Hardware diagnostics and firmware analysis
- BSOD troubleshooting and root cause analysis

**SPECIALIZED FOCUS AREAS for this crash type:**
{focus_areas}

**KEY QUESTIONS to answer:**
{key_questions}

**COMMON FIXES for this category:**
{common_fixes}

Prioritize your analysis based on the specialized focus areas above.
When the crash matches known patterns, increase confidence.
When providing fix steps, prioritize the common fixes for this category.
{BASE_JSON_STRUCTURE}
Be concise but thorough. Provide actionable fix steps ordered by priority."""

    return prompt


# Pre-built prompts for each category (avoids rebuilding on each request)
CATEGORY_PROMPTS = {
    category: _build_category_prompt(category) 
    for category in BugcheckCategory
}


def get_specialized_prompt(category: BugcheckCategory) -> str:
    """
    Get the specialized system prompt for a bugcheck category.
    
    Args:
        category: The BugcheckCategory
        
    Returns:
        Specialized system prompt string
    """
    return CATEGORY_PROMPTS[category]


def get_category_analysis_request(category: BugcheckCategory) -> str:
    """
    Get the specialized analysis request section for a category.
    
    Args:
        category: The BugcheckCategory
        
    Returns:
        Analysis request text with category-specific guidance
    """
    config = get_category_config(category)
    
    # Format key questions as numbered list
    questions = "\n".join(f"{i+1}. {q}" for i, q in enumerate(config.key_questions))
    
    return f"""## Analysis Request - {config.name}

This crash has been categorized as: **{config.name}**

Based on the crash data above, analyze this {config.description.lower()}

Please address these key questions in your analysis:
{questions}

Respond with ONLY valid JSON following the specified structure.
Focus your recommendations on fixes appropriate for {config.name.lower()} issues."""
