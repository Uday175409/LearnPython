# 🐍 LearnPython — Mobile-First Python Learning Platform

A full-stack web app that teaches Python to **absolute beginners with zero programming experience**. Built with a mobile-first approach so learners can study from their phone, tablet, or desktop.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Structured Curriculum** | 10 lessons covering print, variables, types, input, if/else, loops, lists, and functions |
| **Interactive Exercises** | Write and run real Python code in the browser with instant feedback |
| **Sandboxed Execution** | Server-side Python execution with safety checks, time limits, and output limits |
| **Beginner-Friendly Errors** | Python errors are translated into plain English with examples and fix suggestions |
| **Progress Tracking** | Lesson locking, completion tracking, and a progress dashboard |
| **Hints & Solutions** | Every exercise has a hint, partial solution reveal, and full explanation |
| **Free Playground** | Sandbox to run any Python code outside of lessons |
| **Mobile-First UI** | Sticky "Run Code" button, large touch targets, responsive layout |
| **JWT Authentication** | Secure signup/login with token-based auth |

---

## 🏗️ Architecture

```
LearnPython/
├── backend/              ← FastAPI (Python)
│   ├── config.py         ← Settings from .env
│   ├── database.py       ← Async SQLAlchemy setup
│   ├── models.py         ← ORM models (User, Course, Lesson, Exercise, Progress)
│   ├── schemas.py        ← Pydantic request/response models
│   ├── auth.py           ← JWT creation, verification, password hashing
│   ├── sandbox.py        ← Safe Python code execution
│   ├── error_explainer.py← Plain-English error translations
│   ├── seed_data.py      ← Full curriculum (run once)
│   ├── main.py           ← App entry point
│   ├── .env.example      ← Environment variables template
│   ├── Procfile           ← Render start command
│   └── routers/
│       ├── auth_router.py
│       ├── lesson_router.py
│       ├── code_router.py
│       └── progress_router.py
│
├── frontend/             ← React + Vite (JavaScript)
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── vercel.json       ← Vercel SPA rewrite rules
│   ├── .env.example      ← Frontend env vars
│   └── src/
│       ├── main.jsx
│       ├── App.jsx        ← Routes
│       ├── api.js         ← API client
│       ├── context/
│       │   └── AuthContext.jsx
│       ├── components/
│       │   ├── Header.jsx + .css
│       │   ├── CodeEditor.jsx + .css
│       │   ├── OutputPanel.jsx + .css
│       │   ├── ContentBlock.jsx + .css
│       │   └── ExerciseCard.jsx + .css
│       ├── pages/
│       │   ├── HomePage.jsx + .css
│       │   ├── LoginPage.jsx
│       │   ├── RegisterPage.jsx
│       │   ├── AuthPages.css
│       │   ├── CoursesPage.jsx + .css
│       │   ├── LessonsPage.jsx + .css
│       │   ├── LessonPage.jsx + .css
│       │   ├── PlaygroundPage.jsx + .css
│       │   └── ProgressPage.jsx + .css
│       └── styles/
│           └── global.css  ← CSS variables & base styles
│
└── render.yaml           ← Render deployment config
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **npm** or **yarn**

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd LearnPython
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
copy .env.example .env      # Windows
# cp .env.example .env      # Mac/Linux

# Edit .env and set a SECRET_KEY (any random string)
```

### 3. Seed the Database

```bash
# Still in the backend/ folder with venv activated
python seed_data.py
```

This creates `learnpython.db` (SQLite) and populates it with the full curriculum.

### 4. Start the Backend

```bash
uvicorn main:app --reload --port 8000
```

API is now running at **http://localhost:8000**. Visit http://localhost:8000/docs for the interactive API docs.

### 5. Frontend Setup

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend is now running at **http://localhost:3000**. The Vite dev server proxies `/api` requests to the backend automatically.

### 6. Open the App

Visit **http://localhost:3000** in your browser. Create an account and start learning!

---

## 📱 Mobile-First Design Decisions

- **16px minimum font size** on all inputs to prevent iOS auto-zoom
- **Sticky "Run Code" button** always visible at the bottom of the code editor
- **48px+ touch targets** for all interactive elements (Apple HIG: 44px minimum)
- **No hover states** — interactions use `:active` for touch feedback
- **Vertical layouts by default** — horizontal only on screens ≥ 768px
- **`touch-action: manipulation`** prevents double-tap zoom
- **`user-scalable=no`** in viewport meta to prevent accidental zoom
- **System font stack** for fast loading on mobile networks

---

## 🔒 Security: Sandboxed Code Execution

Student code runs on the server with multiple safety layers:

1. **Pattern Blocking** — Blocks dangerous patterns: `import os`, `subprocess`, `eval()`, `exec()`, `open()`, `__import__`, etc.
2. **Import Whitelist** — Only safe modules allowed: `math`, `random`, `string`, `datetime`, `collections`, `itertools`, `functools`
3. **Time Limit** — Code execution times out after 5 seconds
4. **Output Limit** — Output truncated at 5,000 characters
5. **Subprocess Isolation** — Code runs in a separate Python subprocess, not in the server process

> ⚠️ **Production Note:** For production deployments with untrusted users, consider adding Docker container isolation or using a dedicated code execution service like Judge0.

---

## 🌐 Deployment

### Backend → Render

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repo, set the **Root Directory** to `backend`
3. Set the **Build Command**: `pip install -r requirements.txt`
4. Set the **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `DATABASE_URL` — Use Render's free PostgreSQL add-on (starts with `postgresql://`)
   - `SECRET_KEY` — A long random string
   - `FRONTEND_URL` — Your Vercel URL (e.g., `https://learnpython.vercel.app`)

6. After deploying, **seed the database** by running the seed script. You can use Render's shell:
   ```bash
   python seed_data.py
   ```

### Frontend → Vercel

1. Create a new project on [Vercel](https://vercel.com)
2. Connect your GitHub repo, set the **Root Directory** to `frontend`
3. **Framework Preset**: Vite
4. Add environment variable:
   - `VITE_API_URL` — Your Render backend URL (e.g., `https://learnpython-api.onrender.com`)
5. Deploy!

---

## 🧪 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | No | Create account |
| POST | `/api/auth/login` | No | Get JWT token |
| GET | `/api/auth/me` | Yes | Get current user |
| GET | `/api/courses` | No | List all courses |
| GET | `/api/courses/:id/lessons` | Optional | Lessons list (with lock/complete status if authenticated) |
| GET | `/api/lessons/:id` | No | Full lesson content + exercises |
| GET | `/api/exercises/:id` | No | Single exercise |
| GET | `/api/exercises/:id/solution` | Yes | Reveal solution |
| POST | `/api/run` | No | Run Python code (playground) |
| POST | `/api/exercises/:id/submit` | Yes | Submit exercise answer |
| GET | `/api/progress` | Yes | Progress dashboard data |
| POST | `/api/lessons/:id/complete` | Yes | Mark lesson complete |

---

## 📚 Curriculum Overview

| # | Lesson | Topics |
|---|--------|--------|
| 1 | What is Programming? | Concept of instructions, real-world analogy |
| 2 | Your First Code | `print()`, strings, quotes |
| 3 | Variables | Assignment, naming rules, updating values |
| 4 | Data Types | int, float, str, bool, type() |
| 5 | Getting User Input | `input()`, type conversion |
| 6 | Making Decisions | if, elif, else, comparison operators |
| 7 | Loops | while loops, for loops, range() |
| 8 | Lists | Creating, indexing, append, len, iteration |
| 9 | Functions | def, parameters, return, reusability |
| 10 | Putting It All Together | Mini-project combining all concepts |

Each lesson includes:
- 📖 Reading content with code examples
- 💡 Tips for beginners
- ⚠️ Common mistakes with corrections
- ✏️ 2-3 interactive exercises with hints and solutions

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 5, React Router 6 |
| Code Editor | react-simple-code-editor + PrismJS |
| Content Rendering | react-markdown + remark-gfm |
| Backend | FastAPI, Python 3.11 |
| Database | SQLite (dev), PostgreSQL (prod) |
| ORM | SQLAlchemy 2.0 (async) |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Deployment | Vercel (frontend), Render (backend) |

---

## 📝 License

MIT — use it however you like.
