"""
AI Service Module

Handles communication with the AI API (Claude 4 Sonnet via Trend Micro).
"""

import json
import re
import httpx

from ..config import get_settings
from ..models.schemas import AnalysisDataModel, AIAnalysisResult
from ..models.structured_analysis import (
    StructuredAnalysis,
    StructuredAIAnalysisResult,
    AIAnalysisError as StructuredAIError
)
from .prompt_engineering import format_analysis_prompt, get_system_prompt


class AIServiceError(Exception):
    """Raised when AI service encounters an error."""
    pass


class JSONParseError(AIServiceError):
    """Raised when AI response is not valid JSON."""
    def __init__(self, message: str, raw_response: str = None):
        super().__init__(message)
        self.raw_response = raw_response


class AIService:
    """Service for interacting with the AI API."""
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout: float = 120.0
    ):
        """
        Initialize the AI service.
        
        Args:
            base_url: Base URL for the AI API
            api_key: API key for authentication
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
    
    async def analyze(self, data: AnalysisDataModel) -> StructuredAIAnalysisResult:
        """
        Analyze crash dump data using the AI.
        
        Args:
            data: Parsed analysis data from memory dump
        
        Returns:
            StructuredAIAnalysisResult with parsed JSON analysis
        
        Raises:
            AIServiceError: If the API call fails
            JSONParseError: If the response is not valid JSON
        """
        # Format the prompt with category-specific guidance
        user_prompt = format_analysis_prompt(data)
        system_prompt = get_system_prompt(data)  # Pass data for category detection
        
        # Prepare the request
        request_body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.3  # Lower temperature for more focused analysis
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Make the API call
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=request_body,
                    headers=headers
                )
                
                if response.status_code != 200:
                    error_detail = self._parse_error(response)
                    raise AIServiceError(
                        f"AI API returned status {response.status_code}: {error_detail}"
                    )
                
                result = response.json()
                return self._parse_response(result)
                
        except httpx.TimeoutException:
            raise AIServiceError(
                f"AI API request timed out after {self.timeout} seconds"
            )
        except httpx.RequestError as e:
            raise AIServiceError(f"Failed to connect to AI API: {e}")
    
    def _parse_response(self, result: dict) -> StructuredAIAnalysisResult:
        """Parse the API response into a StructuredAIAnalysisResult with JSON parsing."""
        try:
            choices = result.get("choices", [])
            if not choices:
                raise AIServiceError("No response choices returned from AI API")
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            if not content:
                raise AIServiceError("Empty response content from AI API")
            
            # Extract usage information
            usage = result.get("usage", {})
            
            # Parse the JSON response from AI
            structured_analysis = self._parse_json_response(content)
            
            return StructuredAIAnalysisResult(
                structured_analysis=structured_analysis,
                model=result.get("model", self.model),
                tokens_used=usage.get("total_tokens"),
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens")
            )
            
        except KeyError as e:
            raise AIServiceError(f"Unexpected API response format: missing {e}")
    
    def _parse_json_response(self, content: str) -> StructuredAnalysis:
        """
        Parse the AI response content as JSON into a StructuredAnalysis.
        
        Args:
            content: Raw response content from the AI
        
        Returns:
            Parsed StructuredAnalysis object
        
        Raises:
            JSONParseError: If the response is not valid JSON or doesn't match schema
        """
        # Clean up the content - remove any markdown code blocks if present
        cleaned_content = content.strip()
        
        # Remove markdown code blocks if the AI wrapped it
        if cleaned_content.startswith("```"):
            # Find the end of the opening fence
            first_newline = cleaned_content.find("\n")
            if first_newline != -1:
                cleaned_content = cleaned_content[first_newline + 1:]
            # Remove closing fence
            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content[:-3].strip()
        
        # Try to extract JSON from content if it's mixed with text
        json_match = re.search(r'\{[\s\S]*\}', cleaned_content)
        if json_match:
            cleaned_content = json_match.group()
        
        try:
            parsed_json = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            raise JSONParseError(
                f"AI response is not valid JSON: {e}",
                raw_response=content
            )
        
        # Validate and parse into Pydantic model
        try:
            return StructuredAnalysis.model_validate(parsed_json)
        except Exception as e:
            raise JSONParseError(
                f"AI response doesn't match expected schema: {e}",
                raw_response=content
            )
    
    def _parse_error(self, response: httpx.Response) -> str:
        """Parse error details from a failed response."""
        try:
            error_json = response.json()
            if "error" in error_json:
                error = error_json["error"]
                if isinstance(error, dict):
                    return error.get("message", str(error))
                return str(error)
            return response.text[:500]
        except Exception:
            return response.text[:500]
    
    async def chat(
        self,
        messages: list[dict],
        system_prompt: str
    ) -> str:
        """
        Send a chat conversation to the AI and get a response.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: System prompt with context
        
        Returns:
            AI response content as string
        
        Raises:
            AIServiceError: If the API call fails
        """
        # Build the full message list with system prompt
        full_messages = [{"role": "system", "content": system_prompt}]
        full_messages.extend(messages)
        
        request_body = {
            "model": self.model,
            "messages": full_messages,
            "max_tokens": 2048,  # Shorter for chat responses
            "temperature": 0.5  # Slightly higher for conversational tone
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=request_body,
                    headers=headers
                )
                
                if response.status_code != 200:
                    error_detail = self._parse_error(response)
                    raise AIServiceError(
                        f"AI API returned status {response.status_code}: {error_detail}"
                    )
                
                result = response.json()
                return self._extract_chat_response(result)
                
        except httpx.TimeoutException:
            raise AIServiceError(
                f"AI API request timed out after {self.timeout} seconds"
            )
        except httpx.RequestError as e:
            raise AIServiceError(f"Failed to connect to AI API: {e}")
    
    def _extract_chat_response(self, result: dict) -> str:
        """Extract the response content from a chat API response."""
        try:
            choices = result.get("choices", [])
            if not choices:
                raise AIServiceError("No response choices returned from AI API")
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            if not content:
                raise AIServiceError("Empty response content from AI API")
            
            return content
            
        except KeyError as e:
            raise AIServiceError(f"Unexpected API response format: missing {e}")

    async def health_check(self) -> bool:
        """
        Check if the AI service is reachable.
        
        Returns:
            True if the service is healthy
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Try a minimal request to check connectivity
                await client.get(
                    self.base_url,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                # Any response (even 404) means the service is reachable
                return True
        except Exception:
            return False


def create_ai_service() -> AIService:
    """
    Create an AIService instance from settings.
    
    Returns:
        Configured AIService instance
    """
    settings = get_settings()
    
    return AIService(
        base_url=settings.ai.base_url,
        api_key=settings.ai.api_key,
        model=settings.ai.model,
        timeout=settings.ai.timeout
    )
