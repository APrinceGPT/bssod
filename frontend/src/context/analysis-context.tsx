"use client";

import React, { createContext, useContext, useState, useCallback, ReactNode } from "react";
import { AnalysisState, AnalyzeResponse } from "@/types";

interface AnalysisContextType {
  state: AnalysisState;
  setUploading: (fileName: string) => void;
  setAnalyzing: () => void;
  setComplete: (result: AnalyzeResponse) => void;
  setError: (error: string) => void;
  setProgress: (progress: number) => void;
  reset: () => void;
}

const initialState: AnalysisState = {
  status: "idle",
  progress: 0,
};

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AnalysisState>(initialState);

  const setUploading = useCallback((fileName: string) => {
    setState({
      status: "uploading",
      progress: 0,
      fileName,
    });
  }, []);

  const setAnalyzing = useCallback(() => {
    setState((prev) => ({
      ...prev,
      status: "analyzing",
      progress: 50,
    }));
  }, []);

  const setComplete = useCallback((result: AnalyzeResponse) => {
    setState((prev) => ({
      ...prev,
      status: "complete",
      progress: 100,
      result,
    }));
  }, []);

  const setError = useCallback((error: string) => {
    setState((prev) => ({
      ...prev,
      status: "error",
      error,
    }));
  }, []);

  const setProgress = useCallback((progress: number) => {
    setState((prev) => ({
      ...prev,
      progress,
    }));
  }, []);

  const reset = useCallback(() => {
    setState(initialState);
  }, []);

  return (
    <AnalysisContext.Provider
      value={{
        state,
        setUploading,
        setAnalyzing,
        setComplete,
        setError,
        setProgress,
        reset,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  const context = useContext(AnalysisContext);
  if (context === undefined) {
    throw new Error("useAnalysis must be used within an AnalysisProvider");
  }
  return context;
}
