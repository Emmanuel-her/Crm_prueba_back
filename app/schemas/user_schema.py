from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre completo del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico del usuario")

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, description="Contraseña en texto plano")

class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=100, description="Opcional. Nombre completo del usuario")
    correo: EmailStr | None = Field(None, description="Opcional. Correo electrónico del usuario")
    password: str | None = Field(None, min_length=6, description="Opcional. Contraseña en texto plano")

class UsuarioResponse(UsuarioBase):
    id: int
    rol: str
    es_activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True
