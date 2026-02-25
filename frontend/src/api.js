// ============================================================
// api.js — API Client
// ============================================================
// All communication with the backend goes through this file.
// This keeps API logic in one place, making it easy to change
// the backend URL or add error handling globally.
// ============================================================

// In production, this points to your Render backend URL.
// In development, Vite proxies /api to localhost:8000.
const BASE_URL = import.meta.env.VITE_API_URL || "";

/**
 * Make an API request with automatic token handling.
 *
 * @param {string} path - API endpoint path (e.g., "/api/courses")
 * @param {object} options - Fetch options (method, body, etc.)
 * @returns {Promise<object>} - Parsed JSON response
 */
async function request(path, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Attach the JWT token if the user is logged in
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

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
    // The backend sends error details in the "detail" field
    throw new Error(data.detail || `Request failed: ${response.status}`);
  }

  return data;
}

// ── Auth APIs ───────────────────────────────────────────────

export async function registerUser(username, email, password) {
  const data = await request("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });
  // Store the token automatically
  localStorage.setItem("token", data.access_token);
  return data;
}

export async function loginUser(username, password) {
  const data = await request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  localStorage.setItem("token", data.access_token);
  return data;
}

export async function getMe() {
  return request("/api/auth/me");
}

export function logout() {
  localStorage.removeItem("token");
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

// ── Progress APIs ───────────────────────────────────────────

export async function getProgress() {
  return request("/api/progress");
}

export async function markLessonComplete(lessonId) {
  return request(`/api/lessons/${lessonId}/complete`, {
    method: "POST",
  });
}
