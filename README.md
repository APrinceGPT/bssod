<p align="center">
  <img src="https://img.shields.io/badge/Windows-BSOD%20Analyzer-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows BSOD Analyzer"/>
</p>

<h1 align="center">🔵 BSSOD</h1>
<h3 align="center">Blue-Screen Solution Oriented Diagnostics</h3>

<p align="center">
  <strong>AI-powered Windows crash dump analyzer that transforms cryptic Blue Screen errors into actionable solutions</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white" alt="Next.js"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Claude-4%20Sonnet-CC785C?style=flat-square&logo=anthropic&logoColor=white" alt="Claude 4"/>
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript"/>
</p>

<p align="center">
  <a href="#-key-features">Features</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-api-reference">API</a> •
  <a href="#-privacy">Privacy</a>
</p>

---

## 🎯 What is BSSOD?

**BSSOD** (Blue-Screen Solution Oriented Diagnostics) is a complete solution for diagnosing Windows Blue Screen of Death (BSOD) crashes. It combines **local memory dump parsing** with **AI-powered analysis** to help users understand what caused their system crash and how to fix it.

Unlike generic troubleshooting guides, BSSOD analyzes your specific crash dump and provides **personalized, prioritized solutions** based on the exact error codes, faulting drivers, and system context.

---

## ✨ Key Features

### 🤖 AI-Powered Analysis
| Feature | Description |
|---------|-------------|
| **Severity Classification** | Crashes rated as Critical/High/Medium/Low with color-coded badges |
| **Confidence Scoring** | AI indicates certainty level (0-100%) for its diagnosis |
| **Executive Summary** | Non-technical 1-2 sentence explanation anyone can understand |
| **Root Cause Analysis** | Detailed breakdown identifying the affected component |
| **Prioritized Fix Steps** | Numbered recommendations with priority levels |
| **Prevention Tips** | Actionable advice to prevent future crashes |
| **Interactive Chat** | Ask follow-up questions about the analysis |

### 🔒 Privacy-First Design
- All dump parsing happens **locally on your machine**
- Only extracted diagnostic data is uploaded (never raw dump files)
- No personal files, passwords, or browsing history extracted
- Technical crash data only: bugcheck codes, driver info, stack traces

### 📊 Comprehensive Dump Support
| Dump Type | Supported |
|-----------|-----------|
| Full Memory Dump | ✅ |
| Kernel Memory Dump | ✅ |
| Automatic Memory Dump | ✅ |
| Small Memory Dump (Minidump) | ✅ |
| Live Kernel Dump | ✅ |

---

## 🔄 How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Memory Dump    │────▶│  Parser Tool    │────▶│   ZIP Archive   │
│  (.DMP file)    │     │  (Local Parse)  │     │  (Safe data)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI Analysis   │◀────│  Backend API    │◀────│   Web Upload    │
│  (Claude 4)     │     │   (FastAPI)     │     │   (Next.js)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Structured Analysis Results                   │
│  • Severity & Confidence  • Root Cause  • Fix Steps  • Chat    │
└─────────────────────────────────────────────────────────────────┘
```

1. **Parse Locally**: Run the Parser Tool on your Windows machine to extract diagnostic data from the memory dump
2. **Upload Safely**: Upload the generated ZIP file (contains only crash metadata, not personal data)
3. **AI Analyzes**: Claude 4 Sonnet analyzes the crash context with specialized prompts
4. **Get Solutions**: Receive prioritized, actionable fix steps with confidence ratings

---

## 🚀 Quick Start

### Option 1: Use the Parser Tool (Recommended)

Download and run the standalone executable - no installation required:

```
parser-tool/dist/BSSOD_Analyzer_Parser.exe
```

### Option 2: Run the Full Stack

**1. Start the Backend**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --host 127.0.0.1 --port 8080
```

**2. Start the Frontend**
```bash
cd frontend
npm install
npm run dev
```

**3. Open the App**
Navigate to http://localhost:3000

---

## 🏗️ Architecture

BSSOD follows a **three-tier architecture** with clear separation of concerns:

```
┌────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Next.js 16 Frontend                                          │  │
│  │  • React 19 with App Router                                   │  │
│  │  • TypeScript strict mode                                     │  │
│  │  • Tailwind CSS v4 + shadcn/ui                               │  │
│  │  • Responsive design with dark mode                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────┐
│                          SERVICE LAYER                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend                                              │  │
│  │  • RESTful API with OpenAPI docs                             │  │
│  │  • Pydantic v2 validation                                     │  │
│  │  • Async request handling                                     │  │
│  │  • Structured error responses                                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  AI Service                                                   │  │
│  │  • Claude 4 Sonnet integration                               │  │
│  │  • Context-aware prompting                                    │  │
│  │  • Conversation memory                                        │  │
│  │  • Structured JSON output                                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Parser Tool (Desktop)                                        │  │
│  │  • Windows kernel dump parsing (kdmp-parser)                  │  │
│  │  • PE header analysis                                         │  │
│  │  • Driver enumeration                                         │  │
│  │  • Bugcheck code extraction                                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Parser Tool** | Python + PyQt6 | Local memory dump parsing with GUI |
| **Backend API** | FastAPI + Python 3.11+ | REST API, AI orchestration, file handling |
| **Frontend** | Next.js 16 + React 19 | Modern web UI with real-time updates |
| **AI Engine** | Claude 4 Sonnet | Crash analysis, solution generation, chat |

---

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and version |
| `GET` | `/api/v1/health` | Health check with AI status |
| `POST` | `/api/v1/analyze` | Upload ZIP for AI analysis |
| `POST` | `/api/v1/chat/start` | Start interactive chat session |
| `POST` | `/api/v1/chat` | Send follow-up question |

### Analysis Response Schema

```typescript
interface AnalysisResponse {
  success: boolean;
  bugcheck_code: string;      // e.g., "0x0000007E"
  bugcheck_name: string;      // e.g., "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED"
  dump_file: string;          // Original filename
  
  analysis: {
    severity: "critical" | "high" | "medium" | "low";
    confidence: number;       // 0-100
    executive_summary: string;
    
    root_cause: {
      summary: string;
      affected_component: string;
      technical_details: string;
    };
    
    fix_steps: Array<{
      step_number: number;
      title: string;
      description: string;
      priority: "critical" | "high" | "medium" | "low";
      technical_level: "beginner" | "intermediate" | "advanced";
    }>;
    
    prevention_tips: string[];
    additional_notes: string | null;
  };
}
```

---

## ⚙️ Configuration

Create a `.env` file in the project root:

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

---

## 🔒 Privacy

BSSOD is designed with privacy as a core principle:

| What's Collected | What's NOT Collected |
|------------------|---------------------|
| Bugcheck codes | Raw memory dump content |
| Driver names and versions | Personal files |
| Stack trace addresses | Passwords or credentials |
| System timestamp | Browser history |
| Processor context | User documents |

The Parser Tool runs **entirely locally** and only extracts technical crash metadata. The ZIP file uploaded to the analysis service contains no personal information.

---

## ⚠️ Known Limitations

| Limitation | Details |
|------------|---------|
| **Driver Enumeration** | Full driver list requires virtual address translation; basic detection provided |
| **Symbol Resolution** | Full stack traces require PDB debug symbols |
| **Live Dumps** | Some fields may be empty as system was still running |

---

## 📄 License

BSSOD - Blue-Screen Solution Oriented Diagnostics

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Development Progress](DEVELOPMENT.md) | Phase tracking and development notes |
| [Feasibility Study](docs/BSSOD_Feasibility_Study.md) | Initial research and technical planning |
| [Enhancement Assessment](docs/enhancement_assessment.md) | UX/DX improvement details |
| [AI Enhancement Assessment](docs/ai_enhancement_assessment.md) | AI capability breakdown |

---

<p align="center">
  <sub>Built with ❤️ for Windows crash debugging</sub>
</p>
