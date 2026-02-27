// ============================================================
// api.js — API Client (No Authentication)
// ============================================================
// All communication with the backend goes through this file.
// No login or tokens — all endpoints are public.
// ============================================================

// In production, this points to your Render backend URL.
// In development, Vite proxies /api to localhost:8000.
const BASE_URL = import.meta.env.VITE_API_URL || "";

/**
 * Make an API request.
 *
 * @param {string} path - API endpoint path (e.g., "/api/courses")
 * @param {object} options - Fetch options (method, body, etc.)
 * @returns {Promise<object>} - Parsed JSON response
 */
async function request(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });

  // Handle non-JSON responses
  const contentType = response.headers.get("content-type");
  if (!contentType || !contentType.includes("application/json")) {
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    return null;
  }

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || `Request failed: ${response.status}`);
  }

  return data;
}

// ── Course & Lesson APIs ────────────────────────────────────

export async function getCourses() {
  return request("/api/courses");
}

export async function getLessons(courseId) {
  return request(`/api/courses/${courseId}/lessons`);
}

export async function getLesson(lessonId) {
  return request(`/api/lessons/${lessonId}`);
}

export async function getExercise(exerciseId) {
  return request(`/api/exercises/${exerciseId}`);
}

export async function getExerciseSolution(exerciseId) {
  return request(`/api/exercises/${exerciseId}/solution`);
}

// ── Code Execution APIs ─────────────────────────────────────

export async function runCode(code) {
  return request("/api/run", {
    method: "POST",
    body: JSON.stringify({ code }),
  });
}

export async function submitExercise(exerciseId, code) {
  return request(`/api/exercises/${exerciseId}/submit`, {
    method: "POST",
    body: JSON.stringify({ code }),
  });
}

// ── Progress (localStorage) ─────────────────────────────────

const PROGRESS_KEY = "learnpython_progress";

function getCompletedLessons() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || [];
  } catch {
    return [];
  }
}

export function isLessonCompleted(lessonId) {
  return getCompletedLessons().includes(Number(lessonId));
}

export function markLessonComplete(lessonId) {
  const completed = getCompletedLessons();
  const id = Number(lessonId);
  if (!completed.includes(id)) {
    completed.push(id);
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(completed));
  }
}

export function getProgress() {
  return getCompletedLessons();
}
