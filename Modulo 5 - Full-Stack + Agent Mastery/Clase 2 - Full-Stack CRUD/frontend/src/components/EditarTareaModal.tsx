/**
 * Modal para editar una tarea existente.
 * Usa React Hook Form + Zod para validación.
 */
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useActualizarTarea } from '../hooks/useTareas';
import type { Tarea } from '../types/tarea';

const editarTareaSchema = z.object({
  nombre: z
    .string()
    .min(1, 'El nombre es requerido')
    .max(200, 'El nombre no puede exceder 200 caracteres')
    .trim(),
});

type EditarTareaFormData = z.infer<typeof editarTareaSchema>;

interface EditarTareaModalProps {
  tarea: Tarea;
  onClose: () => void;
}

export function EditarTareaModal({ tarea, onClose }: EditarTareaModalProps) {
  const actualizarTarea = useActualizarTarea();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<EditarTareaFormData>({
    resolver: zodResolver(editarTareaSchema),
    defaultValues: {
      nombre: tarea.nombre,
    },
  });

  const onSubmit = async (data: EditarTareaFormData) => {
    try {
      await actualizarTarea.mutateAsync({
        id: tarea.id,
        data: { nombre: data.nombre },
      });
      onClose();
    } catch (error) {
      console.error('Error al actualizar tarea:', error);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Editar Tarea</h2>

        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="form-group">
            <label htmlFor="nombre">Nombre de la tarea:</label>
            <input
              id="nombre"
              type="text"
              className={`form-input ${errors.nombre ? 'error' : ''}`}
              disabled={isSubmitting || actualizarTarea.isPending}
              {...register('nombre')}
            />

            {errors.nombre && (
              <span className="error-message">{errors.nombre.message}</span>
            )}
          </div>

          {actualizarTarea.isError && (
            <div className="error-message">
              Error: {actualizarTarea.error?.message || 'Error desconocido'}
            </div>
          )}

          <div className="modal-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              disabled={isSubmitting || actualizarTarea.isPending}
            >
              Cancelar
            </button>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSubmitting || actualizarTarea.isPending}
            >
              {actualizarTarea.isPending ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
