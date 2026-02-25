// ============================================================
// components/Header.jsx — Top Navigation Bar
// ============================================================
// A simple, mobile-friendly header with navigation links.
// Uses a hamburger menu on mobile (no hover interactions).
// ============================================================

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Header.css";

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  function handleLogout() {
    logout();
    setMenuOpen(false);
    navigate("/");
  }

  function handleNavClick() {
    setMenuOpen(false);
  }

  return (
    <header className="header">
      <div className="header-inner">
        {/* Logo / App Name */}
        <Link to="/" className="header-logo" onClick={handleNavClick}>
          🐍 LearnPython
        </Link>

        {/* Hamburger button — visible on mobile only */}
        <button
          className="hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
        >
          <span className={`hamburger-line ${menuOpen ? "open" : ""}`} />
          <span className={`hamburger-line ${menuOpen ? "open" : ""}`} />
          <span className={`hamburger-line ${menuOpen ? "open" : ""}`} />
        </button>

        {/* Navigation links */}
        <nav className={`header-nav ${menuOpen ? "open" : ""}`}>
          {user ? (
            <>
              <Link to="/courses" className="nav-link" onClick={handleNavClick}>
                📚 Courses
              </Link>
              <Link
                to="/playground"
                className="nav-link"
                onClick={handleNavClick}
              >
                🎮 Playground
              </Link>
              <Link
                to="/progress"
                className="nav-link"
                onClick={handleNavClick}
              >
                📊 Progress
              </Link>
              <button className="nav-link nav-logout" onClick={handleLogout}>
                👋 Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link" onClick={handleNavClick}>
                Log In
              </Link>
              <Link
                to="/register"
                className="nav-link nav-cta"
                onClick={handleNavClick}
              >
                Sign Up Free
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
