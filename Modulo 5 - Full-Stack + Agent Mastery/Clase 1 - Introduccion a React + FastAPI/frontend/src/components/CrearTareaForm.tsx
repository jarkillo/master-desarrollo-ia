// src/components/CrearTareaForm.tsx
import { useState, FormEvent } from 'react';

interface CrearTareaFormProps {
  onCrear: (nombre: string) => Promise<void>;
}

/**
 * Formulario para crear una nueva tarea.
 *
 * Características:
 * - Validación básica (no permite strings vacíos)
 * - Estado de loading durante creación
 * - Limpia el input después de crear
 */
export function CrearTareaForm({ onCrear }: CrearTareaFormProps) {
  const [nombre, setNombre] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const nombreTrimmed = nombre.trim();
    if (!nombreTrimmed) {
      alert('El nombre de la tarea no puede estar vacío');
      return;
    }

    setIsCreating(true);
    try {
      await onCrear(nombreTrimmed);
      setNombre(''); // Limpiar input después de crear
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="crear-tarea-form">
      <input
        type="text"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        placeholder="Nueva tarea..."
        disabled={isCreating}
        maxLength={200}
      />
      <button type="submit" disabled={isCreating || !nombre.trim()}>
        {isCreating ? 'Creando...' : 'Agregar'}
      </button>
    </form>
  );
}
