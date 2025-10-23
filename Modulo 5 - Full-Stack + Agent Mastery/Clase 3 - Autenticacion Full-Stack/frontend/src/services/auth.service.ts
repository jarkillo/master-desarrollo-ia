// src/services/auth.service.ts
/**
 * Servicio de autenticación con Axios.
 *
 * Maneja:
 * - Registro y login
 * - Almacenamiento de token en localStorage
 * - Interceptor de Axios para agregar Authorization header automáticamente
 * - Refresh automático si el token expira
 */
import axios from "axios";
import type { AuthResponse, RegisterRequest, LoginRequest, User } from "../types/auth";

const API_BASE_URL = "http://localhost:8000";

// Crear instancia de Axios con configuración base
export const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ========== Token Management ==========

const TOKEN_KEY = "auth_token";

export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

export const setToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

export const removeToken = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

// ========== Axios Interceptors ==========

// Request interceptor: Agregar token JWT a todas las requests
axiosInstance.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Manejar errores 401 (token expirado/inválido)
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido -> logout automático
      removeToken();
      // Redirigir a login (esto se puede mejorar con React Router)
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// ========== Auth API Calls ==========

export const authService = {
  /**
   * Registra un nuevo usuario.
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await axiosInstance.post<AuthResponse>("/auth/register", data);
    // Guardar token automáticamente
    setToken(response.data.access_token);
    return response.data;
  },

  /**
   * Login de usuario existente.
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await axiosInstance.post<AuthResponse>("/auth/login", data);
    // Guardar token automáticamente
    setToken(response.data.access_token);
    return response.data;
  },

  /**
   * Obtiene los datos del usuario autenticado.
   */
  async getCurrentUser(): Promise<User> {
    const response = await axiosInstance.get<User>("/auth/me");
    return response.data;
  },

  /**
   * Logout (borra token local).
   */
  logout(): void {
    removeToken();
  },

  /**
   * Verifica si hay un token almacenado.
   */
  isAuthenticated(): boolean {
    return getToken() !== null;
  },
};
