// src/types/auth.ts
/**
 * Tipos TypeScript para autenticación.
 */

export interface User {
  id: string;
  email: string;
  nombre: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  nombre: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}
