# Definimos el modelo Usuario basado en la tabla `usuarios` de MySQL
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    numero_usuario = Column(Integer, unique=True, nullable=False)
    user_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    # password = Column(String(32), nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(150), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

    