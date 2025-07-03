# Este script genera un embedding con Gemini por cada usuario activo, usando su nombre + dirección, y lo guarda en ChromaDB
import os
import dotenv
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Usuario
from app.embeddings import generar_embedding, get_chroma_collection

# Cargar variables desde .env (clave API Gemini, cadena conexión DB)
dotenv.load_dotenv()

# Conectamos con la colección de vectores en ChromaDB
collection = get_chroma_collection()

# Crear sesión a la base de datos MySQL
session: Session = SessionLocal()

try:
    # Consultamos todos los usuarios activos
    usuarios = session.query(Usuario).filter(Usuario.activo == 1).all()
    print(f"🔍 Se encontraron {len(usuarios)} usuarios activos para vectorizar.")

    for usuario in usuarios:
        try:
            texto = f"{usuario.user_name or ''} {usuario.direccion or ''}".strip()
            if not texto:
                continue  # Salta si no hay texto a vectorizar

            vector = generar_embedding(texto)
            collection.add(embedding=vector, documents=[texto], ids=[str(usuario.id)])
            print(f"✅ Vectorizado usuario ID {usuario.id}: {usuario.user_name}")
        except Exception as e:
            print(f"❌ Error vectorizando usuario ID {usuario.id}: {e}")

finally:
    session.close()