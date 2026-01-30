/**
 * API Service for BSSOD Frontend
 * 
 * Handles all communication with the backend API.
 */

import { 
  AnalyzeResponse, 
  HealthResponse,
  StartChatRequest,
  StartChatResponse,
  ChatRequest,
  ChatResponse
} from "@/types";
import { API_CONFIG } from "@/lib/constants";
import { getUserFriendlyError, formatErrorMessage } from "@/lib/error-messages";

class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: string
  ) {
    super(message);
    this.name = "ApiError";
  }

  /**
   * Get a user-friendly version of this error
   */
  getUserFriendlyMessage(): string {
    const friendlyError = getUserFriendlyError(this.message, this.statusCode);
    return formatErrorMessage(friendlyError);
  }
}

/**
 * Check if the backend API is healthy
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/health`, {
    method: "GET",
    headers: {
      "Accept": "application/json",
    },
  });

  if (!response.ok) {
    throw new ApiError(
      "Health check failed",
      response.status,
      await response.text()
    );
  }

  return response.json();
}

/**
 * Upload a ZIP file for analysis
 */
export async function analyzeFile(
  file: File,
  onProgress?: (progress: number) => void
): Promise<AnalyzeResponse> {
  // Create form data
  const formData = new FormData();
  formData.append("file", file);

  // Use XMLHttpRequest for progress tracking
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable && onProgress) {
        const percentComplete = Math.round((event.loaded / event.total) * 40);
        onProgress(percentComplete);
      }
    });

    xhr.addEventListener("load", () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText);
          resolve(response);
        } catch {
          const error = new ApiError("Failed to parse server response", xhr.status);
          reject(error);
        }
      } else {
        let errorMessage = "Analysis failed";
        try {
          const errorResponse = JSON.parse(xhr.responseText);
          errorMessage = errorResponse.detail || errorResponse.error || errorMessage;
        } catch {
          errorMessage = xhr.statusText || errorMessage;
        }
        const error = new ApiError(errorMessage, xhr.status);
        reject(error);
      }
    });

    xhr.addEventListener("error", () => {
      const error = new ApiError("Network error - could not connect to server", 0);
      reject(error);
    });

    xhr.addEventListener("timeout", () => {
      const error = new ApiError("Request timed out", 0);
      reject(error);
    });

    xhr.open("POST", `${API_CONFIG.BASE_URL}/api/v1/analyze`);
    xhr.timeout = API_CONFIG.TIMEOUT_MS;
    xhr.send(formData);
  });
}

// ============================================================================
// Chat API Functions (Phase AI-3: Interactive Chat)
// ============================================================================

/**
 * Start a new chat session with crash analysis context
 */
export async function startChatSession(
  context: StartChatRequest
): Promise<StartChatResponse> {
  const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/chat/start`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify(context),
  });

  if (!response.ok) {
    let errorMessage = "Failed to start chat session";
    try {
      const errorData = await response.json();
      errorMessage = errorData.error || errorMessage;
    } catch {
      // Ignore parse errors
    }
    throw new ApiError(errorMessage, response.status);
  }

  return response.json();
}

/**
 * Send a message to the chat and get a response
 */
export async function sendChatMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    let errorMessage = "Failed to send message";
    try {
      const errorData = await response.json();
      errorMessage = errorData.error || errorMessage;
    } catch {
      // Ignore parse errors
    }
    throw new ApiError(errorMessage, response.status);
  }

  return response.json();
}

export { ApiError };
