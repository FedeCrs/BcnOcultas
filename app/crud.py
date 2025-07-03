from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate
from sqlalchemy import or_

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def search_espacios_por_nombre_o_direccion(db: Session, query: str):
    return db.query(Usuario).filter(
        or_(
            Usuario.user_name.ilike(f"%{query}%"),
            Usuario.direccion.ilike(f"%{query}%")
        )
    ).all()
