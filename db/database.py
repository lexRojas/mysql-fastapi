from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database

# URL de la base de datos MySQL
# DATABASE_URL = "mysql+asyncmy://rrojas:G30rg1n@@18.221.154.102:3306/notario"
DATABASE_URL="mysql://admin:RcKrNVUC@mysql-187830-0.cloudclusters.net:10072/notario"

# Crear el motor asíncrono de SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear una fábrica de sesiones asíncronas
SessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base para modelos declarativos
Base = declarative_base()

# Conexión para consultas simples (opcional si usas SQL directamente)
database = Database(DATABASE_URL)
