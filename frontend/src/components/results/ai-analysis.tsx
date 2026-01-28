"use client";

import { Cpu, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AIAnalysisResult } from "@/types";
import { MarkdownRenderer } from "@/components/results/markdown-renderer";

interface AIAnalysisProps {
  analysis: AIAnalysisResult;
}

export function AIAnalysis({ analysis }: AIAnalysisProps) {
  return (
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
      <CardContent>
        <div className="prose prose-sm prose-invert max-w-none">
          <MarkdownRenderer content={analysis.analysis} />
        </div>
      </CardContent>
    </Card>
  );
}
