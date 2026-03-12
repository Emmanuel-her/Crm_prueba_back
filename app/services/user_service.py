from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UsuarioUpdate
from app.domain.user import Usuario

class UserService:
    """Capa de Lógica de Negocio para Operaciones con Usuarios."""
    
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def obtener_perfil(self, usuario_id: int) -> Usuario:
        """Obtiene el perfil de un usuario existente o arroja un 404."""
        usuario = self.user_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario

    def actualizar_perfil(self, usuario_id: int, usuario_in: UsuarioUpdate) -> Usuario:
        """Actualiza el perfil valindando restricciones únicas."""
        if usuario_in.correo:
            usuario_existente = self.user_repo.obtener_por_correo(usuario_in.correo)
            if usuario_existente and usuario_existente.id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electrónico ya está en uso por otro usuario."
                )
                
        usuario = self.user_repo.actualizar_usuario(usuario_id, usuario_in)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        """Obtener lista de todos los usuarios registrados."""
        return self.user_repo.obtener_todos()
