# diagnostico_vectores.py
from app.embeddings import generar_embedding, get_chroma_collection

import chromadb

# Verificar si hay datos en la colección
collection = get_chroma_collection()
print(f"[1] Documentos cargados en la colección 'usuarios': {collection.count()}")

# Verificar una consulta de ejemplo
texto_pregunta = "Dónde está Perro Pako Bar"
try:
    embedding = generar_embedding(texto_pregunta)
    print(f"[2] Embedding generado (primeros valores): {embedding[:5]}")

    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    documentos = resultados.get("documents", [[]])[0]
    distancias = resultados.get("distances", [[]])[0]

    if documentos:
        print("\n[3] Resultados encontrados:")
        for doc, dist in zip(documentos, distancias):
            print(f" - Documento: {doc[:60]}... (distancia: {dist:.4f})")
    else:
        print("\n[3] ⚠️ No se encontraron coincidencias en la colección.")

except Exception as e:
    print(f"\n❌ Error durante el diagnóstico: {e}")
