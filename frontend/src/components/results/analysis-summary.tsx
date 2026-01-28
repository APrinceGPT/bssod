"use client";

import { AlertTriangle, Info } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface AnalysisSummaryProps {
  bugcheckCode?: string;
  bugcheckName?: string;
}

// Common bugcheck descriptions for quick reference
const BUGCHECK_DESCRIPTIONS: Record<string, string> = {
  "IRQL_NOT_LESS_OR_EQUAL": "A kernel-mode driver attempted to access pageable memory at an invalid interrupt request level (IRQL).",
  "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED": "A system thread generated an exception that the error handler did not catch.",
  "PAGE_FAULT_IN_NONPAGED_AREA": "The system tried to access memory that was not available or was invalid.",
  "KERNEL_DATA_INPAGE_ERROR": "A kernel data page could not be read from the paging file or memory.",
  "CRITICAL_PROCESS_DIED": "A critical system process terminated unexpectedly.",
  "DRIVER_IRQL_NOT_LESS_OR_EQUAL": "A driver attempted to access memory at an invalid IRQL.",
  "SYSTEM_SERVICE_EXCEPTION": "An exception occurred while executing a routine that transitions from non-privileged to privileged code.",
  "KMODE_EXCEPTION_NOT_HANDLED": "A kernel-mode program generated an exception which the error handler did not catch.",
  "UNEXPECTED_KERNEL_MODE_TRAP": "The CPU generated a trap that the kernel was not prepared to handle.",
  "DRIVER_POWER_STATE_FAILURE": "A driver is in an inconsistent or invalid power state.",
};

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
            <Info className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
            <p className="text-sm text-muted-foreground">{description}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
