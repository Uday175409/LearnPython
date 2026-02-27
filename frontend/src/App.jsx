// ============================================================
// App.jsx — Root Component & Route Definitions (No Auth)
// ============================================================
// All pages are public — no login required.
// ============================================================

import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

// Pages
import HomePage from "./pages/HomePage";
import CoursesPage from "./pages/CoursesPage";
import LessonsPage from "./pages/LessonsPage";
import LessonPage from "./pages/LessonPage";
import PlaygroundPage from "./pages/PlaygroundPage";
import ProgressPage from "./pages/ProgressPage";

// Layout
import Header from "./components/Header";

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/courses" element={<CoursesPage />} />
          <Route path="/courses/:courseId/lessons" element={<LessonsPage />} />
          <Route path="/lessons/:lessonId" element={<LessonPage />} />
          <Route path="/playground" element={<PlaygroundPage />} />
          <Route path="/progress" element={<ProgressPage />} />

          {/* Catch-all — redirect unknown routes to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
