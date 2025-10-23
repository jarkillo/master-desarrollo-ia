/**
 * Custom Hook para gestión de tareas con React Query.
 *
 * Incluye:
 * - Queries (listado, individual)
 * - Mutations (crear, actualizar, eliminar)
 * - Optimistic updates
 * - Cache invalidation automática
 * - Loading/error states
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { tareasService } from '../services/tareas.service';
import type { Tarea, CrearTareaData, ActualizarTareaData } from '../types/tarea';

const QUERY_KEY = 'tareas';

/**
 * Hook para obtener todas las tareas.
 */
export function useTareas() {
  return useQuery({
    queryKey: [QUERY_KEY],
    queryFn: tareasService.listar,
    staleTime: 1000 * 60, // 1 minuto
  });
}

/**
 * Hook para obtener una tarea específica.
 */
export function useTarea(id: number) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => tareasService.obtener(id),
    enabled: !!id,
  });
}

/**
 * Hook para obtener estadísticas.
 */
export function useEstadisticas() {
  return useQuery({
    queryKey: ['estadisticas'],
    queryFn: tareasService.estadisticas,
    staleTime: 1000 * 30, // 30 segundos
  });
}

/**
 * Hook para crear una tarea con optimistic update.
 */
export function useCrearTarea() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CrearTareaData) => tareasService.crear(data),

    // Optimistic update: actualiza UI antes de la respuesta del servidor
    onMutate: async (nuevaTarea) => {
      // Cancelar queries en progreso
      await queryClient.cancelQueries({ queryKey: [QUERY_KEY] });

      // Snapshot del estado anterior
      const tareasPrevias = queryClient.getQueryData<Tarea[]>([QUERY_KEY]);

      // Optimistically actualizar cache
      if (tareasPrevias) {
        const tareaOptimista: Tarea = {
          id: Date.now(), // ID temporal
          nombre: nuevaTarea.nombre,
          completada: false,
        };

        queryClient.setQueryData<Tarea[]>(
          [QUERY_KEY],
          [...tareasPrevias, tareaOptimista]
        );
      }

      return { tareasPrevias };
    },

    // En caso de error, revertir optimistic update
    onError: (_error, _variables, context) => {
      if (context?.tareasPrevias) {
        queryClient.setQueryData([QUERY_KEY], context.tareasPrevias);
      }
    },

    // Siempre refrescar después de la mutación
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: ['estadisticas'] });
    },
  });
}

/**
 * Hook para actualizar una tarea con optimistic update.
 */
export function useActualizarTarea() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ActualizarTareaData }) =>
      tareasService.actualizar(id, data),

    // Optimistic update
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: [QUERY_KEY] });

      const tareasPrevias = queryClient.getQueryData<Tarea[]>([QUERY_KEY]);

      if (tareasPrevias) {
        const tareasActualizadas = tareasPrevias.map((tarea) =>
          tarea.id === id ? { ...tarea, ...data } : tarea
        );

        queryClient.setQueryData<Tarea[]>([QUERY_KEY], tareasActualizadas);
      }

      return { tareasPrevias };
    },

    onError: (_error, _variables, context) => {
      if (context?.tareasPrevias) {
        queryClient.setQueryData([QUERY_KEY], context.tareasPrevias);
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: ['estadisticas'] });
    },
  });
}

/**
 * Hook para eliminar una tarea con optimistic update.
 */
export function useEliminarTarea() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => tareasService.eliminar(id),

    // Optimistic update
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: [QUERY_KEY] });

      const tareasPrevias = queryClient.getQueryData<Tarea[]>([QUERY_KEY]);

      if (tareasPrevias) {
        const tareasFiltradas = tareasPrevias.filter((tarea) => tarea.id !== id);
        queryClient.setQueryData<Tarea[]>([QUERY_KEY], tareasFiltradas);
      }

      return { tareasPrevias };
    },

    onError: (_error, _variables, context) => {
      if (context?.tareasPrevias) {
        queryClient.setQueryData([QUERY_KEY], context.tareasPrevias);
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: ['estadisticas'] });
    },
  });
}
