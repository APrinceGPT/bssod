"use client";

import { useState } from "react";
import { Copy, Download, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "@/components/ui/sonner";
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
      toast.success("Analysis copied to clipboard");
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
      toast.error("Failed to copy to clipboard");
    }
  };

  const handleExportJSON = () => {
    const json = JSON.stringify(result, null, 2);
    downloadFile(json, "bssod-analysis.json", "application/json");
    toast.success("JSON file downloaded successfully");
  };

  const handleExportMarkdown = () => {
    const markdown = formatResultAsMarkdown(result);
    downloadFile(markdown, "bssod-analysis.md", "text/markdown");
    toast.success("Markdown file downloaded successfully");
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">Export Results</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col sm:flex-row gap-3">
          <Button 
            variant="outline" 
            onClick={handleCopyToClipboard}
            className="gap-2 w-full sm:w-auto"
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
            className="gap-2 w-full sm:w-auto"
          >
            <Download className="h-4 w-4" />
            Export JSON
          </Button>
          <Button 
            variant="outline" 
            onClick={handleExportMarkdown}
            className="gap-2 w-full sm:w-auto"
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

  if (result.ai_analysis?.structured_analysis) {
    const data = result.ai_analysis.structured_analysis;
    
    lines.push("");
    lines.push("-".repeat(50));
    lines.push("AI Analysis:");
    lines.push("-".repeat(50));
    lines.push("");
    
    lines.push(`Severity: ${data.severity.toUpperCase()}`);
    lines.push(`Confidence: ${data.confidence}%`);
    lines.push("");
    
    lines.push("Summary:");
    lines.push(data.executive_summary);
    lines.push("");
    
    lines.push("Root Cause:");
    lines.push(`  ${data.root_cause.title}`);
    lines.push(`  ${data.root_cause.explanation}`);
    if (data.root_cause.affected_component) {
      lines.push(`  Affected Component: ${data.root_cause.affected_component}`);
    }
    lines.push("");
    
    lines.push("Fix Steps:");
    data.fix_steps.forEach((step) => {
      lines.push(`  ${step.step}. [${step.priority.toUpperCase()}] ${step.action}`);
      lines.push(`     ${step.details}`);
    });
    lines.push("");
    
    if (data.prevention_tips?.length) {
      lines.push("Prevention Tips:");
      data.prevention_tips.forEach((tip, i) => {
        lines.push(`  ${i + 1}. ${tip}`);
      });
      lines.push("");
    }
    
    if (data.additional_notes) {
      lines.push("Additional Notes:");
      lines.push(data.additional_notes);
    }
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

  if (result.ai_analysis?.structured_analysis) {
    const data = result.ai_analysis.structured_analysis;
    
    lines.push("");
    lines.push("---");
    lines.push("");
    lines.push("## AI Analysis");
    lines.push("");
    
    lines.push(`| Severity | Confidence |`);
    lines.push(`| --- | --- |`);
    lines.push(`| **${data.severity.toUpperCase()}** | ${data.confidence}% |`);
    lines.push("");
    
    lines.push("### Summary");
    lines.push("");
    lines.push(data.executive_summary);
    lines.push("");
    
    lines.push("### Root Cause");
    lines.push("");
    lines.push(`**${data.root_cause.title}**`);
    lines.push("");
    lines.push(data.root_cause.explanation);
    if (data.root_cause.affected_component) {
      lines.push("");
      lines.push(`> **Affected Component:** ${data.root_cause.affected_component}`);
    }
    if (data.root_cause.technical_details) {
      lines.push("");
      lines.push("<details>");
      lines.push("<summary>Technical Details</summary>");
      lines.push("");
      lines.push("```");
      lines.push(data.root_cause.technical_details);
      lines.push("```");
      lines.push("</details>");
    }
    lines.push("");
    
    lines.push("### Fix Steps");
    lines.push("");
    data.fix_steps.forEach((step) => {
      const priorityEmoji = step.priority === "high" ? "🔴" : step.priority === "medium" ? "🟡" : "🟢";
      lines.push(`${step.step}. ${priorityEmoji} **${step.action}** (${step.priority})`);
      lines.push(`   - ${step.details}`);
    });
    lines.push("");
    
    if (data.prevention_tips?.length) {
      lines.push("### Prevention Tips");
      lines.push("");
      data.prevention_tips.forEach((tip) => {
        lines.push(`- 💡 ${tip}`);
      });
      lines.push("");
    }
    
    if (data.additional_notes) {
      lines.push("### Additional Notes");
      lines.push("");
      lines.push(`> ${data.additional_notes}`);
      lines.push("");
    }
    
    if (data.related_bugchecks?.length) {
      lines.push("### Related Bugchecks");
      lines.push("");
      lines.push(data.related_bugchecks.map((code) => `\`${code}\``).join(", "));
      lines.push("");
    }
    
    if (result.ai_analysis.model) {
      lines.push("---");
      lines.push("");
      lines.push(`*Analysis performed by ${result.ai_analysis.model}*`);
    }
  }

  return lines.join("\n");
}
