/**
 * Componente para renderizar una tarea individual.
 * Optimizado con React.memo para evitar re-renders innecesarios.
 */
import { useState, useCallback, memo } from 'react';
import { useActualizarTarea, useEliminarTarea } from '../hooks/useTareas';
import { EditarTareaModal } from './EditarTareaModal';
import type { Tarea } from '../types/tarea';

interface TareaItemProps {
  tarea: Tarea;
}

function TareaItemBase({ tarea }: TareaItemProps) {
  const [mostrarModal, setMostrarModal] = useState(false);
  const actualizarTarea = useActualizarTarea();
  const eliminarTarea = useEliminarTarea();

  const handleToggleCompletada = useCallback(() => {
    actualizarTarea.mutate({
      id: tarea.id,
      data: { completada: !tarea.completada },
    });
  }, [tarea.id, tarea.completada, actualizarTarea]);

  const handleEliminar = useCallback(() => {
    if (window.confirm('¿Estás seguro de eliminar esta tarea?')) {
      eliminarTarea.mutate(tarea.id);
    }
  }, [tarea.id, eliminarTarea]);

  const handleMostrarModal = useCallback(() => setMostrarModal(true), []);
  const handleCerrarModal = useCallback(() => setMostrarModal(false), []);

  const isLoading = actualizarTarea.isPending || eliminarTarea.isPending;

  return (
    <>
      <div className={`tarea-item ${tarea.completada ? 'completada' : ''} ${isLoading ? 'loading' : ''}`}>
        <div className="tarea-checkbox">
          <input
            type="checkbox"
            checked={tarea.completada}
            onChange={handleToggleCompletada}
            disabled={isLoading}
          />
        </div>

        <div className="tarea-nombre">
          <span>{tarea.nombre}</span>
        </div>

        <div className="tarea-acciones">
          <button
            className="btn btn-small btn-edit"
            onClick={handleMostrarModal}
            disabled={isLoading}
            title="Editar tarea"
          >
            ✏️
          </button>

          <button
            className="btn btn-small btn-delete"
            onClick={handleEliminar}
            disabled={isLoading}
            title="Eliminar tarea"
          >
            🗑️
          </button>
        </div>
      </div>

      {mostrarModal && (
        <EditarTareaModal
          tarea={tarea}
          onClose={handleCerrarModal}
        />
      )}
    </>
  );
}

// Memoizar componente para evitar re-renders cuando otras tareas cambian
export const TareaItem = memo(TareaItemBase, (prevProps, nextProps) => {
  return (
    prevProps.tarea.id === nextProps.tarea.id &&
    prevProps.tarea.nombre === nextProps.tarea.nombre &&
    prevProps.tarea.completada === nextProps.tarea.completada
  );
});
