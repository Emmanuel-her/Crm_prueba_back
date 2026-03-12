from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Annotated

from app.core.config import settings
from app.infrastructure.database import obtener_sesion_db
from app.schemas.auth_schema import TokenData
from app.repositories.user_repository import UserRepository
from app.domain.user import Usuario

# Dependencia de Oauth2 para leer el token del Header Authorization: Bearer <token>
# Se configura la URL relativa donde estará el endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="autenticacion/iniciar-sesion-swagger")

def obtener_usuario_actual(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(obtener_sesion_db)]
) -> Usuario:
    """Extrae el token JWT, lo valida y retorna el objeto usuario actual desde la BD."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o el token expiró",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        correo: str = payload.get("sub")
        rol: str = payload.get("rol")
        if correo is None:
            raise credentials_exception
        token_data = TokenData(correo=correo, rol=rol)
    except JWTError:
        raise credentials_exception
        
    user_repo = UserRepository(db)
    usuario = user_repo.obtener_por_correo(token_data.correo)
    
    if usuario is None:
        raise credentials_exception
    if not usuario.es_activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
        
    return usuario

def obtener_usuario_actual_admin(
    usuario_actual: Annotated[Usuario, Depends(obtener_usuario_actual)]
) -> Usuario:
    """Verifica si el usuario actual posee rol de ADMIN."""
    if usuario_actual.rol != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos necesarios (Rol ADMIN requerido)"
        )
    return usuario_actual
