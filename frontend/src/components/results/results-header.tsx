"use client";

import { CheckCircle, XCircle, FileText } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ResultsHeaderProps {
  dumpFile?: string;
  bugcheckCode?: string;
  bugcheckName?: string;
  success: boolean;
}

export function ResultsHeader({ 
  dumpFile, 
  bugcheckCode, 
  bugcheckName,
  success 
}: ResultsHeaderProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            {success ? (
              <CheckCircle className="h-10 w-10 text-green-500" />
            ) : (
              <XCircle className="h-10 w-10 text-destructive" />
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 flex-wrap mb-2">
              <h1 className="text-2xl font-bold">Analysis Complete</h1>
              {success && (
                <Badge variant="outline" className="text-green-500 border-green-500">
                  Success
                </Badge>
              )}
            </div>
            {dumpFile && (
              <div className="flex items-center gap-2 text-muted-foreground">
                <FileText className="h-4 w-4" />
                <span className="truncate">{dumpFile}</span>
              </div>
            )}
            {bugcheckCode && (
              <div className="mt-3 flex flex-wrap gap-2">
                <Badge variant="destructive" className="font-mono">
                  {bugcheckCode}
                </Badge>
                {bugcheckName && (
                  <Badge variant="secondary">
                    {bugcheckName}
                  </Badge>
                )}
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
