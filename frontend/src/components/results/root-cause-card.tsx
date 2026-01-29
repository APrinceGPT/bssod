"use client";

import { FileSearch, Cpu, Code2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { RootCauseAnalysis as RootCauseAnalysisType } from "@/types";

interface RootCauseCardProps {
  rootCause: RootCauseAnalysisType;
  className?: string;
}

export function RootCauseCard({ rootCause, className }: RootCauseCardProps) {
  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <FileSearch className="h-5 w-5 text-primary" />
          Root Cause Analysis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Title */}
        <div>
          <h4 className="font-semibold text-foreground text-base mb-2">
            {rootCause.title}
          </h4>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {rootCause.explanation}
          </p>
        </div>

        {/* Affected Component */}
        {rootCause.affected_component && (
          <div className="flex items-start gap-3 p-3 rounded-lg bg-muted/50 border border-border/50">
            <Cpu className="h-5 w-5 text-orange-400 mt-0.5 shrink-0" />
            <div>
              <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Affected Component
              </span>
              <p className="text-sm font-medium text-foreground mt-0.5">
                {rootCause.affected_component}
              </p>
            </div>
          </div>
        )}

        {/* Technical Details (collapsible) */}
        {rootCause.technical_details && (
          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="technical-details" className="border-b-0">
              <AccordionTrigger className="py-2 text-sm hover:no-underline">
                <span className="flex items-center gap-2 text-muted-foreground">
                  <Code2 className="h-4 w-4" />
                  Technical Details
                </span>
              </AccordionTrigger>
              <AccordionContent>
                <div className="p-3 rounded-lg bg-muted/30 border border-border/30">
                  <p className="text-sm text-muted-foreground font-mono leading-relaxed whitespace-pre-wrap">
                    {rootCause.technical_details}
                  </p>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        )}
      </CardContent>
    </Card>
  );
}
