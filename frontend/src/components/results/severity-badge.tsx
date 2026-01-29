"use client";

import { AlertTriangle, AlertCircle, Info, CheckCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { SeverityLevel } from "@/types";

interface SeverityBadgeProps {
  severity: SeverityLevel;
  className?: string;
  showIcon?: boolean;
  size?: "sm" | "md" | "lg";
}

const severityConfig = {
  critical: {
    label: "Critical",
    icon: AlertTriangle,
    className: "bg-red-500/20 text-red-400 border-red-500/30 hover:bg-red-500/30",
  },
  high: {
    label: "High",
    icon: AlertCircle,
    className: "bg-orange-500/20 text-orange-400 border-orange-500/30 hover:bg-orange-500/30",
  },
  medium: {
    label: "Medium",
    icon: Info,
    className: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30 hover:bg-yellow-500/30",
  },
  low: {
    label: "Low",
    icon: CheckCircle,
    className: "bg-green-500/20 text-green-400 border-green-500/30 hover:bg-green-500/30",
  },
};

const sizeConfig = {
  sm: "text-xs px-2 py-0.5",
  md: "text-sm px-2.5 py-1",
  lg: "text-base px-3 py-1.5",
};

const iconSizeConfig = {
  sm: "h-3 w-3",
  md: "h-4 w-4",
  lg: "h-5 w-5",
};

export function SeverityBadge({
  severity,
  className,
  showIcon = true,
  size = "md",
}: SeverityBadgeProps) {
  const config = severityConfig[severity] || severityConfig.medium;
  const Icon = config.icon;

  return (
    <Badge
      variant="outline"
      className={cn(config.className, sizeConfig[size], "font-semibold", className)}
    >
      {showIcon && <Icon className={cn(iconSizeConfig[size], "mr-1")} />}
      {config.label}
    </Badge>
  );
}
