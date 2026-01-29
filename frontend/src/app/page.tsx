import Link from "next/link";
import { 
  Download, 
  Upload, 
  FileSearch, 
  Cpu, 
  Shield, 
  Zap,
  ArrowRight,
  Monitor
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="flex flex-col items-center text-center">
            <div className="flex items-center gap-3 mb-6">
              <Monitor className="h-12 w-12 text-primary" />
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
                BSSOD
              </h1>
            </div>
            <p className="text-xl md:text-2xl text-muted-foreground mb-4">
              Blue-Screen Solution Oriented Diagnostics
            </p>
            <p className="text-lg text-muted-foreground max-w-2xl mb-8">
              AI-powered Windows memory dump analyzer that helps you diagnose 
              and troubleshoot Blue Screen of Death issues with actionable insights.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" asChild>
                <Link href="/upload">
                  <Upload className="mr-2 h-5 w-5" />
                  Analyze Now
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <a href="/downloads/BSSOD_Analyzer_Parser.exe" download="BSSOD_Analyzer_Parser.exe">
                  <Download className="mr-2 h-5 w-5" />
                  Download Parser Tool
                </a>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-muted/50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="bg-card">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <Download className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Step 1: Download Parser</CardTitle>
                <CardDescription>
                  Download our lightweight parser tool for Windows
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  The parser tool runs locally on your machine to extract 
                  diagnostic data from memory dump files without uploading 
                  the entire 15+ GB file.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <FileSearch className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Step 2: Extract Data</CardTitle>
                <CardDescription>
                  Run the parser on your memory dump file
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  The tool extracts crash codes, stack traces, driver 
                  information, and system details into a small ZIP file 
                  ready for analysis.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <Cpu className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Step 3: Get AI Analysis</CardTitle>
                <CardDescription>
                  Upload the ZIP and receive instant insights
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Our AI analyzes your crash data and provides root cause 
                  analysis, recommended actions, and detailed explanations 
                  in plain language.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="flex items-start gap-4 p-4">
              <Shield className="h-8 w-8 text-primary flex-shrink-0" />
              <div>
                <h3 className="font-semibold mb-1">Privacy First</h3>
                <p className="text-sm text-muted-foreground">
                  Your crash data is processed in session only. 
                  No data is stored on our servers.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4 p-4">
              <Zap className="h-8 w-8 text-primary flex-shrink-0" />
              <div>
                <h3 className="font-semibold mb-1">Fast Analysis</h3>
                <p className="text-sm text-muted-foreground">
                  Get comprehensive analysis results in seconds, 
                  not hours of manual debugging.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4 p-4">
              <FileSearch className="h-8 w-8 text-primary flex-shrink-0" />
              <div>
                <h3 className="font-semibold mb-1">Detailed Reports</h3>
                <p className="text-sm text-muted-foreground">
                  Export analysis as JSON or copy to clipboard 
                  for documentation and sharing.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-muted/50">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold mb-4">Ready to Diagnose?</h2>
          <p className="text-muted-foreground mb-6 max-w-xl mx-auto">
            Upload your extracted crash data and get AI-powered insights 
            to resolve your Windows Blue Screen issues.
          </p>
          <Button size="lg" asChild>
            <Link href="/upload">
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
