// ============================================================
// pages/LessonPage.jsx — Full Lesson View
// ============================================================
// Displays all lesson content blocks and exercises.
// Has a "Mark as Complete" button for lessons without exercises.
// ============================================================

import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getLesson, getLessons, markLessonComplete } from "../api";
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
  const [prevLesson, setPrevLesson] = useState(null);
  const [nextLesson, setNextLesson] = useState(null);

  useEffect(() => {
    async function fetchLesson() {
      setLoading(true);
      setCompleted(false);
      setPrevLesson(null);
      setNextLesson(null);
      try {
        const data = await getLesson(lessonId);
        setLesson(data);

        // Fetch all lessons in this course to find prev/next
        try {
          const allLessons = await getLessons(data.course_id);
          const sorted = allLessons.sort((a, b) => a.order - b.order);
          const idx = sorted.findIndex((l) => l.id === data.id);
          if (idx > 0) setPrevLesson(sorted[idx - 1]);
          if (idx < sorted.length - 1) setNextLesson(sorted[idx + 1]);
        } catch {
          // Non-critical — navigation just won't show
        }
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

      {/* Prev / Next Navigation */}
      <div className="lesson-nav">
        <div className="lesson-nav-row">
          {prevLesson ? (
            <Link
              to={`/lessons/${prevLesson.id}`}
              className="lesson-nav-button prev"
            >
              <span className="nav-arrow">←</span>
              <span className="nav-label">Previous</span>
              <span className="nav-title">{prevLesson.title}</span>
            </Link>
          ) : (
            <div />  /* empty spacer */
          )}

          {nextLesson ? (
            <Link
              to={`/lessons/${nextLesson.id}`}
              className="lesson-nav-button next"
            >
              <span className="nav-arrow">→</span>
              <span className="nav-label">Next</span>
              <span className="nav-title">{nextLesson.title}</span>
            </Link>
          ) : (
            <div />  /* empty spacer */
          )}
        </div>

        <Link
          to={`/courses/${lesson.course_id}/lessons`}
          className="lesson-nav-all"
        >
          📖 Back to All Lessons
        </Link>
      </div>
    </div>
  );
}
