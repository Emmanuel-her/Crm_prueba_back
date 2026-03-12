from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest, Token, ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.user_schema import UsuarioCreate, UsuarioResponse
from app.services.auth_service import AuthService
from app.infrastructure.database import obtener_sesion_db

router = APIRouter()

@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registrar(usuario_in: UsuarioCreate, db: Session = Depends(obtener_sesion_db)):
    """Registra y asegura el guardado de un usuario nuevo en el sistema."""
    auth_service = AuthService(db)
    return auth_service.registrar_usuario(usuario_in)

@router.post("/iniciar-sesion", response_model=Token)
def iniciar_sesion(login_data: LoginRequest, db: Session = Depends(obtener_sesion_db)):
    """
    Inicia sesión validando las credenciales JSON y devolviendo el token de acceso JWT
    """
    auth_service = AuthService(db)
    return auth_service.autenticar_usuario(login_data)

@router.post("/iniciar-sesion-swagger", response_model=Token, include_in_schema=True)
def iniciar_sesion_swagger(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(obtener_sesion_db)
):
    """
    Este endpoint es unicamente para que fastapi permita utilizar el authorize para probar el api localmente, para el consumo externo es el otro (/iniciar-sesion)
    """
    auth_service = AuthService(db)
    login_data = LoginRequest(correo=form_data.username, password=form_data.password)
    return auth_service.autenticar_usuario(login_data)

@router.post("/recuperar-contraseña", status_code=200)
def recuperar_contraseña(request_data: ForgotPasswordRequest, db: Session = Depends(obtener_sesion_db)):
    """Solicita el envio local (por consola) de un token de recuperación de contraseña."""
    auth_service = AuthService(db)
    return auth_service.solicitar_recuperacion_contra(request_data.correo)

@router.post("/restablecer-contraseña", status_code=200)
def restablecer_contraseña(request_data: ResetPasswordRequest, db: Session = Depends(obtener_sesion_db)):
    """Concreta el reseteo comprobando la validez del token y encriptando la nueva clave."""
    auth_service = AuthService(db)
    return auth_service.resetear_contra(request_data.token, request_data.password)
