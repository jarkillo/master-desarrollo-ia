"""
Repositorio de usuarios con SQLAlchemy.

Implementa las operaciones CRUD para usuarios en la base de datos.
"""


from sqlalchemy.orm import Session

from api.models import UsuarioModel


class RepositorioUsuariosDB:
    """
    Implementación del repositorio de usuarios con SQLAlchemy.

    Maneja la persistencia de usuarios en la base de datos.
    """

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de BD.

        Args:
            session: Sesión activa de SQLAlchemy
        """
        self._session = session

    def crear(self, email: str, nombre: str, password_hash: str) -> UsuarioModel:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            email: Email único del usuario
            nombre: Nombre completo
            password_hash: Hash bcrypt de la contraseña

        Returns:
            Usuario creado con ID asignado

        Raises:
            IntegrityError: Si el email ya existe (unique constraint)
        """
        usuario = UsuarioModel(
            email=email,
            nombre=nombre,
            password_hash=password_hash,
            activo=True
        )
        self._session.add(usuario)
        self._session.commit()
        self._session.refresh(usuario)
        return usuario

    def obtener_por_id(self, user_id: int) -> UsuarioModel | None:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            Usuario si existe, None en caso contrario
        """
        return self._session.query(UsuarioModel).filter(
            UsuarioModel.id == user_id
        ).first()

    def obtener_por_email(self, email: str) -> UsuarioModel | None:
        """
        Obtiene un usuario por su email.

        Args:
            email: Email del usuario

        Returns:
            Usuario si existe, None en caso contrario
        """
        return self._session.query(UsuarioModel).filter(
            UsuarioModel.email == email
        ).first()

    def listar(self, solo_activos: bool = True) -> list[UsuarioModel]:
        """
        Lista todos los usuarios.

        Args:
            solo_activos: Si True, solo devuelve usuarios activos

        Returns:
            Lista de usuarios
        """
        query = self._session.query(UsuarioModel)

        if solo_activos:
            query = query.filter(UsuarioModel.activo == True)

        return query.order_by(UsuarioModel.creado_en.desc()).all()

    def actualizar(self, usuario: UsuarioModel) -> UsuarioModel:
        """
        Actualiza un usuario existente.

        Args:
            usuario: Usuario con los cambios (debe tener ID)

        Returns:
            Usuario actualizado
        """
        self._session.commit()
        self._session.refresh(usuario)
        return usuario

    def desactivar(self, user_id: int) -> bool:
        """
        Desactiva un usuario (soft delete).

        Args:
            user_id: ID del usuario a desactivar

        Returns:
            True si se desactivó, False si no existe
        """
        usuario = self.obtener_por_id(user_id)
        if not usuario:
            return False

        usuario.activo = False
        self._session.commit()
        return True

    def existe_email(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado.

        Args:
            email: Email a verificar

        Returns:
            True si el email existe, False en caso contrario
        """
        return self._session.query(
            self._session.query(UsuarioModel).filter(
                UsuarioModel.email == email
            ).exists()
        ).scalar()
