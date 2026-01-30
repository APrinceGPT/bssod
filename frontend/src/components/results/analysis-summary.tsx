"use client";

import { AlertTriangle, Info } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BUGCHECK_DESCRIPTIONS } from "@/lib/bugcheck-descriptions";

interface AnalysisSummaryProps {
  bugcheckCode?: string;
  bugcheckName?: string;
}

export function AnalysisSummary({ bugcheckCode, bugcheckName }: AnalysisSummaryProps) {
  const description = bugcheckName ? BUGCHECK_DESCRIPTIONS[bugcheckName] : null;

  if (!bugcheckCode && !bugcheckName) {
    return null;
  }

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <AlertTriangle className="h-5 w-5 text-yellow-500" />
          Crash Summary
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid gap-3">
          {bugcheckCode && (
            <div className="flex items-start gap-3">
              <span className="font-medium text-muted-foreground min-w-[100px]">
                Bugcheck Code:
              </span>
              <code className="font-mono text-sm bg-muted px-2 py-1 rounded">
                {bugcheckCode}
              </code>
            </div>
          )}
          {bugcheckName && (
            <div className="flex items-start gap-3">
              <span className="font-medium text-muted-foreground min-w-[100px]">
                Error Name:
              </span>
              <span className="font-medium">{bugcheckName}</span>
            </div>
          )}
        </div>

        {description && (
          <div className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
            <Info className="h-5 w-5 text-primary shrink-0 mt-0.5" />
            <p className="text-sm text-muted-foreground">{description}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
