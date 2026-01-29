"use client";

import { useCallback, useState } from "react";
import { Upload, FileArchive, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { UPLOAD_CONFIG } from "@/lib/constants";

interface FileValidationError {
  type: "size" | "type";
  message: string;
}

interface FileDropzoneProps {
  onFileSelect: (file: File) => void;
  onValidationError?: (error: FileValidationError) => void;
  disabled?: boolean;
  acceptedTypes?: string[];
  maxSizeBytes?: number;
}

export function FileDropzone({ 
  onFileSelect, 
  onValidationError,
  disabled = false,
  acceptedTypes = [".zip"],
  maxSizeBytes = UPLOAD_CONFIG.MAX_FILE_SIZE_BYTES
}: FileDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [validationError, setValidationError] = useState<FileValidationError | null>(null);

  const validateAndSelectFile = useCallback((file: File) => {
    // Clear previous error
    setValidationError(null);

    // Check file type first
    if (!validateFileType(file, acceptedTypes)) {
      const error: FileValidationError = {
        type: "type",
        message: `Invalid file type. Please upload a ${acceptedTypes.join(" or ")} file.`
      };
      setValidationError(error);
      onValidationError?.(error);
      return;
    }

    // Check file size
    if (file.size > maxSizeBytes) {
      const maxSizeMB = maxSizeBytes / (1024 * 1024);
      const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
      const error: FileValidationError = {
        type: "size",
        message: `File is too large (${fileSizeMB} MB). Maximum allowed size is ${maxSizeMB} MB.`
      };
      setValidationError(error);
      onValidationError?.(error);
      return;
    }

    // File is valid
    onFileSelect(file);
  }, [acceptedTypes, maxSizeBytes, onFileSelect, onValidationError]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) {
      setIsDragging(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      validateAndSelectFile(file);
    }
  }, [disabled, validateAndSelectFile]);

  const handleClick = useCallback(() => {
    if (disabled) return;

    const input = document.createElement("input");
    input.type = "file";
    input.accept = acceptedTypes.join(",");
    input.onchange = (e) => {
      const target = e.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        const file = target.files[0];
        validateAndSelectFile(file);
      }
    };
    input.click();
  }, [disabled, acceptedTypes, validateAndSelectFile]);

  return (
    <div className="space-y-3">
      <div
        onClick={handleClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "relative flex flex-col items-center justify-center p-12 border-2 border-dashed rounded-lg transition-colors cursor-pointer",
          isDragging && "border-primary bg-primary/5",
          !isDragging && !validationError && "border-muted-foreground/25 hover:border-primary/50",
          validationError && "border-destructive/50 bg-destructive/5",
          disabled && "opacity-50 cursor-not-allowed"
        )}
      >
        <div className="flex flex-col items-center text-center">
          {isDragging ? (
            <FileArchive className="h-12 w-12 text-primary mb-4" />
          ) : validationError ? (
            <AlertCircle className="h-12 w-12 text-destructive mb-4" />
          ) : (
            <Upload className="h-12 w-12 text-muted-foreground mb-4" />
          )}
          <p className="text-lg font-medium mb-1">
            {isDragging ? "Drop your file here" : "Drag and drop your ZIP file"}
          </p>
          <p className="text-sm text-muted-foreground">
            or click to browse
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            Accepts: {acceptedTypes.join(", ")} (max {maxSizeBytes / (1024 * 1024)} MB)
          </p>
        </div>
      </div>
      {validationError && (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
          <AlertCircle className="h-4 w-4 flex-shrink-0" />
          <span>{validationError.message}</span>
        </div>
      )}
    </div>
  );
}

function validateFileType(file: File, acceptedTypes: string[]): boolean {
  const fileName = file.name.toLowerCase();
  return acceptedTypes.some(type => fileName.endsWith(type.toLowerCase()));
}
