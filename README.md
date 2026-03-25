# DSA Mentor — AI Interview Prep

An agentic AI application for personalized Data Structures & Algorithms interview preparation. DSA Mentor generates adaptive 90-day learning roadmaps, teaches concepts through AI-powered lessons, reviews your code, and tracks long-term retention with spaced repetition — all driven by 10+ specialized AI agents.

## Features

### Adaptive Learning Roadmap
AI-generated 90-day curriculum tailored to your experience level, daily availability, and target company. Topics unlock progressively based on prerequisite mastery, and the roadmap adapts as you learn.

### Daily Study Plans
Each day you get a personalized plan: a concept lesson, warm-up exercises, graded practice problems (easy to hard), and review items — all scheduled to fit your available hours.

### Problem Practice with AI Feedback
300+ LeetCode problems organized by topic with:
- **Progressive hints** — 3 levels from subtle nudge to detailed walkthrough
- **AI code review** — correctness, complexity analysis, strengths, improvements
- **In-browser Python execution** — run and test code directly via Pyodide (no server needed)
- **Pattern recognition** — identifies which algorithmic patterns apply to each problem

### FAANG 75 Crash Course
75 of the most frequently asked interview problems across 15 algorithmic patterns (two pointers, sliding window, binary search, BFS/DFS, DP, and more). Includes story-based pattern teaching, step-by-step walkthroughs, and mastery tracking.

### Spaced Repetition (SM-2)
Review cards scheduled using the SuperMemo 2 algorithm. Rate your recall quality (0-5) and the system automatically adjusts intervals, tracks mastery decay, and surfaces cards due for review.

### Interactive Skill Tree
SVG-based graph visualization of all DSA topics with pan/zoom. Nodes are color-coded by status (locked, available, in-progress, completed, mastered). Click edges for bridge lessons that explain how topics connect.

### Algorithm Visualizer
15+ animated visualizations covering arrays, linked lists, trees, graphs, sorting, binary search, two pointers, sliding window, hash maps, stacks, queues, heaps, DP, and more — with play/pause/step controls.

### AI Mentor Chat
Ask questions about any DSA topic and get detailed explanations with code examples, visualizations, and follow-up suggestions. Context-aware when used from the practice page.

### Learning Statistics
Track problems solved by difficulty, current/max streak, average solve times, XP, level, topics mastered, and weak areas — all displayed on a dashboard with charts.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite, Tailwind CSS 4, React Router 7 |
| Backend | FastAPI, SQLAlchemy 2 (async), SQLite |
| AI/LLM | Multi-provider (NVIDIA NIM, Ollama, Dell AIA) via OpenAI-compatible API |
| Visualizations | Recharts, custom SVG/Canvas |
| Code Execution | Pyodide (in-browser Python via WebAssembly) |
| Code Highlighting | react-syntax-highlighter (Prism) |
| Icons | Lucide React |

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- One of the supported LLM providers (see below)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd dsa-mentor

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # then edit .env with your LLM provider settings
python main.py          # starts on http://localhost:8000

# Frontend (in a separate terminal)
cd frontend
npm install
npm run dev             # starts on http://localhost:5173
```

The frontend dev server proxies `/api` requests to the backend automatically. The database (SQLite) is created on first startup — no setup required.

### Production Build

```bash
# Build the frontend
cd frontend
npm run build           # outputs to frontend/dist/

# The backend serves the built frontend as static files
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## LLM Provider Configuration

DSA Mentor supports three LLM providers. Set `LLM_PROVIDER` in `backend/.env` to choose one:

| Provider | `LLM_PROVIDER` | Description |
|----------|----------------|-------------|
| NVIDIA NIM | `nvidia` | NVIDIA cloud API (DeepSeek, Llama, etc.) |
| Ollama | `ollama` | Run models locally via Ollama |
| Dell AIA | `dell` | Dell enterprise LLM via SSO/OAuth |

### Option 1 — NVIDIA NIM (default)

```env
LLM_PROVIDER=nvidia
NVIDIA_API_KEY=nvapi-your-key-here
NVIDIA_MODEL=deepseek-ai/deepseek-v3.2
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_ENABLE_THINKING=true
```

### Option 2 — Ollama (local)

1. Install Ollama: https://ollama.com
2. Pull a model: `ollama pull qwen2.5:3b`
3. Configure:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### Option 3 — Dell AIA Gateway

```env
LLM_PROVIDER=dell
DELL_LLM_MODEL=gpt-oss-120b
DELL_LLM_BASE_URL=https://aia.gateway.dell.com/genai/dev/v1
USE_SSO=true
```

### Switching Providers at Runtime

You can switch providers without restarting the server:

```bash
# List available providers
curl http://localhost:8000/api/settings/providers

# Switch to ollama
curl -X POST http://localhost:8000/api/settings/provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "ollama"}'

# Switch to nvidia
curl -X POST http://localhost:8000/api/settings/provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "nvidia"}'

# Test the active provider
curl http://localhost:8000/api/settings/provider/test
```

## Architecture

### AI Agents

The backend uses 10+ specialized AI agents, each with a focused responsibility:

| Agent | Purpose |
|-------|---------|
| Roadmap Agent | Generates and adapts personalized 90-day learning plans |
| Teaching Agent | Creates comprehensive concept lessons with code examples |
| Assessment Agent | Reviews submitted code for correctness, complexity, and style |
| Hint Agent | Provides 3-level progressive hints (nudge, approach, strategy) |
| Bridge Lesson Agent | Explains connections between prerequisite and next topics |
| Review Card Agent | Generates spaced repetition quiz questions |
| Chat Agent | Handles general DSA Q&A with context-aware responses |
| Daily Plan Agent | Creates personalized daily study schedules |
| Pattern Analysis Agent | Identifies patterns in user code vs. optimal approach |
| FAANG Story Agent | Teaches patterns through narrative explanations |

### API Endpoints

The backend exposes 50+ endpoints across 11 route modules:

| Prefix | Purpose |
|--------|---------|
| `/api/users` | User profile management |
| `/api/roadmap` | Roadmap generation and topic tracking |
| `/api/problems` | Problem catalog, submissions, hints, AI review |
| `/api/daily-plan` | Daily plans and concept lessons |
| `/api/chat` | AI mentor conversations |
| `/api/stats` | Learning statistics and progress |
| `/api/skill-tree` | Skill tree graph and bridge lessons |
| `/api/review` | Spaced repetition queue and scheduling |
| `/api/videos` | Video search and recommendations |
| `/api/patterns` | Pattern catalog, matching, and code analysis |
| `/api/faang-prep` | FAANG 75 course, stories, and milestones |

Swagger/OpenAPI docs are available at `http://localhost:8000/docs` when the backend is running.

### Project Structure

```
dsa-mentor/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Environment and app configuration
│   ├── database.py              # Async SQLAlchemy setup
│   ├── models.py                # ORM models (10 tables)
│   ├── agents.py                # AI agent implementations
│   ├── llm_client.py            # Multi-provider LLM client
│   ├── spaced_repetition.py     # SM-2 algorithm
│   ├── pattern_engine.py        # Pattern catalog and matching
│   ├── dsa_knowledge.py         # DSA curriculum (50+ topics)
│   ├── faang_questions.py       # FAANG 75 problem set
│   ├── topic_dependencies.py    # Prerequisite graph
│   └── routes/                  # API route handlers
│       ├── users.py
│       ├── roadmap.py
│       ├── problems.py
│       ├── daily_plan.py
│       ├── chat.py
│       ├── stats.py
│       ├── skill_tree.py
│       ├── review.py
│       ├── videos.py
│       ├── patterns.py
│       ├── faang_prep.py
│       └── settings.py
├── frontend/
│   ├── src/
│   │   ├── main.jsx             # React entry point
│   │   ├── App.jsx              # Router configuration
│   │   ├── api/client.js        # API client (50+ endpoints)
│   │   ├── hooks/useUser.js     # User state management
│   │   ├── components/
│   │   │   ├── Layout.jsx       # Sidebar navigation
│   │   │   ├── CodeRunner.jsx   # Pyodide-based code executor
│   │   │   └── PatternCard.jsx  # Pattern recognition cards
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Onboarding.jsx
│   │   │   ├── RoadmapPage.jsx
│   │   │   ├── DailyPlanPage.jsx
│   │   │   ├── PracticePage.jsx
│   │   │   ├── LearnPage.jsx
│   │   │   ├── SkillTreePage.jsx
│   │   │   ├── ReviewQueuePage.jsx
│   │   │   ├── FAANGPrepPage.jsx
│   │   │   └── ChatPage.jsx
│   │   └── visualizations/
│   │       └── AlgorithmVisualizer.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## License

This project is for educational and personal use.
