// ============================================================
// pages/CoursesPage.jsx — Course List
// ============================================================
// Shows all available courses as large, tappable cards.
// ============================================================

import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getCourses } from "../api";
import "./CoursesPage.css";

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchCourses() {
      try {
        const data = await getCourses();
        setCourses(data);
      } catch (err) {
        setError("Unable to load courses. Check your connection.");
      }
      setLoading(false);
    }
    fetchCourses();
  }, []);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" />
        <p>Loading courses...</p>
      </div>
    );
  }

  if (error) {
    return <div className="page-error">{error}</div>;
  }

  return (
    <div className="courses-page">
      <h1 className="page-title">📚 Your Courses</h1>
      <p className="page-subtitle">
        Tap a course to see its lessons. Complete them in order!
      </p>

      <div className="course-list">
        {courses.map((course) => (
          <Link
            key={course.id}
            to={`/courses/${course.id}/lessons`}
            className="course-card"
          >
            <span className="course-icon">{course.icon}</span>
            <div className="course-info">
              <h2 className="course-title">{course.title}</h2>
              <p className="course-desc">{course.description}</p>
              <span className="course-lessons">
                {course.lesson_count} lessons
              </span>
            </div>
            <span className="course-arrow">→</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
