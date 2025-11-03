"""Tools para operaciones de archivos seguras."""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class ToolSuccess(BaseModel):
    status: Literal["success"] = "success"
    data: dict


class ToolError(BaseModel):
    status: Literal["error"] = "error"
    error_type: str
    message: str
    suggestion: str


ToolResult = ToolSuccess | ToolError


def read_file(file_path: str) -> ToolResult:
    """
    Lee archivo del proyecto con validaciones de seguridad.

    **SECURITY**: Previene path traversal attacks.

    Args:
        file_path: Path relativo o absoluto al archivo

    Returns:
        ToolSuccess con contenido O ToolError
    """
    try:
        path = Path(file_path).resolve()
    except Exception as e:
        return ToolError(
            error_type="invalid_path",
            message=f"Path inválido: {str(e)}",
            suggestion=f"Verifica que el path '{file_path}' es correcto.",
        )

    # Validar path traversal
    project_root = Path(__file__).parent.parent.parent.resolve()
    if not str(path).startswith(str(project_root)):
        return ToolError(
            error_type="security_error",
            message="Path traversal detectado",
            suggestion=f"Solo puedes leer archivos dentro de {project_root}",
        )

    if not path.exists():
        return ToolError(
            error_type="file_not_found",
            message=f"Archivo no encontrado: {file_path}",
            suggestion="Usa search_codebase para encontrar archivos por nombre.",
        )

    if not path.is_file():
        return ToolError(
            error_type="not_a_file",
            message=f"{file_path} no es un archivo",
            suggestion="Usa list_files para ver contenido del directorio.",
        )

    # Limitar tamaño
    max_size_mb = 5
    file_size_mb = path.stat().st_size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return ToolError(
            error_type="file_too_large",
            message=f"Archivo muy grande: {file_size_mb:.2f}MB",
            suggestion="Usa read_file_chunked para archivos grandes.",
        )

    try:
        content = path.read_text(encoding="utf-8")
        return ToolSuccess(
            data={
                "file_path": str(path),
                "content": content,
                "size_bytes": path.stat().st_size,
                "lines": len(content.splitlines()),
            }
        )
    except Exception as e:
        return ToolError(
            error_type="read_error",
            message=f"Error leyendo archivo: {str(e)}",
            suggestion="Verifica que el archivo es legible y está en formato texto.",
        )


def edit_file(file_path: str, old_content: str, new_content: str) -> ToolResult:
    """
    Edita archivo aplicando reemplazo de contenido.

    **SECURITY**: Validaciones de seguridad incluidas.

    Args:
        file_path: Path al archivo a editar
        old_content: Contenido a reemplazar
        new_content: Nuevo contenido

    Returns:
        ToolSuccess si el reemplazo fue exitoso O ToolError
    """
    # Leer archivo primero
    read_result = read_file(file_path)
    if read_result.status == "error":
        return read_result

    current_content = read_result.data["content"]

    # Verificar que old_content existe
    if old_content not in current_content:
        return ToolError(
            error_type="content_not_found",
            message=f"Contenido a reemplazar no encontrado en {file_path}",
            suggestion=(
                "Verifica que old_content coincide exactamente con el archivo. "
                "Usa read_file primero para ver el contenido actual."
            ),
        )

    # Aplicar reemplazo
    updated_content = current_content.replace(old_content, new_content, 1)

    try:
        path = Path(file_path).resolve()
        path.write_text(updated_content, encoding="utf-8")

        return ToolSuccess(
            data={
                "file_path": str(path),
                "lines_changed": len(new_content.splitlines())
                - len(old_content.splitlines()),
                "message": f"Archivo {file_path} editado exitosamente",
            }
        )
    except Exception as e:
        return ToolError(
            error_type="write_error",
            message=f"Error escribiendo archivo: {str(e)}",
            suggestion="Verifica que tienes permisos de escritura en el archivo.",
        )
