// src/components/LoginForm.tsx
/**
 * Formulario de login con React Hook Form + Zod.
 *
 * Características:
 * - Validación con Zod schema
 * - Manejo de errores de API
 * - Loading state durante login
 * - Integración con AuthContext
 */
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

// Schema de validación con Zod
const loginSchema = z.object({
  email: z.string().email("Email inválido").min(1, "Email es requerido"),
  password: z.string().min(1, "Contraseña es requerida"),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setError(null);
      await login(data);
      navigate("/dashboard"); // Redirigir a dashboard después de login exitoso
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al iniciar sesión");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Iniciar Sesión</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
          {/* Email */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              {...register("email")}
              placeholder="tu@email.com"
              className={errors.email ? "input-error" : ""}
            />
            {errors.email && <span className="error-message">{errors.email.message}</span>}
          </div>

          {/* Password */}
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              {...register("password")}
              placeholder="••••••••"
              className={errors.password ? "input-error" : ""}
            />
            {errors.password && <span className="error-message">{errors.password.message}</span>}
          </div>

          {/* Error de API */}
          {error && <div className="api-error">{error}</div>}

          {/* Submit */}
          <button type="submit" disabled={isSubmitting} className="submit-button">
            {isSubmitting ? "Iniciando sesión..." : "Iniciar Sesión"}
          </button>
        </form>

        {/* Link a registro */}
        <div className="auth-footer">
          ¿No tienes cuenta? <Link to="/register">Regístrate aquí</Link>
        </div>
      </div>
    </div>
  );
}
