# Aplicación de Asistente Cultural con Búsqueda Semántica en Barcelona

## Descripción

Esta aplicación es un backend API desarrollado con FastAPI que funciona como asistente cultural para Barcelona. Permite consultar información sobre espacios culturales registrados en una base de datos MySQL y realiza búsquedas semánticas avanzadas usando embeddings generados con Google Gemini y ChromaDB para ofrecer respuestas relevantes incluso cuando la información no está directamente disponible en la base local.

El sistema combina búsqueda tradicional SQL con búsqueda por vectores, y utiliza un modelo de lenguaje (Gemini) para generar respuestas naturales y contextuales, adaptadas a preguntas sobre espacios culturales, direcciones y detalles locales.

---

## Características principales

- CRUD básico para gestionar usuarios/espacios culturales.
- Búsqueda por nombre o dirección mediante SQL.
- Búsqueda semántica avanzada con embeddings generados por Google Gemini.
- Indexación y consulta de vectores con ChromaDB para similitud semántica.
- Integración con modelo Gemini para responder preguntas con contexto.
- API REST para interacción desde frontend o aplicaciones externas.
- Manejo de variables de entorno con `.env` para configuración segura.
- Middleware CORS configurado para frontend React (localhost:5173).

---

## Tecnologías usadas

- Python 3.x
- FastAPI (framework web)
- SQLAlchemy (ORM para MySQL)
- PyMySQL (driver MySQL)
- Google Generative AI (Gemini) para generación de embeddings y respuestas
- ChromaDB para almacenamiento y consulta de vectores
- python-dotenv para gestión de variables de entorno
- Uvicorn como servidor ASGI

---

## Instalación

1. Clonar el repositorio:

```bash
git clone <https://github.com/FedeCrs/BcnOcultas.git>
cd <BcnOcultas>
Crear y activar un entorno virtual:

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Instalar dependencias:

bash
Copy code
pip install -r app/requirements.txt
Configurar variables de entorno en un archivo .env en la raíz, con al menos:

env
Copy code
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/tu_basedatos
GEMINI_API_KEY=tu_api_key_de_gemini
Inicializar la base de datos (creación de tablas):

bash
Copy code
python -c "from app import models, database; models.Base.metadata.create_all(bind=database.engine)"
Ejecutar la aplicación:

bash
Copy code
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Uso básico
Acceder a /ping para probar que el servidor está corriendo.

Endpoints para usuarios:

POST /usuarios/ para crear un usuario.

GET /usuarios/ para listar usuarios.

GET /usuarios/{usuario_id} para obtener usuario por ID.

Endpoint principal para preguntas culturales:

POST /api/ask con un JSON { "message": "tu pregunta aquí" } para obtener respuestas contextuales.

Estructura destacada del proyecto
app/main.py: punto de entrada y rutas API.

app/chat.py: lógica para procesar preguntas, combinar búsqueda SQL y vectorial, y llamar a Gemini.

app/crud.py: funciones CRUD para la base de datos.

app/embeddings.py: generación y manejo de embeddings con Gemini y ChromaDB.

app/gemini.py: función para interactuar con el modelo Gemini.

app/database.py: configuración de conexión a MySQL.

app/models.py: definición del modelo Usuario.

app/schemas.py: modelos Pydantic para validación y serialización.

app/vectorize_usuarios.py: script para generar embeddings para todos los usuarios activos.

Contribuciones
¡Bienvenidas! Si deseas contribuir:

Haz un fork del repositorio.

Crea una rama con tu feature o fix: git checkout -b feature/nombre-feature

Haz commit de tus cambios: git commit -m "Descripción del cambio"

Envía un pull request para revisión.

Por favor sigue las buenas prácticas de código y documenta tus cambios.

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

Autor 
Desarrollado por Federico Caruso.

Puedes contactarme en:

Email: fedemacape@gmail.com

GitHub: FedeCrs

