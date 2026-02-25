// ============================================================
// pages/LessonsPage.jsx — Lesson List for a Course
// ============================================================
// Shows all lessons with completion status and lock indicators.
// Locked lessons (prerequisites not met) are visually disabled.
// ============================================================

import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getLessons } from "../api";
import "./LessonsPage.css";

export default function LessonsPage() {
  const { courseId } = useParams();
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchLessons() {
      try {
        const data = await getLessons(courseId);
        setLessons(data);
      } catch (err) {
        setError("Unable to load lessons. Check your connection.");
      }
      setLoading(false);
    }
    fetchLessons();
  }, [courseId]);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" />
        <p>Loading lessons...</p>
      </div>
    );
  }

  if (error) {
    return <div className="page-error">{error}</div>;
  }

  return (
    <div className="lessons-page">
      <Link to="/courses" className="back-link">← Back to Courses</Link>
      <h1 className="page-title">📖 Lessons</h1>
      <p className="page-subtitle">
        Complete lessons in order. Each one unlocks the next!
      </p>

      <div className="lesson-list">
        {lessons.map((lesson, index) => {
          const isLocked = lesson.is_locked;
          const isCompleted = lesson.is_completed;

          return (
            <div key={lesson.id} className="lesson-item-wrapper">
              {isLocked ? (
                // Locked lesson — not tappable
                <div className="lesson-item locked">
                  <div className="lesson-number">{index + 1}</div>
                  <div className="lesson-info">
                    <h3 className="lesson-title">{lesson.title}</h3>
                    <p className="lesson-subtitle">{lesson.subtitle}</p>
                  </div>
                  <span className="lesson-status">🔒</span>
                </div>
              ) : (
                // Unlocked lesson — tappable
                <Link
                  to={`/lessons/${lesson.id}`}
                  className={`lesson-item ${isCompleted ? "completed" : "available"}`}
                >
                  <div className="lesson-number">{index + 1}</div>
                  <div className="lesson-info">
                    <h3 className="lesson-title">{lesson.title}</h3>
                    <p className="lesson-subtitle">{lesson.subtitle}</p>
                  </div>
                  <span className="lesson-status">
                    {isCompleted ? "✅" : "→"}
                  </span>
                </Link>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
