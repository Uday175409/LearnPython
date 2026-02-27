// ============================================================
// components/Header.jsx — Top Navigation Bar (No Auth)
// ============================================================
// A simple, mobile-friendly header with navigation links.
// All links always visible — no login required.
// ============================================================

import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Header.css";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

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
          <Link to="/courses" className="nav-link" onClick={handleNavClick}>
            📚 Courses
          </Link>
          <Link to="/playground" className="nav-link" onClick={handleNavClick}>
            🎮 Playground
          </Link>
          <Link to="/progress" className="nav-link" onClick={handleNavClick}>
            📊 Progress
          </Link>
        </nav>
      </div>
    </header>
  );
}
