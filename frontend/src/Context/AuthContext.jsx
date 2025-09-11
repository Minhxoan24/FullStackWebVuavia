import React, { createContext, useEffect, useState } from "react";
import AuthService from "../Services/AuthService";
import apiClient from "../Services/ApiService";
import { getProfile } from "../Services/ApiUserService";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(() => localStorage.getItem("access_token") || null);

  useEffect(() => {
    if (token) {
      apiClient.defaults.headers.common.Authorization = `Bearer ${token}`;
      if (getProfile) getProfile().then(setUser).catch(() => setUser(null));
    } else {
      delete apiClient.defaults.headers.common.Authorization;
      setUser(null);
    }
  }, [token]);

  const login = async ({ accountname, password }, remember = false) => {
    setLoading(true);
    try {
      const data = await AuthService.login({ accountname, password });
      const access = data.access_token; const refresh = data.refresh_token;
      if (remember) {
        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh);
      } else {
        sessionStorage.setItem("access_token", access);
        sessionStorage.setItem("refresh_token", refresh);
      }
      apiClient.defaults.headers.common.Authorization = `Bearer ${access}`;
      setToken(access);
      return data;
    } finally { setLoading(false); }
  };

  const register = async (payload) => {
    setLoading(true);
    try {
      const data = await AuthService.register(payload);
      // auto-login on register (optional)
      const access = data.access_token; const refresh = data.refresh_token;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      apiClient.defaults.headers.common.Authorization = `Bearer ${access}`;
      setToken(access);
      return data;
    } finally { setLoading(false); }
  };

  const logout = async () => {
    await AuthService.logout();
    localStorage.removeItem("access_token"); localStorage.removeItem("refresh_token");
    sessionStorage.removeItem("access_token"); sessionStorage.removeItem("refresh_token");
    delete apiClient.defaults.headers.common.Authorization;
    setToken(null); setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
