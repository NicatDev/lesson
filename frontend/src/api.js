import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE || "/api";

export const api = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function login(username, password) {
  const { data } = await api.post("/auth/token/", { username, password });
  localStorage.setItem("access", data.access);
  localStorage.setItem("refresh", data.refresh);
  return data;
}

export async function register(payload) {
  await api.post("/auth/register/", payload);
}

export async function refreshAccess() {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) throw new Error("no refresh");
  const { data } = await api.post("/auth/token/refresh/", { refresh });
  localStorage.setItem("access", data.access);
  if (data.refresh) localStorage.setItem("refresh", data.refresh);
  return data.access;
}

export function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}
