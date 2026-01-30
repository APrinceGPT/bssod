"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { 
  AlertCircle, 
  FileSearch, 
  LayoutDashboard,
  Search,
  Wrench,
  Shield,
  Download,
  Cpu,
  Sparkles
} from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useAnalysis } from "@/context/analysis-context";
import { SeverityBadge } from "@/components/results/severity-badge";
import { ConfidenceMeter } from "@/components/results/confidence-meter";
import { FloatingChat } from "@/components/results/floating-chat";
import {
  OverviewTabContent,
  RootCauseTabContent,
  FixStepsTabContent,
  PreventionTabContent,
  ExportTabContent,
} from "@/components/results/tab-panels";

export default function ResultsPage() {
  const router = useRouter();
  const { state, reset } = useAnalysis();
  const [analysisTimestamp] = useState(() => new Date().toISOString());

  // Redirect if no results
  useEffect(() => {
    if (state.status !== "complete" || !state.result) {
      const timeout = setTimeout(() => {
        if (state.status !== "complete" || !state.result) {
          router.push("/upload");
        }
      }, 100);
      return () => clearTimeout(timeout);
    }
  }, [state.status, state.result, router]);

  // Show loading or redirect
  if (state.status !== "complete" || !state.result) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <FileSearch className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">Loading results...</p>
        </div>
      </div>
    );
  }

  const { result } = state;
  const analysis = result.ai_analysis?.structured_analysis;

  const handleNewAnalysis = () => {
    reset();
    router.push("/upload");
  };

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="max-w-5xl mx-auto space-y-4">
        {/* Breadcrumb Navigation */}
        <Breadcrumb 
          items={[
            { label: "Upload", href: "/upload" },
            { label: "Results" }
          ]} 
        />

        {/* Session Warning - Compact */}
        <Alert className="py-2">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle className="text-sm">Session-Only Results</AlertTitle>
          <AlertDescription className="text-xs">
            Export or copy the analysis before leaving this page.
          </AlertDescription>
        </Alert>

        {/* Compact Header with Bugcheck Info */}
        <CompactResultsHeader
          dumpFile={result.dump_file}
          bugcheckCode={result.bugcheck_code}
          bugcheckName={result.bugcheck_name}
          severity={analysis?.severity}
          confidence={analysis?.confidence}
          model={result.ai_analysis?.model}
          analysisTimestamp={analysisTimestamp}
        />

        {/* Tab Navigation */}
        {analysis && (
          <Tabs defaultValue="overview" className="w-full">
            <TabsList className="w-full justify-start overflow-x-auto">
              <TabsTrigger value="overview" className="gap-1.5">
                <LayoutDashboard className="h-4 w-4" />
                <span className="hidden sm:inline">Overview</span>
              </TabsTrigger>
              <TabsTrigger value="root-cause" className="gap-1.5">
                <Search className="h-4 w-4" />
                <span className="hidden sm:inline">Root Cause</span>
              </TabsTrigger>
              <TabsTrigger value="fix-steps" className="gap-1.5">
                <Wrench className="h-4 w-4" />
                <span className="hidden sm:inline">Fix Steps</span>
                <Badge variant="secondary" className="ml-1 h-5 px-1.5 text-xs">
                  {analysis.fix_steps.length}
                </Badge>
              </TabsTrigger>
              <TabsTrigger value="prevention" className="gap-1.5">
                <Shield className="h-4 w-4" />
                <span className="hidden sm:inline">Prevention</span>
              </TabsTrigger>
              <TabsTrigger value="export" className="gap-1.5">
                <Download className="h-4 w-4" />
                <span className="hidden sm:inline">Export</span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="mt-4">
              <OverviewTabContent analysis={analysis} />
            </TabsContent>

            <TabsContent value="root-cause" className="mt-4">
              <RootCauseTabContent analysis={analysis} />
            </TabsContent>

            <TabsContent value="fix-steps" className="mt-4">
              <FixStepsTabContent analysis={analysis} />
            </TabsContent>

            <TabsContent value="prevention" className="mt-4">
              <PreventionTabContent analysis={analysis} />
            </TabsContent>

            <TabsContent value="export" className="mt-4">
              <ExportTabContent result={result} onNewAnalysis={handleNewAnalysis} />
            </TabsContent>
          </Tabs>
        )}

        {/* Floating Chat Button */}
        {result.ai_analysis && (
          <FloatingChat 
            analysisContext={{
              bugcheck_code: result.bugcheck_code,
              bugcheck_name: result.bugcheck_name,
              dump_file: result.dump_file,
              analysis_summary: analysis?.executive_summary || "",
            }}
          />
        )}
      </div>
    </div>
  );
}

/**
 * Compact header with all critical info in one row
 */
interface CompactResultsHeaderProps {
  dumpFile?: string;
  bugcheckCode?: string;
  bugcheckName?: string;
  severity?: "critical" | "high" | "medium" | "low";
  confidence?: number;
  model?: string;
  analysisTimestamp: string;
}

function CompactResultsHeader({
  dumpFile,
  bugcheckCode,
  bugcheckName,
  severity,
  confidence,
  model,
  analysisTimestamp,
}: CompactResultsHeaderProps) {
  const formattedTime = new Date(analysisTimestamp).toLocaleString();

  return (
    <div className="bg-card border rounded-lg p-4">
      {/* Top row: Title and badges */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
            <Sparkles className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Analysis Complete</h1>
            <p className="text-xs text-muted-foreground">{formattedTime}</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2 flex-wrap">
          {severity && <SeverityBadge severity={severity} size="md" />}
          {confidence !== undefined && (
            <ConfidenceMeter confidence={confidence} size="sm" />
          )}
        </div>
      </div>

      {/* Bottom row: File and bugcheck info */}
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm">
        {dumpFile && (
          <div className="flex items-center gap-1.5 text-muted-foreground">
            <FileSearch className="h-4 w-4 shrink-0" />
            <span className="truncate max-w-[200px]">{dumpFile}</span>
          </div>
        )}
        
        {bugcheckCode && (
          <Badge variant="destructive" className="font-mono">
            {bugcheckCode}
          </Badge>
        )}
        
        {bugcheckName && (
          <Badge variant="secondary" className="max-w-[200px] truncate">
            {bugcheckName}
          </Badge>
        )}
        
        {model && (
          <Badge variant="outline" className="font-mono text-xs">
            <Cpu className="h-3 w-3 mr-1" />
            {model}
          </Badge>
        )}
      </div>
    </div>
  );
}
