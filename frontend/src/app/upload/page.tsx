"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Upload, FileArchive, AlertCircle, Loader2, Download, Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";
import { useAnalysis } from "@/context/analysis-context";
import { analyzeFile, ApiError } from "@/lib/api";
import { FileDropzone } from "@/components/upload/file-dropzone";
import { getUserFriendlyError, UserFriendlyError } from "@/lib/error-messages";
import { UPLOAD_CONFIG, PROGRESS_MESSAGES } from "@/lib/constants";

export default function UploadPage() {
  const router = useRouter();
  const { state, setUploading, setAnalyzing, setComplete, setError, setProgress, reset } = useAnalysis();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [friendlyError, setFriendlyError] = useState<UserFriendlyError | null>(null);
  const [progressMessage, setProgressMessage] = useState<string>("");

  const handleFileSelect = useCallback((file: File) => {
    setSelectedFile(file);
    setFriendlyError(null);
    reset();
  }, [reset]);

  const handleUpload = useCallback(async () => {
    if (!selectedFile) return;

    setFriendlyError(null);
    setUploading(selectedFile.name);
    setProgressMessage(PROGRESS_MESSAGES.UPLOADING);

    try {
      // Start upload with progress tracking
      setProgress(10);
      
      // Call API with progress callback
      const result = await analyzeFile(selectedFile, (progress) => {
        setProgress(progress);
        // Update message based on progress phase
        if (progress < 40) {
          setProgressMessage(PROGRESS_MESSAGES.UPLOADING);
        }
      });

      // Move to validation phase
      setProgress(45);
      setProgressMessage(PROGRESS_MESSAGES.VALIDATING);
      await new Promise(resolve => setTimeout(resolve, 300));

      // Move to analyzing state
      setAnalyzing();
      setProgress(60);
      setProgressMessage(PROGRESS_MESSAGES.ANALYZING);

      // Simulate progress during analysis
      await new Promise(resolve => setTimeout(resolve, 400));
      setProgress(80);

      // Preparing results
      setProgress(95);
      setProgressMessage(PROGRESS_MESSAGES.PREPARING);
      await new Promise(resolve => setTimeout(resolve, 200));
      
      setProgress(100);

      // Complete
      setComplete(result);

      // Navigate to results
      router.push("/results");
    } catch (err) {
      let errorMessage = "An unexpected error occurred";
      let userError: UserFriendlyError;
      
      if (err instanceof ApiError) {
        errorMessage = err.message;
        userError = getUserFriendlyError(err.message, err.statusCode);
      } else if (err instanceof Error) {
        errorMessage = err.message;
        userError = getUserFriendlyError(err.message);
      } else {
        userError = getUserFriendlyError(errorMessage);
      }
      
      setFriendlyError(userError);
      setError(errorMessage);
    }
  }, [selectedFile, setUploading, setProgress, setAnalyzing, setComplete, setError, router]);

  const isProcessing = state.status === "uploading" || state.status === "analyzing";

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">Analyze Memory Dump</h1>
          <p className="text-muted-foreground">
            Upload the ZIP file exported from the BSSOD Parser Tool
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload Analysis File
            </CardTitle>
            <CardDescription>
              Drag and drop your ZIP file or click to browse
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* File Dropzone */}
            <FileDropzone
              onFileSelect={handleFileSelect}
              disabled={isProcessing}
              acceptedTypes={[".zip"]}
            />

            {/* Selected File Info */}
            {selectedFile && !isProcessing && (
              <div className="flex items-center gap-3 p-4 rounded-lg bg-muted">
                <FileArchive className="h-8 w-8 text-primary" />
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{selectedFile.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <Button onClick={handleUpload} disabled={isProcessing}>
                  Analyze
                </Button>
              </div>
            )}

            {/* Progress */}
            {isProcessing && (
              <div className="space-y-4">
                <div className="flex items-center gap-3 p-4 rounded-lg bg-muted">
                  <Loader2 className="h-6 w-6 animate-spin text-primary" />
                  <div className="flex-1">
                    <p className="font-medium">
                      {progressMessage || (state.status === "uploading" ? "Uploading..." : "Analyzing...")}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {state.fileName}
                    </p>
                  </div>
                </div>
                <Progress value={state.progress} className="h-2" />
                <p className="text-sm text-center text-muted-foreground">
                  {state.progress}% complete
                </p>
              </div>
            )}

            {/* Error */}
            {state.status === "error" && (
              <div className="space-y-4">
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>{friendlyError?.title || "Error"}</AlertTitle>
                  <AlertDescription>{friendlyError?.message || state.error}</AlertDescription>
                </Alert>
                {friendlyError?.suggestion && (
                  <div className="flex items-start gap-2 p-3 rounded-lg bg-muted text-sm">
                    <Info className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                    <span className="text-muted-foreground">{friendlyError.suggestion}</span>
                  </div>
                )}
                <Button 
                  variant="outline" 
                  onClick={() => {
                    reset();
                    setSelectedFile(null);
                    setFriendlyError(null);
                  }}
                  className="w-full"
                >
                  Try Again
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Instructions */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="text-lg">Requirements</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-primary mt-1">1.</span>
                <span>
                  The ZIP file must be exported from the BSSOD Parser Tool
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary mt-1">2.</span>
                <span>
                  Maximum file size: {UPLOAD_CONFIG.MAX_FILE_SIZE_MB} MB
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary mt-1">3.</span>
                <span>
                  The ZIP must contain an analysis.json file
                </span>
              </li>
            </ul>
            <div className="pt-2 border-t">
              <p className="text-sm text-muted-foreground mb-3">
                Need the parser tool?
              </p>
              <Button variant="outline" size="sm" asChild>
                <a href="/downloads/BSSOD_Analyzer_Parser.exe" download="BSSOD_Analyzer_Parser.exe">
                  <Download className="mr-2 h-4 w-4" />
                  Download Parser Tool
                </a>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
