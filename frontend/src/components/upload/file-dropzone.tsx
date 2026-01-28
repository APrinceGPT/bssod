"use client";

import { useCallback, useState } from "react";
import { Upload, FileArchive } from "lucide-react";
import { cn } from "@/lib/utils";

interface FileDropzoneProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
  acceptedTypes?: string[];
}

export function FileDropzone({ 
  onFileSelect, 
  disabled = false,
  acceptedTypes = [".zip"] 
}: FileDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);

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
      if (validateFile(file, acceptedTypes)) {
        onFileSelect(file);
      }
    }
  }, [disabled, acceptedTypes, onFileSelect]);

  const handleClick = useCallback(() => {
    if (disabled) return;

    const input = document.createElement("input");
    input.type = "file";
    input.accept = acceptedTypes.join(",");
    input.onchange = (e) => {
      const target = e.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        const file = target.files[0];
        if (validateFile(file, acceptedTypes)) {
          onFileSelect(file);
        }
      }
    };
    input.click();
  }, [disabled, acceptedTypes, onFileSelect]);

  return (
    <div
      onClick={handleClick}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={cn(
        "relative flex flex-col items-center justify-center p-12 border-2 border-dashed rounded-lg transition-colors cursor-pointer",
        isDragging && "border-primary bg-primary/5",
        !isDragging && "border-muted-foreground/25 hover:border-primary/50",
        disabled && "opacity-50 cursor-not-allowed"
      )}
    >
      <div className="flex flex-col items-center text-center">
        {isDragging ? (
          <FileArchive className="h-12 w-12 text-primary mb-4" />
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
          Accepts: {acceptedTypes.join(", ")}
        </p>
      </div>
    </div>
  );
}

function validateFile(file: File, acceptedTypes: string[]): boolean {
  const fileName = file.name.toLowerCase();
  return acceptedTypes.some(type => fileName.endsWith(type.toLowerCase()));
}
