/**
 * Formulario para crear tareas usando React Hook Form + Zod.
 */
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCrearTarea } from '../hooks/useTareas';

// Schema de validación con Zod
const tareaSchema = z.object({
  nombre: z
    .string()
    .min(1, 'El nombre es requerido')
    .max(200, 'El nombre no puede exceder 200 caracteres')
    .trim(),
});

type TareaFormData = z.infer<typeof tareaSchema>;

export function CrearTareaForm() {
  const crearTarea = useCrearTarea();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<TareaFormData>({
    resolver: zodResolver(tareaSchema),
    defaultValues: {
      nombre: '',
    },
  });

  const onSubmit = async (data: TareaFormData) => {
    try {
      await crearTarea.mutateAsync(data);
      reset(); // Limpiar formulario después de crear
    } catch (error) {
      console.error('Error al crear tarea:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="crear-tarea-form">
      <div className="form-group">
        <input
          type="text"
          placeholder="Nueva tarea..."
          className={`form-input ${errors.nombre ? 'error' : ''}`}
          disabled={isSubmitting || crearTarea.isPending}
          {...register('nombre')}
        />

        {errors.nombre && (
          <span className="error-message">{errors.nombre.message}</span>
        )}
      </div>

      <button
        type="submit"
        className="btn btn-primary"
        disabled={isSubmitting || crearTarea.isPending}
      >
        {crearTarea.isPending ? 'Creando...' : 'Crear Tarea'}
      </button>

      {crearTarea.isError && (
        <div className="error-message">
          Error al crear tarea: {crearTarea.error?.message || 'Error desconocido'}
        </div>
      )}
    </form>
  );
}
