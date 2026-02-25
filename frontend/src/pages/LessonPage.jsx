// ============================================================
// pages/LessonPage.jsx — Full Lesson View
// ============================================================
// Displays all lesson content blocks and exercises.
// Has a "Mark as Complete" button for lessons without exercises.
// ============================================================

import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getLesson, markLessonComplete } from "../api";
import ContentBlock from "../components/ContentBlock";
import ExerciseCard from "../components/ExerciseCard";
import "./LessonPage.css";

export default function LessonPage() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [completing, setCompleting] = useState(false);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    async function fetchLesson() {
      setLoading(true);
      try {
        const data = await getLesson(lessonId);
        setLesson(data);
      } catch (err) {
        setError("Unable to load this lesson. Check your connection.");
      }
      setLoading(false);
    }
    fetchLesson();
  }, [lessonId]);

  async function handleMarkComplete() {
    setCompleting(true);
    try {
      await markLessonComplete(lessonId);
      setCompleted(true);
    } catch {
      // Silently fail — the button will just stay enabled
    }
    setCompleting(false);
  }

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" />
        <p>Loading lesson...</p>
      </div>
    );
  }

  if (error) {
    return <div className="page-error">{error}</div>;
  }

  if (!lesson) {
    return <div className="page-error">Lesson not found.</div>;
  }

  const hasExercises = lesson.exercises && lesson.exercises.length > 0;

  return (
    <div className="lesson-page">
      {/* Back Link */}
      <Link
        to={`/courses/${lesson.course_id}/lessons`}
        className="back-link"
      >
        ← Back to Lessons
      </Link>

      {/* Lesson Header */}
      <h1 className="lesson-title">{lesson.title}</h1>
      {lesson.subtitle && (
        <p className="lesson-subtitle-text">{lesson.subtitle}</p>
      )}

      {/* Content Blocks */}
      <div className="lesson-content">
        {(lesson.content_blocks || []).map((block, index) => (
          <ContentBlock key={index} block={block} />
        ))}
      </div>

      {/* Exercises */}
      {hasExercises && (
        <div className="lesson-exercises">
          <h2 className="exercises-header">✏️ Practice Time!</h2>
          <p className="exercises-intro">
            Try the exercises below. Don't worry about getting them
            right the first time — that's normal! Use the hints if you
            get stuck.
          </p>
          {lesson.exercises.map((exercise) => (
            <ExerciseCard key={exercise.id} exercise={exercise} />
          ))}
        </div>
      )}

      {/* Mark Complete Button (for reading-only lessons) */}
      {!hasExercises && (
        <div className="lesson-complete-section">
          <button
            className={`complete-button ${completed ? "done" : ""}`}
            onClick={handleMarkComplete}
            disabled={completing || completed}
          >
            {completed
              ? "✅ Lesson Complete!"
              : completing
              ? "⏳ Saving..."
              : "✅ Mark as Complete"}
          </button>
        </div>
      )}

      {/* Navigation to next lesson - simple approach */}
      <div className="lesson-nav">
        <Link
          to={`/courses/${lesson.course_id}/lessons`}
          className="lesson-nav-button"
        >
          📖 Back to All Lessons
        </Link>
      </div>
    </div>
  );
}
