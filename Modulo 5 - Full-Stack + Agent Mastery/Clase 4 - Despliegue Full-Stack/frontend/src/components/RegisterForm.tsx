// src/components/RegisterForm.tsx
/**
 * Formulario de registro con React Hook Form + Zod.
 *
 * Características:
 * - Validación completa con Zod
 * - Password confirmation
 * - Manejo de errores (email duplicado, etc.)
 * - Integración con AuthContext
 */
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

// Schema de validación con Zod
const registerSchema = z
  .object({
    nombre: z.string().min(1, "Nombre es requerido").max(100, "Máximo 100 caracteres"),
    email: z.string().email("Email inválido").min(1, "Email es requerido"),
    password: z.string().min(8, "Contraseña debe tener al menos 8 caracteres").max(100, "Máximo 100 caracteres"),
    confirmPassword: z.string().min(1, "Confirma tu contraseña"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Las contraseñas no coinciden",
    path: ["confirmPassword"],
  });

type RegisterFormData = z.infer<typeof registerSchema>;

export function RegisterForm() {
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      setError(null);
      // Omitir confirmPassword al enviar al backend
      const { confirmPassword, ...registerData } = data;
      await registerUser(registerData);
      navigate("/dashboard"); // Redirigir a dashboard después de registro exitoso
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al registrarse");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Registrarse</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
          {/* Nombre */}
          <div className="form-group">
            <label htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              type="text"
              {...register("nombre")}
              placeholder="Tu nombre"
              className={errors.nombre ? "input-error" : ""}
            />
            {errors.nombre && <span className="error-message">{errors.nombre.message}</span>}
          </div>

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

          {/* Confirm Password */}
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirmar Contraseña</label>
            <input
              id="confirmPassword"
              type="password"
              {...register("confirmPassword")}
              placeholder="••••••••"
              className={errors.confirmPassword ? "input-error" : ""}
            />
            {errors.confirmPassword && <span className="error-message">{errors.confirmPassword.message}</span>}
          </div>

          {/* Error de API */}
          {error && <div className="api-error">{error}</div>}

          {/* Submit */}
          <button type="submit" disabled={isSubmitting} className="submit-button">
            {isSubmitting ? "Registrando..." : "Registrarse"}
          </button>
        </form>

        {/* Link a login */}
        <div className="auth-footer">
          ¿Ya tienes cuenta? <Link to="/login">Inicia sesión aquí</Link>
        </div>
      </div>
    </div>
  );
}
