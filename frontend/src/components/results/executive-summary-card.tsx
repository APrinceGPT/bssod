"use client";

import { MessageSquareText } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SeverityBadge } from "./severity-badge";
import { ConfidenceMeter } from "./confidence-meter";
import { SeverityLevel } from "@/types";

interface ExecutiveSummaryCardProps {
  summary: string;
  severity: SeverityLevel;
  confidence: number;
  className?: string;
}

export function ExecutiveSummaryCard({
  summary,
  severity,
  confidence,
  className,
}: ExecutiveSummaryCardProps) {
  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <CardTitle className="flex items-center gap-2 text-lg">
            <MessageSquareText className="h-5 w-5 text-primary" />
            Summary
          </CardTitle>
          <div className="flex items-center gap-3 flex-wrap">
            <SeverityBadge severity={severity} size="md" />
            <ConfidenceMeter confidence={confidence} size="sm" />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-base text-foreground leading-relaxed">
          {summary}
        </p>
      </CardContent>
    </Card>
  );
}
