from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base

class Usuario(Base):
    """
    Modelo representativo de la base de datos para la tabla 'usuarios'.
    Sigue la estructura solicitada en los requerimientos.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Sistema simple de roles, por defecto los creados son 'USUARIO'
    rol = Column(String(20), default="USUARIO", nullable=False)
    
    es_activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
