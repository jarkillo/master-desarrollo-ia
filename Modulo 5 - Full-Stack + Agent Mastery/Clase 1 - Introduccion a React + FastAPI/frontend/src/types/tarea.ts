// src/types/tarea.ts

/**
 * Tipo que representa una tarea en el sistema.
 *
 * Este tipo debe coincidir con el modelo Pydantic del backend.
 */
export interface Tarea {
  id: number;
  nombre: string;
  completada: boolean;
}

/**
 * Tipo para crear una nueva tarea (sin ID).
 */
export interface CrearTareaDto {
  nombre: string;
}

/**
 * Tipo para actualizar una tarea existente.
 */
export interface ActualizarTareaDto {
  completada: boolean;
}
