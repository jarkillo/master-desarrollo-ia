# api/repositorio_memoria.py
from typing import List, Optional
from api.servicio_tareas import Tarea


class RepositorioMemoria:
    """Implementación en memoria del repositorio de tareas.

    Esta implementación es ideal para:
    - Desarrollo local rápido
    - Tests unitarios
    - Prototipos

    Limitaciones:
    - Los datos se pierden al reiniciar el servidor
    - No es thread-safe (no usar en producción con múltiples workers)
    """

    def __init__(self):
        self._tareas: List[Tarea] = []
        self._contador = 0

    def guardar(self, tarea: Tarea) -> None:
        """Guarda una tarea nueva o actualiza una existente."""
        if tarea.id == 0:
            # Nueva tarea, asignar ID
            self._contador += 1
            tarea.id = self._contador
            self._tareas.append(tarea)
        else:
            # Actualizar tarea existente
            for i, t in enumerate(self._tareas):
                if t.id == tarea.id:
                    self._tareas[i] = tarea
                    break

    def listar(self) -> List[Tarea]:
        """Retorna una copia de la lista de tareas para evitar modificaciones externas."""
        return self._tareas.copy()

    def obtener(self, id: int) -> Optional[Tarea]:
        """Busca una tarea por ID."""
        for tarea in self._tareas:
            if tarea.id == id:
                return tarea
        return None

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea por ID. Retorna True si se eliminó."""
        for i, tarea in enumerate(self._tareas):
            if tarea.id == id:
                self._tareas.pop(i)
                return True
        return False
