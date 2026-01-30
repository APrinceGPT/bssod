"use client";

import { CheckCircle2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { FixStep } from "@/types";

interface FixStepsListProps {
  steps: FixStep[];
  className?: string;
}

const priorityConfig = {
  high: {
    label: "High",
    className: "bg-red-500/20 text-red-400 border-red-500/30",
  },
  medium: {
    label: "Medium",
    className: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  },
  low: {
    label: "Low",
    className: "bg-green-500/20 text-green-400 border-green-500/30",
  },
};

export function FixStepsList({ steps, className }: FixStepsListProps) {
  // Sort steps by step number to ensure correct order
  const sortedSteps = [...steps].sort((a, b) => a.step - b.step);

  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <CheckCircle2 className="h-5 w-5 text-primary" />
          Fix Recommendations
          <Badge variant="secondary" className="ml-auto">
            {steps.length} step{steps.length !== 1 ? "s" : ""}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {sortedSteps.map((step, index) => (
          <FixStepItem key={step.step} step={step} isLast={index === sortedSteps.length - 1} />
        ))}
      </CardContent>
    </Card>
  );
}

interface FixStepItemProps {
  step: FixStep;
  isLast: boolean;
}

function FixStepItem({ step, isLast }: FixStepItemProps) {
  const priority = priorityConfig[step.priority] || priorityConfig.medium;

  return (
    <div className="relative flex gap-4">
      {/* Step number indicator with line */}
      <div className="flex flex-col items-center">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20 text-primary font-semibold text-sm">
          {step.step}
        </div>
        {!isLast && (
          <div className="flex-1 w-0.5 bg-border mt-2" />
        )}
      </div>

      {/* Step content */}
      <div className="flex-1 pb-4">
        <div className="flex items-start justify-between gap-2 mb-1">
          <h4 className="font-medium text-foreground">{step.action}</h4>
          <Badge variant="outline" className={cn("text-xs shrink-0", priority.className)}>
            {priority.label}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground leading-relaxed">
          {step.details}
        </p>
      </div>
    </div>
  );
}
