# LearnPython — Full-Stack Python Learning Platform

A full-stack, mobile-first web application for learning Python from scratch. The backend is a Django REST Framework API that executes untrusted student code inside a hardened sandbox subprocess. The frontend is a React 18 + Vite SPA that renders structured lesson content, a syntax-highlighted code editor, and real-time execution output — all without requiring a user account.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [System Architecture](#3-system-architecture)
4. [Full Request Lifecycle](#4-full-request-lifecycle)
5. [Tech Stack](#5-tech-stack)
6. [Data Model](#6-data-model)
7. [API Reference](#7-api-reference)
8. [Sandboxed Code Execution](#8-sandboxed-code-execution)
9. [Progress Tracking](#9-progress-tracking)
10. [Local Development Setup](#10-local-development-setup)
11. [Environment Variables](#11-environment-variables)
12. [Database Seeding](#12-database-seeding)
13. [Deployment](#13-deployment)
14. [Security Model](#14-security-model)
15. [Curriculum Overview](#15-curriculum-overview)

---

## 1. Project Overview

LearnPython is structured as two completely independent services that share no runtime state:

- **Backend** (`/backend`) — A Django 5.2 project with a single `api` application. It exposes a RESTful JSON API, executes student-submitted Python code in an isolated subprocess, and serves the full course curriculum stored in a SQLite database. There is no authentication — every endpoint is public.
- **Frontend** (`/frontend`) — A React 18 + Vite SPA. It fetches content from the API, renders lesson material as Markdown, and provides a browser-based code editor backed by PrismJS syntax highlighting. Progress (which lessons are completed) is stored in `localStorage` — no server-side session is involved.

The two services are deployed independently: the backend on [Render](https://render.com) as a Python web service running behind Gunicorn/WSGI, and the frontend on [Vercel](https://vercel.com) as a static build with SPA rewrite rules.

---

## 2. Repository Structure

```
LearnPython/
├── README.md                   ← This file (root overview)
├── render.yaml                 ← Render CI/CD config for the backend service
│
├── backend/                    ← Django project root
│   ├── manage.py               ← Django management CLI
│   ├── Procfile                ← Gunicorn start command for Render
│   ├── requirements.txt        ← Python dependencies (pinned versions)
│   ├── db.sqlite3              ← SQLite database file (created on first migrate)
│   │
│   ├── sandbox.py              ← Subprocess-based code execution engine
│   ├── error_explainer.py      ← Regex-based Python error → plain-English translator
│   │
│   ├── learnpython/            ← Django project package
│   │   ├── settings.py         ← All configuration (env-driven)
│   │   ├── urls.py             ← Root URL dispatcher
│   │   ├── wsgi.py             ← WSGI entry point (used by Gunicorn)
│   │   └── asgi.py             ← ASGI entry point (unused, present for completeness)
│   │
│   └── api/                    ← The single Django application
│       ├── models.py           ← ORM models: Course, Lesson, Exercise
│       ├── serializers.py      ← DRF serializers defining API shapes
│       ├── views.py            ← All API view functions
│       ├── urls.py             ← App-level URL patterns
│       ├── admin.py            ← Django admin registration
│       ├── utils.py            ← Custom DRF exception handler
│       ├── migrations/         ← Auto-generated schema migrations
│       └── management/
│           └── commands/
│               └── seed.py     ← Custom management command to populate curriculum
│
└── frontend/                   ← React application
    ├── index.html              ← Vite HTML entry point
    ├── package.json            ← npm dependencies and scripts
    ├── vite.config.js          ← Vite configuration + dev proxy
    ├── vercel.json             ← SPA catch-all rewrite rule for Vercel
    └── src/
        ├── main.jsx            ← ReactDOM.createRoot entry point
        ├── App.jsx             ← BrowserRouter + all Route definitions
        ├── api.js              ← Centralised fetch wrapper + localStorage helpers
        ├── context/
        │   └── AuthContext.jsx ← Placeholder context (auth disabled)
        ├── components/
        │   ├── Header.jsx/css  ← Global nav bar
        │   ├── CodeEditor.jsx/css   ← PrismJS editor with Python-aware keyboard
        │   ├── OutputPanel.jsx/css  ← Execution output display
        │   ├── ContentBlock.jsx/css ← Lesson content renderer (Markdown + code)
        │   └── ExerciseCard.jsx/css ← Full exercise widget (run/submit/hint/solution)
        ├── pages/
        │   ├── HomePage.jsx/css
        │   ├── CoursesPage.jsx/css
        │   ├── LessonsPage.jsx/css
        │   ├── LessonPage.jsx/css
        │   ├── PlaygroundPage.jsx/css
        │   └── ProgressPage.jsx/css
        └── styles/
            └── global.css      ← CSS custom properties + base reset
```

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  Browser (React SPA — Vercel)                                       │
│                                                                     │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────┐               │
│  │  Pages   │→ │  Components  │→ │  api.js fetch  │               │
│  └──────────┘  └──────────────┘  └───────┬────────┘               │
│                                           │ HTTPS JSON              │
│                   ┌───────────────────────┘                         │
│                   ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Django + DRF (Render / Gunicorn)                           │   │
│  │                                                             │   │
│  │  learnpython/urls.py                                        │   │
│  │       ├── /api/  → api/urls.py → views.py                  │   │
│  │       └── /health, /                                        │   │
│  │                                                             │   │
│  │  views.py                                                   │   │
│  │       ├── list_courses      → CourseOutSerializer           │   │
│  │       ├── list_lessons      → manual dict list              │   │
│  │       ├── get_lesson        → LessonDetailSerializer        │   │
│  │       ├── get_exercise      → ExerciseOutSerializer         │   │
│  │       ├── get_solution      → plain dict                    │   │
│  │       ├── run_code          → sandbox.execute_code()        │   │
│  │       └── submit_exercise   → sandbox.run_exercise_tests()  │   │
│  │                                                             │   │
│  │  sandbox.py (code execution pipeline)                       │   │
│  │       ├── check_code_safety()  ← pattern & length checks    │   │
│  │       ├── WRAPPER_TEMPLATE     ← wraps code in try/except   │   │
│  │       └── _run_subprocess()   ← isolated Python process     │   │
│  │                         │                                   │   │
│  │                         ▼                                   │   │
│  │             ┌───────────────────────┐                       │   │
│  │             │  python <tmpfile.py>  │  ← child process      │   │
│  │             │  setrecursionlimit    │    killed after        │   │
│  │             │  resource limits      │    timeout             │   │
│  │             └───────────────────────┘                       │   │
│  │                                                             │   │
│  │  SQLite  ←  ORM  ←  models.py                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Full Request Lifecycle

### 4a. Loading a lesson page

1. User navigates to `/lessons/3`.
2. React Router renders `LessonPage` with `lessonId = 3`.
3. `useEffect` fires, calls `api.getLesson(3)` → `GET /api/lessons/3`.
4. Django routes to `views.get_lesson(request, lesson_id=3)`.
5. ORM: `Lesson.objects.prefetch_related("exercises").get(pk=3)`.
6. `LessonDetailSerializer` serialises the lesson plus all child `Exercise` objects into JSON including the `content_blocks` JSONField.
7. Response JSON arrives in the browser; React sets `lesson` state.
8. `ContentBlock` renders each block — `"text"` blocks go through `ReactMarkdown`, `"code"` blocks render as `<pre>` with PrismJS highlighting.
9. Each exercise is rendered by `ExerciseCard`, which initialises the `CodeEditor` with the exercise's `starter_code`.

### 4b. Running code in the playground

1. User types code and clicks **Run Code**.
2. `PlaygroundPage` calls `api.runCode(code)` → `POST /api/run` with body `{ "code": "..." }`.
3. `views.run_code()` checks:
   - Code is not empty.
   - `len(code) <= SANDBOX_MAX_CODE_LENGTH` (default 10,000 chars).
4. `sandbox.execute_code(code)` runs asynchronously via `asyncio.run()`.
5. `check_code_safety(code)` scans for blocked patterns and import violations.
6. Code is indented and injected into `WRAPPER_TEMPLATE`, which adds recursion limits, OS-level resource limits, and stdout/stderr capture.
7. The wrapped code is written to a `tempfile`, then `_run_subprocess()` is called in a thread via `asyncio.to_thread()`.
8. `asyncio.wait_for(...)` enforces the timeout. If the process hangs, `TimeoutError` is raised, the process is killed, and an informative message is returned.
9. stdout/stderr are captured and returned; output is truncated at `SANDBOX_MAX_OUTPUT_CHARS` (default 5,000 chars).
10. `error_explainer.explain_error()` converts raw tracebacks into plain-English guidance.
11. The response `{ output, error, friendly_error, execution_time_ms }` arrives; `OutputPanel` renders it.

### 4c. Submitting an exercise

1. User clicks **Submit** in `ExerciseCard`.
2. `api.submitExercise(exerciseId, code)` → `POST /api/exercises/:id/submit`.
3. Django fetches the `Exercise` record, pulls `exercise.tests` (a JSON array of `{input, expected_output}` objects).
4. `sandbox.run_exercise_tests(code, tests)` iterates each test case:
   - Safety-check on the student code is done once before the loop.
   - For tests with non-empty `input`, `_execute_with_stdin()` uses `WRAPPER_TEMPLATE_STDIN`, which injects a `io.StringIO` as `sys.stdin` before execution.
   - Each run's actual output is `.strip()`-compared to `expected_output`.
5. Results are aggregated: `is_correct`, `test_results[]` per case, last output/error.
6. If `is_correct`, the frontend calls `markLessonComplete(lessonId)` which writes to `localStorage`.

---

## 5. Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Backend framework | Django | 5.2.x | Project structure, ORM, management commands |
| REST API | Django REST Framework | 3.16.x | Serializers, view decorators, response formatting |
| CORS | django-cors-headers | 4.9.x | Allow browser requests from the Vercel domain |
| Static files | WhiteNoise | 6.7.x | Serve `collectstatic` output directly from Gunicorn |
| WSGI server | Gunicorn | 23.x | Production HTTP server on Render |
| Frontend framework | React | 18.3.x | Component-based UI |
| Build tool | Vite | 5.1.x | Dev server with HMR, production bundling |
| Routing | React Router DOM | 6.22.x | Client-side SPA routing |
| Code editor | react-simple-code-editor | 0.14.x | Textarea with syntax highlighting overlay |
| Syntax highlighting | PrismJS | 1.29.x | Tokeniser for Python |
| Markdown rendering | react-markdown + remark-gfm | 9.x / 4.x | Lesson content blocks |
| Env management | python-dotenv | 1.0.x | Load `.env` in local dev |
| Deployment — frontend | Vercel | — | Static hosting + SPA rewrite |
| Deployment — backend | Render | — | Python web service |

---

## 6. Data Model

```
Course
  id          INTEGER PK
  title       VARCHAR(200)
  description TEXT
  order       INTEGER          ← controls display order
  icon        VARCHAR(50)      ← emoji

  ↳ Lesson (FK: course_id)
      id              INTEGER PK
      course          FK(Course)
      title           VARCHAR(200)
      subtitle        VARCHAR(300)
      content_blocks  JSON         ← list of {type, body} objects
      order           INTEGER

      ↳ Exercise (FK: lesson_id)
          id            INTEGER PK
          lesson        FK(Lesson)
          title         VARCHAR(200)
          instructions  TEXT
          starter_code  TEXT         ← pre-filled code in editor
          hint          TEXT
          solution      TEXT         ← hidden until revealed
          explanation   TEXT         ← shown alongside solution
          tests         JSON         ← list of {input, expected_output}
          order         INTEGER
          difficulty    ENUM(easy, medium, challenge)
```

### content_blocks format

Each lesson stores its teaching content as a JSON array. Each element is an object with a `type` field:

```json
[
  { "type": "text",    "body": "## Why Python?\n\nParagraph text with **markdown**." },
  { "type": "code",    "body": "print('Hello, World!')" },
  { "type": "tip",     "body": "Always use 4 spaces for indentation, not tabs." },
  { "type": "warning", "body": "Python is case-sensitive: `Print` is not the same as `print`." }
]
```

`ContentBlock.jsx` switches on `type` to apply different visual treatment.

### tests format

```json
[
  { "input": "",       "expected_output": "Hello, World!" },
  { "input": "Alice",  "expected_output": "Hello, Alice!" }
]
```

When `input` is empty the normal `execute_code()` path is used. When non-empty the stdin-injection path is used.

---

## 7. API Reference

All endpoints are public — no `Authorization` header required.

```
GET  /                                  → health check ({"message": "...", "status": "healthy"})
GET  /health                            → {"status": "ok"}

GET  /api/courses                       → Course[]
GET  /api/courses/:courseId/lessons     → LessonSummary[]
GET  /api/lessons/:lessonId             → LessonDetail (includes exercises[])
GET  /api/exercises/:exerciseId         → Exercise (no solution/tests)
GET  /api/exercises/:exerciseId/solution → {solution, explanation}

POST /api/run                           → {output, error, friendly_error, execution_time_ms}
  body: { "code": "<python source>" }

POST /api/exercises/:exerciseId/submit  → {is_correct, output, error, friendly_error,
  body: { "code": "..." }                  test_results[], message}
```

Error responses always use the shape `{"detail": "<string>"}`, normalised by `api/utils.py`'s custom DRF exception handler.

---

## 8. Sandboxed Code Execution

The execution pipeline in `sandbox.py` has multiple independent safety layers. They run in order — the first one that triggers short-circuits the rest.

### Layer 1 — HTTP request size (Django setting)

`DATA_UPLOAD_MAX_MEMORY_SIZE = 256 KB` — Django rejects the request body before it reaches any view code.

### Layer 2 — View-level code length check

`views.run_code()` and `views.submit_exercise()` both check `len(code) > SANDBOX_MAX_CODE_LENGTH` (default 10,000 chars) and return HTTP 400 immediately.

### Layer 3 — Static analysis (`check_code_safety`)

Runs before any subprocess is created:

- **Character/line counts**: rejects code exceeding `SANDBOX_MAX_CODE_LENGTH` chars or 500 lines.
- **Blocked pattern scan**: checks both the original code and a whitespace-normalised copy against a list of ~45 dangerous strings: `import os`, `import sys`, `import subprocess`, `eval(`, `exec(`, `open(`, `__import__`, `__subclasses__`, `__class__`, `__mro__`, `bytearray(`, `import threading`, `import multiprocessing`, and more.
- **Import whitelist**: any `import X` or `from X import` where `X` is not in the allowed list (`math`, `random`, `string`, `datetime`, `collections`, `itertools`, `functools`, `json`, `re`, `statistics`, `decimal`, `fractions`, `textwrap`) is rejected.

### Layer 4 — Wrapper template

The student's code is injected into the wrapper before execution:

```python
import sys, io
sys.setrecursionlimit(200)          # caps recursion depth
try:
    import resource as _resource
    _resource.setrlimit(RLIMIT_AS,  (64MB, 64MB))   # virtual memory cap
    _resource.setrlimit(RLIMIT_CPU, (5s, 5s))        # CPU time cap
except Exception:
    pass                            # silently skipped on Windows
sys.stdin  = io.StringIO(...)       # optional: inject test input
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
try:
    <student code, indented 4 spaces>
except MemoryError:
    print("MemoryError: ...")
except Exception as _e:
    print(f"{type(_e).__name__}: {_e}")
# output is truncated at SANDBOX_MAX_OUTPUT_CHARS
```

### Layer 5 — Subprocess isolation

`subprocess.run([sys.executable, "-u", tmpfile])` is called in a worker thread via `asyncio.to_thread`. The subprocess:
- Receives a clean environment (only `PATH`, `PYTHONPATH=""`, `PYTHONDONTWRITEBYTECODE=1`).
- Has its own `subprocess.run(..., timeout=SANDBOX_TIMEOUT_SECONDS + 1)` internal deadline.

### Layer 6 — Asyncio timeout

`asyncio.wait_for(..., timeout=SANDBOX_TIMEOUT_SECONDS)` wraps the entire thread. If it fires, the thread is abandoned and a timeout message is returned immediately.

### Configurable limits (via env vars or `settings.py`)

| Setting | Default | Effect |
|---|---|---|
| `SANDBOX_TIMEOUT_SECONDS` | 5 | Kill subprocess after N seconds |
| `SANDBOX_MAX_OUTPUT_CHARS` | 5000 | Truncate stdout+stderr output |
| `SANDBOX_MAX_CODE_LENGTH` | 10000 | Reject code longer than N chars |
| `SANDBOX_MAX_MEMORY_BYTES` | 67108864 (64 MB) | `RLIMIT_AS` cap inside subprocess |
| `DATA_UPLOAD_MAX_MEMORY_SIZE` | 262144 (256 KB) | Django request body size limit |

---

## 9. Progress Tracking

There is no server-side progress — everything is stored in `localStorage` under the key `learnpython_progress` as a JSON array of completed lesson IDs:

```json
[1, 2, 3]
```

`api.js` exposes:
- `markLessonComplete(lessonId)` — appends to the array
- `isLessonCompleted(lessonId)` — checks membership
- `getCompletedLessons()` — returns the full array

This is called automatically by `ExerciseCard` when a submission returns `is_correct: true`, and can also be triggered manually via the "Mark as Complete" button on lessons that have no exercises.

`ProgressPage` reads this array and cross-references it with the courses/lessons API data to compute per-course and overall completion percentages.

---

## 10. Local Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

### Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations (creates db.sqlite3)
python manage.py migrate

# Seed the curriculum
python manage.py seed

# Start the development server
python manage.py runserver 8000
```

The API is now available at `http://localhost:8000/api/`.

### Frontend

```bash
# In a separate terminal
cd frontend

npm install
npm run dev
```

The dev server starts on `http://localhost:3000`. Vite's proxy (`vite.config.js`) forwards any request starting with `/api` to `http://localhost:8000`, so no CORS configuration is needed locally.

---

## 11. Environment Variables

### Backend (`backend/.env`)

```env
SECRET_KEY=your-long-random-secret-key
DEBUG=false
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# Optional — override sandbox defaults
SANDBOX_TIMEOUT_SECONDS=5
SANDBOX_MAX_OUTPUT_CHARS=5000
SANDBOX_MAX_CODE_LENGTH=10000
SANDBOX_MAX_MEMORY_BYTES=67108864
DATA_UPLOAD_MAX_MEMORY_SIZE=262144
```

### Frontend (`frontend/.env`)

```env
# Leave empty in dev (Vite proxy handles it).
# Set to the Render backend URL in production.
VITE_API_URL=https://learnpython-api.onrender.com
```

If `VITE_API_URL` is not set, `api.js` defaults the base URL to `""`, which means all fetch calls go to the same origin — correct in production if you were serving both from one host, but more importantly it allows the Vite proxy to intercept them during development.

---

## 12. Database Seeding

```bash
python manage.py seed
```

This management command (`api/management/commands/seed.py`) drops and recreates all `Course`, `Lesson`, and `Exercise` rows. It is idempotent and safe to re-run. It creates:

- **1 course**: Python Basics
- **10 lessons** (ordered 1–10), each with `content_blocks` covering: programming concepts, `print()`, variables, data types, `input()`, `if/elif/else`, `while`/`for` loops, lists, functions, and a capstone mini-project.
- **2–3 exercises per lesson**, each with `starter_code`, `hint`, `solution`, `explanation`, `difficulty`, and `tests[]`.

In production on Render, run this once after the first deploy via the Render shell:

```bash
python manage.py seed
```

---

## 13. Deployment

### Backend → Render

`render.yaml` in the project root defines the service:

```yaml
services:
  - type: web
    name: learnpython-api
    runtime: python
    rootDir: backend
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn learnpython.wsgi --bind 0.0.0.0:$PORT
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "false"
      - key: PYTHON_VERSION
        value: "3.11"
      - key: CORS_ALLOWED_ORIGINS
        value: "https://your-frontend-domain.vercel.app"
```

Render auto-detects this file. On every push to the connected branch it:
1. Installs Python 3.11
2. Runs `pip install -r requirements.txt`
3. Runs `python manage.py collectstatic --noinput` (WhiteNoise serves these)
4. Starts Gunicorn

**After first deploy**, open the Render shell and run `python manage.py seed`.

Set `CORS_ALLOWED_ORIGINS` to the exact Vercel frontend URL (no trailing slash).

### Frontend → Vercel

1. Import the repo into Vercel, set **Root Directory** to `frontend`.
2. Vercel detects Vite automatically.
3. Add environment variable: `VITE_API_URL` = your Render service URL.
4. `vercel.json` handles the SPA catch-all:
   ```json
   { "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }
   ```
   Without this, direct navigation to `/courses/1/lessons` would 404 at the CDN layer.

---

## 14. Security Model

The current model is suitable for a low-risk educational platform with trusted learners. For a fully public-facing service:

| Threat | Current Mitigation | Stronger Alternative |
|---|---|---|
| Infinite loops / CPU exhaustion | 5s asyncio timeout + `RLIMIT_CPU` | Docker container with `--cpus`, cgroups |
| Memory bombs | 64 MB `RLIMIT_AS` + `MemoryError` catch | Docker `--memory` flag |
| File system access | `open(` blocked by pattern scanner | Docker read-only rootfs |
| Network access | `import socket/http/urllib/requests` blocked | Docker `--network none` |
| Fork bombs / thread spam | `import threading/multiprocessing` blocked | seccomp profile |
| Code injection via import tricks | `__import__` blocked, AST-free scanner | RestrictedPython or bubblewrap |
| Oversized payloads | 256 KB Django body limit + 10K char limit | nginx `client_max_body_size` |
| Rate limiting | None | nginx rate limiting or a WAF |

---

## 15. Curriculum Overview

| # | Lesson Title | Key Concepts |
|---|---|---|
| 1 | What is Programming? | Instructions, computers, why Python |
| 2 | Your First Line of Code | `print()`, strings, quotes |
| 3 | Variables | Assignment operator, naming rules, reassignment |
| 4 | Data Types | `int`, `float`, `str`, `bool`, `type()` |
| 5 | Getting User Input | `input()`, `int()` / `float()` conversion |
| 6 | Making Decisions | `if`, `elif`, `else`, comparison operators |
| 7 | Loops | `while`, `for`, `range()`, `break`, `continue` |
| 8 | Lists | Indexing, `append()`, `len()`, iteration |
| 9 | Functions | `def`, parameters, `return`, scope |
| 10 | Putting It All Together | Mini-project: number guessing game |

Each lesson stores its content in the `content_blocks` JSON column, which is rendered client-side. This means updating lesson text requires only a database change (re-run `seed.py`), not a code deployment.

---

## License

MIT
