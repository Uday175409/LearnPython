// ============================================================
// pages/RegisterPage.jsx — Sign Up Form (Disabled)
// ============================================================
// Auth was removed. This page redirects to courses.
// ============================================================

import React from "react";
import { Navigate } from "react-router-dom";

export default function RegisterPage() {
  return <Navigate to="/courses" replace />;
}
