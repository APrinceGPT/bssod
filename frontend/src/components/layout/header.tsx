"use client";

import Link from "next/link";
import { Monitor } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
      <div className="container mx-auto flex h-14 max-w-screen-2xl items-center px-4">
        <Link href="/" className="flex items-center space-x-2">
          <Monitor className="h-6 w-6 text-primary" />
          <span className="font-bold text-lg">BSSOD</span>
        </Link>
        <nav className="ml-auto flex items-center space-x-6 text-sm font-medium">
          <Link 
            href="/" 
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            Home
          </Link>
          <Link 
            href="/upload" 
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            Analyze
          </Link>
        </nav>
      </div>
    </header>
  );
}
