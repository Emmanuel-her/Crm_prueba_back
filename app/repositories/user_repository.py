from sqlalchemy.orm import Session
from app.domain.user import Usuario
from app.schemas.user_schema import UsuarioCreate, UsuarioUpdate
from app.core.security import obtener_hash_contraseña

class UserRepository:
    """Capaz de abstracción para el acceso a la Base de Datos para el Usuario."""
    
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, usuario_id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()

    def obtener_todos(self) -> list[Usuario]:
        return self.db.query(Usuario).all()

    def crear_usuario(self, usuario: UsuarioCreate) -> Usuario:
        db_usuario = Usuario(
            nombre=usuario.nombre,
            correo=usuario.correo,
            password_hash=obtener_hash_contraseña(usuario.password),
            rol="USUARIO"
        )
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def actualizar_usuario(self, usuario_id: int, usuario_update: UsuarioUpdate) -> Usuario | None:
        db_usuario = self.obtener_por_id(usuario_id)
        if not db_usuario:
            return None
        
        update_data = usuario_update.model_dump(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            update_data["password_hash"] = obtener_hash_contraseña(update_data.pop("password"))
        elif "password" in update_data:
            update_data.pop("password")
            
        for key, value in update_data.items():
            setattr(db_usuario, key, value)
            
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario
