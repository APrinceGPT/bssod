"""
BSSOD Analyzer Parser Tool - GUI Application

This is the main GUI application for the BSSOD Analyzer Parser Tool.
It provides a user-friendly interface for analyzing Windows memory dump files
and exporting the results for AI analysis.
"""

import os
import sys
import threading
from typing import Optional
from pathlib import Path

import customtkinter as ctk
from tkinter import filedialog, messagebox

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser.analyzer import DumpAnalyzer, analyze_dump, CompleteAnalysis


# Configure CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"


class BSODAnalyzerApp(ctk.CTk):
    """Main application window for BSSOD Analyzer Parser Tool."""
    
    APP_NAME = "BSSOD Analyzer - Parser Tool"
    APP_VERSION = "1.0.0"
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title(self.APP_NAME)
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.minsize(600, 400)
        
        # Center window on screen
        self._center_window()
        
        # State variables
        self.dump_path: Optional[str] = None
        self.analysis_result: Optional[CompleteAnalysis] = None
        self.zip_path: Optional[str] = None
        self.is_analyzing = False
        
        # Create UI
        self._create_widgets()
        
    def _center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header frame
        self._create_header()
        
        # File selection frame
        self._create_file_selection()
        
        # Results frame (scrollable)
        self._create_results_area()
        
        # Action buttons frame
        self._create_action_buttons()
        
        # Status bar
        self._create_status_bar()
    
    def _create_header(self):
        """Create the header section."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🔵 BSSOD Analyzer - Parser Tool",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(anchor="w")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Extract diagnostic data from Windows memory dumps for AI analysis",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack(anchor="w")
    
    def _create_file_selection(self):
        """Create the file selection section."""
        file_frame = ctk.CTkFrame(self)
        file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        file_frame.grid_columnconfigure(1, weight=1)
        
        # File label
        file_label = ctk.CTkLabel(
            file_frame,
            text="Memory Dump File:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # File path entry
        self.file_entry = ctk.CTkEntry(
            file_frame,
            placeholder_text="Select a .DMP file or drop it here...",
            state="readonly",
            font=ctk.CTkFont(size=12)
        )
        self.file_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # Browse button
        browse_btn = ctk.CTkButton(
            file_frame,
            text="📁 Browse",
            width=100,
            command=self._browse_file
        )
        browse_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Analyze button
        self.analyze_btn = ctk.CTkButton(
            file_frame,
            text="🔍 Analyze",
            width=100,
            command=self._start_analysis,
            state="disabled",
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.analyze_btn.grid(row=0, column=3, padx=10, pady=10)
    
    def _create_results_area(self):
        """Create the scrollable results area."""
        # Results frame
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Results header
        results_label = ctk.CTkLabel(
            results_frame,
            text="Analysis Results",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Scrollable text area
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.results_text.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        
        # Initial message
        self._update_results(self._get_welcome_message())
    
    def _create_action_buttons(self):
        """Create the action buttons section."""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Export ZIP button
        self.export_btn = ctk.CTkButton(
            action_frame,
            text="📦 Export ZIP",
            width=150,
            command=self._export_zip,
            state="disabled"
        )
        self.export_btn.pack(side="left", padx=(0, 10))
        
        # Open output folder button
        self.open_folder_btn = ctk.CTkButton(
            action_frame,
            text="📂 Open Output Folder",
            width=150,
            command=self._open_output_folder,
            state="disabled",
            fg_color="gray40",
            hover_color="gray50"
        )
        self.open_folder_btn.pack(side="left", padx=(0, 10))
        
        # Help button
        help_btn = ctk.CTkButton(
            action_frame,
            text="❓ Help",
            width=80,
            command=self._show_help,
            fg_color="gray40",
            hover_color="gray50"
        )
        help_btn.pack(side="right")
        
        # About button
        about_btn = ctk.CTkButton(
            action_frame,
            text="ℹ️ About",
            width=80,
            command=self._show_about,
            fg_color="gray40",
            hover_color="gray50"
        )
        about_btn.pack(side="right", padx=(0, 10))
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=11),
            anchor="w",
            text_color="gray"
        )
        self.status_bar.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        # Progress bar (hidden by default)
        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
    
    def _get_welcome_message(self) -> str:
        """Get the welcome message for the results area."""
        return """Welcome to BSSOD Analyzer Parser Tool!

This tool extracts diagnostic information from Windows memory dump files 
(.DMP files) for AI-powered analysis.

HOW TO USE:
────────────────────────────────────────────────────────────────────────────
1. Click "Browse" to select a memory dump file (MEMORY.DMP)
2. Click "Analyze" to extract diagnostic data
3. Click "Export ZIP" to create a ZIP file for upload
4. Upload the ZIP file to the BSSOD Analyzer website for AI analysis

WHERE TO FIND DUMP FILES:
────────────────────────────────────────────────────────────────────────────
• Full dumps: C:\\Windows\\MEMORY.DMP
• Minidumps: C:\\Windows\\Minidump\\*.dmp
• LiveKernelReports: C:\\Windows\\LiveKernelReports\\*.dmp

SUPPORTED DUMP TYPES:
────────────────────────────────────────────────────────────────────────────
• Full Memory Dump (Complete)
• Kernel Memory Dump
• Automatic Memory Dump
• Small Memory Dump (Minidump)
• Live Kernel Dump

PRIVACY:
────────────────────────────────────────────────────────────────────────────
Only technical diagnostic data is extracted. No personal files, passwords,
or sensitive information is included in the export.
"""
    
    def _update_results(self, text: str):
        """Update the results text area."""
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
        self.results_text.configure(state="disabled")
    
    def _set_status(self, message: str):
        """Update the status bar."""
        self.status_bar.configure(text=message)
    
    def _browse_file(self):
        """Open file browser to select a dump file."""
        filetypes = [
            ("Memory Dump Files", "*.dmp"),
            ("All Files", "*.*")
        ]
        
        # Start in Windows directory if accessible
        initial_dir = "C:\\Windows" if os.path.exists("C:\\Windows") else os.path.expanduser("~")
        
        filepath = filedialog.askopenfilename(
            title="Select Memory Dump File",
            filetypes=filetypes,
            initialdir=initial_dir
        )
        
        if filepath:
            self.dump_path = filepath
            self.file_entry.configure(state="normal")
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, filepath)
            self.file_entry.configure(state="readonly")
            self.analyze_btn.configure(state="normal")
            
            # Get file size
            size_bytes = os.path.getsize(filepath)
            size_str = self._format_size(size_bytes)
            self._set_status(f"Selected: {os.path.basename(filepath)} ({size_str})")
    
    def _format_size(self, size: int) -> str:
        """Format size in human-readable format."""
        if size >= 1024 ** 3:
            return f"{size / (1024 ** 3):.2f} GB"
        elif size >= 1024 ** 2:
            return f"{size / (1024 ** 2):.2f} MB"
        elif size >= 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size} bytes"
    
    def _start_analysis(self):
        """Start the analysis in a separate thread."""
        if not self.dump_path or self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analyze_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        self.open_folder_btn.configure(state="disabled")
        
        # Show progress
        self.progress_bar.grid(row=4, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.progress_bar.start()
        self._set_status("Analyzing dump file... This may take a moment.")
        self._update_results("🔄 Analyzing dump file...\n\nPlease wait while the dump file is being processed.")
        
        # Run analysis in thread
        thread = threading.Thread(target=self._run_analysis, daemon=True)
        thread.start()
    
    def _run_analysis(self):
        """Run the analysis (called in a separate thread)."""
        try:
            analyzer = DumpAnalyzer(self.dump_path)
            self.analysis_result = analyzer.analyze()
            
            # Update UI from main thread
            self.after(0, self._analysis_complete)
            
        except Exception as e:
            self.after(0, lambda: self._analysis_error(str(e)))
    
    def _analysis_complete(self):
        """Called when analysis is complete."""
        self.is_analyzing = False
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        
        if self.analysis_result and self.analysis_result.success:
            # Enable buttons
            self.analyze_btn.configure(state="normal")
            self.export_btn.configure(state="normal")
            
            # Display results
            results_text = self._format_analysis_results()
            self._update_results(results_text)
            self._set_status(f"Analysis complete! Duration: {self.analysis_result.metadata.analysis_duration_seconds:.2f}s")
        else:
            self.analyze_btn.configure(state="normal")
            error_msg = self.analysis_result.error if self.analysis_result else "Unknown error"
            self._update_results(f"❌ Analysis failed:\n\n{error_msg}")
            self._set_status("Analysis failed")
    
    def _analysis_error(self, error: str):
        """Called when analysis encounters an error."""
        self.is_analyzing = False
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.analyze_btn.configure(state="normal")
        
        self._update_results(f"❌ Error during analysis:\n\n{error}")
        self._set_status("Analysis error")
        messagebox.showerror("Analysis Error", f"An error occurred:\n\n{error}")
    
    def _format_analysis_results(self) -> str:
        """Format the analysis results for display."""
        if not self.analysis_result:
            return "No analysis results available."
        
        lines = []
        lines.append("✅ ANALYSIS COMPLETE")
        lines.append("═" * 70)
        lines.append("")
        
        # System Info
        if self.analysis_result.system_info:
            si = self.analysis_result.system_info
            lines.append("📋 SYSTEM INFORMATION")
            lines.append("─" * 70)
            lines.append(f"  OS Version:    {si.os_version}")
            lines.append(f"  Architecture:  {si.architecture}")
            lines.append(f"  Processors:    {si.processor_count}")
            lines.append(f"  Dump Type:     {si.dump_type}")
            lines.append(f"  Dump Size:     {si.dump_size_human}")
            lines.append("")
        
        # Crash Summary
        if self.analysis_result.crash_summary:
            cs = self.analysis_result.crash_summary
            lines.append("💥 CRASH INFORMATION")
            lines.append("─" * 70)
            lines.append(f"  Bugcheck Code: {cs.bugcheck_code}")
            lines.append(f"  Bugcheck Name: {cs.bugcheck_name}")
            lines.append("")
            lines.append("  Parameters:")
            lines.append(f"    P1: {cs.parameter1}")
            lines.append(f"    P2: {cs.parameter2}")
            lines.append(f"    P3: {cs.parameter3}")
            lines.append(f"    P4: {cs.parameter4}")
            lines.append("")
        
        # Bugcheck Analysis
        if self.analysis_result.bugcheck_analysis:
            ba = self.analysis_result.bugcheck_analysis
            lines.append("🔍 BUGCHECK ANALYSIS")
            lines.append("─" * 70)
            lines.append(f"  Category: {ba.category}")
            lines.append(f"  Severity: {ba.severity}")
            lines.append(f"  Description: {ba.description}")
            lines.append("")
            
            if ba.parameters:
                lines.append("  Parameter Interpretation:")
                for p in ba.parameters:
                    lines.append(f"    Param {p.parameter_number}: {p.description}")
                    if p.interpretation:
                        lines.append(f"      → {p.interpretation}")
                lines.append("")
            
            if ba.likely_causes:
                lines.append("  Likely Causes:")
                for cause in ba.likely_causes:
                    lines.append(f"    • {cause}")
                lines.append("")
            
            if ba.recommendations:
                lines.append("  Recommendations:")
                for rec in ba.recommendations:
                    lines.append(f"    → {rec}")
                lines.append("")
        
        # Notes
        if self.analysis_result.metadata.parser_notes:
            lines.append("📝 NOTES")
            lines.append("─" * 70)
            for note in self.analysis_result.metadata.parser_notes:
                lines.append(f"  • {note}")
            lines.append("")
        
        # Next steps
        lines.append("═" * 70)
        lines.append("📦 NEXT STEPS")
        lines.append("─" * 70)
        lines.append("  1. Click 'Export ZIP' to create an analysis package")
        lines.append("  2. Upload the ZIP to the BSSOD Analyzer website")
        lines.append("  3. Get detailed AI-powered analysis and recommendations")
        lines.append("")
        
        return "\n".join(lines)
    
    def _export_zip(self):
        """Export the analysis to a ZIP file."""
        if not self.analysis_result:
            messagebox.showwarning("No Analysis", "Please analyze a dump file first.")
            return
        
        # Ask for save location
        default_name = f"BSOD_Analysis_{Path(self.dump_path).stem}.zip"
        filepath = filedialog.asksaveasfilename(
            title="Save Analysis ZIP",
            defaultextension=".zip",
            filetypes=[("ZIP Files", "*.zip")],
            initialfile=default_name
        )
        
        if filepath:
            try:
                from parser.analyzer import create_analysis_zip
                
                # Create ZIP in the specified location
                output_dir = os.path.dirname(filepath)
                self.zip_path = create_analysis_zip(self.analysis_result, output_dir)
                
                # Rename if needed
                if os.path.basename(self.zip_path) != os.path.basename(filepath):
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    os.rename(self.zip_path, filepath)
                    self.zip_path = filepath
                
                self.open_folder_btn.configure(state="normal")
                self._set_status(f"ZIP exported: {os.path.basename(self.zip_path)}")
                
                # Show success message
                size_str = self._format_size(os.path.getsize(self.zip_path))
                messagebox.showinfo(
                    "Export Successful",
                    f"Analysis exported successfully!\n\n"
                    f"File: {os.path.basename(self.zip_path)}\n"
                    f"Size: {size_str}\n\n"
                    f"Upload this file to the BSSOD Analyzer website for AI analysis."
                )
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export ZIP:\n\n{e}")
    
    def _open_output_folder(self):
        """Open the folder containing the exported ZIP."""
        if self.zip_path and os.path.exists(self.zip_path):
            folder = os.path.dirname(self.zip_path)
            os.startfile(folder)
        else:
            messagebox.showwarning("No Export", "Please export a ZIP file first.")
    
    def _show_help(self):
        """Show help dialog."""
        help_text = """BSSOD Analyzer Parser Tool - Help

This tool extracts diagnostic information from Windows memory dump files
for AI-powered analysis of Blue Screen of Death (BSOD) crashes.

STEPS TO USE:
1. Click 'Browse' to select a memory dump file
2. Click 'Analyze' to extract diagnostic data
3. Click 'Export ZIP' to save the analysis
4. Upload the ZIP to the BSSOD Analyzer website

FINDING DUMP FILES:
• Full dumps: C:\\Windows\\MEMORY.DMP
• Minidumps: C:\\Windows\\Minidump\\
• Live dumps: C:\\Windows\\LiveKernelReports\\

Note: Administrator access may be required to read dump files.

PRIVACY:
Only technical crash data is extracted. No personal files,
passwords, or browsing history is included."""
        
        messagebox.showinfo("Help", help_text)
    
    def _show_about(self):
        """Show about dialog."""
        about_text = f"""{self.APP_NAME}
Version {self.APP_VERSION}

An AI-powered tool for analyzing Windows Blue Screen crashes.

Part of the BSSOD - Blue-Screen Solution Oriented Diagnostics project.

This tool extracts diagnostic data from memory dump files locally,
ensuring privacy while enabling detailed AI analysis.

© 2026 BSSOD Analyzer Project"""
        
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point for the application."""
    app = BSODAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
