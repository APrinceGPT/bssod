"""
Chat Models and Schemas

Defines the data models for the interactive chat feature.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Role of the message sender."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    role: MessageRole = Field(..., description="Who sent this message")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="When the message was sent")


class ConversationContext(BaseModel):
    """
    Context for a chat conversation.
    
    Contains the original crash analysis data and conversation history
    to maintain context across follow-up questions.
    """
    session_id: str = Field(..., description="Unique session identifier")
    bugcheck_code: Optional[str] = Field(None, description="Original bugcheck code")
    bugcheck_name: Optional[str] = Field(None, description="Original bugcheck name")
    dump_file: Optional[str] = Field(None, description="Original dump file name")
    analysis_summary: Optional[str] = Field(None, description="Executive summary from original analysis")
    messages: List[ChatMessage] = Field(default_factory=list, description="Conversation history")
    created_at: datetime = Field(default_factory=datetime.now, description="When session was created")
    
    @property
    def message_count(self) -> int:
        """Get the number of messages in the conversation."""
        return len(self.messages)
    
    def add_message(self, role: MessageRole, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append(ChatMessage(role=role, content=content))
    
    def get_history_for_ai(self, max_messages: int = 10) -> List[dict]:
        """
        Get conversation history formatted for AI API.
        
        Args:
            max_messages: Maximum number of messages to include (most recent)
            
        Returns:
            List of message dicts with role and content
        """
        recent_messages = self.messages[-max_messages:] if len(self.messages) > max_messages else self.messages
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in recent_messages
        ]


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""
    session_id: str = Field(..., description="Session ID from the original analysis")
    message: str = Field(..., min_length=1, max_length=2000, description="User's question or message")


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""
    success: bool = True
    session_id: str = Field(..., description="Session ID for continuity")
    response: str = Field(..., description="AI's response to the user's question")
    message_count: int = Field(..., description="Total messages in conversation")


class ChatErrorResponse(BaseModel):
    """Error response from the chat endpoint."""
    success: bool = False
    error_code: str = Field(..., description="Error code")
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional details")


class StartChatRequest(BaseModel):
    """Request to start a new chat session with analysis context."""
    bugcheck_code: Optional[str] = Field(None, description="Bugcheck code from analysis")
    bugcheck_name: Optional[str] = Field(None, description="Bugcheck name from analysis")
    dump_file: Optional[str] = Field(None, description="Dump file name")
    analysis_summary: Optional[str] = Field(None, description="Executive summary from AI analysis")


class StartChatResponse(BaseModel):
    """Response when starting a new chat session."""
    success: bool = True
    session_id: str = Field(..., description="New session ID for chat")
    message: str = Field(default="Chat session started. You can now ask follow-up questions about the analysis.")
