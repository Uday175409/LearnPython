// ============================================================
// context/AuthContext.jsx — Authentication State
// ============================================================
// Provides user authentication state to the entire app.
// Any component can check if the user is logged in by using
// the useAuth() hook.
// ============================================================

import React, { createContext, useContext, useState, useEffect } from "react";
import { getMe, logout as apiLogout } from "../api";

// Create the context (a way to share data across components)
const AuthContext = createContext(null);

/**
 * AuthProvider wraps the app and provides auth state to all children.
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On mount, check if the user has a valid token
  useEffect(() => {
    async function checkUser() {
      const token = localStorage.getItem("token");
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const userData = await getMe();
        setUser(userData);
      } catch {
        // Token is invalid or expired — clear it
        localStorage.removeItem("token");
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    checkUser();
  }, []);

  /**
   * Call after successful login/register to update the user state.
   */
  async function refreshUser() {
    try {
      const userData = await getMe();
      setUser(userData);
    } catch {
      setUser(null);
    }
  }

  /**
   * Log out — clear token and user state.
   */
  function logout() {
    apiLogout();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, refreshUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access auth state from any component.
 *
 * Usage:
 *   const { user, logout } = useAuth();
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
