import re
from sqlalchemy.orm import Session
from app import crud # Asumo que crud contiene search_espacios_por_nombre_o_direccion
from app.gemini import ask_gemini
from app.embeddings import get_chroma_collection, generar_embedding # Asegúrate de que generen_embedding esté bien

def procesar_pregunta(pregunta: str, db: Session):
    print("🔎 Pregunta recibida:", pregunta)

    # 1. Limpiar la pregunta
    texto_limpio = limpiar_pregunta(pregunta)
    print("🧽 Pregunta limpia:", texto_limpio)

    contexto_db = "" # Inicializamos el contexto que pasaremos a Gemini

    # 2. Buscar por nombre o dirección en SQL
    try:
        resultados_sql = crud.search_espacios_por_nombre_o_direccion(db, texto_limpio)
        print("🔎 Resultados exactos de SQL:", resultados_sql)
        if resultados_sql:
            contexto_db += "Información encontrada en la base de datos local sobre espacios culturales:\n"
            for r in resultados_sql:
                # Aquí incluimos toda la info relevante para que Gemini tenga la dirección
                contexto_db += f"- Nombre: {r.user_name}, Dirección: {r.direccion}, Teléfono: {r.telefono or 'N/A'}\n"
            print(f"✅ SQL encontró respuesta local. Contexto para Gemini: {contexto_db[:200]}...") # Imprime solo el inicio
        else:
            print("❌ SQL: No se encontraron resultados por nombre o dirección.")
    except Exception as e:
        print(f"🚨 ERROR en búsqueda SQL: {e}")

    # 3. Buscar por vectores (embeddings) - Solo si la búsqueda SQL no encontró nada
    # (Esto evita duplicar la búsqueda o usar ChromaDB si ya tienes info directa)
    if not contexto_db: 
        try:
            collection = get_chroma_collection()
            
            query_vector = generar_embedding(texto_limpio)
            print("Embedding generado para la pregunta (primeros 10 val):", query_vector[:10])
            
            resultados_vectores = collection.query(
                query_embeddings=[query_vector],
                n_results=3, # Puedes ajustar el número de resultados de ChromaDB
                include=["documents", "distances", "ids"]
            )
            print("🔍 Resultados de búsqueda por vectores:", resultados_vectores)

            documentos = resultados_vectores.get("documents", [[]])[0]
            distancias = resultados_vectores.get("distances", [[]])[0]

            # Puedes añadir un umbral de distancia si quieres que los resultados sean muy relevantes
            # Por ejemplo, si distancias[0] es menor que 0.3 (significa 70% de similitud)
            if documentos and distancias and distancias[0] < 0.3: # Añadimos una condición para que el resultado sea relevante
                contexto_db += "Información similar encontrada por búsqueda vectorial (ordenada por similitud):\n"
                # Ordenar por similitud (1 - distancia)
                for doc, dist in sorted(zip(documentos, distancias), key=lambda x: x[1]):
                    contexto_db += f"- {doc} (similitud: {1 - dist:.2f})\n"
                print(f"✅ ChromaDB encontró resultados. Contexto para Gemini: {contexto_db[:200]}...")
            else:
                print("❌ ChromaDB: No se encontraron resultados por vectores relevantes o suficientemente similares.")

        except Exception as e:
            print(f"❌ ERROR en búsqueda por vectores (ChromaDB): {e}")

    # 4. Llamar a Gemini con el contexto (sea lleno o vacío)
    # El prompt modificado en app/gemini.py se encargará de usar la BD o el conocimiento general
    if not contexto_db:
        print("🧠 Contexto final para Gemini: Vacío. Gemini usará su conocimiento general.")
        contexto_para_gemini = "No se encontró información específica en la base de datos local."
    else:
        print("🧠 Contexto final para Gemini: Usando información de la DB local.")
        contexto_para_gemini = contexto_db
    
    try:
        respuesta = ask_gemini(pregunta, contexto_para_gemini)
        print(f"🤖 Respuesta final generada por Gemini: {respuesta[:200]}...") # Imprime solo el inicio
        return respuesta
    except Exception as e:
        print("❌ ERROR al consultar Gemini como último recurso:", str(e))
        return "Lo siento, no se pudo procesar tu pregunta en este momento."


# Limpieza de pregunta para búsqueda
def limpiar_pregunta(pregunta: str) -> str:
    """
    Elimina palabras comunes y caracteres especiales para limpiar la pregunta de búsqueda.
    """
    pregunta = pregunta.lower()
    # Elimina todo lo que no sea letra, número o espacio
    pregunta = re.sub(r'[^a-záéíóúüñ\s]', '', pregunta) # Incluye caracteres españoles
    
    palabras_comunes = [
        'donde', 'queda', 'esta', 'es', 'el', 'la', 'los', 'las',
        'barcelona', 'en', 'un', 'una', 'hay', 'por', 'del', 'de', 'al',
        'me', 'gustaria', 'saber', 'necesito', 'que', 'en', 'su', 'cuanto',
        'cuesta', 'el', 'la', 'un', 'una', 'a', 'del', 'de', 'al', 'se', 'encuentra'
    ]
    
    palabras = pregunta.split()
    # Filtramos palabras comunes, solo si la palabra no es solo una letra
    palabras_filtradas = [p for p in palabras if p not in palabras_comunes and len(p) > 1]
    
    return " ".join(palabras_filtradas).strip()