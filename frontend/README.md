# BSSOD Frontend

Web application for the BSSOD (Blue-Screen Solution Oriented Diagnostics) project. Built with Next.js 14, TypeScript, Tailwind CSS, and shadcn/ui.

## Overview

This frontend provides:
- Landing page explaining the BSSOD workflow
- File upload interface for ZIP files from the parser tool
- AI analysis results display with markdown rendering
- Export functionality (JSON, Markdown, Clipboard)

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS 4
- **UI Components:** shadcn/ui
- **Icons:** Lucide React

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout with header/footer
│   │   ├── page.tsx            # Landing page
│   │   ├── upload/
│   │   │   └── page.tsx        # File upload page
│   │   └── results/
│   │       └── page.tsx        # Analysis results page
│   ├── components/
│   │   ├── layout/             # Header, Footer
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── upload/             # File dropzone component
│   │   └── results/            # Results display components
│   ├── context/
│   │   └── analysis-context.tsx # React context for analysis state
│   ├── lib/
│   │   ├── api.ts              # API service layer
│   │   ├── constants.ts        # Centralized configuration constants
│   │   ├── error-messages.ts   # User-friendly error mapping
│   │   └── utils.ts            # Utility functions
│   └── types/
│       └── index.ts            # TypeScript type definitions
├── .env.local                  # Local environment variables
├── .env.example                # Environment variables template
└── package.json
```

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local with your settings
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8080` |
| `NEXT_PUBLIC_PARSER_DOWNLOAD_URL` | Parser tool download URL | `/downloads/BSSOD_Analyzer_Parser.exe` |

## Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run linting
npm run lint
```

## Pages

### Landing Page (`/`)

- Hero section with project branding
- How It Works section (3-step process)
- Features section
- Call-to-action buttons

### Upload Page (`/upload`)

- Drag-and-drop file upload
- ZIP file validation (type and size)
- Client-side file size limit (50 MB)
- Upload progress tracking with phased messages
- User-friendly error handling with suggestions

### Results Page (`/results`)

- Session warning alert
- Crash summary with bugcheck info
- AI analysis with markdown rendering
- Export actions (JSON, Markdown, Copy)

## Session-Only Design

Results are stored in React context (browser memory) only:
- No server-side storage
- No cookies or localStorage
- Page refresh clears results
- Users must export before leaving

This design ensures privacy - no crash data is persisted.

## API Integration

The frontend communicates with the backend API:

```
POST /api/v1/analyze
- Accepts: multipart/form-data with ZIP file
- Returns: AnalyzeResponse with AI analysis
```

## Components

### UI Components (shadcn/ui)

- Button, Card, Alert, Badge
- Progress, Separator, Tabs
- Accordion, Collapsible, Sheet

### Results Components

- `FloatingChat` - Floating AI chat drawer (bottom-right)
- `TabPanels` - Tab content components (Overview, Root Cause, Fix Steps, Prevention, Export)
- `ExecutiveSummaryCard` - Summary with severity and confidence
- `RootCauseCard` - Root cause analysis with technical details
- `FixStepsList` - Prioritized fix recommendations
- `PreventionTipsCard` - Prevention tips list
- `SeverityBadge` - Color-coded severity indicator
- `ConfidenceMeter` - Confidence percentage display
- `MarkdownRenderer` - Simple markdown parser
- `ExportActions` - Export functionality

### Upload Components

- `FileDropzone` - Drag-and-drop file upload

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Output in .next/ directory
```

## Deployment

Deploy to any Next.js-compatible platform:

- Vercel (recommended)
- Netlify
- AWS Amplify
- Self-hosted with Node.js

## License

Part of the BSSOD project.
