"use client";

import { useState, useRef, useEffect } from "react";
import { 
  Send, 
  MessageCircle, 
  User, 
  Bot, 
  Loader2, 
  Minimize2 
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";
import { ChatMessage, ChatState, StartChatRequest } from "@/types";
import { startChatSession, sendChatMessage, ApiError } from "@/lib/api";
import { MarkdownRenderer } from "./markdown-renderer";

interface FloatingChatProps {
  /**
   * Analysis context to start the chat with.
   * Should contain bugcheck_code, bugcheck_name, dump_file, and analysis_summary.
   */
  analysisContext: StartChatRequest;
}

/**
 * Floating chat button with slide-out drawer for AI assistant.
 * Persists across tab navigation and provides quick access to chat.
 */
export function FloatingChat({ analysisContext }: FloatingChatProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [chatState, setChatState] = useState<ChatState>({
    sessionId: null,
    messages: [],
    isLoading: false,
    error: null,
  });
  const [inputMessage, setInputMessage] = useState("");
  const [isInitializing, setIsInitializing] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
      // Clear unread count when drawer is open
      setUnreadCount(0);
    }
  }, [chatState.messages, isOpen]);

  // Focus input when drawer opens with active session
  useEffect(() => {
    if (isOpen && chatState.sessionId && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen, chatState.sessionId]);

  // Track unread messages when drawer is closed
  useEffect(() => {
    if (!isOpen && chatState.messages.length > 0) {
      const lastMessage = chatState.messages[chatState.messages.length - 1];
      if (lastMessage.role === "assistant") {
        setUnreadCount(prev => prev + 1);
      }
    }
  }, [chatState.messages, isOpen]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputMessage(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 100) + "px";
  };

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

  const sendMessage = async () => {
    if (!inputMessage.trim() || !chatState.sessionId || chatState.isLoading) {
      return;
    }

    const userMessage: ChatMessage = {
      role: "user",
      content: inputMessage.trim(),
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));
    setInputMessage("");
    
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

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <Sheet open={isOpen} onOpenChange={setIsOpen}>
        <SheetTrigger asChild>
          <Button
            size="lg"
            className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg z-50"
            aria-label="Open AI Chat Assistant"
          >
            <MessageCircle className="h-6 w-6" />
            {unreadCount > 0 && (
              <Badge 
                variant="destructive" 
                className="absolute -top-1 -right-1 h-5 w-5 p-0 flex items-center justify-center text-xs"
              >
                {unreadCount}
              </Badge>
            )}
          </Button>
        </SheetTrigger>

        <SheetContent 
          side="right" 
          className="w-full sm:w-[420px] flex flex-col p-0"
        >
          <SheetHeader className="px-4 py-3 border-b shrink-0">
            <div className="flex items-center justify-between">
              <SheetTitle className="flex items-center gap-2">
                <Bot className="h-5 w-5 text-primary" />
                AI Assistant
              </SheetTitle>
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={() => setIsOpen(false)}
                className="h-8 w-8"
              >
                <Minimize2 className="h-4 w-4" />
              </Button>
            </div>
          </SheetHeader>

          <div className="flex-1 flex flex-col min-h-0">
            {/* Chat Content */}
            {!chatState.sessionId ? (
              <ChatStartPrompt 
                isInitializing={isInitializing}
                error={chatState.error}
                onStart={initializeChat}
              />
            ) : (
              <ChatMessagesArea
                messages={chatState.messages}
                isLoading={chatState.isLoading}
                error={chatState.error}
                messagesEndRef={messagesEndRef}
              />
            )}

            {/* Input Area - Only show when session is active */}
            {chatState.sessionId && (
              <ChatInputArea
                inputMessage={inputMessage}
                isLoading={chatState.isLoading}
                inputRef={inputRef}
                onInputChange={handleInputChange}
                onKeyDown={handleKeyDown}
                onSend={sendMessage}
              />
            )}
          </div>
        </SheetContent>
      </Sheet>
    </>
  );
}

/**
 * Initial prompt to start chat session
 */
function ChatStartPrompt({ 
  isInitializing, 
  error, 
  onStart 
}: { 
  isInitializing: boolean; 
  error: string | null;
  onStart: () => void;
}) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
      <div className="bg-primary/10 rounded-full p-4 mb-4">
        <MessageCircle className="h-8 w-8 text-primary" />
      </div>
      <h3 className="font-semibold mb-2">Have Questions?</h3>
      <p className="text-sm text-muted-foreground mb-4">
        Ask follow-up questions about the crash analysis.
      </p>
      <Button 
        onClick={onStart} 
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
      {error && (
        <p className="text-sm text-destructive mt-3">{error}</p>
      )}
    </div>
  );
}

/**
 * Messages display area
 */
function ChatMessagesArea({
  messages,
  isLoading,
  error,
  messagesEndRef,
}: {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
}) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3">
      {messages.length === 0 && (
        <div className="text-center py-8">
          <p className="text-sm text-muted-foreground">
            Ask any questions about the crash analysis.
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Examples: &quot;What does this error mean?&quot;
          </p>
        </div>
      )}
      
      {messages.map((message, index) => (
        <ChatBubble key={index} message={message} />
      ))}
      
      {isLoading && (
        <div className="flex items-center gap-2 text-muted-foreground text-sm">
          <Bot className="h-4 w-4" />
          <Loader2 className="h-4 w-4 animate-spin" />
          <span>Thinking...</span>
        </div>
      )}

      {error && (
        <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md">
          {error}
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
}

/**
 * Chat input area
 */
function ChatInputArea({
  inputMessage,
  isLoading,
  inputRef,
  onInputChange,
  onKeyDown,
  onSend,
}: {
  inputMessage: string;
  isLoading: boolean;
  inputRef: React.RefObject<HTMLTextAreaElement | null>;
  onInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onKeyDown: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  onSend: () => void;
}) {
  return (
    <div className="border-t p-4 shrink-0">
      <div className="flex gap-2">
        <textarea
          ref={inputRef}
          value={inputMessage}
          onChange={onInputChange}
          onKeyDown={onKeyDown}
          placeholder="Type your question..."
          disabled={isLoading}
          rows={1}
          className="flex-1 min-h-10 max-h-24 resize-none rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
        />
        <Button
          onClick={onSend}
          disabled={!inputMessage.trim() || isLoading}
          size="icon"
          className="shrink-0"
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </Button>
      </div>
      <p className="text-xs text-muted-foreground text-center mt-2">
        Enter to send, Shift+Enter for new line
      </p>
    </div>
  );
}

/**
 * Single chat message bubble
 */
function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  
  return (
    <div className={`flex gap-2 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="shrink-0 h-7 w-7 rounded-full bg-primary/10 flex items-center justify-center">
          <Bot className="h-3.5 w-3.5 text-primary" />
        </div>
      )}
      
      <div
        className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
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
        <div className="shrink-0 h-7 w-7 rounded-full bg-secondary flex items-center justify-center">
          <User className="h-3.5 w-3.5" />
        </div>
      )}
    </div>
  );
}
