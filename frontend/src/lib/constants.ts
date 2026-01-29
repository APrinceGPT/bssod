/**
 * Application Constants
 * 
 * Centralized configuration values used throughout the frontend.
 */

/**
 * File upload configuration
 */
export const UPLOAD_CONFIG = {
  /** Maximum file size in megabytes */
  MAX_FILE_SIZE_MB: 50,
  /** Maximum file size in bytes */
  MAX_FILE_SIZE_BYTES: 50 * 1024 * 1024,
  /** Accepted file types for upload */
  ACCEPTED_FILE_TYPES: [".zip"],
} as const;

/**
 * API configuration
 */
export const API_CONFIG = {
  /** Base URL for the backend API */
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080",
  /** Request timeout in milliseconds (2 minutes for AI analysis) */
  TIMEOUT_MS: 120000,
} as const;

/**
 * Progress tracking phases
 */
export const PROGRESS_PHASES = {
  /** Upload phase: 0-40% */
  UPLOAD_START: 0,
  UPLOAD_END: 40,
  /** Validation phase: 40-50% */
  VALIDATION_START: 40,
  VALIDATION_END: 50,
  /** AI Analysis phase: 50-90% */
  ANALYSIS_START: 50,
  ANALYSIS_END: 90,
  /** Completion phase: 90-100% */
  COMPLETE_START: 90,
  COMPLETE_END: 100,
} as const;

/**
 * Progress status messages for each phase
 */
export const PROGRESS_MESSAGES = {
  UPLOADING: "Uploading file...",
  VALIDATING: "Validating data...",
  ANALYZING: "AI is analyzing your crash dump...",
  PREPARING: "Preparing results...",
} as const;
