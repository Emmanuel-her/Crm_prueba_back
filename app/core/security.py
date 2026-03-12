from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings

# Configuración de Passlib para hacer hash de contraseñas usando pbkdf2 (nativo de Python, muy seguro y sin dependencias externas)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verificar_contraseña(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    """Valida que la contraseña plana coincida con el hash recuperado de la BD."""
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)

def obtener_hash_contraseña(contrasena: str) -> str:
    """Genera el hash bcrypt para una contraseña dada."""
    return pwd_context.hash(contrasena)

def crear_token_acceso(datos: Dict[str, Any], tiempo_expiracion_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT embebiendo el payload provisto."""
    a_codificar = datos.copy()
    if tiempo_expiracion_delta:
        expira = datetime.now(timezone.utc) + tiempo_expiracion_delta
    else:
        expira = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    a_codificar.update({"exp": expira})
    token_jwt = jwt.encode(a_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token_jwt
