/**
 * Componente principal que muestra la lista de tareas.
 * Usa React Query para data fetching con loading/error states.
 */
import { useTareas, useEstadisticas } from '../hooks/useTareas';
import { TareaItem } from './TareaItem';
import { CrearTareaForm } from './CrearTareaForm';

export function TareasLista() {
  const { data: tareas, isLoading, isError, error, refetch } = useTareas();
  const { data: estadisticas } = useEstadisticas();

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Cargando tareas...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="error-container">
        <h2>❌ Error al cargar tareas</h2>
        <p>{error?.message || 'Error desconocido'}</p>
        <button className="btn btn-primary" onClick={() => refetch()}>
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="tareas-container">
      <div className="tareas-header">
        <h1>📝 Gestión de Tareas</h1>

        {estadisticas && (
          <div className="estadisticas">
            <span className="stat">
              Total: <strong>{estadisticas.total}</strong>
            </span>
            <span className="stat">
              Completadas: <strong>{estadisticas.completadas}</strong>
            </span>
            <span className="stat">
              Pendientes: <strong>{estadisticas.pendientes}</strong>
            </span>
          </div>
        )}
      </div>

      <CrearTareaForm />

      <div className="tareas-lista">
        {tareas && tareas.length === 0 ? (
          <div className="empty-state">
            <p>No hay tareas todavía. ¡Crea tu primera tarea!</p>
          </div>
        ) : (
          tareas?.map((tarea) => <TareaItem key={tarea.id} tarea={tarea} />)
        )}
      </div>
    </div>
  );
}
