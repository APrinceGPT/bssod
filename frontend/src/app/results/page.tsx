"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AlertCircle, FileSearch } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { useAnalysis } from "@/context/analysis-context";
import { ResultsHeader } from "@/components/results/results-header";
import { AnalysisSummary } from "@/components/results/analysis-summary";
import { AIAnalysis } from "@/components/results/ai-analysis";
import { ChatInterface } from "@/components/results/chat-interface";
import { ExportActions } from "@/components/results/export-actions";

export default function ResultsPage() {
  const router = useRouter();
  const { state, reset } = useAnalysis();
  const [analysisTimestamp] = useState(() => new Date().toISOString());

  // Redirect if no results
  useEffect(() => {
    if (state.status !== "complete" || !state.result) {
      // Allow a small delay for hydration
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

  const handleNewAnalysis = () => {
    reset();
    router.push("/upload");
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Breadcrumb Navigation */}
        <Breadcrumb 
          items={[
            { label: "Upload", href: "/upload" },
            { label: "Results" }
          ]} 
        />

        {/* Session Warning */}
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Session-Only Results</AlertTitle>
          <AlertDescription>
            These results are stored in your browser session only. 
            Export or copy the analysis before leaving this page.
          </AlertDescription>
        </Alert>

        {/* Results Header */}
        <ResultsHeader 
          dumpFile={result.dump_file}
          bugcheckCode={result.bugcheck_code}
          bugcheckName={result.bugcheck_name}
          success={result.success}
          analysisTimestamp={analysisTimestamp}
        />

        {/* Analysis Summary */}
        <AnalysisSummary
          bugcheckCode={result.bugcheck_code}
          bugcheckName={result.bugcheck_name}
        />

        {/* AI Analysis */}
        {result.ai_analysis && (
          <AIAnalysis analysis={result.ai_analysis} />
        )}

        {/* Interactive Chat for Follow-up Questions */}
        {result.ai_analysis && (
          <ChatInterface 
            analysisContext={{
              bugcheck_code: result.bugcheck_code,
              bugcheck_name: result.bugcheck_name,
              dump_file: result.dump_file,
              analysis_summary: result.ai_analysis.structured_analysis.executive_summary,
            }}
          />
        )}

        {/* Export Actions */}
        <ExportActions result={result} />

        {/* New Analysis Button */}
        <div className="flex justify-center pt-6">
          <Button variant="outline" onClick={handleNewAnalysis}>
            Analyze Another File
          </Button>
        </div>
      </div>
    </div>
  );
}
