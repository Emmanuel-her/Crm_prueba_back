from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user_schema import UsuarioResponse, UsuarioUpdate
from app.services.user_service import UserService
from app.infrastructure.database import obtener_sesion_db
from app.core.dependencies import obtener_usuario_actual, obtener_usuario_actual_admin
from app.domain.user import Usuario

router = APIRouter()

@router.get("/mi-perfil", response_model=UsuarioResponse)
def obtener_perfil_propio(
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_sesion_db)
):
    """Extrae y devuelve de forma segura la información del usuario autenticado."""
    user_service = UserService(db)
    return user_service.obtener_perfil(usuario_actual.id)

@router.put("/mi-perfil", response_model=UsuarioResponse)
def actualizar_perfil_propio(
    usuario_update: UsuarioUpdate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_sesion_db)
):
    """Permite al propietario del perfil actualizar sus propios detalles de usuario o contraseña."""
    user_service = UserService(db)
    return user_service.actualizar_perfil(usuario_actual.id, usuario_update)

@router.get("", response_model=List[UsuarioResponse])
def listar_todos_usuarios(
    usuario_actual: Usuario = Depends(obtener_usuario_actual_admin),
    db: Session = Depends(obtener_sesion_db)
):
    """Endpoint asegurado que lista a todos los usuarios del sistema (Acceso exclusivo ROL Admin)."""
    user_service = UserService(db)
    return user_service.listar_usuarios()
