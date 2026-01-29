"use client";

import { Shield, Lightbulb } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface PreventionTipsCardProps {
  tips: string[];
  className?: string;
}

export function PreventionTipsCard({ tips, className }: PreventionTipsCardProps) {
  if (!tips || tips.length === 0) {
    return null;
  }

  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <Shield className="h-5 w-5 text-primary" />
          Prevention Tips
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-3">
          {tips.map((tip, index) => (
            <li key={index} className="flex items-start gap-3">
              <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10">
                <Lightbulb className="h-3.5 w-3.5 text-primary" />
              </div>
              <span className="text-sm text-muted-foreground leading-relaxed">
                {tip}
              </span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
