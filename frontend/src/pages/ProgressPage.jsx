// ============================================================
// pages/ProgressPage.jsx — Student Progress Dashboard
// ============================================================
// Shows overall progress and per-lesson completion status.
// ============================================================

import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getProgress } from "../api";
import { useAuth } from "../context/AuthContext";
import "./ProgressPage.css";

export default function ProgressPage() {
  const { user } = useAuth();
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchProgress() {
      try {
        const data = await getProgress();
        setProgress(data);
      } catch (err) {
        setError("Unable to load progress. Check your connection.");
      }
      setLoading(false);
    }
    fetchProgress();
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

  return (
    <div className="progress-page">
      <h1 className="page-title">📊 Your Progress</h1>

      {/* Welcome message */}
      <p className="progress-welcome">
        Hey {user?.username}! Here's how you're doing.
      </p>

      {/* Progress Summary Card */}
      <div className="progress-summary">
        <div className="progress-circle">
          <span className="progress-percent">
            {progress?.percent_complete || 0}%
          </span>
        </div>
        <div className="progress-stats">
          <div className="stat">
            <span className="stat-value">
              {progress?.completed_lessons || 0}
            </span>
            <span className="stat-label">Completed</span>
          </div>
          <div className="stat">
            <span className="stat-value">
              {progress?.total_lessons || 0}
            </span>
            <span className="stat-label">Total Lessons</span>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar-container">
        <div
          className="progress-bar-fill"
          style={{
            width: `${progress?.percent_complete || 0}%`,
          }}
        />
      </div>

      {/* Encouragement */}
      <div className="progress-encouragement">
        {progress?.percent_complete === 0 && (
          <p>🌱 You're just getting started! Begin your first lesson today.</p>
        )}
        {progress?.percent_complete > 0 &&
          progress?.percent_complete < 50 && (
            <p>
              🚀 Great start! Keep going — every lesson builds on the last.
            </p>
          )}
        {progress?.percent_complete >= 50 &&
          progress?.percent_complete < 100 && (
            <p>🔥 You're more than halfway there! Amazing progress!</p>
          )}
        {progress?.percent_complete === 100 && (
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
