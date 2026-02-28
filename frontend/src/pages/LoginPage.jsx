// ============================================================
// pages/LoginPage.jsx — Login Form (Disabled)
// ============================================================
// Auth was removed. This page redirects to courses.
// ============================================================

import React from "react";
import { Navigate } from "react-router-dom";

export default function LoginPage() {
  return <Navigate to="/courses" replace />;
}
