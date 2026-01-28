# BSSOD Analyzer Backend API

FastAPI backend for processing memory dump analysis and AI integration.

## 🎯 Purpose

This API receives ZIP exports from the Parser Tool and provides AI-powered crash analysis using Claude 4 Sonnet via Trend Micro's endpoint.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn src.main:app --host 127.0.0.1 --port 8080

# Or with auto-reload for development
python -m uvicorn src.main:app --host 127.0.0.1 --port 8080 --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and documentation links |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/analyze` | Upload ZIP file for AI analysis |

### POST /api/v1/analyze

Upload a ZIP file exported from the Parser Tool.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` - ZIP file containing `analysis.json`

**Response:**
```json
{
  "success": true,
  "message": "Analysis completed successfully",
  "dump_file": "MEMORY.DMP",
  "bugcheck_code": "0x0000001A",
  "bugcheck_name": "MEMORY_MANAGEMENT",
  "ai_analysis": {
    "analysis": "Full AI analysis text...",
    "model": "claude-4-sonnet",
    "tokens_used": 1234
  }
}
```

## 🔧 Configuration

Create a `.env` file in the `backend` directory or project root:

```env
# AI Configuration (Required)
OPENAI_BASE_URL=https://api.rdsec.trendmicro.com/prod/aiendpoint/v1/
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=claude-4-sonnet
AI_TIMEOUT=120.0

# Server Configuration
HOST=0.0.0.0
PORT=8080
DEBUG=false

# CORS
CORS_ORIGINS=http://localhost:3000

# Upload limits
MAX_UPLOAD_SIZE_MB=50
```

## 📁 Project Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py       # AI API integration
│   │   ├── prompt_engineering.py # AI prompt formatting
│   │   └── zip_validator.py    # ZIP validation
│   ├── __init__.py
│   ├── config.py               # Configuration
│   └── main.py                 # FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_backend.py         # Unit tests
├── .env                        # Environment variables
├── .env.example                # Example configuration
└── requirements.txt            # Python dependencies
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src
```

**Current Test Status:** 10/10 passing ✅

## 📋 Dependencies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **python-dotenv** - Environment variables
- **python-multipart** - File uploads
- **pytest** - Testing

## 🔒 Security

- API key stored in environment variables (never in code)
- File size limits enforced
- ZIP content validation
- CORS configuration for frontend

## ⚠️ Limitations

- Maximum file upload: 50 MB (configurable)
- AI response timeout: 120 seconds (configurable)
- Session-only approach (no database persistence)

## 📊 Module Line Counts

| File | Lines | Status |
|------|-------|--------|
| config.py | 86 | ✅ |
| main.py | 58 | ✅ |
| routes.py | 117 | ✅ |
| schemas.py | 157 | ✅ |
| ai_service.py | 167 | ✅ |
| prompt_engineering.py | 225 | ✅ |
| zip_validator.py | 134 | ✅ |

All modules under 500 lines ✅

---

See the [main project README](../README.md) for full project documentation.
