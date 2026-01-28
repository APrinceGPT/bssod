import { Monitor } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border/40 py-6 md:py-0">
      <div className="container mx-auto flex flex-col items-center justify-between gap-4 px-4 md:h-14 md:flex-row">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Monitor className="h-4 w-4" />
          <span>BSSOD - Blue-Screen Solution Oriented Diagnostics</span>
        </div>
        <p className="text-sm text-muted-foreground">
          AI-powered crash analysis using Claude 4 Sonnet
        </p>
      </div>
    </footer>
  );
}
