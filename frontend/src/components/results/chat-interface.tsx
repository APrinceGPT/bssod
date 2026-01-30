"use client";

import { useState, useRef, useEffect } from "react";
import { Send, MessageCircle, User, Bot, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ChatMessage, ChatState, StartChatRequest } from "@/types";
import { startChatSession, sendChatMessage, ApiError } from "@/lib/api";
import { MarkdownRenderer } from "./markdown-renderer";

interface ChatInterfaceProps {
  /**
   * Analysis context to start the chat with.
   * Should contain bugcheck_code, bugcheck_name, dump_file, and analysis_summary.
   */
  analysisContext: StartChatRequest;
}

/**
 * Interactive chat interface for follow-up questions about crash analysis.
 * Allows users to ask clarifying questions about the AI's analysis.
 */
export function ChatInterface({ analysisContext }: ChatInterfaceProps) {
  const [chatState, setChatState] = useState<ChatState>({
    sessionId: null,
    messages: [],
    isLoading: false,
    error: null,
  });
  const [inputMessage, setInputMessage] = useState("");
  const [isInitializing, setIsInitializing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatState.messages]);

  // Auto-resize textarea
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputMessage(e.target.value);
    // Reset height to auto to get the correct scrollHeight
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
  };

  /**
   * Start a new chat session
   */
  const initializeChat = async () => {
    setIsInitializing(true);
    setChatState(prev => ({ ...prev, error: null }));

    try {
      const response = await startChatSession(analysisContext);
      
      if (response.success) {
        setChatState(prev => ({
          ...prev,
          sessionId: response.session_id,
          messages: [],
          error: null,
        }));
      } else {
        setChatState(prev => ({
          ...prev,
          error: "Failed to start chat session",
        }));
      }
    } catch (err) {
      const errorMessage = err instanceof ApiError 
        ? err.getUserFriendlyMessage() 
        : "Failed to connect to chat service";
      setChatState(prev => ({
        ...prev,
        error: errorMessage,
      }));
    } finally {
      setIsInitializing(false);
    }
  };

  /**
   * Send a message to the chat
   */
  const sendMessage = async () => {
    if (!inputMessage.trim() || !chatState.sessionId || chatState.isLoading) {
      return;
    }

    const userMessage: ChatMessage = {
      role: "user",
      content: inputMessage.trim(),
    };

    // Add user message immediately
    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));
    setInputMessage("");
    
    // Reset textarea height
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
    }

    try {
      const response = await sendChatMessage({
        session_id: chatState.sessionId,
        message: userMessage.content,
      });

      if (response.success) {
        const assistantMessage: ChatMessage = {
          role: "assistant",
          content: response.response,
        };

        setChatState(prev => ({
          ...prev,
          messages: [...prev.messages, assistantMessage],
          isLoading: false,
        }));
      } else {
        setChatState(prev => ({
          ...prev,
          isLoading: false,
          error: "Failed to get response",
        }));
      }
    } catch (err) {
      const errorMessage = err instanceof ApiError 
        ? err.getUserFriendlyMessage() 
        : "Failed to send message";
      setChatState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  };

  /**
   * Handle keyboard shortcuts
   */
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // If no session, show start button
  if (!chatState.sessionId) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <MessageCircle className="h-5 w-5 text-primary" />
            Have Questions?
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center space-y-4">
            <p className="text-sm text-muted-foreground">
              Need clarification about the analysis? Start a chat to ask follow-up questions.
            </p>
            <Button 
              onClick={initializeChat} 
              disabled={isInitializing}
              className="gap-2"
            >
              {isInitializing ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Starting...
                </>
              ) : (
                <>
                  <MessageCircle className="h-4 w-4" />
                  Start Chat
                </>
              )}
            </Button>
            {chatState.error && (
              <p className="text-sm text-destructive">{chatState.error}</p>
            )}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <MessageCircle className="h-5 w-5 text-primary" />
          Chat with AI Assistant
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Messages Area */}
        <div className="max-h-96 overflow-y-auto space-y-3 p-1">
          {chatState.messages.length === 0 && (
            <div className="text-center py-8">
              <p className="text-sm text-muted-foreground">
                Ask any questions about the crash analysis above.
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Examples: &quot;What does this error code mean?&quot; or &quot;How do I perform step 2?&quot;
              </p>
            </div>
          )}
          
          {chatState.messages.map((message, index) => (
            <ChatMessageBubble key={index} message={message} />
          ))}
          
          {chatState.isLoading && (
            <div className="flex items-center gap-2 text-muted-foreground text-sm">
              <Bot className="h-4 w-4" />
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Thinking...</span>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Error Display */}
        {chatState.error && (
          <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md">
            {chatState.error}
          </div>
        )}

        {/* Input Area */}
        <div className="flex gap-2">
          <textarea
            ref={inputRef}
            value={inputMessage}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your question..."
            disabled={chatState.isLoading}
            rows={1}
            className="flex-1 min-h-[40px] max-h-[120px] resize-none rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          />
          <Button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || chatState.isLoading}
            size="icon"
            className="shrink-0"
          >
            {chatState.isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
        
        <p className="text-xs text-muted-foreground text-center">
          Press Enter to send, Shift+Enter for new line
        </p>
      </CardContent>
    </Card>
  );
}

/**
 * Single chat message bubble component
 */
function ChatMessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  
  return (
    <div className={`flex gap-2 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="shrink-0 h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
          <Bot className="h-4 w-4 text-primary" />
        </div>
      )}
      
      <div
        className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-muted"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <MarkdownRenderer content={message.content} />
        )}
      </div>
      
      {isUser && (
        <div className="shrink-0 h-8 w-8 rounded-full bg-secondary flex items-center justify-center">
          <User className="h-4 w-4" />
        </div>
      )}
    </div>
  );
}
