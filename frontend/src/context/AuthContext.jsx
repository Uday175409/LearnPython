// ============================================================
// context/AuthContext.jsx — Authentication State (Placeholder)
// ============================================================
// Auth was removed from this app. All pages are public.
// This file is kept as a placeholder in case auth is re-added.
// ============================================================

import React, { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

/**
 * AuthProvider wraps the app and provides auth state to all children.
 * Currently a no-op since auth is disabled.
 */
export function AuthProvider({ children }) {
  const [user] = useState(null);
  const loading = false;

  function refreshUser() {}
  function logout() {}

  return (
    <AuthContext.Provider value={{ user, loading, refreshUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access auth state from any component.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
