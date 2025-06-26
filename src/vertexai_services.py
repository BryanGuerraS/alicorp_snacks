import os
import uuid
from datetime import datetime
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.preview.vision_models import ImageGenerationModel
from dotenv import load_dotenv

from src.prompts import (
    DESCRIPCION_PRODUCTO_TEMPLATE,
    ANALISIS_FEEDBACK_TEMPLATE,
    PROMPT_IMAGEN_TEMPLATE
)

# Carga las variables de entorno para obtener el PROJECT_ID y REGION
load_dotenv()
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION", "us-central1") # us-central1 es una región común

# Inicializa Vertex AI
try:
    vertexai.init(project=PROJECT_ID, location=REGION)
except Exception as e:
    print(f"Error inicializando Vertex AI. Asegúrate de que GCP_PROJECT_ID esté en tu .env y te hayas autenticado con 'gcloud auth application-default login'. Error: {e}")

# Nombre del modelo a usar
TEXT_MODEL_NAME = "gemini-2.0-flash-lite-001"

def generar_descripcion_producto(nombre_producto, ingredientes, beneficios, publico, tono):
    try:
        model = GenerativeModel(
            model_name=TEXT_MODEL_NAME,
            system_instruction="Actúa como un copywriter experto para Alicorp, especializado en productos de consumo masivo y snacks saludables."
        )
        prompt = DESCRIPCION_PRODUCTO_TEMPLATE.format(
            nombre_producto=nombre_producto,
            ingredientes=ingredientes,
            beneficios=beneficios,
            publico=publico,
            tono=tono
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con la API de Vertex AI (Texto): {e}"

def analizar_feedback(comentarios):
    try:
        model = GenerativeModel(
            model_name=TEXT_MODEL_NAME,
            system_instruction="Actúa como un Analista de Datos especializado en feedback de clientes para Alicorp."
        )
        prompt = ANALISIS_FEEDBACK_TEMPLATE.format(comentarios=comentarios)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con la API de Vertex AI (Análisis): {e}"

def generar_prompt_imagen(descripcion_producto, estilo_visual):
    try:
        model = GenerativeModel(
            model_name=TEXT_MODEL_NAME,
            system_instruction="Actúa como un Director de Arte y Experto en Prompt Engineering para Alicorp. Tu respuesta debe estar completamente en español."
        )
        prompt = PROMPT_IMAGEN_TEMPLATE.format(
            descripcion_producto=descripcion_producto,
            estilo_visual=estilo_visual
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con la API de Vertex AI (Prompt): {e}"

# --- MODELO DE IMAGEN ---

IMAGE_MODEL_NAME = "imagegeneration@006" # Modelo Imagen 2

def generar_imagen_vertex(prompt_detallado, quality=None, size=None):
    """
    Genera una imagen usando el modelo Imagen 2 de Vertex AI.
    Guarda la imagen localmente y devuelve la ruta del archivo.
    """
    try:
        model = ImageGenerationModel.from_pretrained(IMAGE_MODEL_NAME)
        
        # Generar imagen
        response = model.generate_images(
            prompt=prompt_detallado,
            number_of_images=1
        )
        
        # Crear un nombre de archivo único para evitar sobrescribir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:4]
        filename = f"generated_image_{timestamp}_{unique_id}.png"
        output_path = os.path.join("outputs", filename)
        
        # Guardar la imagen en la carpeta 'outputs'
        response.images[0].save(location=output_path, include_generation_parameters=True)
        
        # Devolver la ruta local del archivo guardado
        return output_path
    
    except Exception as e:
        return f"Error al generar imagen con Vertex AI Imagen 2: {e}"