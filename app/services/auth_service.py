from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, Token
from app.schemas.user_schema import UsuarioCreate, UsuarioUpdate
from app.domain.user import Usuario
from app.core.security import verificar_contraseña, crear_token_acceso
from app.core.config import settings

class AuthService:
    """Servicios dedicados a manejar inicio de sesión, recuperación de cuentas y registros."""

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def registrar_usuario(self, usuario_in: UsuarioCreate) -> Usuario:
        """Registra un nuevo usuario verificando colisiones de correo."""
        usuario_existente = self.user_repo.obtener_por_correo(usuario_in.correo)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        return self.user_repo.crear_usuario(usuario_in)

    def autenticar_usuario(self, login_data: LoginRequest) -> Token:
        """Valida credenciales y genera un JWT."""
        usuario = self.user_repo.obtener_por_correo(login_data.correo)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo electrónico o contraseña incorrectos"
            )
        
        if not verificar_contraseña(login_data.password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo electrónico o contraseña incorrectos"
            )
            
        if not usuario.es_activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo, contacte al administrador"
            )

        # Crear el JWT Token encapsulando los roles
        token_acceso = crear_token_acceso(
            datos={"sub": usuario.correo, "rol": usuario.rol}
        )
        
        return Token(access_token=token_acceso, token_type="bearer")

    def solicitar_recuperacion_contra(self, correo: str) -> dict:
        """Prepara el mecanismo de recuperación simulando un envio seguro."""
        usuario = self.user_repo.obtener_por_correo(correo)
        if not usuario:
            # Por seguridad (prevención de enumeración de usuarios), 
            # devolvemos siempre mensaje de éxito neutral.
            return {"mensaje": "Si el correo está registrado, se han enviado las instrucciones."}
            
        # IMPORTANTE: En producción usar Celery o BackgroundTasks para enviar el correo
        # Por propósitos locales simulamos generando temporalmente el token
        token_recuperacion = crear_token_acceso(
            datos={"sub": usuario.correo, "type": "recuperacion_password"}
        )
        
        # Simulamos que lo enviamos por correo imprimiendolo en consola
        print(f"\n[SIMULACIÓN EMAIL] Token de recuperación enviado a {correo}:\n{token_recuperacion}\n")
        
        return {"mensaje": "Si el correo está registrado, se han enviado las instrucciones."}

    def resetear_contra(self, token: str, password: str) -> dict:
        """Recibe token temporal JWT y efectúa el cambio si es válido."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            correo: str = payload.get("sub")
            if correo is None or payload.get("type") != "recuperacion_password":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token no válido")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido o expirado")
            
        usuario = self.user_repo.obtener_por_correo(correo)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
            
        # Actualizamos la contraseña aprovechando la lógica del repositorio
        self.user_repo.actualizar_usuario(usuario.id, UsuarioUpdate(password=password))
        return {"mensaje": "Contraseña actualizada exitosamente."}
