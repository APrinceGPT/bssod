"use client";

import { useState } from "react";
import { Copy, Download, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AnalyzeResponse } from "@/types";

interface ExportActionsProps {
  result: AnalyzeResponse;
}

export function ExportActions({ result }: ExportActionsProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyToClipboard = async () => {
    const text = formatResultAsText(result);
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  const handleExportJSON = () => {
    const json = JSON.stringify(result, null, 2);
    downloadFile(json, "bssod-analysis.json", "application/json");
  };

  const handleExportMarkdown = () => {
    const markdown = formatResultAsMarkdown(result);
    downloadFile(markdown, "bssod-analysis.md", "text/markdown");
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">Export Results</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-3">
          <Button 
            variant="outline" 
            onClick={handleCopyToClipboard}
            className="gap-2"
          >
            {copied ? (
              <>
                <Check className="h-4 w-4" />
                Copied
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                Copy to Clipboard
              </>
            )}
          </Button>
          <Button 
            variant="outline" 
            onClick={handleExportJSON}
            className="gap-2"
          >
            <Download className="h-4 w-4" />
            Export JSON
          </Button>
          <Button 
            variant="outline" 
            onClick={handleExportMarkdown}
            className="gap-2"
          >
            <Download className="h-4 w-4" />
            Export Markdown
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function downloadFile(content: string, filename: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function formatResultAsText(result: AnalyzeResponse): string {
  const lines: string[] = [
    "BSSOD - Blue-Screen Solution Oriented Diagnostics",
    "=".repeat(50),
    "",
    `Status: ${result.success ? "Success" : "Failed"}`,
    `Message: ${result.message}`,
  ];

  if (result.dump_file) {
    lines.push(`Dump File: ${result.dump_file}`);
  }
  if (result.bugcheck_code) {
    lines.push(`Bugcheck Code: ${result.bugcheck_code}`);
  }
  if (result.bugcheck_name) {
    lines.push(`Bugcheck Name: ${result.bugcheck_name}`);
  }

  if (result.ai_analysis) {
    lines.push("");
    lines.push("-".repeat(50));
    lines.push("AI Analysis:");
    lines.push("-".repeat(50));
    lines.push("");
    lines.push(result.ai_analysis.analysis);
  }

  return lines.join("\n");
}

function formatResultAsMarkdown(result: AnalyzeResponse): string {
  const lines: string[] = [
    "# BSSOD Analysis Report",
    "",
    "## Overview",
    "",
    `- **Status:** ${result.success ? "Success" : "Failed"}`,
    `- **Message:** ${result.message}`,
  ];

  if (result.dump_file) {
    lines.push(`- **Dump File:** ${result.dump_file}`);
  }
  if (result.bugcheck_code) {
    lines.push(`- **Bugcheck Code:** \`${result.bugcheck_code}\``);
  }
  if (result.bugcheck_name) {
    lines.push(`- **Bugcheck Name:** ${result.bugcheck_name}`);
  }

  if (result.ai_analysis) {
    lines.push("");
    lines.push("---");
    lines.push("");
    lines.push("## AI Analysis");
    lines.push("");
    lines.push(result.ai_analysis.analysis);
    
    if (result.ai_analysis.model) {
      lines.push("");
      lines.push("---");
      lines.push("");
      lines.push(`*Analysis performed by ${result.ai_analysis.model}*`);
    }
  }

  return lines.join("\n");
}
