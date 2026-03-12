import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    # Nombre del proyecto para Swagger
    PROJECT_NAME: str = "API de Autenticación"
    
    # Configuración de Base de Datos SQL Server
    # Ejemplo de conexión local de SQL Server con autenticación de Windows usando pyodbc:
    # "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=DB_Auth;Trusted_Connection=yes;"
    # En este caso ponemos una por defecto que puedes sobreescribir con un archivo .env
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "mssql+pyodbc://sa:TuPassword123@localhost/DB_Auth?driver=ODBC+Driver+17+for+SQL+Server"
    )
    
    # Configuración JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secreto_para_jwt_cambiar_en_produccion")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 días de validez por defecto

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Config()
