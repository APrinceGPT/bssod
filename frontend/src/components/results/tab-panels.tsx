"use client";

import { Info, Link2, RefreshCcw } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { StructuredAnalysis, AnalyzeResponse } from "@/types";
import { ExecutiveSummaryCard } from "./executive-summary-card";
import { RootCauseCard } from "./root-cause-card";
import { FixStepsList } from "./fix-steps-list";
import { PreventionTipsCard } from "./prevention-tips-card";
import { ExportActions } from "./export-actions";

/**
 * Overview Tab: Executive Summary with severity and confidence
 */
interface OverviewTabProps {
  analysis: StructuredAnalysis;
}

export function OverviewTabContent({ analysis }: OverviewTabProps) {
  return (
    <div className="space-y-4">
      <ExecutiveSummaryCard
        summary={analysis.executive_summary}
        severity={analysis.severity}
        confidence={analysis.confidence}
      />
      
      {/* Quick stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <QuickStatCard
          label="Severity"
          value={analysis.severity.toUpperCase()}
          variant={analysis.severity}
        />
        <QuickStatCard
          label="Confidence"
          value={`${analysis.confidence}%`}
          variant="neutral"
        />
        <QuickStatCard
          label="Fix Steps"
          value={analysis.fix_steps.length.toString()}
          variant="neutral"
        />
        <QuickStatCard
          label="Prevention Tips"
          value={(analysis.prevention_tips?.length || 0).toString()}
          variant="neutral"
        />
      </div>
    </div>
  );
}

/**
 * Root Cause Tab: Detailed analysis
 */
interface RootCauseTabProps {
  analysis: StructuredAnalysis;
}

export function RootCauseTabContent({ analysis }: RootCauseTabProps) {
  return (
    <div className="space-y-4">
      <RootCauseCard rootCause={analysis.root_cause} />
      
      {/* Related Bugchecks */}
      {analysis.related_bugchecks && analysis.related_bugchecks.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Link2 className="h-5 w-5 text-primary" />
              Related Bugchecks
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {analysis.related_bugchecks.map((code, index) => (
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

/**
 * Fix Steps Tab: All recommendations
 */
interface FixStepsTabProps {
  analysis: StructuredAnalysis;
}

export function FixStepsTabContent({ analysis }: FixStepsTabProps) {
  return (
    <FixStepsList steps={analysis.fix_steps} />
  );
}

/**
 * Prevention Tab: Tips, notes, and related info
 */
interface PreventionTabProps {
  analysis: StructuredAnalysis;
}

export function PreventionTabContent({ analysis }: PreventionTabProps) {
  return (
    <div className="space-y-4">
      {/* Prevention Tips */}
      {analysis.prevention_tips && analysis.prevention_tips.length > 0 && (
        <PreventionTipsCard tips={analysis.prevention_tips} />
      )}
      
      {/* Additional Notes */}
      {analysis.additional_notes && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Info className="h-5 w-5 text-primary" />
              Additional Notes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {analysis.additional_notes}
            </p>
          </CardContent>
        </Card>
      )}
      
      {/* Show message if no content */}
      {(!analysis.prevention_tips || analysis.prevention_tips.length === 0) && 
       !analysis.additional_notes && (
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-muted-foreground">
              No additional prevention tips for this issue.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

/**
 * Export Tab: Export options and new analysis button
 */
interface ExportTabProps {
  result: AnalyzeResponse;
  onNewAnalysis: () => void;
}

export function ExportTabContent({ result, onNewAnalysis }: ExportTabProps) {
  return (
    <div className="space-y-4">
      <ExportActions result={result} />
      
      <Card>
        <CardContent className="py-6">
          <div className="text-center space-y-4">
            <p className="text-sm text-muted-foreground">
              Ready to analyze another dump file?
            </p>
            <Button onClick={onNewAnalysis} className="gap-2">
              <RefreshCcw className="h-4 w-4" />
              Analyze Another File
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

/**
 * Quick stat card for overview grid
 */
interface QuickStatCardProps {
  label: string;
  value: string;
  variant: "critical" | "high" | "medium" | "low" | "neutral";
}

function QuickStatCard({ label, value, variant }: QuickStatCardProps) {
  const variantClasses = {
    critical: "border-red-500/50 bg-red-500/10",
    high: "border-orange-500/50 bg-orange-500/10",
    medium: "border-yellow-500/50 bg-yellow-500/10",
    low: "border-green-500/50 bg-green-500/10",
    neutral: "border-border bg-muted/30",
  };

  return (
    <div className={`rounded-lg border p-3 text-center ${variantClasses[variant]}`}>
      <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
        {label}
      </p>
      <p className="text-lg font-semibold">{value}</p>
    </div>
  );
}
