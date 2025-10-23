/**
 * Tipos TypeScript para la aplicación de tareas.
 */

export interface Tarea {
  id: number;
  nombre: string;
  completada: boolean;
}

export interface CrearTareaData {
  nombre: string;
}

export interface ActualizarTareaData {
  nombre?: string;
  completada?: boolean;
}

export interface Estadisticas {
  total: number;
  completadas: number;
  pendientes: number;
}
