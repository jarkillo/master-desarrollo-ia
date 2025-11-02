"""
Gestión de memoria persistente para sistemas multi-agente.

Implementa:
- Persistent Memory (memoria con persistencia en disco)
- Checkpoints (snapshots del estado)
- Recovery (recuperación de errores)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .core import SharedMemory


class PersistentMemory(SharedMemory):
    """
    Memoria compartida con persistencia en disco.

    Permite:
    - Guardar estado entre sesiones
    - Recuperarse de errores (checkpoints)
    - Auditar decisiones de agentes
    - Replay de investigaciones pasadas
    """

    def __init__(self, storage_dir: str = "./memory"):
        """
        Inicializa memoria persistente.

        Args:
            storage_dir: Directorio donde guardar datos
        """
        super().__init__()
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.storage_dir / self.session_id
        self.session_dir.mkdir(exist_ok=True)

    def store(self, key: str, value: Any):
        """
        Almacena en memoria y persiste a disco.

        Args:
            key: Clave del dato
            value: Valor a almacenar
        """
        super().store(key, value)

        # Persistir a disco
        file_path = self.session_dir / f"{key}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                {"key": key, "value": value, "timestamp": datetime.now().isoformat()},
                f,
                indent=2,
                default=str,
                ensure_ascii=False,
            )

    def retrieve(self, key: str, default: Any = None) -> Any:
        """
        Recupera de memoria o disco.

        Args:
            key: Clave del dato
            default: Valor por defecto si no existe

        Returns:
            Valor almacenado o default
        """
        # Intentar memoria primero (más rápido)
        value = super().retrieve(key, None)
        if value is not None:
            return value

        # Si no está en memoria, buscar en disco
        file_path = self.session_dir / f"{key}.json"
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                # Cargar en memoria para próximas lecturas
                super().store(key, data["value"])
                return data["value"]

        return default

    def checkpoint(self, checkpoint_name: str):
        """
        Crea checkpoint del estado actual.

        Args:
            checkpoint_name: Nombre del checkpoint
        """
        checkpoint_data = {
            "session_id": self.session_id,
            "checkpoint_name": checkpoint_name,
            "timestamp": datetime.now().isoformat(),
            "state": self._data,
        }

        checkpoint_path = self.storage_dir / f"checkpoint_{checkpoint_name}.json"
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, indent=2, default=str, ensure_ascii=False)

        print(f"✅ Checkpoint guardado: {checkpoint_name}")

    def restore_checkpoint(self, checkpoint_name: str):
        """
        Restaura estado desde checkpoint.

        Args:
            checkpoint_name: Nombre del checkpoint a restaurar

        Raises:
            FileNotFoundError: Si el checkpoint no existe
        """
        checkpoint_path = self.storage_dir / f"checkpoint_{checkpoint_name}.json"

        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint no encontrado: {checkpoint_name}")

        with open(checkpoint_path, encoding="utf-8") as f:
            checkpoint_data = json.load(f)

        # Restaurar estado
        self._data = checkpoint_data["state"]

        # Recrear archivos en disco para la sesión actual
        for key, value in self._data.items():
            file_path = self.session_dir / f"{key}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "key": key,
                        "value": value,
                        "timestamp": datetime.now().isoformat(),
                        "restored_from": checkpoint_name,
                    },
                    f,
                    indent=2,
                    default=str,
                    ensure_ascii=False,
                )

        print(f"✅ Checkpoint restaurado: {checkpoint_name}")
        print(f"   Session original: {checkpoint_data['session_id']}")
        print(f"   Timestamp: {checkpoint_data['timestamp']}")

    def list_checkpoints(self) -> list[dict[str, Any]]:
        """
        Lista todos los checkpoints disponibles.

        Returns:
            Lista de diccionarios con info de checkpoints
        """
        checkpoints = []
        for path in self.storage_dir.glob("checkpoint_*.json"):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                checkpoints.append(
                    {
                        "name": data["checkpoint_name"],
                        "session_id": data["session_id"],
                        "timestamp": data["timestamp"],
                        "file": str(path),
                    }
                )

        return sorted(checkpoints, key=lambda x: x["timestamp"], reverse=True)

    def export_session(self) -> dict[str, Any]:
        """
        Exporta toda la sesión actual.

        Returns:
            Diccionario con todos los datos de la sesión
        """
        return {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "data": self._data,
        }

    def cleanup_old_sessions(self, keep_last_n: int = 10):
        """
        Limpia sesiones antiguas, manteniendo las últimas N.

        Args:
            keep_last_n: Número de sesiones a mantener
        """
        # Listar directorios de sesiones
        session_dirs = [
            d
            for d in self.storage_dir.iterdir()
            if d.is_dir() and d.name != self.session_id
        ]

        # Ordenar por fecha (del nombre)
        session_dirs.sort(reverse=True)

        # Eliminar directorios viejos
        deleted_count = 0
        for old_dir in session_dirs[keep_last_n:]:
            try:
                for file in old_dir.iterdir():
                    file.unlink()
                old_dir.rmdir()
                deleted_count += 1
            except Exception as e:
                print(f"⚠️  Error eliminando {old_dir}: {e}")

        if deleted_count > 0:
            print(f"✅ Limpieza completada: {deleted_count} sesiones antiguas eliminadas")
