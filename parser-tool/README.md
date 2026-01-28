# BSSOD Analyzer Parser Tool

A Windows application for extracting diagnostic data from Windows memory dump files for AI-powered analysis.

## 🎯 Purpose

This tool extracts diagnostic information from Windows memory dump files (MEMORY.DMP) **locally on your machine**, ensuring your privacy. The extracted data can then be uploaded to the BSSOD Analyzer website for AI-powered crash analysis.

## ✨ Features

- **Privacy-First**: All parsing happens locally - no data leaves your computer during extraction
- **Easy to Use**: Simple GUI interface - just browse, analyze, and export
- **Comprehensive Analysis**: Extracts system info, bugcheck codes, stack traces, and driver info
- **AI-Ready Export**: Creates a ZIP file ready for upload to the AI analysis service
- **No Installation Required**: Standalone executable with no dependencies

## 📦 What Gets Extracted

| Data Type | Description |
|-----------|-------------|
| System Info | OS version, architecture, processor count |
| Crash Info | Bugcheck code, parameters, severity |
| Bugcheck Analysis | Human-readable explanation of the crash |
| Stack Trace | CPU register state (when available) |
| Driver Info | List of loaded drivers (when extractable) |

## 🚀 How to Use

### Option 1: Use the Standalone Executable

1. Download `BSSOD_Analyzer_Parser.exe` from the `dist` folder
2. Run the executable (no installation needed)
3. Click **Browse** to select a memory dump file
4. Click **Analyze** to extract diagnostic data
5. Click **Export ZIP** to save the analysis
6. Upload the ZIP file to the BSSOD Analyzer website

### Option 2: Run from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run the GUI
python gui_app.py

# Or use the batch file
run.bat
```

### Option 3: Command Line (for developers)

```python
from parser.analyzer import analyze_dump

# Analyze a dump file
analysis, zip_path = analyze_dump("C:\\Windows\\MEMORY.DMP", create_zip=True)

# Access the results
print(f"Bugcheck: {analysis.crash_summary.bugcheck_name}")
print(f"ZIP created: {zip_path}")
```

## 📍 Where to Find Dump Files

| Dump Type | Location |
|-----------|----------|
| Full/Kernel Dump | `C:\Windows\MEMORY.DMP` |
| Minidumps | `C:\Windows\Minidump\*.dmp` |
| Live Dumps | `C:\Windows\LiveKernelReports\*.dmp` |

> **Note**: Administrator privileges may be required to access dump files.

## 🔒 Privacy & Security

- ✅ All processing happens **locally** on your machine
- ✅ Only **technical diagnostic data** is extracted
- ❌ NO personal files or documents
- ❌ NO passwords or credentials
- ❌ NO browsing history
- ❌ The original dump file is NOT included in exports

## 📁 Project Structure

```
parser-tool/
├── gui_app.py          # Main GUI application
├── build.py            # Build script for executable
├── run.bat             # Windows launcher
├── requirements.txt    # Python dependencies
├── test_kdmp.py        # Test script
├── src/
│   ├── parser/         # Core parsing modules
│   │   ├── dump_reader.py   # Low-level binary parsing
│   │   ├── header.py        # Header extraction
│   │   ├── bugcheck.py      # Bugcheck analysis
│   │   ├── stack_trace.py   # Stack trace parsing
│   │   ├── drivers.py       # Driver extraction
│   │   └── analyzer.py      # Main orchestrator
│   └── utils/
│       └── constants.py     # Bugcheck codes database
├── dist/
│   └── BSSOD_Analyzer_Parser.exe  # Standalone executable
└── output/             # Default output directory
```

## 🛠️ Building the Executable

To build a new executable:

```bash
# Clean build
python build.py --clean-build

# The executable will be in dist/BSSOD_Analyzer_Parser.exe
```

## 📋 Supported Dump Types

- ✅ Full Memory Dump
- ✅ Kernel Memory Dump  
- ✅ Automatic Memory Dump
- ✅ Small Memory Dump (Minidump)
- ✅ Live Kernel Dump

## ⚠️ Limitations

- **Driver List**: Full driver enumeration requires virtual address translation. The tool provides basic driver detection and notes when WinDbg is needed for complete listings.
- **Stack Traces**: Full symbol resolution requires debug symbols (PDB files). Raw register state is captured.
- **Live Dumps**: Some fields may not be populated in live dumps as the system was still running.

## 🧪 Testing

Run the test suite:

```bash
python test_kdmp.py
```

### About test_kdmp.py

This is the **development test script** that validates all parsing modules work correctly. It:

1. **Tests each module independently** - DumpFileReader, HeaderParser, BugcheckAnalyzer, StackTraceParser, DriverListExtractor
2. **Tests the complete pipeline** - Full analysis with ZIP export
3. **Provides verbose output** - Shows extracted data in human-readable format
4. **Reports pass/fail status** - Clear indication of which tests succeeded

**When to run tests:**
- After modifying any parsing module
- Before building a new executable
- When testing with a new dump file

**Note:** Tests require a sample dump file at `d:\AI Project\MemoryDumper\MEMORY.DMP`. Modify the path in the test file if your dump is elsewhere.

---

## 📋 Changelog

### v1.0.0 (2026-01-29)
- Initial release
- Phase 1 complete: Parser Tool
- Features:
  - Binary parsing of Windows memory dumps (no external dependencies)
  - Bugcheck analysis with 60+ known codes
  - Stack trace and register state extraction
  - Driver detection (with noted limitations)
  - CustomTkinter GUI application
  - ZIP export for AI analysis upload
  - Standalone executable (22.54 MB)

---

## 🗺️ Roadmap

This is **Phase 1** of the BSSOD Analyzer project. Upcoming phases:

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Parser Tool (this) | ✅ Complete |
| Phase 2 | Backend API (FastAPI) | ✅ Complete |
| Phase 3 | Frontend Website (React/Next.js) | 🔜 Planned |
| Phase 4 | Integration & Testing | 🔜 Planned |

See the [main project README](../README.md) for more details.

---

## 📄 License

This project is part of the BSSOD - Blue-Screen Solution Oriented Diagnostics project.

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
- All tests pass before submitting
- Code follows the modular structure (max 500 lines per file)
- No unused imports or dead code
- No graceful degradation - report limitations explicitly
