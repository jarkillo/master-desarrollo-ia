/**
 * Cliente de API para tareas usando Axios.
 */
import axios from 'axios';
import type { Tarea, CrearTareaData, ActualizarTareaData, Estadisticas } from '../types/tarea';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Logging en desarrollo
if (import.meta.env.DEV) {
  api.interceptors.request.use((config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  });
}

/**
 * Servicio de tareas - abstrae las llamadas a la API.
 */
export const tareasService = {
  /**
   * Obtiene todas las tareas.
   */
  async listar(): Promise<Tarea[]> {
    const response = await api.get<Tarea[]>('/tareas');
    return response.data;
  },

  /**
   * Obtiene una tarea específica por ID.
   */
  async obtener(id: number): Promise<Tarea> {
    const response = await api.get<Tarea>(`/tareas/${id}`);
    return response.data;
  },

  /**
   * Crea una nueva tarea.
   */
  async crear(data: CrearTareaData): Promise<Tarea> {
    const response = await api.post<Tarea>('/tareas', data);
    return response.data;
  },

  /**
   * Actualiza una tarea existente (parcial).
   */
  async actualizar(id: number, data: ActualizarTareaData): Promise<Tarea> {
    const response = await api.patch<Tarea>(`/tareas/${id}`, data);
    return response.data;
  },

  /**
   * Elimina una tarea.
   */
  async eliminar(id: number): Promise<void> {
    await api.delete(`/tareas/${id}`);
  },

  /**
   * Obtiene estadísticas de tareas.
   */
  async estadisticas(): Promise<Estadisticas> {
    const response = await api.get<Estadisticas>('/tareas/stats');
    return response.data;
  },
};
