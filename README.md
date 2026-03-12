# CRM Backend - Proyecto de Prueba

Este es el backend de un proyecto de prueba que arme para gestionar el inicio de sesión y usuarios básicos de un CRM. Lo hice directamente enfocado en la funcionalidad usando Python y FastAPI, así que no tiene mucho diseño o cosas extras complejas, va directo al grano.

La idea principal era tener una API REST sólida que pueda:
- Registrar usuarios nuevos
- Cargar un Login que te devuelva un Token de seguridad (JWT)
- Mantener sesiones y poder editar perfiles
- Usar SQL Server como base de datos
- Separar el código ordenadamente por capas (Rutas, Servicios, Repositorios, etc.) para que no sea un desastre o tirar codigo espagueti

## Qué usé para hacerlo
- **Python 3.11+**
- **FastAPI** (para levantar la API rapidísimo)
- **SQLAlchemy** (para conectar con la base de datos sin escribir SQL crudo)
- **SQL Server** (base de datos relacional)
- **Alembic** (para controlar los cambios en las tablas de la base de datos)

## Cómo correrlo localmente

1. Clona el repo.
2. Crea el entorno virtual y actívalo:
   ```bash
   python -m venv venv
   # En Windows: venv\Scripts\activate
   ```
3. Instala los requerimientos:
   ```bash
   pip install -r requirements.txt
   ```
4. Necesitas un archivo `.env` en la raíz (donde está el `main.py`). Adentro debe tener la conexión a tu base de datos SQL Server y una clave para tus tokens:
   ```env
   DATABASE_URL="mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=MIDATABASE_AQUI;Trusted_Connection=yes;"
   SECRET_KEY="tu_super_clave_secreta"
   ```
5. Aplica las tablas a la base de datos con Alembic:
   ```bash
   alembic upgrade head
   ```
6. Corre el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

Una vez que esté levantado, puedes entrar a `http://127.0.0.1:8000/docs` para ver el Swagger interactivo y probar las rutas desde ahí mismo.
