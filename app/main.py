from fastapi import FastAPI, Request, Depends, HTTPException
from app.chat import procesar_pregunta
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import Pregunta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Permite que el frontend (en localhost:5173) comunique con el backend y pueda acceder a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Puerto por defecto de Vite React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"mensaje": "pong desde FastAPI"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/", response_model=list[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print("Ejecutando read_usuarios")
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    print("Entrando al endpoint /usuarios/")
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

# Modelo para recibir la pregunta del frontend
@app.post("/api/ask")
def ask_api(pregunta_data: Pregunta, db: Session = Depends(get_db)):
    pregunta = pregunta_data.message
    respuesta = procesar_pregunta(pregunta, db)
    return {"reply": respuesta}

@app.get("/api/ask")
def ask_invalid():
    return {"error": "Usa POST para enviar preguntas"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
