from pydantic import BaseModel  # Importamos BaseModel desde pydantic, que se usa para definir esquemas de datos
from typing import Optional # Optional permite declarar campos que pueden ser None (opcionales)
from datetime import datetime   # Importamos datetime para manejar fechas

# Este es el modelo base que contiene los campos comunes del usuario.
# Se hereda en otros modelos (como UsuarioCreate y Usuario).
class UsuarioBase(BaseModel):
    user_name: str   # Nombre de usuario (obligatorio)
    email: Optional[str] = None  # Email del usuario (opcional)
    telefono: Optional[str] = None  # Teléfono del usuario (opcional)
    direccion: Optional[str] = None  # Dirección físicadel usuario (opcional)

# Este modelo se usa cuando se crea un nuevo usuario (POST).
# Hereda todos los campos de UsuarioBase.
class UsuarioCreate(UsuarioBase):
    pass    # No agrega nada nuevo, pero está preparado para extenderse si se necesita

# Este modelo representa la respuesta completa de un usuario cuando se consulta (GET).
# Hereda los campos de UsuarioBase y agrega información adicional que viene de la base de datos
class Usuario(UsuarioBase):
    id: int # ID único en la base de datos (clave primaria)
    numero_usuario: int # Número identificador de usuario
    fecha_creacion: datetime     # Fecha y hora en la que fue creado
    activo: bool    # Indica si el usuario está activo (True/False)

    # Esta configuración le indica a Pydantic que puede construir este modelo
    # a partir de un objeto ORM como los de SQLAlchemy.
    model_config = {
        "from_attributes": True # Equivalente moderno de `orm_mode = True` en Pydantic v1
    }
    
class Pregunta(BaseModel):
    message: str