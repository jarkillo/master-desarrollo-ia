"""
Tests unitarios para file_ops tools.
"""

from unittest.mock import Mock, patch

from api.tools.file_ops import edit_file, read_file


def test_read_file_success(tmp_path):
    """Test lectura exitosa de archivo."""
    # Crear archivo temporal
    test_file = tmp_path / "test.py"
    test_content = "def hello():\n    print('Hello')\n"
    test_file.write_text(test_content)

    # Mock project_root para que tmp_path sea válido
    with patch("api.tools.file_ops.Path.__file__") as mock_file:
        mock_file.parent.parent.parent.resolve.return_value = tmp_path.parent

        result = read_file(str(test_file))

        assert result.status == "success"
        assert result.data["content"] == test_content
        assert result.data["lines"] == 2


def test_read_file_not_found():
    """Test cuando archivo no existe."""
    result = read_file("/nonexistent/file.py")

    assert result.status == "error"
    assert result.error_type == "file_not_found"
    assert "no encontrado" in result.message.lower()


def test_read_file_path_traversal():
    """Test que previene path traversal."""
    dangerous_paths = [
        "../../etc/passwd",
        "/etc/passwd",
        "../../../secret.txt",
    ]

    for path in dangerous_paths:
        result = read_file(path)

        assert result.status == "error"
        assert result.error_type == "security_error"
        assert "path traversal" in result.message.lower()


def test_read_file_too_large(tmp_path):
    """Test que rechaza archivos muy grandes."""
    test_file = tmp_path / "large.txt"

    # Mock para simular archivo > 5MB
    with patch("api.tools.file_ops.Path.stat") as mock_stat:
        mock_stat.return_value.st_size = 6 * 1024 * 1024  # 6MB

        with patch("api.tools.file_ops.Path.exists", return_value=True):
            with patch("api.tools.file_ops.Path.is_file", return_value=True):
                result = read_file(str(test_file))

                assert result.status == "error"
                assert result.error_type == "file_too_large"


def test_edit_file_success(tmp_path):
    """Test edición exitosa de archivo."""
    test_file = tmp_path / "test.py"
    original = "def old_function():\n    pass\n"
    test_file.write_text(original)

    old_content = "old_function"
    new_content = "new_function"

    with patch("api.tools.file_ops.Path.__file__") as mock_file:
        mock_file.parent.parent.parent.resolve.return_value = tmp_path.parent

        # Mock read_file para simplificar
        with patch("api.tools.file_ops.read_file") as mock_read:
            mock_read.return_value = Mock(
                status="success", data={"content": original}
            )

            result = edit_file(str(test_file), old_content, new_content)

            assert result.status == "success"


def test_edit_file_content_not_found(tmp_path):
    """Test cuando el contenido a reemplazar no existe."""
    test_file = tmp_path / "test.py"
    test_file.write_text("def function():\n    pass\n")

    with patch("api.tools.file_ops.read_file") as mock_read:
        mock_read.return_value = Mock(
            status="success", data={"content": "def function():\n    pass\n"}
        )

        result = edit_file(str(test_file), "nonexistent", "replacement")

        assert result.status == "error"
        assert result.error_type == "content_not_found"
