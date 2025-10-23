// src/components/Dashboard.tsx
/**
 * Página de Dashboard protegida.
 *
 * Solo accesible si el usuario está autenticado.
 * Muestra información del usuario y datos del dashboard.
 */
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!user) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Dashboard</h1>
        <div className="user-info">
          <span>
            Bienvenido, <strong>{user.nombre}</strong> ({user.email})
          </span>
          <button onClick={handleLogout} className="logout-button">
            Cerrar Sesión
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        <div className="dashboard-card">
          <h2>Información del Usuario</h2>
          <ul>
            <li>
              <strong>ID:</strong> {user.id}
            </li>
            <li>
              <strong>Email:</strong> {user.email}
            </li>
            <li>
              <strong>Nombre:</strong> {user.nombre}
            </li>
            <li>
              <strong>Registrado:</strong> {new Date(user.created_at).toLocaleString("es-ES")}
            </li>
          </ul>
        </div>

        <div className="dashboard-card">
          <h2>Estadísticas</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value">5</div>
              <div className="stat-label">Tareas Totales</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">3</div>
              <div className="stat-label">Pendientes</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">2</div>
              <div className="stat-label">Completadas</div>
            </div>
          </div>
        </div>

        <div className="dashboard-card">
          <h2>Recursos Protegidos</h2>
          <p>Este contenido solo es visible para usuarios autenticados.</p>
          <p>
            El token JWT se envía automáticamente en todas las requests mediante el <strong>Axios interceptor</strong>.
          </p>
        </div>
      </main>
    </div>
  );
}
