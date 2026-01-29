/**
 * Type definitions for BSSOD Frontend
 * 
 * These types match the backend API response schemas.
 */

// ============================================================================
// Analysis Data Types (from Parser Tool output via Backend)
// ============================================================================

export interface SystemInfo {
  os_version?: string;
  architecture?: string;
  processor_count?: number;
  dump_type?: string;
  dump_size_bytes?: number;
  dump_size_human?: string;
  is_64bit?: boolean;
  crash_time_raw?: number;
}

export interface CrashSummary {
  bugcheck_code?: string;
  bugcheck_code_int?: number;
  bugcheck_name?: string;
  parameter1?: string;
  parameter2?: string;
  parameter3?: string;
  parameter4?: string;
  file_path?: string;
  file_name?: string;
}

export interface BugcheckParameter {
  parameter_number?: number;
  raw_value?: number;
  hex_value?: string;
  description?: string;
  interpretation?: string;
}

export interface BugcheckAnalysis {
  code?: number;
  code_hex?: string;
  name?: string;
  category?: string;
  description?: string;
  parameters?: BugcheckParameter[];
  recommendations?: string[];
  likely_causes?: string[];
  severity?: string;
}

/**
 * CPU register values from the crash context.
 * Keys are register names (e.g., "rax", "rbx", "rsp", "rip").
 * Values are hex string representations of register contents.
 */
export interface RegisterValues {
  [registerName: string]: string | number | undefined;
}

/**
 * Exception record from the crash dump.
 */
export interface ExceptionRecord {
  code?: number;
  code_hex?: string;
  flags?: number;
  address?: string;
  parameters?: (string | number)[];
  description?: string;
}

/**
 * Raw stack frame information.
 */
export interface RawStackFrame {
  index?: number;
  return_address?: string;
  stack_address?: string;
  instruction_pointer?: string;
  module?: string;
  function_name?: string;
  offset?: string;
}

export interface StackTrace {
  has_context?: boolean;
  has_exception?: boolean;
  stack_pointer?: string;
  instruction_pointer?: string;
  registers?: RegisterValues;
  exception?: ExceptionRecord;
  raw_frames?: RawStackFrame[];
  raw_frame_count?: number;
  note?: string;
}

export interface Driver {
  name?: string;
  base_address?: string;
  size?: number;
  size_human?: string;
  path?: string;
  timestamp?: number;
  timestamp_human?: string;
  version?: string;
  is_microsoft?: boolean;
  is_problematic?: boolean;
  problematic_reason?: string;
}

export interface DriversInfo {
  total_count?: number;
  microsoft_count?: number;
  third_party_count?: number;
  problematic_count?: number;
  extraction_method?: string;
  note?: string;
  drivers?: Driver[];
  problematic_drivers?: Driver[];
}

export interface Metadata {
  tool_name: string;
  tool_version?: string;
  analysis_timestamp?: string;
  analysis_duration_seconds?: number;
  dump_file?: {
    path?: string;
    name?: string;
    size_bytes?: number;
    size_human?: string;
  };
  dump_filename?: string;
  parser_notes?: string[];
}

// ============================================================================
// API Response Types
// ============================================================================

export interface AIAnalysisResult {
  analysis: string;
  model?: string;
  tokens_used?: number;
  prompt_tokens?: number;
  completion_tokens?: number;
}

export interface AnalyzeResponse {
  success: boolean;
  message: string;
  dump_file?: string;
  bugcheck_code?: string;
  bugcheck_name?: string;
  ai_analysis?: AIAnalysisResult;
}

export interface ErrorResponse {
  success: boolean;
  error: string;
  details?: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  ai_service_available: boolean;
}

// ============================================================================
// Application State Types
// ============================================================================

export type AnalysisStatus = "idle" | "uploading" | "analyzing" | "complete" | "error";

export interface AnalysisState {
  status: AnalysisStatus;
  progress: number;
  fileName?: string;
  result?: AnalyzeResponse;
  error?: string;
}
