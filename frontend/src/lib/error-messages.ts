/**
 * Error Message Utilities
 * 
 * Provides user-friendly error messages for API and network errors.
 */

/**
 * Error codes for categorizing different error types
 */
export enum ErrorCode {
  // Network errors
  CONNECTION_REFUSED = "CONNECTION_REFUSED",
  NETWORK_ERROR = "NETWORK_ERROR",
  TIMEOUT = "TIMEOUT",
  
  // File validation errors
  INVALID_FILE_TYPE = "INVALID_FILE_TYPE",
  FILE_TOO_LARGE = "FILE_TOO_LARGE",
  MISSING_ANALYSIS_JSON = "MISSING_ANALYSIS_JSON",
  INVALID_ZIP = "INVALID_ZIP",
  
  // API errors
  AI_UNAVAILABLE = "AI_UNAVAILABLE",
  AI_TIMEOUT = "AI_TIMEOUT",
  SERVER_ERROR = "SERVER_ERROR",
  BAD_REQUEST = "BAD_REQUEST",
  
  // Generic
  UNKNOWN = "UNKNOWN",
}

/**
 * Structured error with user-friendly messaging
 */
export interface UserFriendlyError {
  code: ErrorCode;
  title: string;
  message: string;
  suggestion?: string;
}

/**
 * Maps API error messages to user-friendly versions
 */
const ERROR_MESSAGE_MAP: Record<string, UserFriendlyError> = {
  // Network errors
  "Network error - could not connect to server": {
    code: ErrorCode.CONNECTION_REFUSED,
    title: "Connection Failed",
    message: "Unable to connect to the analysis server.",
    suggestion: "Please ensure the backend server is running on port 8080.",
  },
  "Request timed out": {
    code: ErrorCode.TIMEOUT,
    title: "Request Timeout",
    message: "The analysis is taking longer than expected.",
    suggestion: "Please try again. If the issue persists, the file may be too complex.",
  },
  
  // File validation errors
  "File must be a ZIP archive": {
    code: ErrorCode.INVALID_FILE_TYPE,
    title: "Invalid File Type",
    message: "The uploaded file is not a ZIP archive.",
    suggestion: "Please upload the ZIP file exported from the BSSOD Parser Tool.",
  },
  "Missing required file: analysis.json": {
    code: ErrorCode.MISSING_ANALYSIS_JSON,
    title: "Invalid ZIP Contents",
    message: "The ZIP file does not contain the required analysis.json file.",
    suggestion: "Please ensure you're uploading a ZIP exported from the BSSOD Parser Tool.",
  },
  "Invalid ZIP file format": {
    code: ErrorCode.INVALID_ZIP,
    title: "Corrupted ZIP File",
    message: "The uploaded file appears to be corrupted or not a valid ZIP.",
    suggestion: "Try exporting the analysis again from the Parser Tool.",
  },
  
  // AI errors
  "AI API request timed out": {
    code: ErrorCode.AI_TIMEOUT,
    title: "AI Analysis Timeout",
    message: "The AI service took too long to respond.",
    suggestion: "Please try again. The AI service may be experiencing high load.",
  },
  "Failed to connect to AI API": {
    code: ErrorCode.AI_UNAVAILABLE,
    title: "AI Service Unavailable",
    message: "Unable to connect to the AI analysis service.",
    suggestion: "Please try again later. The AI service may be temporarily unavailable.",
  },
};

/**
 * Pattern-based error matching for partial matches
 */
const ERROR_PATTERNS: Array<{ pattern: RegExp; error: UserFriendlyError }> = [
  {
    pattern: /connection refused|ECONNREFUSED|net::ERR_CONNECTION_REFUSED/i,
    error: {
      code: ErrorCode.CONNECTION_REFUSED,
      title: "Connection Failed",
      message: "Unable to connect to the analysis server.",
      suggestion: "Please ensure the backend server is running on port 8080.",
    },
  },
  {
    pattern: /timeout|timed out/i,
    error: {
      code: ErrorCode.TIMEOUT,
      title: "Request Timeout",
      message: "The request took too long to complete.",
      suggestion: "Please try again. If the issue persists, check your network connection.",
    },
  },
  {
    pattern: /file too large|exceeds.*limit|max.*size/i,
    error: {
      code: ErrorCode.FILE_TOO_LARGE,
      title: "File Too Large",
      message: "The uploaded file exceeds the maximum allowed size.",
      suggestion: "Maximum file size is 50 MB. Please check your file.",
    },
  },
  {
    pattern: /AI.*fail|analysis.*fail|claude|openai/i,
    error: {
      code: ErrorCode.AI_UNAVAILABLE,
      title: "AI Analysis Failed",
      message: "The AI service encountered an error during analysis.",
      suggestion: "Please try again. If the issue persists, the service may be temporarily unavailable.",
    },
  },
  {
    pattern: /network|fetch|request/i,
    error: {
      code: ErrorCode.NETWORK_ERROR,
      title: "Network Error",
      message: "A network error occurred while processing your request.",
      suggestion: "Please check your internet connection and try again.",
    },
  },
];

/**
 * Convert a raw error message to a user-friendly error
 * 
 * @param rawMessage - The original error message from the API or network
 * @param statusCode - Optional HTTP status code
 * @returns A user-friendly error object
 */
export function getUserFriendlyError(
  rawMessage: string,
  statusCode?: number
): UserFriendlyError {
  // Check exact matches first
  if (ERROR_MESSAGE_MAP[rawMessage]) {
    return ERROR_MESSAGE_MAP[rawMessage];
  }

  // Check pattern matches
  for (const { pattern, error } of ERROR_PATTERNS) {
    if (pattern.test(rawMessage)) {
      return error;
    }
  }

  // Handle by status code
  if (statusCode) {
    if (statusCode === 0) {
      return {
        code: ErrorCode.NETWORK_ERROR,
        title: "Connection Error",
        message: "Could not connect to the server.",
        suggestion: "Please check if the backend server is running.",
      };
    }
    if (statusCode >= 400 && statusCode < 500) {
      return {
        code: ErrorCode.BAD_REQUEST,
        title: "Invalid Request",
        message: rawMessage || "The request could not be processed.",
        suggestion: "Please check the uploaded file and try again.",
      };
    }
    if (statusCode >= 500) {
      return {
        code: ErrorCode.SERVER_ERROR,
        title: "Server Error",
        message: "The server encountered an unexpected error.",
        suggestion: "Please try again later.",
      };
    }
  }

  // Default unknown error
  return {
    code: ErrorCode.UNKNOWN,
    title: "Error",
    message: rawMessage || "An unexpected error occurred.",
    suggestion: "Please try again. If the issue persists, contact support.",
  };
}

/**
 * Format a user-friendly error for display
 * 
 * @param error - The user-friendly error object
 * @returns Formatted string with message and suggestion
 */
export function formatErrorMessage(error: UserFriendlyError): string {
  if (error.suggestion) {
    return `${error.message} ${error.suggestion}`;
  }
  return error.message;
}
