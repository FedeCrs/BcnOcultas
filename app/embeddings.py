# Funciones para generar embeddings desde texto usando Gemini y gestionar ChromaDB.
import os
import google.generativeai as genai
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

# Cargamos variables (.env)
load_dotenv()

# Configuramos la clave API de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Función para generar el vector de un texto usando Gemini
# Este vector representa el "significado" del texto para búsquedas semánticas

def generar_embedding(texto):
    model = genai.get_model("embedding-001")
    response = model.embed_content(
        content=texto,
        task_type="retrieval_document",
        title="Lugar Cultural"
    )
    return response["embedding"]

# Cliente local de ChromaDB para guardar/reconsultar vectores
chroma_client = chromadb.Client(Settings(persist_directory="chroma_db"))

# Constante para el nombre de la colección
CHROMA_COLLECTION_NAME = "usuarios"

# Función para obtener/crear la colección de vectores
def get_chroma_collection():
    return chroma_client.get_or_create_collection(name="usuarios")