"use client";

import { Cpu, Sparkles, Info, Link2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { StructuredAIAnalysisResult } from "@/types";
import { ExecutiveSummaryCard } from "./executive-summary-card";
import { RootCauseCard } from "./root-cause-card";
import { FixStepsList } from "./fix-steps-list";
import { PreventionTipsCard } from "./prevention-tips-card";

interface AIAnalysisProps {
  analysis: StructuredAIAnalysisResult;
}

export function AIAnalysis({ analysis }: AIAnalysisProps) {
  const { structured_analysis: data } = analysis;

  return (
    <div className="space-y-4">
      {/* Header Card with AI Info */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Sparkles className="h-5 w-5 text-primary" />
              AI Analysis
            </CardTitle>
            <div className="flex items-center gap-2">
              {analysis.model && (
                <Badge variant="outline" className="font-mono text-xs">
                  <Cpu className="h-3 w-3 mr-1" />
                  {analysis.model}
                </Badge>
              )}
              {analysis.tokens_used && (
                <Badge variant="secondary" className="text-xs">
                  {analysis.tokens_used.toLocaleString()} tokens
                </Badge>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Executive Summary with Severity & Confidence */}
      <ExecutiveSummaryCard
        summary={data.executive_summary}
        severity={data.severity}
        confidence={data.confidence}
      />

      {/* Root Cause Analysis */}
      <RootCauseCard rootCause={data.root_cause} />

      {/* Fix Steps */}
      <FixStepsList steps={data.fix_steps} />

      {/* Prevention Tips */}
      {data.prevention_tips && data.prevention_tips.length > 0 && (
        <PreventionTipsCard tips={data.prevention_tips} />
      )}

      {/* Additional Notes */}
      {data.additional_notes && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Info className="h-5 w-5 text-primary" />
              Additional Notes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {data.additional_notes}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Related Bugchecks */}
      {data.related_bugchecks && data.related_bugchecks.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Link2 className="h-5 w-5 text-primary" />
              Related Bugchecks
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {data.related_bugchecks.map((code, index) => (
                <Badge key={index} variant="outline" className="font-mono">
                  {code}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
