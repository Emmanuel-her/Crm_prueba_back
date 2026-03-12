from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_routes, user_routes
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservicio Backend para Registro y Autenticación con JWT sobre SQL Server bajo arquitectura limpia.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración básica de CORS para que los frontends puedan comunicarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro centralizado de controladores o routers
app.include_router(auth_routes.router, prefix="/autenticacion", tags=["Autenticación"])
app.include_router(user_routes.router, prefix="/usuarios", tags=["Usuarios"])

@app.get("/", tags=["Health"])
def health_check():
    """Valida la salud del contenedor y proyecto web."""
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "message": "Bienvenido, los endpoints se encuentran listos de acuerdo a requisitos de Colombia."
    }
