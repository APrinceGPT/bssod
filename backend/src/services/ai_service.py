"""
AI Service Module

Handles communication with the AI API (Claude 4 Sonnet via Trend Micro).
"""

import httpx

from ..config import get_settings
from ..models.schemas import AnalysisDataModel, AIAnalysisResult
from .prompt_engineering import format_analysis_prompt, get_system_prompt


class AIServiceError(Exception):
    """Raised when AI service encounters an error."""
    pass


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
    
    async def analyze(self, data: AnalysisDataModel) -> AIAnalysisResult:
        """
        Analyze crash dump data using the AI.
        
        Args:
            data: Parsed analysis data from memory dump
        
        Returns:
            AIAnalysisResult with the analysis
        
        Raises:
            AIServiceError: If the API call fails
        """
        # Format the prompt
        user_prompt = format_analysis_prompt(data)
        system_prompt = get_system_prompt()
        
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
    
    def _parse_response(self, result: dict) -> AIAnalysisResult:
        """Parse the API response into an AIAnalysisResult."""
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
            
            return AIAnalysisResult(
                analysis=content,
                model=result.get("model", self.model),
                tokens_used=usage.get("total_tokens"),
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens")
            )
            
        except KeyError as e:
            raise AIServiceError(f"Unexpected API response format: missing {e}")
    
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
