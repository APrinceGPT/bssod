# BSSOD Technology Stack

Complete inventory of tools, libraries, frameworks, and dependencies used in the BSSOD project.

---

## 🏗️ Architecture Overview

| Layer | Technology | Version |
|-------|------------|---------|
| **Frontend** | Next.js (React) | 16.1.6 |
| **Backend** | FastAPI (Python) | 0.115+ |
| **Desktop App** | CustomTkinter (Python) | 5.2.2 |
| **AI Engine** | Claude 4 Sonnet | via API |
| **Styling** | Tailwind CSS | 4.x |
| **Component Library** | shadcn/ui + Radix UI | Latest |

---

## 🖥️ Frontend (Next.js)

### Core Framework
| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 16.1.6 | React framework with App Router |
| **React** | 19.2.3 | UI library |
| **React DOM** | 19.2.3 | React rendering for web |
| **TypeScript** | 5.x | Type-safe JavaScript |

### UI Components & Styling
| Library | Version | Purpose |
|---------|---------|---------|
| **Tailwind CSS** | 4.x | Utility-first CSS framework |
| **@tailwindcss/postcss** | 4.x | PostCSS integration for Tailwind v4 |
| **tw-animate-css** | 1.4.0 | Animation utilities |
| **tailwind-merge** | 3.4.0 | Merge Tailwind classes intelligently |
| **class-variance-authority** | 0.7.1 | Variant-based component styling |
| **clsx** | 2.1.1 | Conditional className utility |

### Radix UI (Headless Components)
| Component | Version | Purpose |
|-----------|---------|---------|
| **@radix-ui/react-accordion** | 1.2.12 | Expandable content sections |
| **@radix-ui/react-collapsible** | 1.1.12 | Collapsible panels |
| **@radix-ui/react-progress** | 1.1.8 | Progress indicators |
| **@radix-ui/react-separator** | 1.1.8 | Visual dividers |
| **@radix-ui/react-slot** | 1.2.4 | Polymorphic components |
| **@radix-ui/react-tabs** | 1.1.13 | Tab navigation |

### Icons & Notifications
| Library | Version | Purpose |
|---------|---------|---------|
| **lucide-react** | 0.563.0 | Icon library (500+ icons) |
| **sonner** | 2.0.7 | Toast notifications |

### Development & Testing
| Tool | Version | Purpose |
|------|---------|---------|
| **ESLint** | 9.x | Code linting |
| **eslint-config-next** | 16.1.6 | Next.js ESLint rules |
| **Jest** | 30.2.0 | Testing framework |
| **jest-environment-jsdom** | 30.2.0 | Browser environment for tests |
| **@testing-library/react** | 16.3.2 | React component testing |
| **@testing-library/jest-dom** | 6.9.1 | DOM matchers for Jest |
| **@testing-library/user-event** | 14.6.1 | User interaction simulation |
| **ts-jest** | 29.4.6 | TypeScript Jest transformer |
| **ts-node** | 10.9.2 | TypeScript execution |
| **babel-plugin-react-compiler** | 1.0.0 | React compiler optimization |

### Type Definitions
| Package | Purpose |
|---------|---------|
| **@types/node** | Node.js types |
| **@types/react** | React types |
| **@types/react-dom** | React DOM types |
| **@types/jest** | Jest types |

---

## ⚙️ Backend (FastAPI)

### Core Framework
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.115+ | Async Python web framework |
| **Uvicorn** | 0.30+ | ASGI server |
| **Python** | 3.11+ | Runtime |

### Data & Validation
| Library | Version | Purpose |
|---------|---------|---------|
| **Pydantic** | 2.9+ | Data validation & serialization |
| **python-multipart** | 0.0.12 | File upload handling |

### HTTP & API
| Library | Version | Purpose |
|---------|---------|---------|
| **httpx** | 0.27+ | Async HTTP client for AI API |

### Configuration
| Library | Version | Purpose |
|---------|---------|---------|
| **python-dotenv** | 1.0+ | Environment variable loading |

### Testing
| Library | Version | Purpose |
|---------|---------|---------|
| **pytest** | 8.0+ | Testing framework |
| **pytest-asyncio** | 0.24+ | Async test support |

---

## 🖱️ Parser Tool (Desktop)

### GUI Framework
| Technology | Version | Purpose |
|------------|---------|---------|
| **CustomTkinter** | 5.2.2 | Modern Tkinter-based GUI |
| **Python** | 3.11+ | Runtime |

### Memory Parsing
| Technology | Purpose |
|------------|---------|
| **struct** (builtin) | Binary data parsing |
| **mmap** (builtin) | Memory-mapped file access |
| **io** (builtin) | Stream handling |

### Packaging
| Tool | Version | Purpose |
|------|---------|---------|
| **PyInstaller** | 6.11.1 | Standalone executable builder |

### Testing
| Library | Version | Purpose |
|---------|---------|---------|
| **pytest** | 8.3.4 | Testing framework |

---

## 🤖 AI Integration

| Technology | Details |
|------------|---------|
| **Model** | Claude 4 Sonnet |
| **Provider** | Trend Micro AI Endpoint |
| **Protocol** | OpenAI-compatible REST API |
| **Features** | Structured JSON output, conversation memory |

---

## 🛠️ Development Tools

### Version Control
| Tool | Purpose |
|------|---------|
| **Git** | Source control |
| **GitHub** | Repository hosting |

### IDE & Extensions
| Tool | Purpose |
|------|---------|
| **VS Code** | Primary IDE |
| **Pylance** | Python language server |
| **ESLint** | JavaScript/TypeScript linting |
| **Prettier** | Code formatting |

### Package Managers
| Tool | Platform | Purpose |
|------|----------|---------|
| **npm** | Frontend | Node.js package management |
| **pip** | Backend/Parser | Python package management |

---

## 📊 Skills Demonstrated

### Languages
- **TypeScript** - Strict mode, generics, type inference
- **Python** - Async/await, type hints, dataclasses
- **CSS** - Tailwind utility classes, responsive design

### Frontend Skills
- React 19 with hooks and context
- Next.js App Router architecture
- Server/Client component patterns
- Responsive design with dark mode
- Accessible UI with Radix primitives
- Component composition patterns

### Backend Skills
- RESTful API design
- Async request handling
- Pydantic validation schemas
- Error handling patterns
- File upload processing
- AI API integration

### Testing Skills
- Unit testing with Jest/pytest
- Component testing with Testing Library
- Async testing patterns
- Mock implementations

### DevOps Skills
- Environment configuration
- CORS configuration
- Build optimization
- Executable packaging

---

## 📦 Dependency Summary

| Category | Count |
|----------|-------|
| **Frontend Dependencies** | 14 |
| **Frontend DevDependencies** | 16 |
| **Backend Dependencies** | 8 |
| **Parser Dependencies** | 3 |
| **Total Packages** | ~41 |

---

## 🏷️ Portfolio Tags

```
React, Next.js, TypeScript, Python, FastAPI, Tailwind CSS, 
Radix UI, shadcn/ui, Claude AI, REST API, Pydantic, 
Jest, Testing Library, pytest, Git, VS Code
```

### Skill Categories
- **Frontend Development** - React, Next.js, TypeScript, Tailwind CSS
- **Backend Development** - Python, FastAPI, REST API, Async
- **AI/ML Integration** - LLM APIs, Prompt Engineering, Structured Output
- **Desktop Development** - Python GUI, Binary Parsing
- **Testing** - Unit Testing, Integration Testing, TDD
- **DevOps** - Git, Environment Config, Build Tools
