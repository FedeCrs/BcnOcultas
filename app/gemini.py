import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

chat_model_name = "gemini-1.5-flash"
chat_model = genai.GenerativeModel(chat_model_name)

def ask_gemini(pregunta: str, contexto: str) -> str:
    try:
        # Detectar si la pregunta explícitamente pide el barrio o la zona
        pregunta_baja = pregunta.lower()
        pide_barrio = "barrio" in pregunta_baja or "vecindario" in pregunta_baja or "zona" in pregunta_baja

        prompt = f"""
Eres un asistente cultural de Barcelona. Tu objetivo es proporcionar información precisa sobre espacios culturales.
Aquí tienes información relevante de una base de datos local:
{contexto}

**Instrucciones clave:**
1.  Si la información de la "base de datos local" es directamente relevante y suficiente para responder a la pregunta del usuario, utilízala.
2.  Si la pregunta del usuario es sobre un espacio cultural **ya mencionado o encontrado en la base de datos local** (cuyo nombre o dirección está en el contexto):
    * Si el usuario pregunta **explícitamente** por el barrio o la zona (es decir, la pregunta contiene palabras como "barrio", "vecindario" o "zona"):
        * Puedes intentar inferir ese dato utilizando tu conocimiento general sobre Barcelona.
        * **PERO SOLO SI ESTÁS COMPLETAMENTE SEGURO de la información del barrio.**
        * **SI NO ESTÁS SEGURO del barrio, NO lo inventes; simplemente indica que no tienes esa información específica sobre el barrio.**
    * **Si el usuario NO pregunta explícitamente por el barrio o la zona:**
        * **NO menciones el barrio en absoluto.**
        * **NO menciones que no tienes información sobre el barrio.** Concéntrate solo en responder lo que se te ha preguntado directamente.
3.  Si no encuentras ninguna información relevante en la "base de datos local" y la pregunta del usuario no está relacionada con datos de tu base de datos o si necesitas conocimiento más allá de lo local, utiliza tu conocimiento general para responder de forma útil y concisa.
4.  Siempre mantén un tono amable y servicial.

Pregunta del usuario:
{pregunta}
"""
        response = chat_model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error al procesar la pregunta en ask_gemini: {e}")
        return "Lo siento, hubo un error al procesar tu pregunta en este momento."