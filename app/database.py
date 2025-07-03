# Conexión a base de datos MySQL usando SQLAlchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargamos variables de entorno (.env)
load_dotenv()

# Cadena de conexión tipo: mysql+pymysql://user:pass@localhost:3306/mydb
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"DATABASE_URL: {DATABASE_URL}")


# Creamos el engine y la sesión para SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print(f"engine: {engine}")
print(f"SessionLocal: {SessionLocal}")
print(f"Base: {Base}")
