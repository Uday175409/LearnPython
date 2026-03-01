# LearnPython — Frontend

This is the client-side component of LearnPython. It is a React 18 + Vite SPA with no build-time server rendering, no authentication, and no global state management library. All data comes from the Django API. Progress tracking is stored in `localStorage`.

---

## Table of Contents

1. [Tech Stack](#1-tech-stack)
2. [Project Layout](#2-project-layout)
3. [Build System: Vite](#3-build-system-vite)
4. [Application Entry Point](#4-application-entry-point)
5. [Routing](#5-routing)
6. [API Client (api.js)](#6-api-client-apijs)
7. [Progress Tracking (localStorage)](#7-progress-tracking-localstorage)
8. [Components](#8-components)
   - [CodeEditor](#codeEditor)
   - [OutputPanel](#outputpanel)
   - [ContentBlock](#contentblock)
   - [ExerciseCard](#exercisecard)
   - [Header](#header)
9. [Pages](#9-pages)
10. [Styling Architecture](#10-styling-architecture)
11. [Auth Context (Placeholder)](#11-auth-context-placeholder)
12. [Running Locally](#12-running-locally)
13. [Environment Variables](#13-environment-variables)
14. [Production Build & Deployment (Vercel)](#14-production-build--deployment-vercel)
15. [Key Design Decisions](#15-key-design-decisions)

---

## 1. Tech Stack

| Package | Version | Role |
|---|---|---|
| react | 18.3.x | Component rendering |
| react-dom | 18.3.x | DOM mounting |
| react-router-dom | 6.22.x | Client-side SPA routing |
| react-simple-code-editor | 0.14.x | Textarea-based code editor with syntax overlay |
| prismjs | 1.29.x | Syntax tokeniser (Python grammar) |
| react-markdown | 9.x | Safe Markdown → HTML renderer for lesson content |
| remark-gfm | 4.x | GitHub Flavored Markdown plugin (tables, strikethrough, etc.) |
| vite | 5.1.x | Dev server with HMR, production bundler |
| @vitejs/plugin-react | 4.2.x | Babel transform for JSX and fast refresh |

No UI component library (no MUI, Chakra, etc.). All styles are hand-written CSS.

---

## 2. Project Layout

```
frontend/
├── index.html              ← Vite HTML template — contains <div id="root">
├── package.json            ← npm dependencies and scripts
├── vite.config.js          ← Vite config: React plugin, port 3000, /api proxy
├── vercel.json             ← SPA catch-all rewrite rule
└── src/
    ├── main.jsx            ← ReactDOM.createRoot + BrowserRouter + AuthProvider
    ├── App.jsx             ← Route definitions (all public pages)
    ├── api.js              ← All fetch calls + localStorage helpers
    │
    ├── context/
    │   └── AuthContext.jsx ← Placeholder auth context (auth is disabled)
    │
    ├── components/
    │   ├── CodeEditor.jsx     ← Python-aware editor: syntax highlight, auto-indent,
    │   ├── CodeEditor.css       auto-close pairs, mobile toolbar
    │   ├── OutputPanel.jsx    ← Renders execution output + friendly error
    │   ├── OutputPanel.css
    │   ├── ContentBlock.jsx   ← Renders a single lesson content block by type
    │   ├── ContentBlock.css
    │   ├── ExerciseCard.jsx   ← Full exercise widget: run, submit, hint, solution
    │   ├── ExerciseCard.css
    │   ├── Header.jsx         ← Global navigation bar
    │   └── Header.css
    │
    ├── pages/
    │   ├── HomePage.jsx + .css       ← Landing page with feature cards
    │   ├── CoursesPage.jsx + .css    ← Course listing
    │   ├── LessonsPage.jsx + .css    ← Lesson list for a given course
    │   ├── LessonPage.jsx + .css     ← Full lesson: content blocks + exercises
    │   ├── PlaygroundPage.jsx + .css ← Free code playground
    │   ├── ProgressPage.jsx + .css   ← Completion dashboard
    │   ├── LoginPage.jsx             ← Placeholder (auth disabled)
    │   ├── RegisterPage.jsx          ← Placeholder (auth disabled)
    │   └── AuthPages.css
    │
    └── styles/
        └── global.css      ← CSS custom properties, base reset, utility classes
```

---

## 3. Build System: Vite

`vite.config.js`:

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "dist",
  },
});
```

### Dev server proxy

During development, any fetch to `/api/*` is transparently forwarded to `http://localhost:8000` by Vite's built-in proxy. This means:
- No CORS issues locally (the browser sees all requests as same-origin).
- `api.js` uses `const BASE_URL = import.meta.env.VITE_API_URL || ""`. In dev, `VITE_API_URL` is not set, so `BASE_URL` is `""`, and the proxy intercepts.
- In production, `VITE_API_URL` is set to the Render backend URL (e.g., `https://learnpython-api.onrender.com`), so all fetch calls go cross-origin to that URL.

### Production build

```bash
npm run build
```

Vite bundles all JS/CSS into `dist/`, with content-hashed filenames for cache busting. Vercel deploys the `dist/` directory as a static site.

---

## 4. Application Entry Point

`src/main.jsx`:

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import App from "./App";
import "./styles/global.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

`BrowserRouter` must wrap everything because `App.jsx` uses `<Routes>` and `<Route>`. In production, `vercel.json` rewrites all paths to `/index.html` so React Router handles the navigation.

`AuthProvider` currently does nothing (auth is disabled) but is kept in the tree so it can be re-enabled without changing any component that calls `useAuth()`.

---

## 5. Routing

`App.jsx` defines all routes:

```jsx
<Routes>
  <Route path="/"                               element={<HomePage />} />
  <Route path="/courses"                        element={<CoursesPage />} />
  <Route path="/courses/:courseId/lessons"      element={<LessonsPage />} />
  <Route path="/lessons/:lessonId"              element={<LessonPage />} />
  <Route path="/playground"                     element={<PlaygroundPage />} />
  <Route path="/progress"                       element={<ProgressPage />} />
  <Route path="*"                               element={<Navigate to="/" replace />} />
</Routes>
```

All routes are public. The catch-all `*` redirects unknown paths to home. `<Header>` is rendered outside `<Routes>` so it appears on every page.

### URL parameter access

Pages that need route parameters use `useParams()`:
```jsx
const { lessonId } = useParams();
const { courseId } = useParams();
```

---

## 6. API Client (api.js)

All HTTP communication with the backend goes through `src/api.js`. It exports named async functions, one per API endpoint.

### Base URL strategy

```javascript
const BASE_URL = import.meta.env.VITE_API_URL || "";
```

- **Dev**: `""` → Vite proxy handles `/api/*` → `http://localhost:8000`
- **Prod**: `"https://learnpython-api.onrender.com"` → direct cross-origin fetch

### Core request function

```javascript
async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...options.headers };
  const response = await fetch(`${BASE_URL}${path}`, { ...options, headers });

  const contentType = response.headers.get("content-type");
  if (!contentType || !contentType.includes("application/json")) {
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    return null;
  }

  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || `Request failed: ${response.status}`);
  return data;
}
```

The `data.detail` fallback matches the backend's custom exception handler, which normalises all errors to `{"detail": "..."}`. Components that call API functions wrap them in `try/catch` and set local error state.

### Exported functions

```javascript
getCourses()                          → GET /api/courses
getLessons(courseId)                  → GET /api/courses/:id/lessons
getLesson(lessonId)                   → GET /api/lessons/:id
getExercise(exerciseId)               → GET /api/exercises/:id
getExerciseSolution(exerciseId)       → GET /api/exercises/:id/solution
runCode(code)                         → POST /api/run
submitExercise(exerciseId, code)      → POST /api/exercises/:id/submit
markLessonComplete(lessonId)          → writes to localStorage
isLessonCompleted(lessonId)           → reads from localStorage
getCompletedLessons()                 → reads from localStorage
```

---

## 7. Progress Tracking (localStorage)

Progress is stored entirely client-side in `localStorage` under the key `"learnpython_progress"`.

```javascript
const PROGRESS_KEY = "learnpython_progress";

function getCompletedLessons() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || [];
  } catch {
    return [];
  }
}

export function markLessonComplete(lessonId) {
  const completed = getCompletedLessons();
  const id = Number(lessonId);
  if (!completed.includes(id)) {
    completed.push(id);
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(completed));
  }
}

export function isLessonCompleted(lessonId) {
  return getCompletedLessons().includes(Number(lessonId));
}
```

`markLessonComplete` is called in two places:
1. `ExerciseCard` — automatically when `submitExercise` returns `is_correct: true`
2. `LessonPage` — via the "Mark as Complete" button on lessons with no exercises

**Trade-offs of localStorage:**
- Pros: No server round-trip, works without accounts, zero complexity
- Cons: Progress is device-specific (lost if you clear storage or switch devices), not portable

---

## 8. Components

### CodeEditor

`src/components/CodeEditor.jsx`

The most complex component in the codebase. It wraps `react-simple-code-editor` (which is itself a `<textarea>` with an absolutely-positioned `<pre>` overlay for syntax highlighting) and adds:

#### Props

```jsx
<CodeEditor
  initialCode=""         // pre-filled code string
  onRun={fn}             // called with current code when Run button clicked
  running={false}        // disables button and shows spinner
  buttonLabel="▶ Run Code"
  onCodeChange={fn}      // called on every keystroke with current code
/>
```

#### Python-aware keyboard handling (`handleKeyDown`)

The `onKeyDown` handler intercepts several key combinations before letting the browser/textarea handle them:

| Key | Behaviour |
|---|---|
| `Tab` | Insert 4 spaces at cursor position (or indent selected lines) |
| `Shift+Tab` | Dedent current/selected lines by up to 4 spaces |
| `Enter` after `:` | Auto-indent: insert newline + current indentation + 4 spaces |
| `Enter` in empty block | Smart dedent: detect empty indented line, step back one indent level |
| `(`, `[`, `{`, `"`, `'` with selection | Wrap selection in the pair |
| `(`, `[`, `{`, `"`, `'` without selection | Insert pair and place cursor between them |
| `)`, `]`, `}` when next char is `)`, `]`, `}` | Skip over (don't double up) |
| `Backspace` when cursor is between pair | Delete both characters in the pair |

This logic operates directly on the `<textarea>` DOM node via `e.target.value`, `e.target.selectionStart`, and `e.target.selectionEnd`. The `pendingCursor` ref stores the desired cursor position after the next React render, and a `useLayoutEffect` applies it synchronously after the DOM update.

#### Cursor management

`react-simple-code-editor` re-renders the textarea on every change, which resets the cursor to the end. To prevent this:

```javascript
const pendingCursor = useRef(null); // { start, end }

function applyEdit(newCode, cursorStart, cursorEnd = cursorStart) {
  pendingCursor.current = { start: cursorStart, end: cursorEnd };
  setCode(newCode);
  if (onCodeChange) onCodeChange(newCode);
}

useLayoutEffect(() => {
  if (pendingCursor.current === null) return;
  const ta = containerRef.current?.querySelector("textarea");
  if (ta) {
    ta.selectionStart = pendingCursor.current.start;
    ta.selectionEnd   = pendingCursor.current.end;
  }
  pendingCursor.current = null;
});
```

`useLayoutEffect` runs synchronously after the DOM update, before the browser paints — this prevents the cursor flash.

#### Mobile toolbar

A row of quick-insert buttons is rendered below the editor for characters that are hard to type on mobile keyboards: `:  (  )  [  ]  {  }  "  '  =  ==  !=  <=  >=  **  #`. Each button calls `insertAtCursor(char)` which inserts the string at the current cursor position.

#### Syntax highlighting

```javascript
const highlight = useCallback(
  (src) => Prism.highlight(src, Prism.languages.python, "python"),
  []
);
```

Passed to `react-simple-code-editor`'s `highlight` prop. PrismJS tokenises the Python source and returns HTML with `<span class="token ...">` elements. The editor's `<pre>` overlay renders this HTML while the invisible `<textarea>` handles actual input.

---

### OutputPanel

`src/components/OutputPanel.jsx`

Displays the result of a code execution run. Receives the API response shape:

```javascript
{
  output: "",
  error: "",
  friendly_error: "",
  execution_time_ms: 0,
}
```

Logic:
- If `error` is set, shows the friendly error (if available) in a styled error box, then the raw error in a `<pre>` below it.
- If `output` is empty and no error, shows a "no output" message.
- Always shows execution time in the footer.
- The `friendly_error` is rendered via `ReactMarkdown` so the backend's Markdown-formatted explanations (code blocks, bold text, bullet lists) render correctly.

---

### ContentBlock

`src/components/ContentBlock.jsx`

Renders a single lesson content block object. Switches on the `type` field:

```jsx
switch (block.type) {
  case "text":    return <ReactMarkdown remarkPlugins={[remarkGfm]}>{block.body}</ReactMarkdown>
  case "code":    return <pre><code className="language-python">...</code></pre>
  case "tip":     return <div className="content-block tip">...</div>
  case "warning": return <div className="content-block warning">...</div>
  default:        return <div className="content-block">{block.body}</div>
}
```

For `"code"` blocks, PrismJS's `highlightElement` is called via a `useEffect` after the component mounts.

---

### ExerciseCard

`src/components/ExerciseCard.jsx`

A self-contained widget that manages the full exercise lifecycle. It contains a `CodeEditor`, an `OutputPanel`, and controls for hint/solution reveal.

#### State

```javascript
const [output, setOutput]             // last runCode result
const [running, setRunning]           // Run button loading state
const [submitting, setSubmitting]     // Submit button loading state
const [showHint, setShowHint]        // toggle hint text
const [showSolution, setShowSolution] // toggle solution panel
const [solution, setSolution]         // fetched solution (lazy)
const [submitResult, setSubmitResult] // last submitExercise result
const [currentCode, setCurrentCode]  // tracks live code from CodeEditor
```

#### Run flow

1. User clicks "Run Code" in the embedded `CodeEditor`.
2. `handleRun(code)` is called with the current code string.
3. Sets `running=true`, clears previous output/submitResult.
4. Calls `api.runCode(code)` → `POST /api/run`.
5. Sets `output` to the response.
6. Sets `running=false`.

#### Submit flow

1. User clicks "Submit" (separate button in ExerciseCard controls).
2. `handleSubmit()` uses `currentCode` (kept in sync via `onCodeChange` prop).
3. Calls `api.submitExercise(exercise.id, currentCode)` → `POST /api/exercises/:id/submit`.
4. Sets `submitResult` to the response.
5. If `result.is_correct`, calls `markLessonComplete(lessonId)`.

#### Solution reveal

Solutions are lazy-loaded — `handleShowSolution()` only calls `api.getExerciseSolution(exercise.id)` on the first reveal. Subsequent toggles just show/hide the already-fetched `solution` state.

#### Test results display

When `submitResult` is set: renders each test case in a table showing pass/fail, the input, expected output, and actual output. Failed tests are highlighted in red.

---

### Header

`src/components/Header.jsx`

Global navigation bar rendered on every page. Contains:
- Logo/brand link to `/`
- Nav links: Courses, Playground, Progress
- Mobile hamburger menu (toggle via state)

Uses `useLocation()` from React Router to apply an `active` class to the currently-matched nav item.

---

## 9. Pages

### HomePage

Landing page. Contains a hero section and a feature grid. No API calls. Static content.

### CoursesPage

Fetches `GET /api/courses` on mount. Renders a card grid. Each card links to `/courses/:id/lessons`. Annotates cards with `lesson_count` from the API.

### LessonsPage

Route: `/courses/:courseId/lessons`

Fetches `GET /api/courses/:courseId/lessons`. Renders lesson cards ordered by `lesson.order`. Each card shows:
- Title and subtitle
- Completion badge (from `isLessonCompleted(lesson.id)`)
- Lock icon (currently never shown — all lessons are unlocked)

### LessonPage

Route: `/lessons/:lessonId`

The central content page. On mount:
1. Fetches `GET /api/lessons/:lessonId` to get the full lesson including `content_blocks` and `exercises`.
2. Checks `isLessonCompleted(lessonId)` to set initial completed state.
3. Fetches `GET /api/courses/:courseId/lessons` to compute previous/next lesson navigation.

Renders:
- All `content_blocks` via `ContentBlock` components.
- All `exercises` via `ExerciseCard` components.
- Previous/Next lesson navigation buttons.
- "Mark as Complete" button (shown when there are no exercises, or as a fallback).

### PlaygroundPage

Free code sandbox. Contains a full-page `CodeEditor` with a "Run Code" button. No exercises, no tests. Calls `api.runCode()` and renders `OutputPanel`.

### ProgressPage

Reads `getCompletedLessons()` from localStorage, then fetches all courses and their lessons from the API. Computes:
- Per-course completion count and percentage
- Overall completion across all lessons
- Renders a progress bar and lesson-by-lesson checklist

No API writes — purely a read of localStorage + API.

### LoginPage / RegisterPage

Placeholder pages. Display a "login not required" message. The routes `/login` and `/register` were in the original design when auth was planned; they have been kept but point to stub components.

---

## 10. Styling Architecture

### CSS custom properties (`global.css`)

All design tokens are defined as CSS variables on `:root`:

```css
:root {
  --color-primary: #4f46e5;       /* Indigo */
  --color-primary-hover: #4338ca;
  --color-success: #16a34a;
  --color-error: #dc2626;
  --color-warning: #d97706;
  --color-bg: #f9fafb;
  --color-surface: #ffffff;
  --color-border: #e5e7eb;
  --color-text: #111827;
  --color-text-muted: #6b7280;

  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: "Fira Code", "Cascadia Code", "JetBrains Mono", monospace;

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;

  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.15);

  --spacing-page: 1rem;
}
```

### Component-scoped CSS files

Each component has a co-located `.css` file. There is no CSS Modules or CSS-in-JS — imports are global, but selectors are scoped by convention using the component's root class name (e.g., `.code-editor`, `.exercise-card`, `.output-panel`).

### Mobile-first responsive design

Media queries use `min-width` breakpoints:
```css
/* Mobile default styles */
.lesson-layout { flex-direction: column; }

/* Tablet/desktop override */
@media (min-width: 768px) {
  .lesson-layout { flex-direction: row; }
}
```

Key mobile UX decisions:
- `font-size: 16px` on all `<input>` and `<textarea>` elements — prevents iOS auto-zoom when focused
- `touch-action: manipulation` on buttons and interactive elements — prevents the 300ms tap delay and accidental double-tap zoom
- Sticky "Run Code" button — uses `position: sticky; bottom: 0` so it is always reachable without scrolling to the bottom of a long code editor
- Minimum touch target size of 44–48px on all interactive controls

---

## 11. Auth Context (Placeholder)

`src/context/AuthContext.jsx` provides a `useAuth()` hook that currently returns `{ user: null, loading: false }`. It exists so:

1. Any component that calls `useAuth()` won't throw if auth is re-enabled.
2. The `AuthProvider` wrapper in `main.jsx` is already in place.

To re-enable authentication, you would:
1. Add signup/login endpoints to the Django backend.
2. Update `AuthContext.jsx` to manage JWT tokens (e.g., in `localStorage` or `HttpOnly` cookies).
3. Update `api.js` to include `Authorization: Bearer <token>` on protected requests.
4. Add `PrivateRoute` wrapper components around lessons/progress routes if you want to gate content.

---

## 12. Running Locally

```bash
# Install dependencies
npm install

# Start dev server on port 3000
npm run dev
```

Requires the Django backend to be running on port 8000 (Vite proxies `/api` to it).

Other commands:

```bash
npm run build     # production bundle → dist/
npm run preview   # serve the dist/ build locally to test before deploying
```

---

## 13. Environment Variables

Vite exposes environment variables prefixed with `VITE_` via `import.meta.env`.

Create a `.env` file in the `frontend/` directory:

```env
# Leave empty in local dev — Vite proxy handles /api → localhost:8000
VITE_API_URL=

# Set this to the Render backend URL in production:
# VITE_API_URL=https://learnpython-api.onrender.com
```

Variables without the `VITE_` prefix are not accessible in browser code (Vite strips them for security).

---

## 14. Production Build & Deployment (Vercel)

### Build output

`npm run build` produces `dist/`:
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js   ← bundled JS
│   └── index-[hash].css  ← bundled CSS
```

### Vercel configuration

`vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

This is the critical SPA rule. Without it, navigating directly to `/courses/1/lessons` or refreshing the page would return a 404 from Vercel's CDN edge because there is no `courses/1/lessons/index.html` file. The rewrite sends all paths to `index.html`, and React Router's `BrowserRouter` reads `window.location.pathname` to render the correct component.

### Deployment steps

1. Import the repo to Vercel.
2. Set **Root Directory** to `frontend`.
3. Vercel auto-detects Vite and uses `npm run build` as the build command and `dist` as the output directory.
4. Add environment variable: `VITE_API_URL` = your Render backend URL (no trailing slash).
5. Deploy. All subsequent pushes to the connected branch auto-deploy.

### CORS requirement

After deploying, copy your Vercel URL (e.g., `https://learnpython-abc123.vercel.app`) and set it as `CORS_ALLOWED_ORIGINS` in your Render backend service's environment variables. Without this, the browser will block all API fetches with a CORS error.

---

## 15. Key Design Decisions

### No global state management (no Redux/Zustand)

State is fully local to each page component. Data is fetched per-page on mount. There is no global store because:
- There are no cross-page state dependencies (lesson progress is in localStorage)
- The data model is read-heavy and simple (no optimistic updates needed)
- Adding React Query or SWR would be the natural next step if caching and refetching become a concern

### No authentication in the current build

Auth was intentionally removed to reduce complexity for the learning platform's scope. Every endpoint is public. The `AuthContext` placeholder and `LoginPage`/`RegisterPage` stubs exist to make re-enabling auth straightforward.

### react-simple-code-editor over Monaco/CodeMirror

Monaco (VSCode's editor) is ~2MB gzipped and requires a worker. CodeMirror 6 is ~250KB but has a complex API. `react-simple-code-editor` is ~5KB and is essentially a `<textarea>` with a syntax-highlighting overlay. For simple Python snippets under 50 lines, it is more than sufficient and loads almost instantly on mobile.

### Progress in localStorage instead of the server

Since there are no user accounts, tracking progress server-side would require either anonymous sessions (cookie-based) or some device fingerprinting approach. localStorage is simpler, transparent, and works offline. The downside (progress not syncing across devices) is acceptable for this use case.

### Markdown in content blocks

Storing lesson content as Markdown strings in a JSONField means:
- Content can include formatted text, code spans, headers, lists, and tables without any special frontend components
- Content is fully editable by modifying the seed script — no admin UI needed
- The same content can theoretically be exported or rendered in other contexts (email, PDF)
