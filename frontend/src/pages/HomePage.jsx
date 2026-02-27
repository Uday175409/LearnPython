// ============================================================
// pages/HomePage.jsx — Landing Page (No Auth)
// ============================================================
// The first page visitors see. Direct CTA to start learning.
// ============================================================

import React from "react";
import { Link } from "react-router-dom";
import "./HomePage.css";

export default function HomePage() {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-emoji">🐍</div>
        <h1 className="hero-title">Learn Python on Your Phone</h1>
        <p className="hero-subtitle">
          Free, beginner-friendly lessons that explain everything
          step by step. No experience needed — just your phone
          and curiosity.
        </p>

        <Link to="/courses" className="cta-button">
          🚀 Start Learning — Free
        </Link>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2 className="features-title">Built For You</h2>

        <div className="feature-card">
          <span className="feature-icon">📱</span>
          <h3>Phone-First Design</h3>
          <p>
            Practice coding right on your phone. No computer needed.
            Big buttons, vertical layout, fast loading.
          </p>
        </div>

        <div className="feature-card">
          <span className="feature-icon">🐢</span>
          <h3>Slow & Patient</h3>
          <p>
            Every concept is explained before showing code.
            No jargon. No rushing. Learn at your own pace.
          </p>
        </div>

        <div className="feature-card">
          <span className="feature-icon">✏️</span>
          <h3>Practice Immediately</h3>
          <p>
            Write and run real Python code after each lesson.
            Get instant feedback and helpful error explanations.
          </p>
        </div>

        <div className="feature-card">
          <span className="feature-icon">🎯</span>
          <h3>Clear Learning Path</h3>
          <p>
            Follow a structured path from "What is programming?"
            all the way to writing real programs.
          </p>
        </div>

        <div className="feature-card">
          <span className="feature-icon">🆘</span>
          <h3>Hints & Solutions</h3>
          <p>
            Stuck? Every exercise has hints, full solutions,
            and detailed explanations of why they work.
          </p>
        </div>

        <div className="feature-card">
          <span className="feature-icon">🔒</span>
          <h3>Safe to Experiment</h3>
          <p>
            You can't break anything! Your code runs in a safe
            sandbox. Try things out — that's how you learn.
          </p>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="bottom-cta">
        <h2>Ready to Start?</h2>
        <p>It's free. No account needed. Just begin.</p>
        <Link to="/courses" className="cta-button">
          📚 Browse Courses
        </Link>
      </section>
    </div>
  );
}
