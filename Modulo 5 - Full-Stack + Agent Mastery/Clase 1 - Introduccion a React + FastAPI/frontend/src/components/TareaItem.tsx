// src/components/TareaItem.tsx
import { useState } from 'react';
import type { Tarea } from '../types/tarea';

interface TareaItemProps {
  tarea: Tarea;
  onToggle: (id: number, completada: boolean) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

/**
 * Componente que representa una tarea individual.
 *
 * Características:
 * - Checkbox para marcar como completada
 * - Botón para eliminar
 * - Estados de loading durante operaciones async
 */
export function TareaItem({ tarea, onToggle, onDelete }: TareaItemProps) {
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggle(tarea.id, !tarea.completada);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`¿Eliminar la tarea "${tarea.nombre}"?`)) {
      setIsDeleting(true);
      try {
        await onDelete(tarea.id);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <div className="tarea-item">
      <input
        type="checkbox"
        checked={tarea.completada}
        onChange={handleToggle}
        disabled={isToggling || isDeleting}
      />
      <span
        className={tarea.completada ? 'completada' : ''}
        style={{ textDecoration: tarea.completada ? 'line-through' : 'none' }}
      >
        {tarea.nombre}
      </span>
      <button
        onClick={handleDelete}
        disabled={isToggling || isDeleting}
        className="btn-delete"
      >
        {isDeleting ? 'Eliminando...' : '🗑️'}
      </button>
    </div>
  );
}
