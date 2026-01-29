"use client";

import { cn } from "@/lib/utils";
import { Gauge } from "lucide-react";

interface ConfidenceMeterProps {
  confidence: number;
  className?: string;
  showLabel?: boolean;
  size?: "sm" | "md" | "lg";
}

const getConfidenceLevel = (confidence: number) => {
  if (confidence >= 90) return { label: "Very High", color: "bg-green-500" };
  if (confidence >= 70) return { label: "High", color: "bg-blue-500" };
  if (confidence >= 50) return { label: "Moderate", color: "bg-yellow-500" };
  return { label: "Low", color: "bg-red-500" };
};

const sizeConfig = {
  sm: { height: "h-1.5", width: "w-24", text: "text-xs" },
  md: { height: "h-2", width: "w-32", text: "text-sm" },
  lg: { height: "h-3", width: "w-40", text: "text-base" },
};

export function ConfidenceMeter({
  confidence,
  className,
  showLabel = true,
  size = "md",
}: ConfidenceMeterProps) {
  const level = getConfidenceLevel(confidence);
  const config = sizeConfig[size];
  const clampedConfidence = Math.max(0, Math.min(100, confidence));

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <Gauge className="h-4 w-4 text-muted-foreground" />
      <div className="flex items-center gap-2">
        {/* Progress bar */}
        <div
          className={cn(
            "rounded-full bg-muted overflow-hidden",
            config.height,
            config.width
          )}
        >
          <div
            className={cn("h-full rounded-full transition-all duration-500", level.color)}
            style={{ width: `${clampedConfidence}%` }}
          />
        </div>
        {/* Percentage and label */}
        <span className={cn("font-medium text-foreground", config.text)}>
          {clampedConfidence}%
        </span>
        {showLabel && (
          <span className={cn("text-muted-foreground", config.text)}>
            ({level.label})
          </span>
        )}
      </div>
    </div>
  );
}
