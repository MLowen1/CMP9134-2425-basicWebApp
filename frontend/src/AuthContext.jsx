import React, { createContext, useContext, useState, useEffect } from 'react';

// Default context values for unauthenticated usage
const AuthContext = createContext({
  user: null,
  token: null,
  isAuthenticated: false,
  login: async () => ({ success: false }),
  register: async () => ({ success: false }),
  logout: () => {},
});

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('token'));

  // Helper to load current user from token
  const fetchCurrentUser = async (accessToken) => {
    try {
      const resp = await fetch('http://localhost:5000/@me', {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (resp.ok) {
        const data = await resp.json();
        setUser(data);
      } else {
        setUser(null);
        localStorage.removeItem('token');
        setToken(null);
      }
    } catch {
      setUser(null);
    }
  };

  // On mount or when token changes, attempt to load user
  useEffect(() => {
    if (token) {
      fetchCurrentUser(token);
    }
  }, [token]);

  // Login function
  const login = async (username, password) => {
    try {
      const resp = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await resp.json();
      if (resp.ok && data.access_token) {
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
        await fetchCurrentUser(data.access_token);
        return { success: true };
      }
      return { success: false, message: data.message || 'Login failed' };
    } catch (e) {
      return { success: false, message: e.message };
    }
  };

  // Register function
  const register = async (username, password) => {
    try {
      const resp = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await resp.json();
      if (resp.ok && data.access_token) {
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
        await fetchCurrentUser(data.access_token);
        return { success: true };
      }
      return { success: false, message: data.message || 'Registration failed' };
    } catch (e) {
      return { success: false, message: e.message };
    }
  };

  // Logout function
  const logout = async () => {
    if (token) {
      await fetch('http://localhost:5000/logout', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
    }
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, token, isAuthenticated: !!user, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);