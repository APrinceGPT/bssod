# BSSOD - Blue-Screen Solution Oriented Diagnostics

An AI-powered Windows crash dump analyzer that helps users understand and fix Blue Screen of Death (BSOD) errors.

## 🎯 Overview

BSSOD Analyzer is a complete solution for diagnosing Windows crashes:

1. **Parser Tool** (Desktop) - Extracts diagnostic data locally from memory dump files
2. **Backend API** (FastAPI) - Processes uploads and integrates with AI
3. **Website** (Next.js) - Modern web interface with **structured AI analysis**

### ✨ AI-Powered Features

- **Severity Classification** - Crashes rated critical/high/medium/low with color-coded badges
- **Confidence Scoring** - AI indicates certainty level (0-100%) with visual meter
- **Executive Summaries** - Non-technical 1-2 sentence explanations
- **Root Cause Analysis** - Detailed breakdown with affected component identification
- **Prioritized Fix Steps** - Numbered recommendations with priority levels
- **Prevention Tips** - Actionable advice to prevent future crashes

## 📦 Project Structure

```
MemoryDumper/
├── parser-tool/        # Phase 1: Desktop parser application
│   ├── gui_app.py      # GUI application
│   ├── src/parser/     # Core parsing modules
│   └── dist/           # Standalone executable
├── backend/            # Phase 2: FastAPI backend API
│   ├── src/
│   │   ├── api/        # API routes
│   │   ├── models/     # Pydantic schemas
│   │   ├── services/   # Business logic
│   │   ├── config.py   # Configuration
│   │   └── main.py     # FastAPI app
│   └── tests/          # Backend tests
├── frontend/           # Phase 3: Next.js website
│   ├── src/
│   │   ├── app/        # Next.js App Router pages
│   │   ├── components/ # React components
│   │   ├── context/    # React context
│   │   ├── lib/        # API service layer
│   │   └── types/      # TypeScript definitions
│   └── package.json
├── docs/               # Project documentation
│   └── feasibility_study.md
└── .env                # Environment configuration
```

## 🚀 Quick Start

### Parser Tool (Phase 1)

Download and run the standalone executable - no installation required:

```
parser-tool/dist/BSSOD_Analyzer_Parser.exe
```

Or run from source:
```bash
cd parser-tool
pip install -r requirements.txt
python gui_app.py
```

### Backend API (Phase 2)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --host 127.0.0.1 --port 8080
```

API endpoints:
- `GET /` - API info
- `GET /api/v1/health` - Health check
- `POST /api/v1/analyze` - Upload ZIP for AI analysis

### Frontend Website (Phase 3)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
# AI Configuration
OPENAI_BASE_URL=https://api.rdsec.trendmicro.com/prod/aiendpoint/v1/
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=claude-4-sonnet

# Server Configuration
HOST=0.0.0.0
PORT=8080
DEBUG=false

# CORS
CORS_ORIGINS=http://localhost:3000

# Upload limits
MAX_UPLOAD_SIZE_MB=50
```

## 📋 Development Progress

| Phase | Component | Status | Description |
|-------|-----------|--------|-------------|
| 1 | Parser Tool | ✅ Complete | Desktop app for local dump parsing |
| 2 | Backend API | ✅ Complete | FastAPI with AI integration |
| 3 | Frontend | ✅ Complete | Next.js website with shadcn/ui |
| 4 | Integration | ✅ Complete | Full system integration |
| 5 | Enhancements | ✅ Complete | UX/DX improvements |
| 6 | AI Intelligence | 🔄 In Progress | Advanced AI capabilities |

### Enhancement Progress

| Phase | Focus Area | Status |
|-------|------------|--------|
| Phase 1 | Critical UX Fixes | ✅ Complete |
| Phase 2 | Backend Robustness | ✅ Complete |
| Phase 3 | Polish & Accessibility | ✅ Complete |
| Phase 4 | Quality & Testing | ✅ Complete |

### AI Enhancement Progress

| Phase | Focus Area | Status |
|-------|------------|--------|
| AI-1 | Structured Intelligence | ✅ Complete |
| AI-2 | Smart Prompting | 🔲 Planned |
| AI-3 | Interactive Chat | 🔲 Planned |

See [Enhancement Assessment](docs/enhancement_assessment.md) and [AI Enhancement Assessment](docs/ai_enhancement_assessment.md) for details.

## 🚀 Running the Full Stack

### 1. Start the Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --host 127.0.0.1 --port 8080
```

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Open the App
Navigate to http://localhost:3000 in your browser.

## 🧪 Running Tests

### Parser Tool Tests
```bash
cd parser-tool
python test_kdmp.py
```

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Build Test
```bash
cd frontend
npm run build
```

## 🔒 Privacy First

- All dump parsing happens **locally** on your machine
- Only extracted diagnostic data is uploaded (never the raw dump file)
- No personal files, passwords, or browsing history is extracted
- Technical crash data only: bugcheck codes, driver info, stack traces

## 📊 Supported Dump Types

| Type | Support |
|------|---------|
| Full Memory Dump | ✅ |
| Kernel Memory Dump | ✅ |
| Automatic Memory Dump | ✅ |
| Small Memory Dump (Minidump) | ✅ |
| Live Kernel Dump | ✅ |

## ⚠️ Known Limitations

- **Driver enumeration**: Full driver list requires virtual address translation; basic detection provided
- **Symbol resolution**: Full stack traces require PDB debug symbols
- **Live dumps**: Some fields may be empty as system was still running

## 🤝 Contributing

Please ensure:
- All tests pass before submitting
- Code follows modular structure (max 500 lines per file)
- No unused imports or dead code
- No graceful degradation - report limitations explicitly

## 📄 License

BSSOD - Blue-Screen Solution Oriented Diagnostics Project

---

## 📚 Documentation

- [Feasibility Study](docs/BSSOD_Feasibility_Study.md)
- [Enhancement Assessment](docs/enhancement_assessment.md)
- [AI Enhancement Assessment](docs/ai_enhancement_assessment.md)
- [Parser Tool README](parser-tool/README.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
