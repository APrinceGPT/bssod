"""
Conversation Service

Manages chat sessions and conversation context for follow-up questions.
Uses in-memory storage for session data (suitable for single-instance deployment).
"""

import uuid
from typing import Optional, Dict
from datetime import datetime, timedelta

from ..models.chat_models import (
    ConversationContext,
    MessageRole,
    ChatMessage,
)


class ConversationStore:
    """
    In-memory store for conversation sessions.
    
    Note: This is suitable for single-instance deployment.
    For multi-instance deployment, consider Redis or database storage.
    """
    
    def __init__(self, max_sessions: int = 1000, session_ttl_hours: int = 24):
        """
        Initialize the conversation store.
        
        Args:
            max_sessions: Maximum number of sessions to keep in memory
            session_ttl_hours: Hours until a session expires
        """
        self._sessions: Dict[str, ConversationContext] = {}
        self._max_sessions = max_sessions
        self._session_ttl = timedelta(hours=session_ttl_hours)
    
    def create_session(
        self,
        bugcheck_code: Optional[str] = None,
        bugcheck_name: Optional[str] = None,
        dump_file: Optional[str] = None,
        analysis_summary: Optional[str] = None,
    ) -> ConversationContext:
        """
        Create a new conversation session.
        
        Args:
            bugcheck_code: Bugcheck code from original analysis
            bugcheck_name: Bugcheck name from original analysis
            dump_file: Original dump file name
            analysis_summary: Executive summary from AI analysis
            
        Returns:
            New ConversationContext with unique session ID
        """
        # Clean up old sessions if we're at capacity
        if len(self._sessions) >= self._max_sessions:
            self._cleanup_old_sessions()
        
        session_id = str(uuid.uuid4())
        context = ConversationContext(
            session_id=session_id,
            bugcheck_code=bugcheck_code,
            bugcheck_name=bugcheck_name,
            dump_file=dump_file,
            analysis_summary=analysis_summary,
        )
        
        self._sessions[session_id] = context
        return context
    
    def get_session(self, session_id: str) -> Optional[ConversationContext]:
        """
        Get an existing conversation session.
        
        Args:
            session_id: The session ID to look up
            
        Returns:
            ConversationContext if found and not expired, None otherwise
        """
        context = self._sessions.get(session_id)
        if context is None:
            return None
        
        # Check if session has expired
        if datetime.now() - context.created_at > self._session_ttl:
            del self._sessions[session_id]
            return None
        
        return context
    
    def update_session(self, context: ConversationContext) -> None:
        """
        Update a session in the store.
        
        Args:
            context: The updated ConversationContext
        """
        self._sessions[context.session_id] = context
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: The session ID to delete
            
        Returns:
            True if session was deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
    
    def _cleanup_old_sessions(self) -> int:
        """
        Remove expired sessions.
        
        Returns:
            Number of sessions removed
        """
        now = datetime.now()
        expired_ids = [
            sid for sid, ctx in self._sessions.items()
            if now - ctx.created_at > self._session_ttl
        ]
        
        for sid in expired_ids:
            del self._sessions[sid]
        
        # If still at capacity, remove oldest sessions
        if len(self._sessions) >= self._max_sessions:
            sorted_sessions = sorted(
                self._sessions.items(),
                key=lambda x: x[1].created_at
            )
            # Remove oldest 10%
            to_remove = max(1, len(sorted_sessions) // 10)
            for sid, _ in sorted_sessions[:to_remove]:
                del self._sessions[sid]
                expired_ids.append(sid)
        
        return len(expired_ids)
    
    @property
    def session_count(self) -> int:
        """Get the current number of active sessions."""
        return len(self._sessions)


# Global conversation store instance
_conversation_store: Optional[ConversationStore] = None


def get_conversation_store() -> ConversationStore:
    """
    Get the global conversation store instance.
    
    Creates the store on first call (lazy initialization).
    
    Returns:
        ConversationStore instance
    """
    global _conversation_store
    if _conversation_store is None:
        _conversation_store = ConversationStore()
    return _conversation_store


# Chat system prompt for follow-up questions
CHAT_SYSTEM_PROMPT = """You are a helpful Windows crash dump analysis assistant. 
You are continuing a conversation about a BSOD (Blue Screen of Death) crash analysis.

Context from the original analysis:
{context}

Your role is to:
1. Answer follow-up questions about the crash analysis
2. Explain technical terms in simple language when asked
3. Provide more detailed instructions for fix steps when requested
4. Clarify any part of the analysis the user doesn't understand
5. Suggest additional diagnostic steps if helpful

Be helpful, clear, and concise. If you don't have enough information to answer a question,
say so and suggest what additional information might help.

Keep responses focused and practical. Users are trying to fix their computer issues."""


def build_chat_system_prompt(context: ConversationContext) -> str:
    """
    Build the system prompt for a chat conversation.
    
    Args:
        context: The conversation context with crash analysis info
        
    Returns:
        Formatted system prompt
    """
    context_parts = []
    
    if context.bugcheck_code:
        context_parts.append(f"- Bugcheck Code: {context.bugcheck_code}")
    
    if context.bugcheck_name:
        context_parts.append(f"- Bugcheck Name: {context.bugcheck_name}")
    
    if context.dump_file:
        context_parts.append(f"- Dump File: {context.dump_file}")
    
    if context.analysis_summary:
        context_parts.append(f"- Analysis Summary: {context.analysis_summary}")
    
    if not context_parts:
        context_str = "No specific crash context available."
    else:
        context_str = "\n".join(context_parts)
    
    return CHAT_SYSTEM_PROMPT.format(context=context_str)
