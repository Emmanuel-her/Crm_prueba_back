from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Conector Engine para SQL Server
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping revisa la conexión antes de usarla, útil en SQL Server
    pool_pre_ping=True
)

# Fábrica de sesiones para interactuar con la Base de Datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase Base de la que heredarán todos los modelos de dominio (SQLAlchemy)
Base = declarative_base()

def obtener_sesion_db():
    """
    Dependencia de FastAPI que genera y entrega una sesión de base de datos
    por cada petición y la cierra al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
