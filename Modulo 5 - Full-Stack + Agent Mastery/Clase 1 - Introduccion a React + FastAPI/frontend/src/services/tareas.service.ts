// src/services/tareas.service.ts
import axios, { AxiosError } from 'axios';
import type { Tarea, CrearTareaDto, ActualizarTareaDto } from '../types/tarea';

/**
 * Configuración base de Axios para comunicación con el backend.
 *
 * En desarrollo, Vite proxy redirige /api a http://localhost:8000
 * En producción, configura la URL completa del backend.
 */
const api = axios.create({
  baseURL: '/api',  // Usa el proxy de Vite en desarrollo
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,  // 5 segundos timeout
});

/**
 * Tipo para errores de API estructurados.
 */
export interface ApiError {
  message: string;
  status?: number;
  detail?: string;
}

/**
 * Maneja errores de Axios y los convierte en objetos de error estructurados.
 */
function handleApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string }>;
    return {
      message: axiosError.response?.data?.detail || axiosError.message || 'Error desconocido',
      status: axiosError.response?.status,
      detail: axiosError.response?.data?.detail,
    };
  }

  return {
    message: error instanceof Error ? error.message : 'Error desconocido',
  };
}

/**
 * Servicio para interactuar con la API de tareas.
 *
 * Todas las funciones son async y retornan Promises.
 * Los errores se capturan y se convierten en ApiError.
 */
export const tareasService = {
  /**
   * Obtiene todas las tareas.
   */
  async listarTareas(): Promise<Tarea[]> {
    try {
      const response = await api.get<Tarea[]>('/tareas');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Crea una nueva tarea.
   */
  async crearTarea(dto: CrearTareaDto): Promise<Tarea> {
    try {
      const response = await api.post<Tarea>('/tareas', dto);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Actualiza el estado de completitud de una tarea.
   */
  async actualizarTarea(id: number, dto: ActualizarTareaDto): Promise<Tarea> {
    try {
      const response = await api.patch<Tarea>(`/tareas/${id}`, dto);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Elimina una tarea.
   */
  async eliminarTarea(id: number): Promise<void> {
    try {
      await api.delete(`/tareas/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
