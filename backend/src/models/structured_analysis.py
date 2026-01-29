"""
Structured AI Analysis Response Models

Defines the expected JSON structure from AI analysis for rich UI rendering.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class RootCauseAnalysis(BaseModel):
    """Root cause analysis of the crash."""
    title: str = Field(..., description="Short title summarizing the root cause")
    explanation: str = Field(..., description="Detailed explanation of what caused the crash")
    affected_component: Optional[str] = Field(None, description="The driver, process, or component that caused the issue")
    technical_details: Optional[str] = Field(None, description="Low-level technical details for advanced users")


class FixStep(BaseModel):
    """A single fix step recommendation."""
    step: int = Field(..., description="Step number")
    priority: str = Field(..., description="Priority level: high, medium, or low")
    action: str = Field(..., description="Short action title")
    details: str = Field(..., description="Detailed instructions on how to perform this step")


class StructuredAnalysis(BaseModel):
    """
    Complete structured AI analysis response.
    
    This model defines the JSON structure that the AI should return
    for rich UI rendering with severity badges, confidence meters,
    and organized content sections.
    """
    # Severity and confidence
    severity: str = Field(..., description="Severity level: critical, high, medium, or low")
    confidence: int = Field(..., ge=0, le=100, description="Confidence percentage 0-100")
    
    # Summary for non-technical users
    executive_summary: str = Field(..., description="Simple 1-2 sentence explanation for non-technical users")
    
    # Root cause analysis
    root_cause: RootCauseAnalysis = Field(..., description="Detailed root cause analysis")
    
    # Fix recommendations
    fix_steps: List[FixStep] = Field(..., description="Ordered list of fix steps")
    
    # Prevention tips
    prevention_tips: List[str] = Field(..., description="Tips to prevent this issue in the future")
    
    # Additional info
    additional_notes: Optional[str] = Field(None, description="Any other relevant information or warnings")
    related_bugchecks: Optional[List[str]] = Field(None, description="Related bugcheck codes that may have similar causes")


class StructuredAIAnalysisResult(BaseModel):
    """
    AI analysis result with structured data for rich UI rendering.
    
    Contains both the parsed structured analysis and metadata about the AI call.
    """
    structured_analysis: StructuredAnalysis = Field(..., description="Parsed structured analysis")
    model: Optional[str] = Field(None, description="Model used for analysis")
    tokens_used: Optional[int] = Field(None, description="Total tokens used")
    prompt_tokens: Optional[int] = Field(None, description="Prompt tokens used")
    completion_tokens: Optional[int] = Field(None, description="Completion tokens used")


class AIAnalysisError(BaseModel):
    """Error response when AI analysis fails."""
    success: bool = False
    error_code: str = Field(..., description="Error code for the failure")
    error_message: str = Field(..., description="Human-readable error message")
    raw_response: Optional[str] = Field(None, description="Raw AI response if available for debugging")
