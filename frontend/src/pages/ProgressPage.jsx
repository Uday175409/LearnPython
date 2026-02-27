// ============================================================
// pages/ProgressPage.jsx — Student Progress Dashboard
// ============================================================
// Shows overall progress tracked via localStorage.
// ============================================================

import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getProgress, getCourses, getLessons } from "../api";
import "./ProgressPage.css";

export default function ProgressPage() {
  const [totalLessons, setTotalLessons] = useState(0);
  const [completedCount, setCompletedCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const completedIds = getProgress();
        const courses = await getCourses();

        // Get total lesson count from all courses
        let total = 0;
        for (const course of courses) {
          const lessons = await getLessons(course.id);
          total += lessons.length;
        }

        setTotalLessons(total);
        setCompletedCount(completedIds.length);
      } catch (err) {
        setError("Unable to load progress. Check your connection.");
      }
      setLoading(false);
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" />
        <p>Loading progress...</p>
      </div>
    );
  }

  if (error) {
    return <div className="page-error">{error}</div>;
  }

  const percent = totalLessons > 0
    ? Math.round(completedCount / totalLessons * 100)
    : 0;

  return (
    <div className="progress-page">
      <h1 className="page-title">📊 Your Progress</h1>

      <p className="progress-welcome">
        Here's how you're doing!
      </p>

      {/* Progress Summary Card */}
      <div className="progress-summary">
        <div className="progress-circle">
          <span className="progress-percent">
            {percent}%
          </span>
        </div>
        <div className="progress-stats">
          <div className="stat">
            <span className="stat-value">{completedCount}</span>
            <span className="stat-label">Completed</span>
          </div>
          <div className="stat">
            <span className="stat-value">{totalLessons}</span>
            <span className="stat-label">Total Lessons</span>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar-container">
        <div
          className="progress-bar-fill"
          style={{ width: `${percent}%` }}
        />
      </div>

      {/* Encouragement */}
      <div className="progress-encouragement">
        {percent === 0 && (
          <p>🌱 You're just getting started! Begin your first lesson today.</p>
        )}
        {percent > 0 && percent < 50 && (
          <p>🚀 Great start! Keep going — every lesson builds on the last.</p>
        )}
        {percent >= 50 && percent < 100 && (
          <p>🔥 You're more than halfway there! Amazing progress!</p>
        )}
        {percent === 100 && (
          <p>🎉 You've completed all lessons! You're a Python star!</p>
        )}
      </div>

      {/* Action Button */}
      <Link to="/courses" className="progress-action-button">
        📚 Continue Learning
      </Link>
    </div>
  );
}
