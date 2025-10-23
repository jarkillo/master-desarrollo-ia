// src/components/TareasLista.tsx
import { useState, useEffect } from 'react';
import { tareasService, type ApiError } from '../services/tareas.service';
import type { Tarea } from '../types/tarea';
import { TareaItem } from './TareaItem';
import { CrearTareaForm } from './CrearTareaForm';

/**
 * Componente principal que maneja la lista de tareas.
 *
 * Demuestra los conceptos fundamentales de React:
 * - useState: manejo de estado local (tareas, loading, errores)
 * - useEffect: efectos secundarios (fetch inicial de datos)
 * - Event handlers: callbacks para crear, actualizar, eliminar
 * - Composition: compone TareaItem y CrearTareaForm
 */
export function TareasLista() {
  // Estado: lista de tareas
  const [tareas, setTareas] = useState<Tarea[]>([]);

  // Estado: loading durante fetch inicial
  const [isLoading, setIsLoading] = useState(true);

  // Estado: mensajes de error
  const [error, setError] = useState<string | null>(null);

  /**
   * useEffect para cargar tareas al montar el componente.
   *
   * El array vacío [] significa que solo se ejecuta una vez al montar.
   */
  useEffect(() => {
    cargarTareas();
  }, []);

  /**
   * Carga todas las tareas desde el backend.
   */
  const cargarTareas = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await tareasService.listarTareas();
      setTareas(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Error al cargar las tareas');
      console.error('Error cargando tareas:', apiError);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Crea una nueva tarea.
   */
  const crearTarea = async (nombre: string) => {
    setError(null);

    try {
      const nuevaTarea = await tareasService.crearTarea({ nombre });
      // Actualizar estado local agregando la nueva tarea
      setTareas((prev) => [...prev, nuevaTarea]);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Error al crear la tarea');
      throw err; // Re-throw para que el form maneje el error
    }
  };

  /**
   * Actualiza el estado de completitud de una tarea.
   */
  const toggleTarea = async (id: number, completada: boolean) => {
    setError(null);

    try {
      const tareaActualizada = await tareasService.actualizarTarea(id, { completada });

      // Actualizar estado local reemplazando la tarea modificada
      setTareas((prev) =>
        prev.map((t) => (t.id === id ? tareaActualizada : t))
      );
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Error al actualizar la tarea');
      throw err;
    }
  };

  /**
   * Elimina una tarea.
   */
  const eliminarTarea = async (id: number) => {
    setError(null);

    try {
      await tareasService.eliminarTarea(id);

      // Actualizar estado local removiendo la tarea eliminada
      setTareas((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Error al eliminar la tarea');
      throw err;
    }
  };

  // Render de estados de loading y error
  if (isLoading) {
    return <div className="loading">Cargando tareas...</div>;
  }

  return (
    <div className="tareas-lista">
      <h1>Lista de Tareas</h1>

      {/* Mostrar errores si existen */}
      {error && (
        <div className="error-message">
          ⚠️ {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* Formulario para crear tareas */}
      <CrearTareaForm onCrear={crearTarea} />

      {/* Lista de tareas */}
      {tareas.length === 0 ? (
        <p className="empty-state">No hay tareas. ¡Crea una para empezar!</p>
      ) : (
        <div className="tareas-container">
          {tareas.map((tarea) => (
            <TareaItem
              key={tarea.id}
              tarea={tarea}
              onToggle={toggleTarea}
              onDelete={eliminarTarea}
            />
          ))}
        </div>
      )}

      {/* Estadísticas */}
      <div className="stats">
        Total: {tareas.length} | Completadas: {tareas.filter((t) => t.completada).length}
      </div>
    </div>
  );
}
